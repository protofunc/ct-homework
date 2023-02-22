CREATE TABLE customers(
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    club_member BOOLEAN
);

CREATE TABLE concessions(
    concession_id SERIAL PRIMARY KEY,
    concession_type VARCHAR(25),
    cost MONEY,
    discount INT
);

CREATE TABLE movies(
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    rating VARCHAR(5)
);

CREATE TABLE tickets(
    ticket_id SERIAL PRIMARY KEY,
    seat_num VARCHAR(3),
    theater_num VARCHAR(3),
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    movie_id INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);