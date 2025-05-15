from PyQt6.QtWidgets import QDialog, QLineEdit
from PyQt6.uic import loadUi
from database import setup_database
from screens.main_screen import MainScreen

class LoginScreen(QDialog):
    def __init__(self, stack):
        super().__init__()
        loadUi("ui/login.ui", self)
        self.stack = stack
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
        self.loginButton.clicked.connect(self.login_function)

    def login_function(self):
        user = self.usernameField.text()
        password = self.passwordField.text()

        if not user or not password:
            self.error1.setText("Please input all fields.")
            return

        conn = setup_database()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (user,))
        result = cursor.fetchone()
        if result and result[0] == password:
            self.error1.setText("")
            main = MainScreen(user)
            self.stack.addWidget(main)
            self.stack.setCurrentWidget(main)
        else:
            self.error1.setText("Invalid username or password.")
        conn.close()