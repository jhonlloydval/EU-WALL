from PyQt6.QtWidgets import QDialog, QLineEdit
from PyQt6.uic import loadUi
from database import setup_database
from screens.login_screen import LoginScreen
import mysql.connector

class RegisterScreen(QDialog):
    def __init__(self, stack):
        super().__init__()
        loadUi("ui/register.ui", self)
        self.stack = stack
        self.newpasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmpasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        self.registerButton.clicked.connect(self.register_function)

    def register_function(self):
        user = self.newusernameField.text()
        password = self.newpasswordField.text()
        confirmpassword = self.confirmpasswordField.text()

        if not user or not password or not confirmpassword:
            self.error2.setText("Please input all fields.")
        elif password != confirmpassword:
            self.error2.setText("Passwords do not match.")
        else:
            conn = setup_database()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (user,))
            if cursor.fetchone():
                self.error2.setText("Username already taken.")
            else:
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, password))
                    conn.commit()
                    login = LoginScreen(self.stack)
                    self.stack.addWidget(login)
                    self.stack.setCurrentWidget(login)
                except mysql.connector.Error as err:
                    self.error2.setText(f"Database error: {err}")
            conn.close()
