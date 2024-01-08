DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS registration;
DROP TABLE IF EXISTS waitlist;

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    date_joined DATE NOT NULL
);

CREATE TABLE section (
    section_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    registration_capactity INTEGER NOT NULL,
    waitlist_capactity INTEGER NOT NULL,
);

CREATE TABLE registration (
    user_id INTEGER,
    section_id INTEGER,
    registration_date DATE,
    PRIMARY KEY (user_id, section_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES section (section_id) ON DELETE CASCADE
);

CREATE TABLE dropped (
    user_id INTEGER,
    section_id INTEGER,
    drop_date DATE,
    type CHAR,
    PRIMARY KEY (user_id, section_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id)
    FOREIGN KEY (section_id) REFERENCES section (section_id)
);

/* TODO: IF it was a withdrawal NOT a deregister or dewaitlist */
CREATE TRIGGER update_dropped
AFTER DELETE ON registration
FOR EACH ROW
BEGIN
    INSERT INTO dropped (user_id, section_id, drop_date) VALUES (OLD.user_id, OLD.section_id, DATE('now'));
END;

CREATE TABLE waitlist (
    user_id INTEGER,
    section_id INTEGER,
    waitlist_date DATE,
    PRIMARY KEY (user_id, section_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES section (section_id) ON DELETE CASCADE
);