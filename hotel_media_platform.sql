CREATE DATABASE IF NOT EXISTS hotel_media_platform
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE hotel_media_platform;

-- ========================
-- 1. USERS
-- ========================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'guest') DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (full_name, email, password_hash, role)
VALUES (
    'Administrator',
    'admin@hotel.com',
    'pbkdf2:sha256:600000$sB1G02sYzPpM0eq9$3fbb41f3a4c54ce58b406fbbf64e07a03b5f9de343d07e9bb3fde1997e7465d0',
    'admin'
);


-- ========================
-- 2. ROOM_TYPES
-- ========================
CREATE TABLE room_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL
);

-- ========================
-- 3. ROOMS
-- ========================
CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) UNIQUE NOT NULL,
    type_id INT NOT NULL,
    status ENUM('available', 'occupied', 'maintenance') DEFAULT 'available',
    FOREIGN KEY (type_id) REFERENCES room_types(type_id)
);

-- ========================
-- 4. BOOKINGS
-- ========================
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- ========================
-- 5. ARTICLES
-- ========================
CREATE TABLE articles (
    article_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,
    author_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

-- ========================
-- 6. MEDIA
-- ========================
CREATE TABLE media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    article_id INT,
    url VARCHAR(500) NOT NULL,
    media_type ENUM('image', 'video') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

-- ========================
-- 7. CAMPAIGNS
-- ========================
CREATE TABLE campaigns (
    campaign_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(255) NOT NULL,
    platform ENUM('facebook', 'tiktok', 'instagram', 'youtube', 'google', 'other') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================
-- 8. ANALYTICS
-- ========================
CREATE TABLE analytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    article_id INT NOT NULL,
    seo_score INT,
    traffic INT,
    views INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

-- ========================
-- 9. LIVESTREAM
-- ========================
CREATE TABLE livestream (
    stream_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    stream_title VARCHAR(255) NOT NULL,
    start_time DATETIME NOT NULL,
    stream_link VARCHAR(500) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(user_id)
);
