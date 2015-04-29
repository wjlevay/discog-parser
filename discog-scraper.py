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
	session['location'] = ''
	session['label'] = ''
	session['personnel'] = ''

	# find all the spans in the session header
	session_spans = fragment_soup.find_all('span', class_= 'rptLabel')

	# loop through the spans and parse
	for a_session_span in session_spans:

		for a_session_head_element in a_session_span:

			if a_session_head_element.string == 'Date: ':
				session['date'] = a_session_head_element.next_element

			if a_session_head_element.string == 'Location: ':
				session['location'] = a_session_head_element.next_element

			if a_session_head_element.string == 'Label: ':
				session['label'] = a_session_head_element.next_element

	# now let's find the personnel
	session_personnel = fragment_soup.find('p', class_='SessCollPers')
	personnel = []

	########### NEED TO FIX THIS ################
	# below method fails when personnel is listed: Abbey, Bobby, Carlos (v), indicating same instrument for all three performers
	# must add logic that says: if ', ' not directly preceded by '(x)', then find next ' (x)' and append to name

	# check for NoneType, then find the personnel, excluding the (ldr), which is wrapped in a <b> tag
	# remove the comma-space separator, and strip any whitespace
	if session_personnel is not None:
		if session_personnel.next_element.name == 'b':
			personnel_string = session_personnel.next_element.next_element.next_element.replace(', ', '').strip()
		else:
			personnel_string = session_personnel.next_element.replace(', ', '').strip()

		# find the personnel-instrumentation combo and make a list
		personnel = re.findall('(.+? \(.+?\))', personnel_string)

		#write to the subdict
		session['personnel'] = personnel

	# let's get some songs!
	session_songs = fragment_soup.find_all('span', class_='PerfTitle')
	songs = []
	for session_song in session_songs:
		if session_song.string is not None:
			if session_song.string not in songs:
				songs.append(session_song.string)

	session['songs'] = songs

	# need to add the composers & arrangers

	# grab the notes





	# check if we actually have data in the sub dict
	if session['date'] == '' and session['location'] == '' and session['personnel'] == '':
		pass
	# write to the main dict
	else:
		discog[session_id] = session
		session_id += 1

#print (discog)

with open('data/'+name+'_discog.csv', 'w', newline='', encoding='utf8') as csv_out:

	for a_session in discog:
		fieldnames = discog[a_session].keys()
		w = csv.DictWriter(csv_out, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_ALL)
		
		#only write the headers the first time
		if a_session == 1:
			w.writeheader()
		
		w.writerow(discog[a_session])

	csv_out.close()

with codecs.open('data/'+name+'_discog.json', 'w', encoding='utf-8') as json_out:

	#write the updated dictionary to json
	dump = json.dumps(discog, sort_keys=True, indent=4)
	json_out.write(dump)

#close the file
json_out.close

print ("All done! Your files for", name_input, "are ready.")