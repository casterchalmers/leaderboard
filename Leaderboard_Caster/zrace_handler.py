from tkinter import *
from screeninfo import get_monitors
from datetime import datetime

class RaceUI:
    def __init__(self, username):
        # Initialisera fönster och UI-komponenter
        self.username = username
        self.screen_width = get_monitors()[0].width
        self.screen_height = get_monitors()[0].height
        self.window = Tk()
        self.window.geometry(f'{self.screen_width}x{self.screen_height}')
        self.window.attributes("-fullscreen", True)
        self.window.configure(bg="black")
        
        self.time_ref = None
        self.create_initial_ui()

    def start_race(self):
        time_today = datetime.today().strftime("%Y%m%d%H%M%S")
        self.time_ref = int(time_today)
        self.kill_ui_elements()
        self.button_finish_race.pack()

    def finish_race(self):
        wait_label = Label(self.window, text="Please wait (3 sec)....", bg="black", fg="white", font=("Arial", 30), relief="flat", justify=CENTER)
        wait_label.pack()
        self.window.update()
        self.window.after(3000, self.window.destroy)  # Vänta i 3 sekunder innan fönstret stängs

    def create_initial_ui(self):
        distance = Label(self.window, text="A", bg="black", fg="black", font=("Arial", 200), relief="flat", justify=CENTER)
        distance.pack()

        self.welcome_label = Label(self.window, text=(f"Welcome, {self.username}!"), bg="black", fg="white", font=("Arial", 30), relief="flat", justify=CENTER)
        self.welcome_label.pack()

        self.button_start_race = Button(self.window, text="Start Race", command=self.start_race, height=1, bg='green', fg='white', font=('Arial', 30))
        self.button_start_race.pack()

        self.button_finish_race = Button(self.window, text="Finish Race", command=self.finish_race, height=1, bg='red', fg='white', font=('Arial', 30), activebackground="white")

    def kill_ui_elements(self):
        self.welcome_label.destroy()
        self.button_start_race.destroy()

    def run(self):
        self.window.mainloop()








