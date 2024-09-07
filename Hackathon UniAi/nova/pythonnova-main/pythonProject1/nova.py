import pymysql
import mysql.connector

# Set the database credentials
def create_connection():
    connection = mysql.connector.connect(
        host="database-nova.c7a6a2808nfy.us-west-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="digitalsnova",
        #database="database-nova"
    )
    return connection

# Save data to the database
def save_data_to_database(data):
    connection = create_connection()
    cursor = connection.cursor()

    # Create the table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS nova_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        h1 VARCHAR(255),
        time VARCHAR(255),
        div_id VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

    # Insert data into the database
    insert_query = "INSERT INTO nova_data (h1, time, div_id) VALUES (%s, %s, %s)"
    for entry in data:
        cursor.execute(insert_query, (entry.get('h1', None), entry.get('time', None), entry.get('div', None)))

    # Commit changes and close the connection
    connection.commit()
    connection.close()

# Εδώ πρέπει να είναι ο κώδικάς σας για τη λήψη των δεδομένων από τον ιστότοπο
# Κατόπιν, μπορείτε να καλέσετε τη συνάρτηση save_data_to_database με το αποτέλεσμα

