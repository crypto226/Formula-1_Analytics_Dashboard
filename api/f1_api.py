
import requests

BASE_URL = "https://api.openf1.org/v1"


def get_f1_sessions(year):
    url = f"{BASE_URL}/sessions"

    params = {
        "year": year,
        "session_name": "Race"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()


def get_f1_meetings(year):
    url = f"{BASE_URL}/meetings"

    params = {
        "year": year
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()


def get_race_details(year):

    sessions = get_f1_sessions(year)
    meetings = get_f1_meetings(year)

    # Create a dictionary to match meetings by meeting_key
    meeting_lookup = {
        meeting["meeting_key"]: meeting
        for meeting in meetings
    }

    race_details = []

    for session in sessions:

        meeting_key = session.get("meeting_key")

        # Find the matching Grand Prix
        meeting = meeting_lookup.get(meeting_key, {})

        race = {
            "race_name": meeting.get("meeting_name", "N/A"),
            "country": session.get("country_name") or meeting.get("country_name", "N/A"),
            "circuit": session.get("circuit_short_name") or meeting.get("circuit_short_name", "N/A"),
            "session": session.get("session_name", "N/A"),
            "date": session.get("date_start", "N/A")
        }

        race_details.append(race)

    return race_details


if __name__ == "__main__":

    races = get_race_details(2025)

    print("\nFORMULA 1 RACE CALENDAR - 2025\n")
    print("-" * 75)

    for race in races:

        print("Grand Prix:", race["race_name"])
        print("Country:", race["country"])
        print("Circuit:", race["circuit"])
        print("Session:", race["session"])
        print("Date:", race["date"])

        print("-" * 75)

