CREATE DATABASE fitness_club;

CREATE TABLE clients (
  client_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  address VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL
);

CREATE TABLE trainers (
  trainer_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  speciality VARCHAR(50) NOT NULL
);

CREATE TABLE classes (
  class_id SERIAL PRIMARY KEY,
  class_name VARCHAR(100) NOT NULL,
  trainer_id INTEGER REFERENCES trainers(trainer_id),
  class_date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL
);

CREATE TABLE memberships (
  membership_id SERIAL PRIMARY KEY,
  client_id INTEGER REFERENCES clients(client_id),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE subscriptions (
  subscription_id SERIAL PRIMARY KEY,
  client_id INTEGER REFERENCES clients(client_id),
  class_id INTEGER REFERENCES classes(class_id),
  subscription_date DATE NOT NULL
);

INSERT INTO clients (name, address, phone) VALUES
  ('John Smith', '123 Main St, Anytown, USA', '555-1234'),
  ('Jane Doe', '456 Elm St, Anycity, USA', '555-5678'),
  ('Michael Johnson', '789 Oak St, Anystate, USA', '555-9012'),
  ('Emily Williams', '321 Pine St, Anyvillage, USA', '555-3456');

INSERT INTO trainers (name, speciality) VALUES
  ('Mike Davis', 'Cardio'),
  ('Sara Green', 'Strength training'),
  ('Bob Brown', 'Yoga'),
  ('Emma Robertson', 'Pilates');

INSERT INTO classes (class_name, trainer_id, class_date, start_time, end_time) VALUES
  ('Morning Yoga', 3, '2023-11-01', '08:00:00', '10:00:00'),
  ('HIIT', 1, '2023-11-01', '11:00:00', '12:30:00'),
  ('Strength & Conditioning', 2, '2023-11-02', '16:00:00', '18:00:00'),
  ('Pilates', 4, '2023-11-03', '14:00:00', '16:00:00');

INSERT INTO memberships (client_id, start_date, end_date, cost) VALUES
  (1, '2023-01-01', '2023-12-31', 300.00),
  (2, '2023-04-01', '2024-03-31', 300.00),
  (3, '2023-07-01', '2024-06-30', 300.00),
  (4, '2023-10-01', '2024-09-30', 300.00);

INSERT INTO subscriptions (client_id, class_id, subscription_date) VALUES
  (1, 1, '2023-11-01'),
  (2, 2, '2023-11-01'),
  (3, 3, '2023-11-02'),
  (4, 4, '2023-11-03');
