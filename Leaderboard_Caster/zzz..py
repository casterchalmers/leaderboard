#import hashlib
#import time



'''
def calculate_file_hash(laplog_path):
    with open(laplog_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash

def detect_file_changes(laplog_path):
    last_hash = calculate_file_hash(laplog_path)
    while True:
        current_hash = calculate_file_hash(laplog_path)
        if current_hash != last_hash:
            print("File has changed!")
            last_hash = current_hash
        time.sleep(1)

# Usage
detect_file_changes("H:\TESTKORNING\Leaderboard_Caster\laplog.txt")
'''

'''
# Läser av hela filen vid början nedifrån och upp och slutar vid "laps".
def read_file_reverse(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Börja läsa från sista raden
    for line in reversed(lines):
        print(line.strip())
        if 'laps' in line:
            break


# Exempel på användning
read_file_reverse("D:\\Studier\\Chalmers\\Caster\\Github_Leaderboard\\leaderboard\\Leaderboard_Caster\\laplog.txt")
'''

# 1. Tiden kommer fram på skärmen när den hittar" RACE END".
#    När txt-filen uppdateras ska programmet känna av det och därefter försöka hitta "RACE END"

# 2. Användaren väljer att trycka på "SAVE TIME" och scannar RFID och skriver in sitt namn

# 3. När txt-filen uppdateras till "SESSION STARTED" ta bort tiden från skärmen


# 1-3 loopas om och om igen
import time

def monitor_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        file.seek(0, 2)  # Gå till slutet av filen

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)  # Vänta en halv sekund innan nästa försök
                continue

            print(line.strip())
            if 'laps' in line:
                print("STOP")
                break

monitor_file("D:\\Studier\\Chalmers\\Caster\\Github_Leaderboard\\leaderboard\\Leaderboard_Caster\\laplog.txt")


















#zlaplog reder
'''
import re
from datetime import datetime

# Filvägen till loggfilen
#laplog_path = "L:\laplog.txt"
laplog_path = "H:\TESTKORNING\Leaderboard_Caster\laplog.txt"
track = None
car = None
bestlap = None
start_time = None
end_time = None

def find_track_car(track, car, bestlap):
    # Öppna filen och läs alla rader
    with open(laplog_path, "r") as file:
        laplog_text = file.readlines()
    # Läs den senaste raden
    last_line = laplog_text[-1].strip()
        #print(f"Senaste raden: {last_line}")
        # Kontrollera om datumet finns i den senaste raden
      
    session_started = "Session started"
    Race_end = "RACE_END"

    if session_started in last_line:
        start_time = int((last_line[12:20]).replace(":", ""))
        print(start_time)
    if Race_end in last_line:
        end_time = int((last_line[12:20]).replace(":", ""))
            #print(start_time)

            #datum = "20-03-2024" # TA BORT Används vid testning!
            #time = 181552 # TA BORT Används vid testning!
        if start_time is not None and end_time is not None and end_time >= start_time:
            track_match = re.search(r'\btrack\s+(\S+)', last_line)
            car_match = re.search(r'\bcar\s+(\S+)', last_line)
            bestlap_match = re.search(r'\bbestlap\s+(\S+)', last_line)
            if track_match and car_match and bestlap_match:
                track = track_match.group(1).replace('"', '')
                car = car_match.group(1).replace('"', '')
                bestlap = bestlap_match.group(1).replace('"', '')
                return track, car, bestlap


    return None, None, None
        
track, car, bestlap = find_track_car(track, car, bestlap)

if track and car and bestlap:
    print(f"Track: {track}, Car: {car}, Best Lap: {bestlap}")
'''