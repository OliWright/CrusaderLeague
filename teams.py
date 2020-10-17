from helpers import ParseDate_dmy
from helpers import CalcAge
import datetime

lane_order = (
	'Halton',
	'Cosacss',
	'Winsford'
)
event_date = datetime.date( 2019, 6, 29 )

num_teams = len(lane_order)
event_teams_per_lane = []
swimmers_per_team = [{},{},{},{}]

def get_event_team(event, lane):
	assert(lane < num_teams)
	return event_teams_per_lane[lane][event]

class Event():
	def __init__(self, sex, num_legs, max_age):
		self.sex = sex
		self.num_legs = num_legs
		self.max_age = max_age
		
	def is_relay(self):
		return self.num_legs > 1
		
	def is_open(self):
		return self.max_age == 99
		
	def swim_up_min_age(self):
		if self.is_open():
			return 14
		else:
			return self.max_age - 2

events = (
	Event( '', 0, 99), # 0
	Event( 'F', 1, 99), # 1  Women's Open 100m IM
	Event( 'M', 1, 99), # 2  Men's Open 100m IM
	Event( 'F', 4, 10), # 3  Women's 10 Yrs/Under 4x50m Free
	Event( 'M', 4, 10), # 4  Men's 10 Yrs/Under 4x50m Free
	Event( 'F', 4, 14), # 5  Women's 14 Yrs/Under 4x50m Medley
	Event( 'M', 4, 14), # 6  Men's 14 Yrs/Under 4x50m Medley
	Event( 'F', 1, 99), # 7  Women's 12 Yrs/Under 50m Butterfly
	Event( 'M', 1, 99), # 8  Men's 12 Yrs/Under 50m Butterfly
	Event( 'F', 1, 99), # 9  Women's Open 100m Backstroke
	Event( 'M', 1, 99), # 10 Men's Open 100m Backstroke
	Event( 'F', 1, 10), # 11 Women's 10 Yrs/Under 50m Breaststroke
	Event( 'M', 1, 10), # 12 Men's 10 Yrs/Under 50m Breaststroke
	Event( 'F', 1, 14), # 13 Women's 14 Yrs/Under 50m Freestyle
	Event( 'M', 1, 14), # 14 Men's 14 Yrs/Under 50m Freestyle
	Event( 'F', 4, 12), # 15 Women's 12 Yrs/Under 4x50m Free
	Event( 'M', 4, 12), # 16 Men's 12 Yrs/Under 4x50m Free
	Event( 'F', 4, 99), # 17 Women's Open 4x50m Medley
	Event( 'M', 4, 99), # 18 Men's Open 4x50m Medley
	Event( 'F', 1, 10), # 19 Women's 10 Yrs/Under 50m Butterfly
	Event( 'M', 1, 10), # 20 Men's 10 Yrs/Under 50m Butterfly
	Event( 'F', 1, 14), # 21 Women's 14 Yrs/Under 50m Backstroke
	Event( 'M', 1, 14), # 22 Men's 14 Yrs/Under 50m Backstroke
	Event( 'F', 1, 12), # 23 Women's 12 /Under 50m Breaststroke
	Event( 'M', 1, 12), # 24 Men's 12 Yrs/Under 50m Breaststroke
	Event( 'F', 1, 99), # 25 Women's Open 100m Freestyle
	Event( 'M', 1, 99), # 26 Men's Open 100m Freestyle
	Event( 'F', 4, 10), # 27 Women's 10 Yrs/Under 4x50m Medley
	Event( 'M', 4, 10), # 28 Men's 10 Yrs/Under 4x50m Medley
	Event( 'F', 4, 14), # 29 Women's 14 Yrs/Under 4x50m Free
	Event( 'M', 4, 14), # 30 Men's 14 Yrs/Under 4x50m Free
	Event( 'F', 1, 12), # 31 Women's 12 Yrs/Under 50m Backstroke
	Event( 'M', 1, 12), # 32 Men's 12 Yrs/Under 50m Backstroke
	Event( 'F', 1, 99), # 33 Women's Open 100m Breaststroke
	Event( 'M', 1, 99), # 34 Men's Open 100m Breaststroke
	Event( 'F', 1, 10), # 35 Women's 10 Yrs/Under 50m Freestyle
	Event( 'M', 1, 10), # 36 Men's 10 Yrs/Under 50m Freestyle
	Event( 'F', 1, 14), # 37 Women's 14 Yrs/Under 50m Butterfly
	Event( 'M', 1, 14), # 38 Men's 14 Yrs/Under 50m Butterfly
	Event( 'F', 4, 12), # 39 Women's 12 Yrs/Under 4x50m Medley
	Event( 'M', 4, 12), # 40 Men's 12 Yrs/Under 4x50m Medley
	Event( 'F', 4, 99), # 41 Women's Open 4x50m Free
	Event( 'M', 4, 99), # 42 Men's Open 4x50m Free
	Event( 'F', 1, 10), # 43 Women's 10 Yrs/Under 50m Backstroke
	Event( 'M', 1, 10), # 44 Men's 10 Yrs/Under 50m Backstroke
	Event( 'F', 1, 14), # 45 Women's 14 /Under 50m Breaststroke
	Event( 'M', 1, 14), # 46 Men's 14 Yrs/Under 50m Breaststroke
	Event( 'F', 1, 12), # 47 Women's 12 Yrs/Under 50m Freestyle
	Event( 'M', 1, 12), # 48 Men's 12 Yrs/Under 50m Freestyle
	Event( 'F', 1, 99), # 49 Women's Open 100m Butterfly
	Event( 'M', 1, 99), # 50 Men's Open 100m Butterfly
	Event( 'X', 8, 99), # 51 Cannon
)

