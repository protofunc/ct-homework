-- Q1: List all customers who live in Texas (use JOINs)
SELECT customer_id, first_name, last_name, district
FROM customer
INNER JOIN address
ON customer.customer_id = address.address_id
WHERE district = 'Texas';

-- Q2: Get all payments above $6.99 with the Customer's Full Name
SELECT first_name, last_name, amount
FROM customer
INNER JOIN payment
ON customer.customer_id = payment.customer_id
WHERE amount >= 6.99;

-- Q3: Show all customers names who have made payments over $175 (use subqueries)
SELECT first_name, last_name
FROM customer
WHERE customer_id IN (
    SELECT customer_id
    FROM payment
    GROUP BY customer_id
    HAVING SUM(amount) > 175
);

-- Q4: List all customers that live in Nepal (use the city table)
SELECT customer_id, first_name, last_name
FROM customer
INNER JOIN address
ON customer.customer_id = address.address_id
INNER JOIN city
ON address.city_id = city.city_id
WHERE country_id IN (
    SELECT country_id
    FROM country
    WHERE country = 'Nepal'
);

-- Q5: Which staff member had the most transactions?
SELECT first_name, last_name, COUNT(amount)
FROM staff
INNER JOIN payment
ON staff.staff_id = payment.staff_id
GROUP BY staff.staff_id;
-- Answer: Jon Stephens w/ 7304 transactions

-- Q6: How many movies of each rating are there?
SELECT rating, COUNT(film_id)
FROM film
GROUP BY rating
ORDER BY COUNT(film_id) DESC;

-- Q7: Show all customers who have made a single payment above $6.99 (Use Subqueries) 
SELECT first_name, last_name
FROM customer
WHERE customer_id IN (
    SELECT customer_id
    FROM payment
    GROUP BY customer_id, amount
    HAVING amount >= 6.99
);

-- Q8: How many free rentals did our stores give away?
-- I don't know how to answer this question :/