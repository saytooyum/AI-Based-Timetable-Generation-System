import os
import pandas as pd


DATA_PATH = os.path.join(os.path.dirname(__file__), "..")

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]

TIME_SLOTS = [
    "9:00 AM",
    "10:00 AM",
    "11:00 AM",
    "12:00 PM",
    "2:00 PM",
    "3:00 PM",
]


def generate_slots():
    """Generate all available weekly timetable slots."""
    return [
        f"{day} {time}"
        for day in DAYS
        for time in TIME_SLOTS
    ]
SLOTS = generate_slots()


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
def calculate_quality_score(timetable):
    """Calculate a basic quality score for a generated timetable."""

    score = 100

    # --------------------------------------------------
    # 1. Penalize slot collisions
    # --------------------------------------------------

    slots = [item["assigned_slot"] for item in timetable]

    collisions = len(slots) - len(set(slots))

    score -= collisions * 20

    # --------------------------------------------------
    # 2. Reward balanced daily workload
    # --------------------------------------------------

    day_counts = {day: 0 for day in DAYS}

    for item in timetable:
        for day in DAYS:
            if item["assigned_slot"].startswith(day):
                day_counts[day] += 1
                break

    daily_values = list(day_counts.values())

    if daily_values:
        max_classes = max(daily_values)
        min_classes = min(daily_values)

        imbalance = max_classes - min_classes

        score -= imbalance * 3

    # --------------------------------------------------
    # 3. Reward course distribution across days
    # --------------------------------------------------

    course_days = {}

    for item in timetable:
        course = item["course_code"]

        if course not in course_days:
            course_days[course] = set()

        for day in DAYS:
            if item["assigned_slot"].startswith(day):
                course_days[course].add(day)
                break

    for days in course_days.values():
        if len(days) >= 2:
            score += 2

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return score

def generate_simple_timetable():
    """Generate a timetable with sessions distributed across the week."""
    courses_file = os.path.join(DATA_PATH, "courses.csv")
    courses = pd.read_csv(courses_file)

    sessions = generate_sessions(courses)

    if len(sessions) > len(SLOTS):
        raise ValueError(
            f"Not enough time slots: {len(sessions)} sessions "
            f"require {len(sessions)} slots, but only {len(SLOTS)} are available."
        )

    timetable = []

    # Track how many sessions have been assigned to each day
    day_counts = {day: 0 for day in DAYS}

    # Group available slots by day
    slots_by_day = {
        day: [slot for slot in SLOTS if slot.startswith(day)]
        for day in DAYS
    }

    # Track the next available slot for each day
    day_indices = {day: 0 for day in DAYS}

    # Assign sessions round-robin across days
    for i, session in enumerate(sessions):
        day = DAYS[i % len(DAYS)]

        if day_indices[day] >= len(slots_by_day[day]):
            raise ValueError(f"No available slots remaining on {day}.")

        slot = slots_by_day[day][day_indices[day]]
        day_indices[day] += 1
        day_counts[day] += 1

        timetable.append({
            **session,
            "assigned_slot": slot,
        })

    return timetable

if __name__ == "__main__":
    timetable = generate_simple_timetable()

    for item in timetable:
        print(item)

    score = calculate_quality_score(timetable)

    print("\n----------------------------")
    print(f"Timetable Quality Score: {score}/100")
    print("----------------------------")