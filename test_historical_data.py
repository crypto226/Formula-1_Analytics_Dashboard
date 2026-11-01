
from api.f1_api import (
    get_race_details,
    get_session_laps,
    get_driver_positions,
    get_pit_stops,
    get_tyre_stints,
    get_session_weather,
    get_race_control
)

# Select the year
YEAR = 2025

races = get_race_details(YEAR)

if not races:
    print("No races found!")
    raise SystemExit

# Select a Grand Prix
for index, race in enumerate(races):
    print(f"{index + 1}. {race['race_name']}")

choice = int(input("\nSelect a Grand Prix: "))

selected_race = races[choice - 1]
session_key = selected_race["session_key"]

print("\nSelected:", selected_race["race_name"])
print("Session key:", session_key)

# Retrieve historical data
laps = get_session_laps(session_key)
positions = get_driver_positions(session_key)
pits = get_pit_stops(session_key)
stints = get_tyre_stints(session_key)
weather = get_session_weather(session_key)
race_control = get_race_control(session_key)

print("\n========== DATA SUMMARY ==========")

print("Lap records:", len(laps))
print("Position records:", len(positions))
print("Pit stop records:", len(pits))
print("Tyre stint records:", len(stints))
print("Weather records:", len(weather))
print("Race control messages:", len(race_control))

if laps:
    print("\nSample lap record:")
    print(laps[0])

if weather:
    print("\nLatest returned weather record:")
    print(weather[-1])

print("\nHistorical data retrieval completed!")
