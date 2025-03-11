import re
import time
from datetime import datetime

class LapLogParser:
    """ Hanterar parsing av loggfil för att extrahera bil, bana och bästa varvtid, med tidskontroll. """

    def __init__(self, filepath):
        self.filepath = filepath
        self.track = None
        self.car = None
        self.bestlap = None
        self.start_time = None  # Hämtas från GUI
        self.end_time = None

    def set_start_time(self):
        """ Sätt starttiden från GUI när RFID skannas """
        self.start_time = int(datetime.now().strftime('%H:%M:%S').replace(":", ""))
        #print(f"🏁 Start Time Set: {self.start_time.strftime('%H:%M:%S')}")

    def parse_race_end(self, line):
        """ Letar efter 'RACE_END' och extraherar data """
        self.time_match = int(((re.search(r'(\d{2}:\d{2}:\d{2})', line)).group(1)).replace(":", ""))  # Hämta tiden från raden
        track_match = re.search(r'\btrack\s+\"?([\w_]+)\"?', line)
        car_match = re.search(r'\bcar\s+\"?([\w_]+)\"?', line)
        bestlap_match = re.search(r'\bbestlap\s+(\S+)', line)

        if self.time_match and track_match and car_match and bestlap_match:
            print("hello2")
            # Kontrollera om detta race är det som startades senast
            #print("self")
            if self.start_time < self.time_match:
                self.track = track_match.group(1)
                self.car = car_match.group(1)
                self.bestlap = bestlap_match.group(1)

                print(f"\n✅ Valid Race Found!")
                print(f"🛣️ Track: {self.track}")
                print(f"🚗 Car: {self.car}")
                print(f"⏱️ Best Lap Time: {self.bestlap}")

                return self.track, self.car, self.bestlap

        return None

    def monitor_logfile(self):
        """ Övervakar loggfilen i realtid och väntar på 'RACE_END' """
        print(f"📡 Monitoring log file: {self.filepath}")
        with open(self.filepath, 'r', encoding='utf-8') as file:
            file.seek(0, 2)  # Gå till slutet av filen

            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)  # Vänta en halv sekund innan nästa försök
                    continue

                print(line.strip())  # Skriv ut varje rad (kan tas bort om det blir för mycket logg)
                
                if "RACE_END" in line:
                    self.parse_race_end(line)  # Extrahera info
                    
                    
                    
                    
'''
if __name__ == "__main__":
    laplog_path = "D:\\Studier\\Chalmers\\Caster\\Github_Leaderboard\\leaderboard\\Leaderboard_Caster\\laplog.txt"

    parser = LapLogParser(laplog_path)

    # Simulerar att RFID skannas och starttid sätts från GUI
    parser.set_start_time()

    # Starta övervakning av loggfilen
    parser.monitor_logfile()
'''