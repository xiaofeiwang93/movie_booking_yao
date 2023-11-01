class Constants:
    database_path = "./Database/"

    database_path = "./Database/"
    movie_db_name = f"{database_path}movie.csv"
    movie_db_columns = ["id", "title", "description", "duration_mins", "language", "release_date", "country", "genre"]
    movie_media_db_name = f"{database_path}movieMedia.csv"
    movie_media_db_columns = ["id", "movieid", "cardsrcaddress", "detailbanneraddress"]
    screening_db_name = f"{database_path}screening.csv"
    screening_db_columns = ["id", "movieid", "date", "starttime", "endtime", "hallid"]
    booking_db_name = f"{database_path}booking.csv"
    booking_db_columns = ["id", "movieid", "screeningid", "hallid", "customerid"]
    booking_seats_db_name = f"{database_path}bookingseats.csv"
    booking_seats_db_columns = ["id", "bookingid", "type", "row", "seatnumber", "price", "bookingid"]
    date_format = "%d/%m/%Y"
