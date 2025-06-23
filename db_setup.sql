CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL UNIQUE,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    technical_inspection_date DATE NOT NULL,
    insurance_date DATE NOT NULL,
    contact_person TEXT NOT NULL,
    contact_email TEXT NOT NULL
);

-- Przykładowe dane
INSERT INTO cars (registration_number, brand, model, year, technical_inspection_date, insurance_date, contact_person, contact_email)
VALUES 
    ('WA12345', 'Toyota', 'Corolla', 2020, date('now', '+20 days'), date('now', '+45 days'), 'Jan Kowalski', 'jan.kowalski@example.com'),
    ('KR54321', 'Ford', 'Focus', 2019, date('now', '+7 days'), date('now', '+14 days'), 'Anna Nowak', 'anna.nowak@example.com'),
    ('GD98765', 'Volkswagen', 'Passat', 2021, date('now', '+35 days'), date('now', '+3 days'), 'Piotr Wiśniewski', 'piotr.wisniewski@example.com'),
    ('PO24680', 'Skoda', 'Octavia', 2018, date('now', '+3 days'), date('now', '+60 days'), 'Katarzyna Dąbrowska', 'katarzyna.dabrowska@example.com'),
    ('WR13579', 'Hyundai', 'i30', 2022, date('now', '+90 days'), date('now', '+30 days'), 'Michał Lewandowski', 'michal.lewandowski@example.com');
