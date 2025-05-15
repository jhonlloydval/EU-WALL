from PyQt6.QtWidgets import QDialog, QMessageBox, QInputDialog
from PyQt6.uic import loadUi

class MyPostsDialog(QDialog):
    def __init__(self, user_id, db_connection, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.conn = db_connection
        loadUi("ui/MyPostsDialog.ui", self)
        self.editButton.clicked.connect(self.edit_post)
        self.deleteButton.clicked.connect(self.delete_post)
        self.closeButton.clicked.connect(self.close)
        self.load_my_posts()

    def load_my_posts(self):
        self.myPostListWidget.clear()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, content, timestamp FROM posts WHERE user_id = %s ORDER BY timestamp DESC", (self.user_id,))
        self.posts = cursor.fetchall()
        for post_id, content, timestamp in self.posts:
            display_text = f"{timestamp.strftime('%Y-%m-%d %H:%M')}:\n{content}"
            self.myPostListWidget.addItem(display_text)

    def get_selected_post_index(self):
        return self.myPostListWidget.currentRow()

    def edit_post(self):
        index = self.get_selected_post_index()
        if index < 0:
            QMessageBox.warning(self, "No Selection", "Please select a post to edit.")
            return
        post_id, content, _ = self.posts[index]
        new_content, ok = QInputDialog.getMultiLineText(self, "Edit Post", "Edit your post:", content)
        if ok and new_content.strip():
            cursor = self.conn.cursor()
            cursor.execute("UPDATE posts SET content = %s WHERE id = %s", (new_content.strip(), post_id))
            self.conn.commit()
            self.load_my_posts()

    def delete_post(self):
        index = self.get_selected_post_index()
        if index < 0:
            QMessageBox.warning(self, "No Selection", "Please select a post to delete.")
            return
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this post?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            post_id, _, _ = self.posts[index]
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
            self.conn.commit()
            self.load_my_posts()
