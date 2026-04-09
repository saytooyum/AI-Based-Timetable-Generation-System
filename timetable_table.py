import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def generate_simple_timetable():
    courses_file = os.path.join(DATA_PATH, "courses.csv")
    
    courses = pd.read_csv(courses_file)

    slots = [
        "Monday 9:00 AM",
        "Monday 11:00 AM",
        "Tuesday 10:00 AM",
        "Wednesday 12:00 PM",
        "Thursday 2:00 PM"
    ]

    timetable = []

    for i, row in courses.iterrows():
        timetable.append({
            "course_code": row["course_code"],
            "course_name": row["course_name"],
            "assigned_slot": slots[i % len(slots)]
        })

    return timetable


if __name__ == "__main__":
    tt = generate_simple_timetable()
    for item in tt:
        print(item)