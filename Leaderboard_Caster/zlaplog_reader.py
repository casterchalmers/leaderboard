#CASTER LEADERBOARD
#Version 1
#Filip Johansson


import re
import os
import time
from datetime import datetime

# Filvägen till loggfilen
laplog_path = "L:\\laplog.txt" 
track = None
car = None
bestlap = None
start_time = None
end_time = None

def find_track_car(track, car, bestlap):
    global  start_time, end_time

    # Öppna filen och läs alla rader
    with open(laplog_path, "r") as file:
        laplog_text = file.readlines()

    # Läs den senaste raden
    last_line = laplog_text[-1].strip()
    print("ddd", last_line)
    session_started = "Session started"
    race_end = "RACE_END"

    if session_started in last_line:
        start_time = int((last_line[12:20]).replace(":", ""))
        print(f"New session started at {start_time}")

    if race_end in last_line:
        end_time = int((last_line[12:20]).replace(":", ""))
        print(f"Race ended at {end_time}")

        if start_time is not None and end_time is not None and end_time >= start_time:
            track_match = re.search(r'\btrack\s+(\S+)', last_line)
            car_match = re.search(r'\bcar\s+(\S+)', last_line)
            bestlap_match = re.search(r'\bbestlap\s+(\S+)', last_line)

            if track_match and car_match and bestlap_match:
                track = track_match.group(1).replace('"', '')
                car = car_match.group(1).replace('"', '')
                bestlap = bestlap_match.group(1).replace('"', '')
    print(track, car, bestlap)
    return track, car, bestlap

    #return None, None, None

def watch_file_for_updates():
    global track, car, bestlap  # Definiera dessa som globala variabler

    last_modified_time = os.path.getmtime(laplog_path)

    while True:
        current_modified_time = os.path.getmtime(laplog_path)
        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
            track, car, bestlap = find_track_car()
            
            if track and car and bestlap:
                print(f"Updated - Track: {track}, Car: {car}, Best Lap: {bestlap}")

        time.sleep(2)  # Kontrollera filen varannan sekund

