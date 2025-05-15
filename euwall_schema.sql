-- Valencia, Jhon Lloyd M.
-- EU-WALL: Your Enverga Wall of Expression 
-- “Speak Your Mind, Share Your Truth, MSEUF”

CREATE DATABASE IF NOT EXISTS EuWall;
USE EuWAll;

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  content TEXT NOT NULL,
  is_anonymous BOOLEAN NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