class Swimmer():
	def __init__(self, first_name = None, last_name = None, dob = None, sex = None):
		self.first_name = first_name
		self.last_name = last_name
		if first_name is None:
			self.full_name = ''
		else:
			self.full_name = first_name + ' ' + last_name
		self.dob = dob
		self.sex = sex
		if dob is not None:
			self.age_on_day = CalcAge(dob, event_date)
			
	def __hash__(self):
		return hash((self.full_name, self.dob, self.sex))		
			
	def __eq__(self, other):
		return (self.full_name, self.dob, self.sex) == (self.full_name, self.dob, self.sex)
		
	def __lt__(self, other):
		if self.last_name == other.last_name:
			return self.first_name < other.first_name
		else:
			return self.last_name < other.last_name
	
class SwimmerStats():
	def __init__(self):
		self.individual_events = []
		self.relays = []
		self.individual_swim_up_events = []

class EventTeam():
	# Constructor.  Passed in a row of text describing the swimmers for each leg.
	def __init__(self, event_number, team_idx, tokens):
		self.legs = []
		self.team_idx = team_idx
		self.event_number = event_number
		self.append_legs(event_number, tokens)

	def append_legs(self, event_number, tokens):
		num_tokens = len( tokens )
		assert(num_tokens == 14) # Expected from CSV
		event = events[event_number]
		swimmers = swimmers_per_team[self.team_idx]
		for leg in range(4):
			first_token = (leg * 3) + 2
			first_name = tokens[first_token].strip()
			#print('{:d} {:d} {:}'.format(event_number, leg, first_name))
			if len(first_name) == 0:
				if len(self.legs) < event.num_legs:
					# This is a genuine non-entry
					assert(len(self.legs) == 0)
					self.legs.append(Swimmer())
				break
					
			last_name = tokens[first_token + 1].strip()
			assert(len(first_name))
			assert(len(self.legs) < event.num_legs)
			dob = ParseDate_dmy(tokens[first_token + 2])
			sex = event.sex
			if event.sex == 'X':
				# In the cannon, the legs alternate between F/M
				sex = 'F'
				if len(self.legs) & 1:
					sex = 'M'
			swimmer = Swimmer(first_name, last_name, dob, sex)
			if swimmer not in swimmers:
				swimmers[swimmer] = SwimmerStats()
			self.legs.append(swimmer)
			
			swimmer_stats = swimmers.get(swimmer)
			if event.is_relay():
				swimmer_stats.relays.append(self)
			else:
				swimmer_stats.individual_events.append(self)
				# Was the swimmer swimming up in an individual event?
				if swimmer.age_on_day <= event.swim_up_min_age():
					swimmer_stats.individual_swim_up_events.append(self)

def read_team_file(filename, team_idx):
	file = open(filename, 'r')
	previous_event_number = 0
	event_teams = {}
	for line in file:
		tokens = line.split( "," )
		if len(tokens) > 0:
			if(tokens[0].isdigit()):
				event_number = int(tokens[0])
				assert(event_number == (previous_event_number + 1))
				#print('Event ' + str(event_number))
				event_teams[event_number] = EventTeam(event_number, team_idx, tokens)
				previous_event_number = event_number
			elif previous_event_number > 0:
				# Cannon
				assert(previous_event_number == 51)
				event_teams[51].append_legs(event_number, tokens)
	return event_teams

# Read all the teams
def read_team_files():
	for team_idx in range(num_teams):
		team_file_name = 'teams/Crusader 2019 Winsford Round - ' + lane_order[team_idx] + ' - Team Entry.csv'
		print('Reading {:}'.format(team_file_name))
		event_teams_per_lane.append(read_team_file(team_file_name, team_idx))
