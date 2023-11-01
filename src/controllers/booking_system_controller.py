import csv
from datetime import datetime, timedelta
import random

from flask import render_template, request

from constants import Constants
from models.movie import Movie

class BookingSystemController:
    """!
    BookingSystemController class
    """
    def movie_list(self):
        """!
        Get a list of movies

        @return: A list of movies
        """
        movie_list = []
        
        movies_data = BookingSystemController.read(Constants.movie_db_name)

        for data in movies_data:
            movie = Movie()
            movie.title = data.get("title")
            movie.description = data.get("description")
            movie.duration_mins = data.get("duration_mins")
            movie.language = data.get("language")
            movie.release_date = data.get("release_date")
            movie.country = data.get("country")
            movie.genre = data.get("genre")
            movie_list.append(movie)

        return render_template('movie_list.html', movie_list=movie_list)

    def search_movies(self):
        """!
        Search for movies

        @param search_data: The data to search by
        @return: A list of movies
        """
        movie = Movie()
        movie.title = request.form.get('titleSearch')
        movie.language = request.form.get('languageSearch')
        movie.genre = request.form.get('genreSearch')
        movie.release_date = request.form.get('releasedateSearch')

        movies_data = BookingSystemController.search_records_by_multiple_attributes(Constants.movie_db_name, movie)

        movie_list = []

        for data in movies_data:
            movie = Movie()
            movie.title = data.get("title")
            movie.description = data.get("description")
            movie.duration_mins = data.get("duration_mins")
            movie.language = data.get("language")
            movie.release_date = data.get("release_date")
            movie.country = data.get("country")
            movie.genre = data.get("genre")
            movie_list.append(movie)

        return render_template('movie_list.html', movie_list=movie_list)

    def create_table(tablename, columns):
        """!
        Create a table in the database

        @param tablename: The name of the table to be created
        """
        try:
            with open(tablename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(columns)  

            print(f"Data written to the CSV file - {tablename} successfully.")
        except FileNotFoundError:
            print(f"File '{tablename}' not found.")
        except Exception as e:
            print(f"An error occurred while writing data: {str(e)}")
    
    def get_latest_id(tablename):
        """!
        Get the next available id for a table

        @param tablename: The name of the table to get the next id from
        """
        try:
            with open(tablename, 'r', newline='') as file:
                reader = csv.DictReader(file)
                existing_ids = [int(row['id']) for row in reader]

                if not existing_ids:  
                    return 1  
                else:
                    return max(existing_ids) + 1
        except FileNotFoundError:
            return 1
        
    def insert(tablename, record, columns):
        """!
        Insert a record into a table

        @param tablename: The name of the table to insert the record into
        @param record: The record to be inserted
        @param columns: The columns of the table
        """
        try:
            next_id = BookingSystemController.get_latest_id(tablename)
            record['id'] = next_id

            with open(tablename, 'a', newline='') as file:
                fieldnames = columns  
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                if file.tell() == 0:  
                    writer.writeheader()

                writer.writerow(record)
                return True
        except FileNotFoundError:
            print(f"File '{tablename}' not found.")
        except Exception as e:
            print(f"An error occurred while adding a record: {str(e)}")

    def read(tablename):
        """!
        Read all records from a table

        @param tablename: The name of the table to read the records from
        """
        try:
            records = []
            with open(tablename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    records.append(row)
            return records
        except FileNotFoundError:
            print(f"File '{tablename}' not found.")
            return []
        except Exception as e:
            print(f"An error occurred while reading records: {str(e)}")
            return []
        
    def search_by_id(id, tablename):
        """!
        Search for a record by its id

        @param search_id: The id of the record to search for
        @param tableName: The name of the table to search in
        """
        try:
            with open(tablename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("id") == str(id):
                        return row
            print("Record not found.")
            return None
        except FileNotFoundError:
            print(f"File '{tablename}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    
    def search_by_attribute(search_attribute, search_value, tablename):
        """!
        Search for a record by a specific attribute

        @param search_attribute: The attribute to search by
        @param search_value: The value of the attribute to search by
        @param tablename: The name of the table to search in
        """
        try:
            records = []
            with open(tablename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if search_attribute.lower().find("date") == -1:
                        if row.get(search_attribute).lower().find(search_value.lower()) != -1:
                            records.append(row)
                    else:
                        if row.get(search_attribute) == search_value:
                            records.append(row)
            return records
        except FileNotFoundError:
            print(f"File '{tablename}' not found.")
            return []
        except Exception as e:
            print(f"An error occurred while reading records: {str(e)}")
            return []
    
    def validate_coupon(couponid):
        """!
        Check if the coupon is valid. 

        @param coupon: The coupon to be checked.
        @return: True if the coupon is valid, False otherwise.
        """

        if couponid == "validcoupon":
            coupon = Coupon(
                coupon_id=couponid,
                expiry_date=None,
                discount=0.8
            )

            return "Valid"
        
        return "Invalid"
    
    def search_records_by_multiple_attributes(tablename, search_data):
        """!
        Search for a record by multiple attributes

        @param tablename: The name of the table to search in
        @param search_data: The data to search by
        """
        try:
            records = []
            with open(tablename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        release_date = row.get("release_date")
                        release_date = datetime.strptime(release_date, Constants.date_format)
                        search_release_date = datetime.strptime(search_data.release_date, Constants.date_format)
                    except ValueError:
                        search_release_date = ''

                    if (BookingSystemController.is_movie_matches(row, search_data, release_date, search_release_date)):
                        records.append(row)
            return records
        except FileNotFoundError:
            print(f"File '{tablename}' not found.")
            return []
        except Exception as e:
            print(f"An error occurred while reading records: {str(e)}")
            return []
        
    def is_movie_matches(row, search_data, release_date, search_release_date):
        """!
        Check if the movie matches the search data

        @param row: The row to check
        @param search_data: The data to search by
        @param release_date: The release date of the movie
        @param search_release_date: The release date of the movie to search by
        """
        return ((row.get("title").lower().find(search_data.title) != -1 and search_data.title.lower() != '') or
                        (row.get("language").lower().find(search_data.language) != -1 and search_data.language.lower() != '') or
                        (row.get("genre").lower().find(search_data.genre) != -1 and search_data.genre.lower() != '') or 
                        (release_date == search_release_date and search_release_date != ''))
    
    def initial_db_setup():
        """!
        Create the database and add some initial records

        @return: None
        """

        # create movie table
        BookingSystemController.create_table(Constants.movie_db_name, Constants.movie_db_columns)

        # Create a list of movie records
        movie_records = [
            {
                'title': "The Nun II",
                'description': "1956 - France. A priest is murdered. An evil is spreading. The sequel to the worldwide smash hit follows Sister Irene as she once again comes face-to-face with Valak, the demon nun.",
                'duration_mins': 110,
                'language': "English",
                'release_date': "07/09/2023",
                'country': "United States",
                'genre': "Thriller"
            },
            {
                'title': "Inception",
                'description': "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                'duration_mins': 148,
                'language': "English",
                'release_date': "16/07/2010",
                'country': "United States",
                'genre': "Sci-Fi"
            },
            {
                'title': "The Godfather",
                'description': "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                'duration_mins': 175,
                'language': "English",
                'release_date': "24/03/1972",
                'country': "United States",
                'genre': "Crime"
            },
            {
                'title': "Pulp Fiction",
                'description': "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                'duration_mins': 154,
                'language': "English",
                'release_date': "14/10/1994",
                'country': "United States",
                'genre': "Crime"
            },
            {
                'title': "Avatar",
                'description': "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
                'duration_mins': 162,
                'language': "English",
                'release_date': "18/12/2009",
                'country': "United States",
                'genre': "Action"
            },
            {
                'title': "The Matrix",
                'description': "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                'duration_mins': 136,
                'language': "English",
                'release_date': "31/03/1999",
                'country': "United States",
                'genre': "Sci-Fi"
            },
            {
                'title': "Forrest Gump",
                'description': "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold through the perspective of an Alabama man with an IQ of 75.",
                'duration_mins': 142,
                'language': "English",
                'release_date': "06/07/1994",
                'country': "United States",
                'genre': "Drama"
            },
            {
                'title': "The Shawshank Redemption",
                'description': "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                'duration_mins': 142,
                'language': "English",
                'release_date': "14/10/1994",
                'country': "United States",
                'genre': "Drama"
            },
            {
                'title': "Gladiator",
                'description': "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
                'duration_mins': 155,
                'language': "English",
                'release_date': "05/05/2000",
                'country': "United States",
                'genre': "Action"
            },
            {
                'title': "The Dark Knight",
                'description': "When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                'duration_mins': 152,
                'language': "English",
                'release_date': "18/07/2008",
                'country': "United States",
                'genre': "Action"
            }
        ]

        # Add each record to the CSV
        for record in movie_records:
            BookingSystemController.insert(Constants.movie_db_name, record, Constants.movie_db_columns)

        # create movie screening table
        BookingSystemController.create_table(Constants.screening_db_name, Constants.screening_db_columns)

        screening_records = []

        # Add additional screening records for the next 10 days
        for i in range(0, 11):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime(Constants.date_format)
            
            # Generate a random start time for each movie
            start_times = [f"{random.randint(10, 21)}:00" for _ in range(1, 31)]

            for movieid, hallid, starttime in zip(range(1, 31), range(1, 31), start_times):
                endtime = (int(starttime.split(":")[0]) + 2) % 24  # Assuming screenings are 2 hours long
                endtime = f"{endtime:02d}:00"

                screening_records.append({
                    'movieid': str(movieid),
                    'date': date_str,
                    'starttime': starttime,
                    'endtime': endtime,
                    'hallid': str(hallid)
                })

        # Add the screenings to the database
        for record in screening_records:
            BookingSystemController.insert(Constants.screening_db_name, record, Constants.screening_db_columns)

        # create movie booking table
        BookingSystemController.create_table(Constants.booking_db_name, Constants.booking_db_columns)

        bookings = [
            {
                'movieid': '1',
                'screeningid': '1',
                'hallid': '1',
                'customerid': '1'
            },
            {
                'movieid': '2',
                'screeningid': '2',
                'hallid': '2',
                'customerid': '2'
            },
            {
                'movieid': '3',
                'screeningid': '3',
                'hallid': '3',
                'customerid': '3'
            },
            {
                'movieid': '4',
                'screeningid': '4',
                'hallid': '4',
                'customerid': '4'
            },
            {
                'movieid': '5',
                'screeningid': '5',
                'hallid': '5',
                'customerid': '5'
            },
            {
                'movieid': '6',
                'screeningid': '6',
                'hallid': '6',
                'customerid': '6'
            },
            {
                'movieid': '7',
                'screeningid': '7',
                'hallid': '7',
                'customerid': '7'
            },
            {
                'movieid': '8',
                'screeningid': '8',
                'hallid': '8',
                'customerid': '8'
            }
        ]

        for record in bookings:
            BookingSystemController.insert(Constants.booking_db_name, record, Constants.booking_db_columns)

        BookingSystemController.create_table(Constants.booking_seats_db_name, Constants.booking_seats_db_columns)

        seats = [
            {
                'type': 'Adult',
                'bookingid': 1,
                'row': '1',
                'seatnumber': '1',
                'price': 10,
            },
            {
                'type': 'Adult',
                'bookingid': 1,
                'row': '1',
                'seatnumber': '2',
                'price': 10,
            },
            {
                'type': 'Adult',
                'bookingid': 1,
                'row': '1',
                'seatnumber': '3',
                'price': 10,
            }
        ]

        for record in seats:
            BookingSystemController.insert(Constants.booking_seats_db_name, record, Constants.booking_seats_db_columns)