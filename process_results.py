import teams
import html_bookends
from race_time import RaceTime

teams.read_team_files()

event_names = (
	"",
	"Women's Open 100m IM",
	"Men's Open 100m IM",
	"Women's 10 Yrs/Under 4x50m Free",
	"Men's 10 Yrs/Under 4x50m Free",
	"Women's 14 Yrs/Under 4x50m Medley",
	"Men's 14 Yrs/Under 4x50m Medley",
	"Women's 12 Yrs/Under 50m Butterfly",
	"Men's 12 Yrs/Under 50m Butterfly",
	"Women's Open 100m Backstroke",
	"Men's Open 100m Backstroke",
	"Women's 10 Yrs/Under 50m Breaststroke",
	"Men's 10 Yrs/Under 50m Breaststroke",
	"Women's 14 Yrs/Under 50m Freestyle",
	"Men's 14 Yrs/Under 50m Freestyle",
	"Women's 12 Yrs/Under 4x50m Free",
	"Men's 12 Yrs/Under 4x50m Free",
	"Women's Open 4x50m Medley",
	"Men's Open 4x50m Medley",
	"Women's 10 Yrs/Under 50m Butterfly",
	"Men's 10 Yrs/Under 50m Butterfly",
	"Women's 14 Yrs/Under 50m Backstroke",
	"Men's 14 Yrs/Under 50m Backstroke",
	"Women's 12 /Under 50m Breaststroke",
	"Men's 12 Yrs/Under 50m Breaststroke",
	"Women's Open 100m Freestyle",
	"Men's Open 100m Freestyle",
	"Women's 10 Yrs/Under 4x50m Medley",
	"Men's 10 Yrs/Under 4x50m Medley",
	"Women's 14 Yrs/Under 4x50m Free",
	"Men's 14 Yrs/Under 4x50m Free",
	"Women's 12 Yrs/Under 50m Backstroke",
	"Men's 12 Yrs/Under 50m Backstroke",
	"Women's Open 100m Breaststroke",
	"Men's Open 100m Breaststroke",
	"Women's 10 Yrs/Under 50m Freestyle",
	"Men's 10 Yrs/Under 50m Freestyle",
	"Women's 14 Yrs/Under 50m Butterfly",
	"Men's 14 Yrs/Under 50m Butterfly",
	"Women's 12 Yrs/Under 4x50m Medley",
	"Men's 12 Yrs/Under 4x50m Medley",
	"Women's Open 4x50m Free",
	"Men's Open 4x50m Free",
	"Women's 10 Yrs/Under 50m Backstroke",
	"Men's 10 Yrs/Under 50m Backstroke",
	"Women's 14 /Under 50m Breaststroke",
	"Men's 14 Yrs/Under 50m Breaststroke",
	"Women's 12 Yrs/Under 50m Freestyle",
	"Men's 12 Yrs/Under 50m Freestyle",
	"Women's Open 100m Butterfly",
	"Men's Open 100m Butterfly",
	"Cannon"
)

class EventLaneResult():
	# Constructor.  Pass in the results line from the gen file
	def __init__(self, gen_file_result_line):
		tokens = gen_file_result_line.split(';')
		if tokens[0] == 'Q':
			# DQ
			self.finish_position = -1
			self.points = 0
		elif tokens[0] == '0':
			# DNS
			self.finish_position = -2
			self.points = 0
		else:
			self.finish_position = int(tokens[0])
			self.points = 7 - self.finish_position
			times = []
			for i in range(1,len(tokens)):
				if len(tokens[i]) == 0:
					break
				times.append(float(tokens[i]))
			# Times contains all the splits followed by the final
			# approved race time.
			# So we can ignore the final split
			assert(len(times) > 0)
			num_splits = max(len(times)-1,1)
			# copy across all the splits before the finish time
			self.splits = []
			for i in range(num_splits-1):
				self.splits.append(times[i])
			# add the finish time
			self.finish_time = times[len(times)-1]
			self.splits.append(self.finish_time)

	def report(self, file, team, team_name):
		relay = ()
		result = ''
		show_splits = True
		if self.finish_position == -2:
			result = 'DNC'
			show_splits = False
		elif self.finish_position == -1:
			result = 'DQ'
			show_splits = False
		else:
			result = str(RaceTime(self.finish_time))
			show_splits = len(self.splits) > 1

		if len(team.legs) != 1:
			# Relay or DNS or DQ
			file.write('<tr class="team"><th colspan="3">{:}</th><td>{:}</td><td>{:}</td></tr>\n'.format(team_name, result, self.points))
			if show_splits:
				if len(team.legs) <= 4:
					# Also write out the swimmer names
					file.write('<tr class="splits">')
					for swimmer in team.legs:
						file.write('<td>{:}</td>'.format(swimmer.full_name))
					file.write('</tr>\n')
				file.write('<tr class="splits">')
				for split in self.splits:
					file.write('<td>{:}</td>'.format(str(RaceTime(split))))
				file.write('</tr>\n')
		else:
			# Individual
			file.write('<tr class="team"><th>{:}</th><td colspan="2">{:}</td><td>{:}</td><td>{:}</td></tr>\n'.format(team_name, team.legs[0].full_name, result, self.points))
			if show_splits:
				file.write('<tr class="splits">')
				for split in self.splits:
					file.write('<td>{:}</td>'.format(str(RaceTime(split))))
				file.write('</tr>\n')


class EventResult():
	# Constructor.  Pass in a results file
	def __init__(self, event_number, gen_file):
		self.event_number = event_number
		self.lane_results = []
		# Read and ignore the first line
		first_line = gen_file.readline()
		# Read the results for each lane
		for lane in range(teams.num_teams):
			team_name = teams.lane_order[lane]
			self.lane_results.append(EventLaneResult(gen_file.readline()))
			# Double points for the cannon
			if event_number == 51:
				self.lane_results[lane].points *= 2

	def report(self, file):
		file.write('<tr><th class="event" colspan="4">{:} - {:}</th><th class="points">Pts</th></tr>\n'.format(event_number, event_names[self.event_number]))
		for lane in range(teams.num_teams):
			team = teams.get_event_team(event_number, lane)
			team_name = teams.lane_order[lane]
			self.lane_results[lane].report(file, team, team_name)

results = {}

# Read the results '.gen' files
for event_number in range(1,52):
	gen_file_name = 'SST/001-{:03d}-01F{:04d}.gen'.format(event_number,event_number)
	try:
		gen_file = open(gen_file_name, 'r')
	except:
		# File does not exist
		print('File ' + gen_file_name + ' does not exist')
	else:
		# File exists
		print('Reading ' + gen_file_name)
		results[event_number] = EventResult(event_number, gen_file)


# Report
file_name = 'output/CW19mfsw.txt'
print('Writing {:}'.format(file_name))
file = open(file_name, 'w')
file.write(html_bookends.prologue)
file.write('<h2>Event Results</h2>\n')
file.write('<table>\n')
for event_number, result in results.items():
	#print('Results for ' + str(event_number))
	result.report(file)
file.write('</table>\n')

# Score totals
scores = [0]*teams.num_teams
for event_number, result in results.items():
	for lane in range(teams.num_teams):
		scores[lane] += result.lane_results[lane].points

file.write('<h2>Score Totals</h2>\n')
file.write('<table>\n')
for lane in range(teams.num_teams):
	file.write('<tr class="team"><th>{:}</th><th class="score">{:}</th></tr>\n'.format(teams.lane_order[lane], scores[lane]))
file.write('</table>\n')


file.write(html_bookends.epilogue)
