CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'qwerty';

GRANT ALL PRIVILEGES ON *.* TO 'db_user'@'localhost';

CREATE DATABASE game_store;