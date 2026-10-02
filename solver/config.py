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
