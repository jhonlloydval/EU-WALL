import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from screens.welcome_screen import WelcomeScreen

app = QApplication(sys.argv)

widget = QStackedWidget()
welcome = WelcomeScreen(widget)
widget.addWidget(welcome)

widget.setFixedHeight(551)
widget.setFixedWidth(801)
widget.show()

try:
    sys.exit(app.exec())
except Exception as e:
    print("Exiting due to error:", e)