# Parses discography personnel list and outputs Gephi-formatted csv

import csv, codecs, json

name_input = input('Enter musician name, using regular case and spaces: ')
name = name_input.lower().replace(' ', '_')

discog = {}

with codecs.open('data/'+name+'_discog.json', encoding='utf-8') as filename:
	discog = json.load(filename)

	source_target_list = []
	node_list = []
	node_list_1 = []
	node_list_2 = []
	node_list_3 = []

	for session in discog:
		
		date = discog[session]['date']
		year = discog[session]['year']
		personnel = discog[session]['personnel']
		persons = []
		record_label = discog[session]['label']
		location = discog[session]['location']
		songs = discog[session]['songs']

		for person in personnel:

			persons.append(person)

			if personnel[person][0] == 'Congas':
				instr = 'Percussion'
			elif personnel[person][0] == 'Flügelhorn':
				instr = 'Trumpet'
			elif personnel[person][0] == 'Electric Bass':
				instr = 'Bass'
			elif personnel[person][0] == 'Violoncello':
				instr = 'Cello'
			else:
				instr = personnel[person][0]

			if int(year) > 1950 and int(year) < 1970:
				year_range = '1950s-1960s'
				if [person, instr, year_range] not in node_list_1:
					node_list_1.append([person, instr, year_range])
			elif int(year) > 1969 and int(year) < 1990:
				year_range = '1970s-1980s'
				if [person, instr, year_range] not in node_list_2:
					node_list_2.append([person, instr, year_range])
			elif int(year) > 1989:
				year_range = '1990s-2000s'
				if [person, instr, year_range] not in node_list_3:
					node_list_3.append([person, instr, year_range])


			if [person, instr, year_range] not in node_list:
				node_list.append([person, instr, year_range])

			if date != '' and location != '':
				gephi_label = date+', '+location
			elif date != '':
				gephi_label = date
			elif location != '':
				gephi_label = location

		if name_input in persons:

			for x in persons:

				for y in persons:

					if x.strip() != y.strip():

						if [y.strip(), x.strip(), 'undirected', gephi_label] not in source_target_list:

							source_target_list.append([x.strip(), y.strip(), 'undirected', gephi_label])


with open('data/'+name+'_discog_gephi_edge.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['source', 'target', 'type', 'label'])
	for a_pair in source_target_list:
		w.writerow(a_pair)

	csv_out.close()

with open('data/'+name+'_discog_gephi_node.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['id', 'instrument', 'year'])
	for a_node in node_list:
		w.writerow(a_node)

	csv_out.close()

with open('data/'+name+'_discog_gephi_node_1950s-60s.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['id', 'instrument', 'year'])
	for a_node in node_list_1:
		w.writerow(a_node)

	csv_out.close()

with open('data/'+name+'_discog_gephi_node_1970s-80s.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['id', 'instrument', 'year'])
	for a_node in node_list_2:
		w.writerow(a_node)

	csv_out.close()

with open('data/'+name+'_discog_gephi_node_1990s-2000s.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['id', 'instrument', 'year'])
	for a_node in node_list_3:
		w.writerow(a_node)

	csv_out.close()


print ("All done! Your file for", name_input, "is ready.")