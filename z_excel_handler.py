import pandas as pd
from pathlib import Path

class LeaderboardManager:
    """Hantera leaderboard i en Excel-fil för en specifik bana och bil."""

    def __init__(self, track, car):
        """Initialiserar leaderboarden baserat på track och car."""
        self.excel_filename = f"{track}_{car}.xlsx"
        self.users_file = "users.xlsx"  # Filen som innehåller alla registrerade användare
        self.df = self.load_or_create_leaderboard()

    def load_or_create_leaderboard(self):
        """Laddar eller skapar en ny leaderboard-fil."""
        if not Path(self.excel_filename).is_file():
            # Skapa ny fil med kolumnrubriker om den inte finns
            df = pd.DataFrame(columns=['RFID', 'NAME', 'LAPTIME'])
            df.to_excel(self.excel_filename, index=False)
        else:
            # Läs in befintlig fil
            df = pd.read_excel(self.excel_filename)
        return df

    def update_or_add_racer(self, input_rfid, bestlap):
        """Uppdaterar eller lägger till racer baserat på RFID och bästa varvtid."""

        # Kolla om users.xlsx existerar
        if not Path(self.users_file).is_file():
            print("⚠ ERROR: users.xlsx hittades inte!")
            return

        # Läs in användare från users.xlsx
        users_df = pd.read_excel(self.users_file)

        # Kolla om RFID finns i users.xlsx
        if input_rfid not in users_df["RFID"].astype(str).values:
            print(f"⚠ ERROR: RFID {input_rfid} finns inte i users.xlsx! Ingen uppdatering sker.")
            return

        # Hämta användarnamn kopplat till RFID
        input_name = users_df.loc[users_df["RFID"].astype(str) == input_rfid, "Name"].values[0]

        # Konvertera bästa varvtiden till timedelta
        input_laptime = pd.to_timedelta(bestlap)

        if input_rfid in self.df['RFID'].astype(str).values:
            # Hämta befintligt namn och tid
            existing_name = self.df.loc[self.df['RFID'].astype(str) == input_rfid, 'NAME'].values[0]
            current_time_str = self.df.loc[self.df['RFID'].astype(str) == input_rfid, 'LAPTIME'].values[0]
            current_time = pd.to_timedelta(current_time_str)

            # Uppdatera om den nya tiden är bättre
            if input_laptime < current_time:
                self.df.loc[self.df['RFID'].astype(str) == input_rfid, 'LAPTIME'] = bestlap
                print(f"✅ Uppdaterade varvtid för {existing_name} ({input_rfid}) till {bestlap}.")
        else:
            # Ny förare, lägg till i leaderboarden
            new_row = pd.DataFrame({'RFID': [input_rfid], 'NAME': [input_name], 'LAPTIME': [bestlap]})
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            print(f"🆕 Lade till ny förare {input_name} ({input_rfid}) med varvtid {bestlap}.")

        self.sort_leaderboard()
        self.save_leaderboard()

    def sort_leaderboard(self):
        """Sorterar leaderboarden efter bästa varvtid."""
        self.df['Laptime_Timedelta'] = pd.to_timedelta(self.df['LAPTIME'])
        self.df = self.df.sort_values(by='Laptime_Timedelta').drop(columns='Laptime_Timedelta')

    def save_leaderboard(self):
        """Sparar den uppdaterade leaderboarden till Excel."""
        self.df.to_excel(self.excel_filename, index=False)
        print(f"💾 Sparade leaderboard till {self.excel_filename}")

    def get_leaderboard(self):
        """Returnerar leaderboarden som en DataFrame."""
        return self.df


# **🔹 Exempel på hur klassen används**
'''
if __name__ == "__main__":
    # Skapa leaderboard för en specifik bana och bil
    leaderboard = LeaderboardManager(track="adsdutodromo_nazionale_monza", car="ferrari_f2004")

    # Uppdatera leaderboard med ny racer
    leaderboard.update_or_add_racer(input_rfid="69", input_name="Agusut Uttersäv", bestlap="00:01:27.784")

    # Hämta och visa leaderboard
    df = leaderboard.get_leaderboard()
    print(df)
'''