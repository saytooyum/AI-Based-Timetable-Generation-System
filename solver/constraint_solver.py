import os
import pandas as pd

from ortools.sat.python import cp_model

from solver.config import DAYS, generate_slots


DATA_PATH = os.path.join(os.path.dirname(__file__), "..")


def generate_sessions(courses):
    """Convert course hour requirements into individual weekly sessions."""
    sessions = []

    for _, course in courses.iterrows():

        for _ in range(int(course["theory_hours"])):
            sessions.append({
                "course_code": course["course_code"],
                "course_name": course["course_name"],
                "session_type": "Theory",
            })

        for _ in range(int(course["practical_hours"])):
            sessions.append({
                "course_code": course["course_code"],
                "course_name": course["course_name"],
                "session_type": "Practical",
            })

    return sessions


def generate_optimized_timetable():
    """Generate an optimized timetable using OR-Tools CP-SAT."""

    courses_file = os.path.join(DATA_PATH, "courses.csv")
    courses = pd.read_csv(courses_file)

    sessions = generate_sessions(courses)
    slots = generate_slots()

    model = cp_model.CpModel()

    # --------------------------------------------------
    # DECISION VARIABLES
    # --------------------------------------------------

    assignment = {}

    for session_index in range(len(sessions)):
        for slot_index in range(len(slots)):
            assignment[(session_index, slot_index)] = model.NewBoolVar(
                f"session_{session_index}_slot_{slot_index}"
            )

    # --------------------------------------------------
    # HARD CONSTRAINT 1
    # Every session must have exactly one slot.
    # --------------------------------------------------

    for session_index in range(len(sessions)):
        model.Add(
            sum(
                assignment[(session_index, slot_index)]
                for slot_index in range(len(slots))
            ) == 1
        )

    # --------------------------------------------------
    # HARD CONSTRAINT 2
    # A slot can contain at most one session.
    # --------------------------------------------------

    for slot_index in range(len(slots)):
        model.Add(
            sum(
                assignment[(session_index, slot_index)]
                for session_index in range(len(sessions))
            ) <= 1
        )

    # --------------------------------------------------
    # OPTIMIZATION
    # Spread sessions of the same course across days.
    # --------------------------------------------------

    course_codes = sorted(
        set(session["course_code"] for session in sessions)
    )

    course_day_used = {}

    for course_code in course_codes:

        course_day_used[course_code] = {}

        course_sessions = [
            i
            for i, session in enumerate(sessions)
            if session["course_code"] == course_code
        ]

        for day in DAYS:

            day_slots = [
                slot_index
                for slot_index, slot in enumerate(slots)
                if slot.startswith(day)
            ]

            day_used = model.NewBoolVar(
                f"{course_code}_{day}_used"
            )

            course_day_used[course_code][day] = day_used

            # If a course is assigned to any slot on this day,
            # the day_used variable must be true.
            for session_index in course_sessions:
                for slot_index in day_slots:
                    model.AddImplication(
                        assignment[(session_index, slot_index)],
                        day_used
                    )

            # If day_used is true, at least one session of this
            # course must be assigned to this day.
            model.Add(
                sum(
                    assignment[(session_index, slot_index)]
                    for session_index in course_sessions
                    for slot_index in day_slots
                ) >= day_used
            )

    # --------------------------------------------------
    # PENALTY
    #
    # A course appearing multiple times on the same day
    # should be discouraged.
    # --------------------------------------------------

    repeated_day_penalties = []

    for course_code in course_codes:

        course_sessions = [
            i
            for i, session in enumerate(sessions)
            if session["course_code"] == course_code
        ]

        for day in DAYS:

            day_slots = [
                slot_index
                for slot_index, slot in enumerate(slots)
                if slot.startswith(day)
            ]

            sessions_on_day = sum(
                assignment[(session_index, slot_index)]
                for session_index in course_sessions
                for slot_index in day_slots
            )

            # Number of extra sessions beyond the first.
            penalty = model.NewIntVar(
                0,
                len(course_sessions),
                f"{course_code}_{day}_repeat_penalty"
            )

            model.Add(
                penalty >= sessions_on_day - 1
            )

            model.Add(
                penalty >= 0
            )

            repeated_day_penalties.append(penalty)

        # --------------------------------------------------
    # OPTIMIZATION 2
    # Balance the number of classes across weekdays.
    # --------------------------------------------------

    daily_loads = {}

    for day in DAYS:

        day_slots = [
            slot_index
            for slot_index, slot in enumerate(slots)
            if slot.startswith(day)
        ]

        daily_loads[day] = model.NewIntVar(
            0,
            len(sessions),
            f"{day}_load"
        )

        model.Add(
            daily_loads[day]
            ==
            sum(
                assignment[(session_index, slot_index)]
                for session_index in range(len(sessions))
                for slot_index in day_slots
            )
        )

    # Find the busiest and least-busy days.
    max_daily_load = model.NewIntVar(
        0,
        len(sessions),
        "max_daily_load"
    )

    min_daily_load = model.NewIntVar(
        0,
        len(sessions),
        "min_daily_load"
    )

    model.AddMaxEquality(
        max_daily_load,
        list(daily_loads.values())
    )

    model.AddMinEquality(
        min_daily_load,
        list(daily_loads.values())
    )

    # Difference between busiest and least-busy day.
    daily_imbalance = model.NewIntVar(
        0,
        len(sessions),
        "daily_imbalance"
    )

    model.Add(
        daily_imbalance
        == max_daily_load - min_daily_load
    )

    # --------------------------------------------------
    # COMBINED OBJECTIVE
    # --------------------------------------------------

    model.Minimize(
        10 * sum(repeated_day_penalties)
        + daily_imbalance
    )

    # --------------------------------------------------
    # SOLVE
    # --------------------------------------------------

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = 10

    status = solver.Solve(model)

    if status not in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE,
    ):
        raise RuntimeError(
            "No feasible timetable could be generated."
        )

    # --------------------------------------------------
    # BUILD TIMETABLE
    # --------------------------------------------------

    timetable = []

    for session_index, session in enumerate(sessions):

        for slot_index, slot in enumerate(slots):

            if solver.Value(
                assignment[(session_index, slot_index)]
            ):

                timetable.append({
                    **session,
                    "assigned_slot": slot,
                })

                break

    return timetable, solver.ObjectiveValue()


if __name__ == "__main__":

    timetable, objective = generate_optimized_timetable()

    print("\nOR-Tools Optimized Timetable")
    print("=" * 55)

    for item in timetable:
        print(item)

    print("\n" + "=" * 55)
    print(f"Total sessions: {len(timetable)}")
    print(f"Optimization objective: {objective}")
