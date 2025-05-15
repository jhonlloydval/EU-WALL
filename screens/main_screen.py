from PyQt6.QtWidgets import QDialog, QLabel, QMessageBox
from PyQt6.uic import loadUi
from database import setup_database
from dialogs.my_posts import MyPostsDialog

class MainScreen(QDialog):
    def __init__(self, username):
        super().__init__()
        loadUi("ui/main.ui", self)
        self.username = username
        self.anonymousCheckBox.setChecked(False)
        self.postButton.clicked.connect(self.post_content)
        self.myPostsButton.clicked.connect(self.open_my_posts)
        self.searchButton.clicked.connect(self.open_search)
        self.errorPost = QLabel(self)
        self.errorPost.setStyleSheet("color: white;")
        self.errorPost.setGeometry(50, 490, 400, 20)
        self.load_posts()

    def load_posts(self):
        self.postListWidget.clear()
        conn = setup_database()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT content, is_anonymous, timestamp, username
            FROM posts
            JOIN users ON users.id = posts.user_id
            ORDER BY timestamp DESC
        """)
        for content, is_anon, timestamp, username in cursor.fetchall():
            author = "Anonymous" if is_anon else username
            display = f"{author} ({timestamp.strftime('%Y-%m-%d %H:%M')}):\n{content}\n"
            self.postListWidget.addItem(display)
        conn.close()

    def post_content(self):
        content = self.newPostTextEdit.toPlainText()
        is_anonymous = self.anonymousCheckBox.isChecked()
        if not content.strip():
            self.errorPost.setText("Post cannot be empty.")
            return
        conn = setup_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO posts (user_id, content, is_anonymous) VALUES (%s, %s, %s)", (user_id, content, is_anonymous))
        conn.commit()
        conn.close()
        self.newPostTextEdit.clear()
        self.load_posts()
        self.errorPost.setText("")

    def open_my_posts(self):
        dialog = MyPostsDialog(user_id=self.get_user_id(), db_connection=setup_database())
        dialog.exec()

    def open_search(self):
        keyword = self.searchLineEdit.text().strip()
        self.postListWidget.clear()

        if not keyword:
            # No keyword: just reload all posts (normal feed)
            self.load_posts()
            self.errorPost.setText("")
            return

        conn = setup_database()
        cursor = conn.cursor()

        query = """
            SELECT content, is_anonymous, timestamp, username
            FROM posts
            JOIN users ON users.id = posts.user_id
            WHERE content LIKE %s OR DATE_FORMAT(timestamp, '%Y-%m-%d') LIKE %s
            ORDER BY timestamp DESC
        """

        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword))
        results = cursor.fetchall()
        conn.close()

        if results:
            for content, is_anon, timestamp, username in results:
                author = "Anonymous" if is_anon else username
                display = f"{author} ({timestamp.strftime('%Y-%m-%d %H:%M')}):\n{content}\n"
                self.postListWidget.addItem(display)
            self.errorPost.setText("")
        else:
            self.postListWidget.addItem("No matching posts found.")
            self.errorPost.setText("")

    def get_user_id(self):
        conn = setup_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id