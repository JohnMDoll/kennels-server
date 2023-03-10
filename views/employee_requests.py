import sqlite3
from models import Employee, Location, Animal

EMPLOYEES = [{"id": 1, "name": "Jenna Solis"}]


def get_all_employees():
    """given code to fetch all employees from sql database"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.*,
            l.name location_name,
            l.address as location_address
        FROM employee e
        JOIN Location l ON l.id = e.location_id
        """
        )

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Employee class above.
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"], None, None
            )
            location = Location(row["id"], row["location_name"], row["location_address"])

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    return employees


# Function with a single parameter
def get_single_employee(id):
    """given code to fetch single employee from sql database given id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            e.*,
            l.name location_name,
            l.address as location_address,
			a.name as animal,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id customer_id,
			a.id as animal_table_id
		FROM employee e
        JOIN Location l ON l.id = e.location_id
        JOIN employee_animals ea ON ea.employee_id = e.id
		JOIN Animal a ON animal_table_id = ea.animal_id
        WHERE e.id = ?
        """,
            (id,),
        )
        employee = None
        employee_animals = []
        # Load the single result into memory
        dataset = db_cursor.fetchall()
        for data in dataset:
            if employee is None:
                employee = Employee(
                        data["id"], data["name"], data["address"], data["location_id"], None, None
                    )
                location = Location(
                    data["id"], data["location_name"], data["location_address"]
                )
                employee.location = location.__dict__
            if data["animal"] is not None:
                animal = Animal(data['animal_table_id'], data['animal'], data['breed'], data['status'], data['location_id'], data['customer_id'])
                employee_animals.append(animal.__dict__)

        employee.animals = employee_animals
        print(employee)
        return employee.__dict__


def get_employees_by_location(location_id):
    """retrieves employee data from sql db from given location_id"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        select
            *
        from Employee e
        WHERE e.location_id = ?
        """,
            (location_id,),
        )

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"], None, None
            )

            employees.append(employee.__dict__)
    return employees


def create_employee(employee):
    """docstring for create employee. It posts employees"""
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee


def delete_employee(id):
    """deletes employee with matching employee Id"""
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
    """overwrites db employee"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Employee
            SET
                name = ?,
                address = ?,
                location_id = ?
        WHERE id = ?
        """,
            (
                new_employee["name"],
                new_employee["address"],
                new_employee["locationId"],
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
