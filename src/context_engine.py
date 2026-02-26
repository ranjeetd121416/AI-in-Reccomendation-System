from datetime import datetime
from config import STUDY_START, STUDY_END

def get_context():

    now = datetime.now()
    hour = now.hour
    day = now.weekday()

    if day < 5 and STUDY_START <= hour <= STUDY_END:
        return "study"

    elif day < 5:
        return "entertainment"

    return "weekend"