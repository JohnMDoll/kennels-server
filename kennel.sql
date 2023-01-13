CREATE TABLE `Location` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`address`	TEXT NOT NULL
);

CREATE TABLE `Customer` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`    TEXT NOT NULL,
    `address`    TEXT NOT NULL,
    `email`    TEXT NOT NULL,
    `password`    TEXT NOT NULL
);

CREATE TABLE `Animal` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`  TEXT NOT NULL,
	`status` TEXT NOT NULL,
	`breed` TEXT NOT NULL,
	`customer_id` INTEGER NOT NULL,
	`location_id` INTEGER,
	FOREIGN KEY(`customer_id`) REFERENCES `Customer`(`id`),
	FOREIGN KEY(`location_id`) REFERENCES `Location`(`id`)
);


CREATE TABLE `Employee` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`address`	TEXT NOT NULL,
	`location_id` INTEGER NOT NULL,
	FOREIGN KEY(`location_id`) REFERENCES `Location`(`id`)

);

INSERT INTO `Location` VALUES (null, 'Nashville North', "64 Washington Heights");
INSERT INTO `Location` VALUES (null, 'Nashville South', "101 Penn Ave");


INSERT INTO `Employee` VALUES (null, "Madi Peper", "35498 Madison Ave", 1);
INSERT INTO `Employee` VALUES (null, "Kristen Norris", "100 Main St", 1);
INSERT INTO `Employee` VALUES (null, "Meg Ducharme", "404 Unknown Ct", 2);
INSERT INTO `Employee` VALUES (null, "Hannah Hall", "204 Empty Ave", 1);
INSERT INTO `Employee` VALUES (null, "Leah Hoefling", "200 Success Way", 2);


INSERT INTO `Customer` VALUES (null, "Mo Silvera", "201 Created St", "mo@silvera.com", "password");
INSERT INTO `Customer` VALUES (null, "Bryan Nilsen", "500 Internal Error Blvd", "bryan@nilsen.com", "password");
INSERT INTO `Customer` VALUES (null, "Jenna Solis", "301 Redirect Ave", "jenna@solis.com", "password");
INSERT INTO `Customer` VALUES (null, "Emily Lemmon", "454 Mulberry Way", "emily@lemmon.com", "password");



INSERT INTO `Animal` VALUES (null, "Snickers", "Recreation", "Dalmation", 4, 1);
INSERT INTO `Animal` VALUES (null, "Jax", "Treatment", "Beagle", 1, 1);
INSERT INTO `Animal` VALUES (null, "Falafel", "Treatment", "Siamese", 4, 2);
INSERT INTO `Animal` VALUES (null, "Doodles", "Kennel", "Poodle", 3, 1);
INSERT INTO `Animal` VALUES (null, "Daps", "Kennel", "Boxer", 2, 2);
INSERT INTO `Animal` VALUES (null, "Cleo", "Kennel", "Poodle", 2, 2);
INSERT INTO `Animal` VALUES (null, "Popcorn", "Kennel", "Beagle", 3, 2);
INSERT INTO `Animal` VALUES (null, "Curly", "Treatment", "Poodle", 4, 2);

INSERT INTO `Animal` VALUES (null, "Daps", "Kennel", "Boxer", 2, 2);

SELECT
    a.id,
    a.name,
    a.breed,
    a.status,
    a.location_id,
    a.customer_id,
    l.name location_name,
    l.address location_address,
	c.name customer_name
FROM Animal a
Left JOIN Location l ON l.id = a.location_id 
Left JOIN Customer c ON c.id = a.customer_id
-- Why does belore return 1 row/location if GROUP BY isn't included?
SELECT
		location.*,
		COUNT(*) as animals
	FROM location
	JOIN Animal ON location.id = location_id
	GROUP BY location.id HAVING location.id = 1

CREATE TABLE employee_animals (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    animal_id INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (animal_id) REFERENCES animals(id)
);
INSERT INTO employee_animals (employee_id, animal_id)
SELECT e1.id, a1.id
FROM employees e1
JOIN animals a1 ON e1.location_id = a1.location_id
JOIN employees e2 ON e1.location_id = e2.location_id
JOIN animals a2 ON a1.location_id = a2.location_id
WHERE e1.id <> e2.id
AND a1.id <> a2.id;

WITH employee_table AS (SELECT id, location_id FROM employee),
    animal_table AS (SELECT id, location_id FROM animal)
INSERT INTO employee_animals ( employee_id, animal_id)
SELECT employee_table.id, animal_table.id
FROM employee_table
JOIN animal_table ON employee_table.location_id = animal_table.location_id
WHERE employee_table.id <> animal_table.id;

DELETE FROM employee_animals
WHERE id = 16

SELECT
            e.*,
            l.name location_name,
            l.address as location_address,
			a.name as animal_name,
			a.id as animal_table_id
		FROM employee e
        JOIN Location l ON l.id = e.location_id
        JOIN employee_animals ea ON ea.employee_id = e.id
		JOIN Animal a ON animal_table_id = ea.animal_id
        WHERE e.id = 2

SELECT
	location.*,
	COUNT(*) as animals,
	animal.name
FROM location
JOIN Animal ON location.id = location_id
GROUP BY location.id
HAVING location.id = 1