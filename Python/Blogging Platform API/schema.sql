-- Author:      Wajid Ali Saleem Chaudhry
-- Description: SQLite schema for the blogging platform.

CREATE TABLE IF NOT EXISTS posts (
    id         INTEGER PRIMARY KEY,
    title      TEXT NOT NULL,
    content    TEXT NOT NULL,
    category   TEXT NOT NULL,
    tags       TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
