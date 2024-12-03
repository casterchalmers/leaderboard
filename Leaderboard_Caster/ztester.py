import pandas as pd
from pathlib import Path

# Globala variabler
excel_filename = None

def set_excel_filename(track, car):
    """Sätt värdet på excel_filename baserat på track och car."""
    global excel_filename
    excel_filename = f"{track}_{car}.xlsx"
    return excel_filename
# Kör set_excel_filename för att sätta värdet direkt vid import

def load_or_create_leaderboard():
    """Ladda eller skapa en ny leaderboard."""
    global excel_filename
    # Kontrollera om filen redan finns
    if not Path(excel_filename).is_file():
        # Skapa en ny Excel-fil om den inte redan finns
        headers = ['RFID', 'NAME', 'LAPTIME']
        df = pd.DataFrame(columns=headers)
        # Spara DataFrame till Excel-fil
        df.to_excel(excel_filename, index=False)
    else:
        # Om filen redan existerar, läs in den
        df = pd.read_excel(excel_filename)
    return df

# Andra importsatser ...

def update_or_add_racer(df, input_rfid, input_name, bestlap):
    """Uppdatera eller lägg till racer baserat på RFID och varvtid."""
    if input_rfid in df['RFID'].astype(str).values:
        # Hämta namnet kopplat till RFID
        existing_name = df.loc[df['RFID'].astype(str) == input_rfid, 'NAME'].values[0]
        print(f"RFID {input_rfid} är kopplat till namnet {existing_name}.")
        
        # Få in den nya varvtiden
        input_laptime = bestlap
        
        # Hämta den existerande tiden för RFID
        current_time_str = df.loc[df['RFID'].astype(str) == input_rfid, 'LAPTIME'].values[0]
        
        # Konvertera tider till timedelta för jämförelse
        current_time = pd.to_timedelta(current_time_str)
        input_time = pd.to_timedelta(input_laptime)
        
        # Jämför den nya tiden med den existerande
        if input_time < current_time:
            # Uppdatera tiden om den nya är bättre
            df.loc[df['RFID'].astype(str) == input_rfid, 'LAPTIME'] = input_laptime
            print(f"Uppdaterad varvtid för {existing_name} till {input_laptime}.") #TA BORT
        else:
            print(f"Den befintliga tiden för {existing_name} ({current_time_str}) är bättre eller samma.") #TA BORT
    else:
        # Ny RFID, lägg till ny post med namn och varvtid
        input_laptime = bestlap
        
        new_row = pd.DataFrame({'RFID': [input_rfid], 'NAME': [input_name], 'LAPTIME': [input_laptime]})
        df = pd.concat([df, new_row], ignore_index=True)
        print(f"Lade till nytt RFID: {input_rfid}, namn: {input_name} med varvtid {input_laptime}.")
    
    return df



def sort_leaderboard(df):
    """Sortera leaderboarden baserat på Laptime."""
    # Konvertera Laptime-kolumnen till timedelta för korrekt sortering
    df['Laptime_Timedelta'] = pd.to_timedelta(df['LAPTIME'])
    
    # Sortera leaderboarden baserat på Laptime_Timedelta i stigande ordning
    df = df.sort_values(by='Laptime_Timedelta').drop(columns='Laptime_Timedelta')
    
    return df





