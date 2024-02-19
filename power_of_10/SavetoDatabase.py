import psycopg2
from psycopg2 import sql
from power_of_10 import search_athletes, get_athlete, get_rankings

# Database connection parameters
DB_NAME = "runners"
DB_USER = "postgres"
DB_PASSWORD = "Forest75Ever"
DB_HOST = "localhost"
DB_PORT = "5432"

def split_name(full_name):
    # Split the full name into parts based on whitespace
    name_parts = full_name.split()

    # The first part will be the first name
    first_name = name_parts[0]

    # The last part will be the last name
    last_name = name_parts[-1]

    # If there are more than two parts, assume the rest are middle names
    if len(name_parts) > 2:
        # Middle names are everything between the first and last parts
        last_name = name_parts[1] + " " + name_parts[2]

    return first_name, last_name

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
            print(athlete['firstname'] + " " + athlete['surname'])
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
        rankingAthletes = get_rankings(2023, 'M', 'ALL', '1500',None)
        print(rankingAthletes)
        athletes = []
        for Rathlete in rankingAthletes:
            first_name, last_name = split_name(Rathlete['name'])
            print("FIRSTNAME: " + first_name + " LASTNAME: " + last_name + " CLUB: " + Rathlete['club'])
            #not able to search using club if a runner has changed club since running 'x' time
            athletes.append(search_athletes(firstname=first_name, surname=last_name )) # Example search criteria
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


