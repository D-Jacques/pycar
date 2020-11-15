CREATE TABLE IF NOT EXISTS pycar_user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    user_mail TEXT UNIQUE NOT NULL,
    user_role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pycar_cars(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_name TEXT NOT NULL,
    car_brand TEXT NOT NULL,
    car_price REAL NOT NULL,
    to_repair INTEGER NOT NULL 
);

