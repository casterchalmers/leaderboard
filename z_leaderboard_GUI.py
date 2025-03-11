import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt6.QtGui import (
    QGuiApplication, QPixmap, QPainter
)
from PyQt6.QtCore import Qt

# Exempeldata för 12 förare
ALL_DATA = [
    (1,  "MAXSTEPPER",             "02:07.342"),
    (2,  "FEROCIOUS ROACHES",      "02:07.322"),
    (3,  "JEAN JACKET",            "02:07.312"),
    (4,  "TWITCHREACH97",          "02:07.424"),
    (5,  "BEETLEJUICE",            "02:07.432"),
    (6,  "THE REAPER",             "02:08.452"),
    (7,  "OCCULONIMBUS EDOEQUUS",  "02:08.478"),
    (8,  "TERMINATOR1000",         "02:08.542"),
    (9,  "INITIALG",               "02:09.564"),
    (10, "LUPIN NIPUL",            "02:09.582"),
    (11, "SPEEDFLYER",             "02:10.642"),
    (12, "MAROONLINE",             "02:10.655"),
]

def create_leaderboard_table(data_slice):
    """
    Skapar och returnerar en QTableWidget för en uppsättning förare.
    data_slice förväntas vara en lista av tupler: (rank, driver, best_lap).
    """
    table = QTableWidget()
    table.setObjectName("LeaderboardTable")

    # 1) Ingen redigering
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    # 2) Ingen markering alls
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    # 3) Ingen fokusram
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    # 3 kolumner: "#", "Förare", "Bästa Varv"
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["#", "Förare", "Bästa Varv"])

    # Dölj radhuvudena (så vi inte får dubbel numrering)
    table.verticalHeader().setVisible(False)

    # Fyll tabellen
    table.setRowCount(len(data_slice))
    for row, (rank, driver, best_lap) in enumerate(data_slice):
        table.setItem(row, 0, QTableWidgetItem(str(rank)))
        table.setItem(row, 1, QTableWidgetItem(driver))
        table.setItem(row, 2, QTableWidgetItem(best_lap))

    # Kolumninställningar
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # "#"
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # "Förare"
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # "Bästa Varv"

    return table

class LeaderboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # === Skärminformation & fönsterstorlek ===
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Fönstret ~80% av skärmens storlek (exempel)
        width = int(screen_geometry.width() * 0.8)
        height = int(screen_geometry.height() * 0.8)
        self.setWindowTitle("Autodromo – Porsche 911")
        self.resize(width, height)

        # Centrera fönstret
        frame_geo = self.frameGeometry()
        frame_geo.moveCenter(screen_geometry.center())
        self.move(frame_geo.topLeft())

        # === Ladda in bakgrundsbild ===
        # Använd absolut sökväg om du är osäker på var bilden ligger.
        self.original_bg = QPixmap("porsche.webp")  
        print("Is porsche.png null?", self.original_bg.isNull())

        # === Central widget & layout ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Lägg in marginaler runt om så tabellerna inte går kant i kant
        main_layout.setContentsMargins(50, 50, 50, 50)

        # === Titel / Rubrik högst upp ===
        title_label = QLabel("Autodromo – Porsche 911")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # === Två tabeller sida vid sida ===
        data_left = ALL_DATA[:6]
        data_right = ALL_DATA[6:]

        table_layout = QHBoxLayout()
        main_layout.addLayout(table_layout)

        table_left = create_leaderboard_table(data_left)
        table_right = create_leaderboard_table(data_right)

        # Lägg in tabellerna i en horisontell layout
        table_layout.addWidget(table_left)
        table_layout.addSpacing(50)  # Mellanrum mellan tabellerna
        table_layout.addWidget(table_right)

        # === Stylesheet (ingen background-image, vi ritar bilden i paintEvent) ===
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0b1f2c; /* fallback-färg */
            }
            QLabel#TitleLabel {
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 36px;
                font-weight: bold;
                color: #ffffff;
                margin-top: 20px;
                margin-bottom: 20px;
                background-color: rgba(0, 0, 0, 80); /* halvt genomskinlig bakgrund */
            }
            QTableWidget#LeaderboardTable {
                background-color: rgba(0, 0, 0, 120);
                color: #ffffff;
                gridline-color: rgba(255, 255, 255, 50);
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 16px;
                border: 2px solid rgba(255, 255, 255, 40);
            }
            QTableWidget#LeaderboardTable::item {
                border-bottom: 1px solid rgba(255, 255, 255, 40);
                padding: 6px;
            }
            /* Ingen markering, men om man ändrar sig i framtiden: */
            QTableWidget#LeaderboardTable::item:selected {
                background: rgba(255, 255, 255, 50);
            }
            QHeaderView::section {
                background: rgba(0, 0, 0, 180);
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 40);
            }
        """)

    def paintEvent(self, event):
        """
        Ritar bakgrundsbilden i fönstret.
        """
        painter = QPainter(self)
        if not self.original_bg.isNull():
            # Skala bilden för att fylla fönstret
            scaled_bg = self.original_bg.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_bg)
        painter.end()

        super().paintEvent(event)

def main():
    app = QApplication(sys.argv)
    window = LeaderboardWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
