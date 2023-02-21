-- 1. How many actors are there with the last name ‘Wahlberg’?
SELECT first_name, last_name
FROM actor
WHERE last_name = 'Wahlberg';
-- Answer: 2 actors 

-- 2. How many payments were made between $3.99 and $5.99?
SELECT COUNT(amount)
FROM payment
WHERE amount BETWEEN 3.99 AND 5.99;
-- Answer: 4794 payments were made

-- 3. What film does the store have the most of? (search in inventory table)
SELECT film_id, COUNT(film_id)
FROM inventory
GROUP BY film_id
ORDER BY COUNT(film_id) DESC
LIMIT 100;

SELECT title
FROM film
WHERE film_id = '911';
-- Answer: The most was 8 copies of 50+ films between both stores. One of them is Trip Newton.

-- 4. How many customers have the last name ‘William’?
SELECT first_name, last_name
FROM customer
WHERE last_name = 'William';
-- Answer: None

-- 5. What store employee (get the id) sold the most rentals?
SELECT staff_id, COUNT(rental_id)
FROM payment
GROUP BY staff_id;

SELECT first_name, last_name
FROM staff
WHERE staff_id = 2;
-- Answer: Jon Stephens sold the most (7304 rentals)

-- 6. How many different distinct names are there?
SELECT COUNT(DISTINCT name)
FROM category;
-- Answer: There are 16 distinct names in the category table. 
-- Note: The question doesn't specify what table....

-- 7. What film has the most actors in it? (use film_actor table and get film_id)
SELECT film_id, COUNT(actor_id)
FROM film_actor
GROUP BY film_id
ORDER BY COUNT(actor_id) DESC;

SELECT title
FROM film
WHERE film_id = '508';
-- Answer: film_id 508, or Lambs Cincinatti, has 15 actors.

-- 8. From store_id 1, how many customers have a last name ending with ‘es’? (use customer table)
SELECT first_name, last_name
FROM customer
WHERE last_name LIKE '%es';
-- Answer: There are 21 customers.

-- 9. How many payment amounts (4.99, 5.99, etc.) had a number of rentals above 250 for customers
-- with ids between 380 and 430? (use group by and having > 250)
SELECT amount, COUNT(customer_id)
FROM payment
WHERE customer_id BETWEEN 280 AND 430
GROUP BY amount
HAVING COUNT(customer_id) > 250
ORDER BY COUNT(customer_id) DESC;
-- Answer: There are 4 payment amounts with rentals above 250 for customer_ids 380-430.

-- 10. Within the film table, how many rating categories are there? And what rating has the most
-- movies total?
SELECT COUNT(DISTINCT rating)
FROM film;

SELECT rating, COUNT(film_id)
FROM film
GROUP BY rating
ORDER BY COUNT(film_id) DESC;
-- Answer: There are 5 rating categories in the film table. PG-13 has the most movies (223 films).