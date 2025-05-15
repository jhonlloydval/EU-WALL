from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen

class WelcomeScreen(QDialog):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi("ui/welcomescreen.ui", self)

        self.loginButton.clicked.connect(self.go_to_login)
        self.registerButton.clicked.connect(self.go_to_register)

    def go_to_login(self):
        login = LoginScreen(self.stacked_widget)
        self.stacked_widget.addWidget(login)
        self.stacked_widget.setCurrentWidget(login)

    def go_to_register(self):
        register = RegisterScreen(self.stacked_widget)
        self.stacked_widget.addWidget(register)
        self.stacked_widget.setCurrentWidget(register)