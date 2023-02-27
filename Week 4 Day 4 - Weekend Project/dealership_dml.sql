-- Populate customer table
INSERT INTO customer(
    first_name,
    last_name,
    email
) VALUES (
    'john',
    'doe',
    'jdoe@gmail.com'
),
(
    'jane',
    'foster',
    'jfoster@gmail.com'
),
(
    'carley',
    'weever',
    'cweever@gmail.com'
);

-- Populate mechanic table
INSERT INTO mechanic(
    first_name,
    last_name,
    phone_num
) VALUES (
    'jerry',
    'wrench',
    '619-123-4567'
),
(
    'kerry',
    'hammer',
    '619-123-4568'
),
(
    'bobby',
    'nails',
    '619-123-4569'
);

-- Populate salesperson table
INSERT INTO salesperson(
    first_name,
    last_name,
    phone_num
) VALUES (
    'joey',
    'pockets',
    '619-123-0001'
),
(
    'ravi',
    'wallet',
    '619-123-0002'
),
(
    'sara',
    'purse',
    '619-123-0003'
);

-- Populate cars table
INSERT INTO cars(
    make,
    model,
    car_year,
    salesperson_id,
    customer_id
) VALUES (
    'honda',
    'civic',
    '2022',
    1,
    1
),
(
    'toyota',
    'camry',
    '2020',
    2,
    2
),
(
    'volkswagon',
    'gti',
    '2021',
    3,
    3
);

-- Populate services table
INSERT INTO services(
    service_type,
    service_mins,
    customer_id,
    car_id
) VALUES (
    'oil change',
    30,
    1,
    1
),
(
    'starter replacement',
    90,
    2,
    2
),
(
    'ecu update',
    120,
    3,
    3
);

-- Populate mechanic_ticket table
INSERT INTO mechanic_ticket(
    service_id,
    mechanic_id
) VALUES (
    1,
    1
),
(
    2,
    2
),
(
    3,
    1
),
(
    3,
    3
);

-- Populate invoice table
INSERT INTO invoice(
    total_cost,
    car_id,
    salesperson_id,
    customer_id,
    service_id
) VALUES (
    90,
    1,
    1,
    1,
    1
),
(
    600,
    2,
    2,
    2,
    2
),
(
    300,
    3,
    3,
    3,
    3
);

SELECT invoice_id, total_cost, service_type
FROM invoice
FULL JOIN services
ON invoice.service_id = services.service_id;