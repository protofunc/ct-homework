-- Populate customers table
INSERT INTO customers(
    first_name,
    last_name,
    club_member
) VALUES (
    'john',
    'doe',
    'TRUE'
),
(
    'jane',
    'foster',
    'TRUE'
),
(
    'carley',
    'weever',
    'FALSE'
),
(
    'jethro',
    'farms',
    'FALSE'
);

-- Populate concessions table
INSERT INTO concessions(
    concession_type,
    cost,
    discount
) VALUES (
    'reeses',
    '2.99',
    '15'
),
(
    'skittles',
    '2.99',
    '15'
),
(
    'oreos',
    '2.99',
    '15'
),
(
    'popcorn',
    '4.99',
    '10'
);

-- Populate tickets table
INSERT INTO tickets(
    seat_num,
    theater_num
) VALUES (
    'A1',
    '1'
),
(
    'A2',
    '1'
),
(
    'B1',
    '1'
),
(
    'B2',
    '1'
),
(
    'C1',
    '1'
),
(
    'C2',
    '1'
),
(
    'A1',
    '2'
),
(
    'A2',
    '2'
),
(
    'B1',
    '2'
),
(
    'B2',
    '2'
),
(
    'C1',
    '2'
),
(
    'C2',
    '2'
);

-- Populate movies table
INSERT INTO movies(
    title,
    rating
) VALUES (
    'Inception',
    'PG-13'
),
(
    'Tenet',
    'PG-13'
);

-- Add a couple more customers
INSERT INTO customers(
    first_name,
    last_name,
    club_member
) VALUES (
    'matt',
    'mahomes',
    'TRUE'
),
(
    'leslie',
    'parker',
    'FALSE'
);

-- Update tickets table with customer and movie id's
UPDATE tickets
SET customer_id = 2, movie_id = 1
WHERE ticket_id = 1;

UPDATE tickets
SET customer_id = 3, movie_id = 1
WHERE ticket_id = 2;

UPDATE tickets
SET customer_id = 4, movie_id = 1
WHERE ticket_id = 3;

UPDATE tickets
SET customer_id = 5, movie_id = 1
WHERE ticket_id = 4;

UPDATE tickets
SET customer_id = 6, movie_id = 1
WHERE ticket_id = 5;

UPDATE tickets
SET customer_id = 7, movie_id = 1
WHERE ticket_id = 6;

UPDATE tickets
SET customer_id = 2, movie_id = 2
WHERE ticket_id = 7;

UPDATE tickets
SET customer_id = 3, movie_id = 2
WHERE ticket_id = 8;

UPDATE tickets
SET customer_id = 4, movie_id = 2
WHERE ticket_id = 9;

UPDATE tickets
SET customer_id = 5, movie_id = 2
WHERE ticket_id = 10;

UPDATE tickets
SET customer_id = 6, movie_id = 2
WHERE ticket_id = 11;

UPDATE tickets
SET customer_id = 7, movie_id = 2
WHERE ticket_id = 12;

-- Change column name in concessions table from discount to discount_percent
ALTER TABLE concessions
RENAME COLUMN discount to discount_percent;