
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

    # dictionary to match meetings by meeting_key
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
            "date": session.get("date_start", "N/A"),
            "session_key": session.get("session_key"),
            "meeting_key":meeting_key
        }

        race_details.append(race)
    return race_details

       


def get_session_drivers(session_key):

    url = f"{BASE_URL}/drivers"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()    


#LAP DATA
def get_session_laps(session_key):
    url = f"{BASE_URL}/laps"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


#DRIVER POSITION

def get_driver_positions(session_key):
    url = f"{BASE_URL}/position"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


#pit-stop information

def get_pit_stops(session_key):
    url = f"{BASE_URL}/pit"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


#TYRE STATEGY

def get_tyre_stints(session_key):
    url = f"{BASE_URL}/stints"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


#WEATHER INFORMATION

def get_session_weather(session_key):
    url = f"{BASE_URL}/weather"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


#RACE CONTROL

def get_race_control(session_key):
    url = f"{BASE_URL}/race_control"

    params = {
        "session_key": session_key
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()



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
        # Select a Grand Prix
    choice = int(input("\nSelect a Grand Prix number: "))

    selected_race = races[choice - 1]

    # Get the selected race's session key
    session_key = selected_race["session_key"]

    # Fetch drivers for that session
    drivers = get_session_drivers(session_key)

    print("\nDRIVERS PARTICIPATING IN THIS SESSION\n")

    for driver in drivers:
        print("Driver:", driver.get("full_name") or "N/A")
        print("Number:", driver.get("driver_number") or "N/A")
        print("Team:", driver.get("team_name") or "N/A")
        print("Abbreviation:", driver.get("name_acronym") or "N/A")
        print("-" * 50)    

