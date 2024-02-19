import psycopg2
from psycopg2 import sql
from power_of_10 import search_athletes, get_athlete

# Database connection parameters
DB_NAME = "runners"
DB_USER = "postgres"
DB_PASSWORD = "Forest75Ever"
DB_HOST = "localhost"
DB_PORT = "5432"

def insert_athlete_data(athletes):
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        cursor = conn.cursor()

        # Insert athlete data into the database
        insert_query = sql.SQL("""
            INSERT INTO athlete
            VALUES (%s, %s, %s, %s, %s)
        """)
        
        for athlete in athletes:
            athlete_data = get_athlete(athlete['athlete_id'])
            cursor.execute(insert_query, (
                    athlete['athlete_id'],
                    athlete['firstname'],
                    athlete['surname'],
                    athlete['track'],
                    athlete_data['lead coach']
                ))

        conn.commit()
        print("Athlete data inserted successfully!")
    except psycopg2.Error as e:
        print("Error inserting athlete data:", e)
    finally:
        cursor.close()
        conn.close()


# Function to populate the database with athlete data
def populate_database_with_athletes():
    try:
        # Search for athletes
        athletes = search_athletes(firstname="Ben", surname="Squire" ) # Example search criteria
        # Retrieve detailed data for each athlete
        detailed_athlete_data_id = []
        for athlete in athletes:
            print()
            print(athlete['firstname'])
            print(athlete['surname'])
            print(athlete['track'])
            detailed_athlete_data_id.append(athlete)

        # Insert athlete data into the database
        insert_athlete_data(athletes)
    except Exception as e:
        print("Error populating database with athletes:", e)

# Call the function to populate the database with athlete data
populate_database_with_athletes()
