
def get_opening_status():
    """Determines the opening status based on the day of the week and time."""
    now = datetime.now()
    day_of_week = now.weekday()  # 0 (Monday) to 6 (Sunday)
    hour = now.hour

    if day_of_week < 5:  # Monday to Friday
        if 9 <= hour < 23:  # 9 AM to 11 PM
            return "Open", "success"  # Bootstrap success class for green
        else:
            return "Closed", "danger"   # Bootstrap danger class for red
    elif day_of_week == 5: # Saturday
        if 10 <= hour < 14: # 10 AM to 2 PM
            return "Open", "success"
        else:
            return "Closed", "danger"
    else:  # Sunday
        return "Closed", "danger"

def get_word_of_the_day():
    """Returns a word based on the day of the week."""
    days = ["Motivation", "Innovation", "Productivity", "Focus", "Growth", "Relaxation", "Reflection"]
    day_index = datetime.now().weekday()
    return days[day_index]

