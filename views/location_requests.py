import sqlite3
import json
from models import Location

LOCATIONS = [
    {"id": 1, "name": "Nashville North", "address": "8422 Johnson Pike"},
    {"id": 2, "name": "Nashville South", "address": "209 Emory Drive"},
]


def get_all_locations():
    """given code to fetch all locations from sql database"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            location.*,
            COUNT(*) as animals
        FROM location
        JOIN Animal ON location.id = location_id
        GROUP BY location.id
        """
        )

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            location = Location(row["id"], row["name"], row["address"], row['animals'])

            locations.append(location.__dict__)

    return locations


# Function with a single parameter
def get_single_location(id):
    """given code to fetch single location from sql database given id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            location.*,
            COUNT(*) as animals
        FROM location
        JOIN Animal ON location.id = location_id
        GROUP BY location.id
        HAVING location.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an location instance from the current row
        location = Location(data["id"], data["name"], data["address"], data['animals'])

        return location.__dict__


def create_location(location):
    """docstring for create location. It posts locations"""
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the location dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location


def delete_location(id):
    """deletes location with matching location Id"""
    # Initial -1 value for location index, in case one isn't found
    location_index = -1

    # Iterate the LOCATIONS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the location was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)


def update_location(id, new_location):
    """adds updated location to list"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """,
            (
                new_location["name"],
                new_location["address"],
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
