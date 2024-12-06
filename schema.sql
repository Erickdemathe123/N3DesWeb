-- Criação do banco de dados e a tabela User
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
);

-- Inserir dados iniciais
INSERT INTO user (username, password, is_admin)
VALUES ('admin', 'admin', 1),
       ('user1', 'user1', 0);
