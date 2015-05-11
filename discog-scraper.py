### Discog Scraper

from bs4 import BeautifulSoup
import json, csv, codecs, re

name_input = input('Enter musician name, using regular case and spaces: ')
name = name_input.lower().replace(' ', '_')

discog = {}

# set session ID
session_id = 1

# open the html file and read as text
discog_page = open('data/'+name+'_discog-page.html')
discog_html = discog_page.read()

# split the text on the <hr>
fragment_list = discog_html.split('<hr style="clear:both;"  />')

# for each fragment of html, convert to a soup object
for fragment in fragment_list:
	fragment_soup = BeautifulSoup(fragment)

	# empty sub-dict
	session = {}
	session['date'] = ''
	session['year'] = ''
	session['location'] = ''
	session['label'] = ''
	session['personnel'] = ''
	session['ensemble_size'] = ''

	# find all the spans in the session header
	session_spans = fragment_soup.find_all('span', class_= 'rptLabel')

	# loop through the spans and parse
	for a_session_span in session_spans:

		for a_session_head_element in a_session_span:

			if a_session_head_element.string == 'Date: ':
				session['date'] = a_session_head_element.next_element

				# find year in date '(19|20)\d{2}$'
				find_year = re.compile('(19|20)\d{2}$')
				year_match = re.search(find_year, session['date'])
				session['year'] = year_match.group(0)

			if a_session_head_element.string == 'Location: ':
				session['location'] = a_session_head_element.next_element

			if a_session_head_element.string == 'Label: ':
				session['label'] = a_session_head_element.next_element

	# now let's find the personnel
	session_personnel = fragment_soup.find('p', class_='SessCollPers')
	personnel = []


	# check for NoneType, then find the personnel, excluding the (ldr), which is wrapped in a <b> tag
	# remove the comma-space separator, and strip any whitespace
	if session_personnel is not None:
		if session_personnel.next_element.name == 'b':
			personnel_string = session_personnel.next_element.next_element.next_element.lstrip(', ').strip()
		else:
			personnel_string = session_personnel.next_element.lstrip(', ').strip()

		personnel = re.split('(.+? \(.+?\)), ', personnel_string)

		# personnel = re.split('(, )[A-Z]', personnel_string)

		personnel_clean = []

		#cleanup on personnel list
		for person in personnel:
			if person is not '':
				personnel_clean.append(person)


		#if there is more than one person on an instrument, find the instrument, split the people and append the instrument

		#pattern for more than one person on same instrument
		find_group = re.compile(', [A-Z]')

		#pattern for instrument in parentheses
		find_ax = re.compile('\(.+?\)')

		personnel_subdict = {}

		for person in personnel_clean:
			group = re.search(find_group, person)
			ax_match = find_ax.search(person)

			#the instrument string, with parentheses
			ax = ax_match.group(0)
		
			#are we dealing with a group of people on the same instrument? 
			#clean up the person name and add the instrument to each person
			if group:
				#if group, split names into a list
				sub_list = person.split(', ')
				for x in sub_list:
					#pull out the instrument from the list
					if ax in x:
						x = find_ax.sub('', x)
					#then, clean up the instrument abbreviation and split the instruments into a list
					personnel_subdict[x.strip()] = ax.strip('()').split(', ')

			#otherwise, we have one person with one or more instruments
			else:
				person = find_ax.sub('', person)
				personnel_subdict[person.strip()] = ax.strip('()').split(', ')
			


		#write to the subdict
		session['personnel'] = personnel_subdict
		session['ensemble_size'] = len(personnel_subdict)


	# let's get some songs!
	session_songs = fragment_soup.find_all('span', class_='PerfTitle')
	songs = {}
	for session_song in session_songs:
		song = {}
		if session_song.string is not None:
			song['title'] = session_song.string

			siblings = session_song.next_siblings
			for sibling in siblings:

				if sibling.string is not None:
					if ':' in sibling.string and '-' in sibling.string:
						song['timing'] = sibling.string.lstrip(' - ').strip()
					if '(' in sibling.string and ':' not in sibling.string:
						song['composer'] = sibling.string.strip().lstrip('(').rstrip(')').strip()
					if 'arr:' in sibling.string:
						song['arranger'] = sibling.string.strip().lstrip('/ arr: ').strip()


			song_num = session_song.parent.parent.find('i').string.replace('.', '')
			songs[song_num] = song

	session['songs'] = songs
	session['song_count'] = len(songs)

	# need to add the composers & arrangers

	# grab the exceptions
	session_excepts = fragment_soup.find('p', class_='SessPersExcp')
	# this is a NavigableString, so use get_text instead of string
	if session_excepts is not None:
		session['exceptions'] = session_excepts.get_text().replace('  ', ' ')

	# grab the notes
	session_notes = fragment_soup.find('p', class_='SessRptNotes')
	if session_notes is not None:
		if session_notes.string is not None:
			session['notes'] = session_notes.string

	#open the instrument name look-up dictionary and replace abbreviations with full instrument names
	#comment out this section if you want to keep instrument abbreviations
	with codecs.open('data/instruments.json', encoding='utf-8') as filename:
		instruments = json.load(filename)

		for person in session['personnel']:
			instrument_list = []
			for instr in session['personnel'][person]:
				instrument = instruments[instr]
				instrument_list.append(instrument)
			session['personnel'][person] = instrument_list

	#close the instruments file
	filename.close

	# check if we actually have data in the sub dict
	if session['date'] == '' and session['location'] == '' and session['personnel'] == '':
		pass
	# write to the main dict
	else:
		discog[session_id] = session
		session_id += 1

#print (discog)

# with open('data/'+name+'_discog.csv', 'w', newline='', encoding='utf8') as csv_out:

# 	for a_session in discog:
# 		fieldnames = discog[a_session].keys()
# 		w = csv.DictWriter(csv_out, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL)
		
# 		#only write the headers the first time
# 		if a_session == 1:
# 			w.writeheader()
		
# 		w.writerow(discog[a_session])

# 	csv_out.close()

with codecs.open('data/'+name+'_discog.json', 'w', encoding='utf-8') as json_out:

	#write the updated dictionary to json
	dump = json.dumps(discog, sort_keys=True, indent=4)
	json_out.write(dump)

#close the file
json_out.close

print ("All done! Your files for", name_input, "are ready.")

