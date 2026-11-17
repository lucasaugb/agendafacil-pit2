-- =============================================================
-- AgendaFácil - Projeto Físico do Banco de Dados
-- SGBD: SQLite 3
-- =============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS agendamento;
DROP TABLE IF EXISTS servico;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS usuario;

-- Usuários que acessam o sistema (dono / atendente)
CREATE TABLE usuario (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    senha_hash  VARCHAR(255) NOT NULL,
    criado_em   TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Clientes do estabelecimento
CREATE TABLE cliente (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        VARCHAR(100) NOT NULL CHECK (length(trim(nome)) >= 3),
    telefone    VARCHAR(20)  NOT NULL,
    email       VARCHAR(120),
    observacoes TEXT,
    criado_em   TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Serviços oferecidos (corte, barba, escova...)
CREATE TABLE servico (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         VARCHAR(80) NOT NULL UNIQUE,
    descricao    TEXT,
    preco        DECIMAL(8,2) NOT NULL CHECK (preco >= 0),
    duracao_min  INTEGER NOT NULL CHECK (duracao_min BETWEEN 5 AND 480),
    ativo        INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

-- Agendamentos: liga um cliente a um serviço em uma data/hora
CREATE TABLE agendamento (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id  INTEGER NOT NULL REFERENCES cliente(id) ON DELETE RESTRICT,
    servico_id  INTEGER NOT NULL REFERENCES servico(id) ON DELETE RESTRICT,
    data_hora   TEXT NOT NULL,           -- formato 'AAAA-MM-DD HH:MM'
    status      VARCHAR(12) NOT NULL DEFAULT 'agendado'
                CHECK (status IN ('agendado', 'concluido', 'cancelado')),
    observacoes TEXT,
    criado_em   TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX idx_agendamento_data ON agendamento (data_hora);
CREATE INDEX idx_agendamento_cliente ON agendamento (cliente_id);
CREATE INDEX idx_cliente_nome ON cliente (nome);
