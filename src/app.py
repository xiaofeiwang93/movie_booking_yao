from flask import Flask
from controllers.booking_system_controller import BookingSystemController

get=['GET']
post=['POST']
both=['GET','POST']

app = Flask(__name__, template_folder='views')
booking_system_controller = BookingSystemController()

#BookingSystemController.initial_db_setup()

app.add_url_rule('/movies', methods=both, view_func=booking_system_controller.movie_list)

app.add_url_rule('/movies/search', methods=both, view_func=booking_system_controller.search_movies)

app.add_url_rule('/booking', methods=both, view_func=booking_system_controller.book_movie)

app.add_url_rule('/checkout', methods=both, view_func=booking_system_controller.checkout)