CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE 
);

CREATE TABLE professors (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE lectures (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL,
    professor_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES professors (id)
          ON DELETE SET NULL
          ON UPDATE CASCADE 
);

CREATE TABLE marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    student_id INTEGER,
    lecture_id INTEGER,
    mark INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students (id)
          ON DELETE CASCADE
          ON UPDATE CASCADE
    FOREIGN KEY (lecture_id) REFERENCES lectures (id)
          ON DELETE CASCADE
          ON UPDATE CASCADE 
);

INSERT INTO groups (name)
VALUES ('bioglogy'),
('physics'),
('economy');

INSERT INTO students (name, group_id)
VALUES ('Boris', 1), ('Hanna', 1), ('Carim', 1), ('Violetta', 1), ('Katt', 1), ('Bory', 1), ('Anna', 1), ('Cary', 1), ('Vio', 1), ('Katyy', 1),
('Nadja', 2), ('Merry', 2), ('Kor', 2), ('Tor', 2), ('Sam', 2), ('Nati', 2), ('Samanta', 2), ('Nata', 2), ('Samantak', 3), ('Natalia', 3),
('Met', 3), ('Lulu', 3), ('Tam', 3), ('Ken', 3), ('Metttu', 3), ('Luna', 3), ('Tata', 3), ('Koly', 3) , ('Marco', 3), ('Nency', 3);

INSERT INTO professors (name)
VALUES ('Mr. Smith'),
('Ms. Collin'),
('Mr. Djons');

INSERT INTO lectures (name, professor_id)
VALUES ('BioBasics', 1), ('HightEnergies', 2), ('Markt', 3), ('ETFs', 3), ('Ecology', 1);


INSERT INTO marks (student_id, lecture_id, mark)
VALUES (28, 2, 8), (28, 2, 9), (27, 3, 10) , (28, 4, 7), (27, 5, 9),
(28, 2, 9), (26, 2, 9), (27, 3, 9) , (26, 4, 7), (28, 5, 6),
(28, 2, 8), (28, 2, 9), (27, 3, 9) , (27, 4, 7), (28, 5, 8);