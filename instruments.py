from bs4 import BeautifulSoup
import json, codecs

instruments = {}

# open the html file and read as text
instrument_page = open('data/instruments.html')
instrument_html = instrument_page.read()

instrument_soup = BeautifulSoup(instrument_html)

instrument_rows = instrument_soup.find_all('tr')

for row in instrument_rows:

	row_element = row.find_all('td')

	abbr = row_element[0].string.strip()
	instr = row_element[1].string.strip()

	instruments[abbr] = instr

with codecs.open('data/instruments.json', 'w', encoding='utf-8') as json_out:

	#write the updated dictionary to json
	dump = json.dumps(instruments, sort_keys=True, indent=4)
	json_out.write(dump)

#close the file
json_out.close

print ("All done! Your instrument file is ready.")