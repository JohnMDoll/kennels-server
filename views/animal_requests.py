import sqlite3
import json
from models import Animal, Location, Customer

# This is a Docstring it should be at the beginning of all classes and functions
# It gives a description of the class or function
"""Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted",
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted",
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted",
    },
]


def get_all_animals(query_params):
    """given code to fetch all animals from sql database"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""

    if len(query_params) != 0:
        param = query_params[0]
        [qs_key, qs_value] = param.split("=")

        if qs_key == "_sortBy":
            if qs_value == 'location':
                sort_by = " ORDER BY location_id"

    sql_to_execute = f"""
    SELECT
        a.id,
        a.name,
        a.breed,
        a.status,
        a.location_id,
        a.customer_id,
        l.name location_name,
        l.address location_address,
        c.name customer_name,
        c.address customer_address
    FROM Animal a
    JOIN Location l ON l.id = a.location_id
    JOIN Customer c ON c.id = a.customer_id
    {sort_by}"""

    # Execute SQL written above
    db_cursor.execute( sql_to_execute )

    # Initialize an empty list to hold all animal representations
    animals = []

    # Convert rows of data into a Python list
    dataset = db_cursor.fetchall()

    # Iterate list of data returned from database
    for row in dataset:

        # Create an animal instance from the current row
        animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                        row['location_id'], row['customer_id'])

        # Create a Location instance from the current row
        location = Location(row['location_id'], row['location_name'], row['location_address'])

        #Create a customer instance from the current row
        customer = Customer(row["customer_id"], row["customer_name"], row["customer_address"])

        # Add the dictionary representation of the location to the animal
        animal.location = location.__dict__
        animal.customer = customer.__dict__

        # Add the dictionary representation of the animal to the list
        animals.append(animal.__dict__)

    return animals


# Function with a single parameter
def get_single_animal(id):
    """given code to fetch single animal from sql database given id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(
            data["id"],
            data["name"],
            data["breed"],
            data["status"],
            data["location_id"],
            data["customer_id"],
        )

        return animal.__dict__


def get_animals_by_location(location_id):
    """retrieves animal data from sql db from given location_id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        select
            *
        from Animal a
        WHERE a.location_id = ?
        """,
            (location_id,),
        )

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )

            animals.append(animal.__dict__)
    return animals


def get_animals_by_status(status):
    """retrieves animal data from sql db from given status"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        select
            *
        from Animal a
        WHERE a.status like ?
        """,
            (status,),
        )

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["breed"],
                row["status"],
                row["location_id"],
                row["customer_id"],
            )

            animals.append(animal.__dict__)
    return animals


def create_animal(new_animal):
    """docstring for create animal. It posts animals"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
            new_animal['status'], new_animal['locationId'],
            new_animal['customerId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal

def delete_animal(id):
    """deletes animal from sql db from given id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM animal
        WHERE id = ?
        """,
            (id,),
        )

def update_animal(id, new_animal):
    """replaces existing sql db animal table row with new data"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Animal
            SET
                name = ?,
                status = ?,
                breed = ?,
                customer_id = ?,
                location_id = ?
        WHERE id = ?
        """,
            (
                new_animal["name"],
                new_animal["status"],
                new_animal["breed"],
                new_animal["customerId"],
                new_animal["locationId"],
                id,
            ),
        )

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
