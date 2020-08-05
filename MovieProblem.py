import sys
from datetime import datetime, timedelta
import calendar 

#######################################Assumptions##########################

MOVIE_THEATRE_OPENING = '8:00:00'
MOVIE_THREATE_CLOSING = "23:59:00"
MOVIE_THEATRE_SETUP = "01:00"
CLEANING_TIME = "00:35"

######################################Definitions##########################
class Movie: 
	def __init__(self, name, release_year, rating, run_time, showtimes) :
		self.name = name
		self.release_year = release_year
		self.rating = rating
		self.run_time = run_time
		self.showtimes = []
		

movies = {}

########################################SET TIMING VARIABLES########################################								
current_day = datetime.now().date() 								
opening_time = datetime.strptime(MOVIE_THEATRE_OPENING, '%H:%M:%S').time() 					
closing_time = datetime.strptime(MOVIE_THREATE_CLOSING, '%H:%M:%S').time() 					
[movie_setup_hours, movie_setup_minutes] = [int(x) for x in MOVIE_THEATRE_SETUP.split(':')]  
[clean_hours, clean_minutes] = [int(x) for x in CLEANING_TIME.split(':')] 
opening_time = datetime.combine(current_day, opening_time) 
closing_time = datetime.combine(current_day, closing_time) 
movie_setup = timedelta(hours=movie_setup_hours, minutes=movie_setup_minutes) 
cleaning_time = timedelta(hours=clean_hours, minutes=clean_minutes) 
earliest_move_start_time = opening_time + movie_setup 


######################################FUNCTION DEFINITIONS##############################
#Reads in a file from the command line 
def readinfile() :
	file = open(sys.argv[1], "r") 
	line_count=0
	for line in file:
		line_count += 1
		if (line_count == 1): 
			continue  
		name, release_year, rating, run_time = line.split(',')
		movie = Movie(name, release_year, rating, run_time, []) 
		movies[line_count] = movie

def determineShowtimes():
	for each_key in movies: 
		movie_Length = movies[each_key].run_time 
		[movie_runtime_hours, movie_runtime_minutes] = [int(x) for x in movie_Length.split(':')] 	
		movie_runTime = timedelta(hours = movie_runtime_hours, minutes = movie_runtime_minutes) 	
		unadjusted_end_time = closing_time 																
		while unadjusted_end_time- movie_runTime > earliest_move_start_time: 
			unadjusted_start_time = unadjusted_end_time - movie_runTime  
			offset = (unadjusted_start_time.minute) % 5 
			offsetTime = timedelta(minutes = offset) 
			start_time = unadjusted_start_time - offsetTime 
			end_time = start_time + movie_runTime 
			if (start_time >= earliest_move_start_time): 
				print_start = start_time.strftime('%H:%M') 
				print_end = end_time.strftime('%H:%M') 
				print_time = print_start + "-" + print_end 
				movies[each_key].showtimes.insert(0,print_time) 
				unadjusted_end_time = start_time - cleaning_time 
			else : 
				break

def print_showings() : 
	day_of_week = calendar.day_name[current_day.weekday()]
	current_day_printout = day_of_week + " " + current_day.strftime("%B %d, %Y")
	print current_day_printout
	for each_key in movies: 
		current = movies[each_key]
		print_out = current.name + ", " + current.release_year + ", " + current.rating + ", " + current.run_time
		print print_out
		for each_showtime in movies[each_key].showtimes: 
			print each_showtime

def run():
	readinfile()
	determineShowtimes()
	print_showings()

#################################RUN######################
run()


