import teams

teams.read_team_files()

# Write the scb files
for event_number in range(1,52):
	scb_file_name = 'SST/E{:03d}.scb'.format(event_number)
	print('Writing {:}'.format(scb_file_name))
	file = open(scb_file_name, 'w')
	file.write('#{:d}\n'.format(event_number))

	for lane in range(10): # scb files always have 10 lanes per heat
		swimmer = ''
		team_name = ''
		if lane < teams.num_teams:
			team = teams.get_event_team(event_number, lane)
			team_name = teams.lane_order[lane]
			if len(team.legs) > 1:
				# Relay. Use team name.
				swimmer = team_name
			else:
				swimmer = team.legs[0]
		file.write('{:20.20}--{:16.16}\n'.format(swimmer, team_name))
