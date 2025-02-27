import zlaplog_reader
import zRFID
import ztester
import zrace_handler
import threading
#import znew_leaderboard

'''def update_leaderboard(leaderboard_window, fastest_driver_label, leaderboard_label, groups, excel_filename):
    # Uppdatera leaderboarden kontinuerligt
    znew_leaderboard.continuous_update(leaderboard_window, fastest_driver_label, leaderboard_label, groups, excel_filename)
    leaderboard_window.after(1000, update_leaderboard, leaderboard_window, fastest_driver_label, leaderboard_label, groups, excel_filename)'''

def main():
    # Starta leaderboard-fönstret
    #leaderboard_window, fastest_driver_label, leaderboard_label, groups = znew_leaderboard.initialize_leaderboard_window()

    # Starta den kontinuerliga uppdateringen av leaderboard-fönstret
    #update_leaderboard(leaderboard_window, fastest_driver_label, leaderboard_label, groups, None)
    #file_watcher_thread = threading.Thread(target=zlaplog_reader.watch_file_for_updates, daemon = True)
    #file_watcher_thread.start()
    while True:
        
        track, car, bestlap = None, None, None
        #print("HEj")
        # Hämta datum och tid

        # Hämta banan, bilen och bästa varvtiden från loggen
        try:
            track, car, bestlap = zlaplog_reader.find_track_car(track, car, bestlap)
            # Hantera leaderboard-fil
            excel_filename = ztester.set_excel_filename(track, car)
            df = ztester.load_or_create_leaderboard()
            print(excel_filename)

        except:
            continue
        


        #zlaplog_reader.watch_file_for_updates()


        # Hämta RFID och kolla om den redan finns i data
        input_rfid = zRFID.get_rfid()

        if input_rfid in df['RFID'].astype(str).values:
            # Om RFID redan finns, hämta namnet som är kopplat till det
            existing_name = df.loc[df['RFID'].astype(str) == input_rfid, 'NAME'].values[0]
            print(f"RFID {input_rfid} är kopplat till namnet {existing_name}.")
            print(f"Welcome back, {existing_name}!")
            input_name = existing_name
        else:
            # Om RFID är nytt, fråga efter namn
            input_name = zRFID.get_name()
            print(f"En ny användare {input_name} har skapats.")

        # Uppdatera eller lägg till racerns information i leaderboard
        df = ztester.update_or_add_racer(df, input_rfid, input_name, bestlap)
        df = ztester.sort_leaderboard(df)
        df.to_excel(excel_filename, index=False)

        # Uppdatera leaderboard-fönstret med den nya filen
        #znew_leaderboard.continuous_update(leaderboard_window, fastest_driver_label, leaderboard_label, groups, excel_filename)

        # Starta race UI
        race_ui = zrace_handler.RaceUI(input_name)
        race_ui.run()

        # RFID ska visas igen efter att race är klart
        print("Återstartar RFID-inmatningen...")
        continue  # Startar om loopen för att återgå till RFID-inmatningen
        
if __name__ == "__main__":
    main()





#Leta upp senasted RACE end och hätma tiden
#Laps tar bort best lap på skärmen och även om användaren sparar tiden

