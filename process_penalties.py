import teams
import html_bookends
from operator import itemgetter    

teams.read_team_files()

# Report
file_name = 'output/penalties.html'
print('Writing {:}'.format(file_name))
file = open(file_name, 'w')
file.write(html_bookends.prologue)
file.write('<h2>Penalties Report</h2>\n')

total_penalties_per_team = [0,0,0,0]

def write_event_list(file, heading, events, penalty_threshold):
	if len(events) > 0:
		file.write('<tr><td>{:}</td><td class="event_number">'.format(heading))
		class_name = 'event_number'
		count = 0
		separator = ''
		for event in events:
			file.write('{:}E{:d}'.format(separator, event.event_number))
			separator = ', '
			count = count + 1
			if count == penalty_threshold:
				file.write('<em>')
		if count >= penalty_threshold:
			file.write('</em>')
		file.write('</td></tr>\n')

for team_idx in range(teams.num_teams):
	team_swimmers = teams.swimmers_per_team[team_idx]
	sorted_swimmers = sorted(team_swimmers.items(), key = itemgetter(0))
	file.write('<h3>{:}</h3>\n'.format(teams.lane_order[team_idx]))
	file.write('<table>\n')
	for swimmer, stats in sorted_swimmers:
		file.write('<tr><th colspan="2">{:}</th>\n'.format(swimmer.full_name))
		write_event_list(file, 'Individual events', stats.individual_events, 4)
		write_event_list(file, 'Relays', stats.relays, 99)
		write_event_list(file, 'Individual swim-ups', stats.individual_swim_up_events, 1)
	file.write('</table>\n')

file.write(html_bookends.epilogue)
