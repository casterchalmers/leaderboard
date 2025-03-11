import sys
import os
import pandas as pd
import threading
from PyQt6.QtWidgets import QApplication
from znew_RFID_qt import RFIDApp
from z_get_info import LapLogParser
from z_excel_handler import LeaderboardManager
from pathlib import Path

# 🔹 Filväg till loggfilen (ändra vid behov)
LOG_FILE_PATH = Path("D:/Studier/Chalmers/Caster/Github_Leaderboard/leaderboard/Leaderboard_Caster/laplog.txt")

class RaceSystem:
    """ Huvudklass som kopplar ihop GUI, loggfil och leaderboard-hantering. """

    def __init__(self):
        """ Initierar systemet och startar GUI samt loggövervakning. """
        # Skapa GUI och skicka in self som referens
        self.gui = RFIDApp(self)

        # Skapa log-parser
        self.log_parser = LapLogParser(str(LOG_FILE_PATH))

        # Variabler för race-info
        self.current_rfid = None
        self.current_name = None
        self.track = None
        self.car = None
        self.bestlap = None

        # Starta en tråd för att övervaka loggfilen
        self.log_thread = threading.Thread(target=self.monitor_race_end, daemon=True)
        self.log_thread.start()

    def handle_rfid_input(self, rfid_code):
        """ Hanterar RFID-inmatning från GUI (startar racet och sätter start_time). """
        self.current_rfid = rfid_code

        # Läs in användarnamn från Excel-filen (om finns)
        users_file = Path("users.xlsx")
        if users_file.exists():
            df = pd.read_excel(users_file)
            if rfid_code in df["RFID"].astype(str).values:
                self.current_name = df.loc[df["RFID"].astype(str) == rfid_code, "Name"].values[0]
            else:
                self.current_name = None

        # Sätt starttiden för racet
        self.log_parser.set_start_time()

    def monitor_race_end(self):
        """ Övervakar loggfilen i realtid och hämtar raceresultat när race avslutas. """
        print("📡 Startar övervakning av loggfilen...")

        while True:
            with open(LOG_FILE_PATH, 'r', encoding='utf-8') as file:
                file.seek(0, 2)  # Hoppa till slutet av filen
                while True:
                    line = file.readline()
                    if not line:
                        continue
                    if "RACE_END" in line:
                        result = self.log_parser.parse_race_end(line)
                        if result:
                            self.track, self.car, self.bestlap = result
                            self.process_race_results()
                            break

    def process_race_results(self):
        """ Processar race-resultaten och uppdaterar leaderboarden. """
        print(f"🏁 Race avslutat: {self.track}, {self.car}, {self.bestlap}")

        if self.current_rfid and self.track and self.car and self.bestlap:
            leaderboard = LeaderboardManager(track=self.track, car=self.car)
            leaderboard.update_or_add_racer(self.current_rfid, self.bestlap)

            print(f"✅ Leaderboard uppdaterad för {self.track} med bilen {self.car}!")

            # När race är klart, uppdatera GUI och visa varvtiden
            self.gui.goto_time_saved()
        else:
            print("⚠ ERROR: Race-resultat saknar nödvändig information och GUI byter inte skärm.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    race_system = RaceSystem()
    
    # OBS! Vi tar bort (eller kommenterar bort) denna rad så vi inte 
    # överskuggar GUI:ts befintliga check_rfid-metod:
    # race_system.gui.check_rfid = race_system.handle_rfid_input

    race_system.gui.show()
    sys.exit(app.exec())
