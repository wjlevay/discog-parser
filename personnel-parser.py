# Parses discography personnel list and outputs Gephi-formatted csv
# note: regex to find (instr) is \(.+?\)

import csv, re

name_input = input('Enter musician name, using regular case and spaces: ')
name = name_input.lower().replace(' ', '_')

### FIX THIS ###
# load the json file instead of the csv, so that we can specify the key-value pairs

with open('data/'+name+'_discog.csv', newline='', encoding='utf-8') as csv_in:

	source_target_list = []

	#dumps the file into the cvs library with some info on how it is formatted
	discog = csv.reader(csv_in, delimiter=',')

	for row in discog:
		
		date = row[2]
		personnel = row[3]
		#label = row[1]
		location = row[0]

		pattern = re.compile(' \(.+?\)')
		person = pattern.sub('', person.strip().split(', ')
		persons.append(person)

		if date != '' and location != '':
			label = date+', '+location
		elif date != '':
			label = date
		elif location != '':
			label = location

		#print(label)

		if name_input in persons:

			for x in persons:

				for y in persons:

					if x.strip() != y.strip():

						if [y.strip(), x.strip(), 'undirected', label] not in source_target_list:

							source_target_list.append([x.strip(), y.strip(), 'undirected', label])

	#print (source_target_list)

with open('data/'+name+'_discog_gephi.csv', 'w', newline='', encoding='utf8') as csv_out:
	w = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
	w.writerow(['source', 'target', 'type', 'label'])
	for a_pair in source_target_list:
		w.writerow(a_pair)

	csv_out.close()

print ("All done! Your file for", name_input, "is ready.")