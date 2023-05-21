DROP TABLE authorizations;
DROP TABLE messages;
DROP TABLE chats;
DROP TABLE users;
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(128) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    nickname VARCHAR(128) NOT NULL,
    picture BYTEA,
    age INTEGER,
    gender VARCHAR(64),
    description VARCHAR(256)
);
CREATE TABLE IF NOT EXISTS authorizations (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    authorization_token VARCHAR(64) UNIQUE NOT NULL,
    CONSTRAINT fk_users 
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS chats (
    id BIGSERIAL PRIMARY KEY,
    users INTEGER[] NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    chat_id BIGINT NOT NULL,
    sender INTEGER NOT NULL,
    send_time TIMESTAMP NOT NULL,
    CONSTRAINT fk_chats 
        FOREIGN KEY (chat_id)
        REFERENCES chats(id),
    CONSTRAINT fk_users 
        FOREIGN KEY (sender)
        REFERENCES users(id)
);