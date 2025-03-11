import sys
import pandas as pd
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget
)
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtCore import Qt, QTimer

FILE_NAME = "users.xlsx"

class RFIDApp(QWidget):
    def __init__(self, race_system):
        """
        Ge GUI-klassen en referens till RaceSystem-objektet,
        så att vi kan anropa race_system.handle_rfid_input(rfid_code).
        """
        super().__init__()

        self.race_system = race_system  # <-- Spara referensen
        self.setWindowTitle("RFID Leaderboard")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #2E3440; color: white;")

        self.stack = QStackedWidget(self)
        self.current_user_name = ""

        self.initUI()

    def initUI(self):
        """ Skapar alla vyer och lägger dem i stacked widget """
        self.rfid_screen = self.create_rfid_screen()
        self.name_screen = self.create_name_screen()
        self.welcome_screen = self.create_text_screen("Welcome back, ", "welcome_label")
        self.new_user_screen = self.create_text_screen("Welcome, ", "new_user_label")
        self.race_wait_screen = self.create_text_screen("Waiting for race to finish...")
        self.time_saved_screen = self.create_time_saved_screen()

        for screen in [self.rfid_screen, self.name_screen, self.welcome_screen,
                       self.new_user_screen, self.race_wait_screen, self.time_saved_screen]:
            self.stack.addWidget(screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.stack.setCurrentWidget(self.rfid_screen)

    def create_label(self, text, font_size=24):
        """ Skapar en standardiserad QLabel """
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def create_button(self, text, callback):
        """ Skapar en standardiserad QPushButton """
        button = QPushButton(text)
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet("background-color: #88C0D0; color: black; padding: 10px;")
        button.clicked.connect(callback)
        return button

    def create_text_screen(self, text, label_attr=None):
        """ Skapar en generisk skärm med text """
        widget = QWidget()
        layout = QVBoxLayout()

        label = self.create_label(text)
        if label_attr:
            setattr(self, label_attr, label)  # Dynamiskt sätta klassattribut för uppdatering senare

        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def create_rfid_screen(self):
        """ Skapar RFID-inmatningsskärmen """
        widget = QWidget()
        layout = QVBoxLayout()

        label = self.create_label("Scan RFID")
        self.rfid_input = QLineEdit()
        self.rfid_input.setPlaceholderText("Scan RFID here...")
        self.rfid_input.setFont(QFont("Arial", 18))
        self.rfid_input.setStyleSheet("background-color: #4C566A; color: white; padding: 5px;")
        self.rfid_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rfid_input.setValidator(QIntValidator())  # Endast siffror tillåtna

        button = self.create_button("Submit RFID", self.check_rfid)

        layout.addWidget(label)
        layout.addWidget(self.rfid_input)
        layout.addWidget(button)
        widget.setLayout(layout)

        return widget

    def create_name_screen(self):
        """ Skapar skärmen där nya användare kan ange sitt namn """
        widget = QWidget()
        layout = QVBoxLayout()

        label = self.create_label("Enter Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name...")
        self.name_input.setFont(QFont("Arial", 18))
        self.name_input.setStyleSheet("background-color: #4C566A; color: white; padding: 5px;")
        self.name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = self.create_button("Enter", self.save_new_user)

        layout.addWidget(label)
        layout.addWidget(self.name_input)
        layout.addWidget(button)
        widget.setLayout(layout)

        return widget

    def create_time_saved_screen(self):
        """ Skapar skärmen där användaren ser att tiden sparats """
        widget = QWidget()
        layout = QVBoxLayout()

        self.time_saved_label = self.create_label("Time saved to ")

        button = self.create_button("Scan new RFID", self.restart_process)

        layout.addWidget(self.time_saved_label)
        layout.addWidget(button)
        widget.setLayout(layout)

        return widget

    def check_rfid(self):
        """
        Kollar om RFID redan finns i Excel-filen.
        Kallas när man trycker på knappen 'Submit RFID'.
        """
        rfid_code = self.rfid_input.text()

        # Finns filen inte - skapa en tom
        if not os.path.exists(FILE_NAME):
            pd.DataFrame(columns=["RFID", "Name"]).to_excel(FILE_NAME, index=False)

        df = pd.read_excel(FILE_NAME)

        if rfid_code in df["RFID"].astype(str).values:
            self.current_user_name = df.loc[df["RFID"].astype(str) == rfid_code, "Name"].values[0]
            self.welcome_label.setText(f"Welcome back, {self.current_user_name}")
            # Kalla RaceSystem för att sätta start_time etc.
            self.race_system.handle_rfid_input(rfid_code)

            self.stack.setCurrentWidget(self.welcome_screen)
            QTimer.singleShot(3000, self.goto_race_wait)
        else:
            self.stack.setCurrentWidget(self.name_screen)

    def save_new_user(self):
        """ Sparar en ny användare i Excel-filen och visar välkomstskärmen """
        rfid_code = self.rfid_input.text()
        user_name = self.name_input.text()

        if user_name:
            df = pd.read_excel(FILE_NAME)
            df = pd.concat([df, pd.DataFrame({"RFID": [rfid_code], "Name": [user_name]})], ignore_index=True)
            df.to_excel(FILE_NAME, index=False)

            self.current_user_name = user_name
            self.new_user_label.setText(f"Welcome, {user_name}")
            # Även här sätter vi start_time, eftersom detta är en ny användare som ska starta race
            self.race_system.handle_rfid_input(rfid_code)

            self.stack.setCurrentWidget(self.new_user_screen)
            QTimer.singleShot(3000, self.goto_race_wait)

    def goto_race_wait(self):
        """ Byt till racevänteskärmen """
        self.stack.setCurrentWidget(self.race_wait_screen)

    def goto_time_saved(self):
        """Byt till 'Time Saved'-skärmen och visa rätt namn """
        self.time_saved_label.setText(f"Time saved to {self.current_user_name}")
        self.stack.setCurrentWidget(self.time_saved_screen)

        # 1) Skapa en timer-instans
        self.auto_return_timer = QTimer()
        
        # 2) Sätt timern i 'SingleShot'-läge (körs bara en gång)
        self.auto_return_timer.setSingleShot(True)
        
        # 3) Koppla timerns timeout-signal till self.restart_process
        self.auto_return_timer.timeout.connect(self.restart_process)
        
        # 4) Starta timern på 60 sekunder (60000 ms)
        self.auto_return_timer.start(10000)

    def restart_process(self):
        """ Återställ GUI och växla tillbaka till RFID-inmatningen """
        # Om timern fortfarande är aktiv, stoppa den
        if hasattr(self, "auto_return_timer") and self.auto_return_timer.isActive():
            self.auto_return_timer.stop()

        self.stack.setCurrentWidget(self.rfid_screen)
        self.rfid_input.clear()
        self.name_input.clear()
        
        
        
        
        
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RFIDApp()
    window.show()
    sys.exit(app.exec())
'''