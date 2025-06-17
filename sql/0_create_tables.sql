CREATE TABLE cocktails
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    category    TEXT NOT NULL,
    glass       TEXT NOT NULL,
    instruction TEXT NOT NULL,
    thumb       TEXT NOT NULL
);

CREATE TABLE cocktail_images
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cocktail INTEGER NOT NULL UNIQUE,
    image_path  TEXT    NOT NULL,
    FOREIGN KEY (id_cocktail) REFERENCES cocktails (id) ON DELETE CASCADE
);

CREATE TABLE snacks
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    content     TEXT,
    instruction TEXT,
    source      TEXT
);

CREATE TABLE ingredients
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    id_snack INTEGER,
    FOREIGN KEY (id_snack) REFERENCES snacks (id) ON DELETE CASCADE
);

CREATE TABLE cocktail_ingr
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cocktail       INTEGER NOT NULL,
    id_ingr           INTEGER NOT NULL,
    cocktail_position INTEGER NOT NULL,
    measure           TEXT,
    UNIQUE (id_cocktail, id_ingr),
    FOREIGN KEY (id_cocktail) REFERENCES cocktails (id) ON DELETE CASCADE,
    FOREIGN KEY (id_ingr) REFERENCES ingredients (id) ON DELETE CASCADE
);

CREATE TABLE users
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE cocktail_likes (
    user_id INTEGER NOT NULL,
    cocktail_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, cocktail_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id)
);
