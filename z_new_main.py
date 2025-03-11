import sys
import os
import pandas as pd
import threading
from PyQt6.QtWidgets import QApplication
from znew_RFID_qt import RFIDApp
from z_get_info import LapLogParser
from z_excel_handler import LeaderboardManager

# 🔹 Filväg till loggfilen (ändra vid behov)
LOG_FILE_PATH = "D:\\Studier\\Chalmers\\Caster\\Github_Leaderboard\\leaderboard\\Leaderboard_Caster\\laplog.txt"

class RaceSystem:
    """ Huvudklass som kopplar ihop GUI, loggfil och leaderboard-hantering. """

    def __init__(self):
        """ Initierar systemet och startar GUI samt loggövervakning. """
        self.gui = RFIDApp()
        self.log_parser = LapLogParser(LOG_FILE_PATH)

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
        """ Hanterar RFID-inmatning från GUI. """
        self.current_rfid = rfid_code

        # Läs in användarnamn från Excel-filen
        if os.path.exists("users.xlsx"):
            df = pd.read_excel("users.xlsx")
            if rfid_code in df["RFID"].astype(str).values:
                self.current_name = df.loc[df["RFID"].astype(str) == rfid_code, "Name"].values[0]
            else:
                self.current_name = None

        # Starta race och sätt starttiden
        self.log_parser.set_start_time()

    def monitor_race_end(self):
        """ Övervakar loggfilen i realtid och hämtar raceresultat när race avslutas. """
        while True:
            race_data = self.log_parser.monitor_logfile()  # Väntar på RACE_END
            if race_data:
                self.track, self.car, self.bestlap = race_data
                self.process_race_results()

    def process_race_results(self):
        """ Processar race-resultaten och uppdaterar leaderboarden. """
        print(f"🔍 DEBUG: process_race_results() kallades.")
        print(f"🎯 RFID: {self.current_rfid}, Track: {self.track}, Car: {self.car}, Bestlap: {self.bestlap}")

        if self.current_rfid and self.track and self.car and self.bestlap:
            leaderboard = LeaderboardManager(track=self.track, car=self.car)
            leaderboard.update_or_add_racer(self.current_rfid, self.bestlap)

            print(f"🏁 Leaderboard uppdaterad för {self.track} med bilen {self.car}!")
            print(f"🔄 Växlar GUI till 'Time Saved' med tiden: {self.bestlap}")

            # 🟢 När race är klart, uppdatera GUI och visa varvtiden
            self.gui.show_time_saved_screen(self.bestlap)
        else:
            print("⚠ ERROR: Race-resultat saknar nödvändig information och GUI byter inte skärm.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    race_system = RaceSystem()

    # Koppla GUI:ts RFID-inmatning till systemet
    race_system.gui.check_rfid = race_system.handle_rfid_input

    race_system.gui.show()
    sys.exit(app.exec())
