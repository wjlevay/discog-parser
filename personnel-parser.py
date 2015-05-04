# Parses discography personnel list and outputs Gephi-formatted csv

import csv, codecs, json

name_input = input('Enter musician name, using regular case and spaces: ')
name = name_input.lower().replace(' ', '_')

discog = {}

with codecs.open('data/'+name+'_discog.json', encoding='utf-8') as filename:
	discog = json.load(filename)

	source_target_list = []

	for session in discog:
		
		date = discog[session]['date']
		personnel = discog[session]['personnel']
		persons = []
		record_label = discog[session]['label']
		location = discog[session]['location']
		songs = discog[session]['songs']

		for person in personnel:

			persons.append(person)

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


with open('data/'+name+'_discog_gephi.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['source', 'target', 'type', 'label'])
	for a_pair in source_target_list:
		w.writerow(a_pair)

	csv_out.close()

print ("All done! Your file for", name_input, "is ready.")