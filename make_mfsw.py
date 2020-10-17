import teams
from operator import itemgetter    

teams.read_team_files()

file_name = 'output/CW19mfsw.txt'
print('Writing {:}'.format(file_name))
file = open(file_name, 'w')
for team_idx in range(teams.num_teams):
	team = teams.lane_order[team_idx]
	team_swimmers = teams.swimmers_per_team[team_idx]
	sorted_swimmers = sorted(team_swimmers.items(), key = itemgetter(0))
	for swimmer, stats in sorted_swimmers:
		file.write('{:},{:},{:}/{:}/{:},{:},{:}\n'.format(swimmer.last_name, swimmer.first_name, swimmer.dob.year, swimmer.dob.month, swimmer.dob.day, team, swimmer.sex))
