from flask import Flask

get=['GET']
post=['POST']
both=['GET','POST']

app = Flask(__name__, template_folder='views')
ticketing_controller = MovieTicketController(DbService, LoginService, CommonService, MovieService, BookingService, AdminServce)

app.add_url_rule('/', methods=both, view_func=ticketing_controller.login)

app.add_url_rule('/home', methods=both, view_func=ticketing_controller.home)

app.add_url_rule('/movies', methods=both, view_func=ticketing_controller.view_movie_list)

app.add_url_rule('/movies/<int:movie_id>', methods=both, view_func=ticketing_controller.view_movie_detail)

app.add_url_rule('/movies/search', methods=both, view_func=ticketing_controller.search_movies)

app.add_url_rule('/movies/search/title', methods=both, view_func=ticketing_controller.search_movies_by_title) 

app.add_url_rule('/movies/searchscreening', methods=both, view_func=ticketing_controller.search_movie_by_screening_date)

app.add_url_rule('/movies/searchscreeninglist', methods=both, view_func=ticketing_controller.search_movie_list_by_screening_date)

app.add_url_rule('/selectseats', methods=both, view_func=ticketing_controller.select_seats) 

app.add_url_rule('/checkout', methods=both, view_func=ticketing_controller.checkout) 

app.add_url_rule('/payment', methods=both, view_func=ticketing_controller.make_payment)

app.add_url_rule('/mybookings', methods=both, view_func=ticketing_controller.my_bookings)

app.add_url_rule('/movie/add', methods=both, view_func=ticketing_controller.add_movie)