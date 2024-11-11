# This script extracts and transforms data from the JSON output of the radio browser project (see the readme)
# All of it's output is written to the output subdirectory

import json


def clean_url(url):
  return url.replace(";","")


def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text



def read_stations():
  with open('input/stations.json', encoding='utf-8') as stations_file:
    stations = json.load(stations_file)
  stations= [s for s in stations if ((s['lastcheckok'] == 1) and (s['codec'] == 'MP3'))]
  return stations

def parse_countries(stations):
  countries = ([(s['countrycode'].upper(), s['country']) for s in stations])
  countries = sorted(list(set(countries)))
  return countries

def generate_filename(country_code, country_name):
  filename = "_unknown"
  if (len(country_code) > 0):
    filename = country_code + " " + country_name
  return filename

def create_countries_csv_file(countries):
  with open('output/countries.csv', 'w', encoding='utf-8') as countries_file:
    for country in countries:
      countries_file.write("\"" + country[0] + "\",\"" + country[1] + "\"\n")

def create_countries_txt_file(countries):
  with open('output/countries.txt', 'w', encoding='utf-8') as countries_file:
    for country in countries:
      countries_file.write(country[0] + " " + country[1] + "\n")



def create_m3u_file(country_code, country_name, stations):
  with open('output/m3u/' + generate_filename(country_code,country_name) + '.m3u', 'w', encoding='utf-8') as output_file:
    output_file.write("#EXTM3U\n")
    output_file.write("#PLAYLIST:Internet Radio Stations for " + country_code + " " + country_name + "\n")
    last_name = ""
    for s in stations:
      if ((s['name'] != last_name) and s['lastcheckok'] == 1) and (s['countrycode'].upper() == country_code) and (s['codec'] == 'MP3'):
        output_file.write("#EXTINF:-1 " + s['name'] + '\n')
        output_file.write(clean_url(s['url']) + '\n')
      last_name = s['name']


def create_pls_file(country_code, country_name, stations):
  with open('output/pls/' + generate_filename(country_code,country_name) + '.pls', 'w', encoding='utf-8') as output_file:
    output_file.write("[playlist]\n")
    i = 0
    last_name = ""
    for s in stations:
      if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == country_code) and (s['codec'] == 'MP3'):
        i+=1
        output_file.write("File" + str(i) + "=" + clean_url(s['url']) + '\n')
        output_file.write("Title" + str(i) + "=" + s['name'] + '\n')
      last_name = s['name']
    output_file.write("NumberOfEntries=" + str(i))


def create_opml_file(country_code, country_name, stations):
  with open('output/opml/' + generate_filename(country_code,country_name) + '.opml', 'w', encoding='utf-8') as opml_file:
    opml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    opml_file.write("<opml version=\"1.0\">\n")
    opml_file.write("<head>\n<title>Internet Radio Stations for " + country_code + " " + country_name + "</title>\n</head>\n<body>\n")
    last_name = ""
    for s in stations:
      if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == country[0]) and (s['codec'] == 'MP3'):
        opml_file.write("<outline text=\"" + encodeXMLText(s['name']) + "\" title=\"" + encodeXMLText(s['name']) + "\" type=\"rss\" url=\"" + encodeXMLText(clean_url(s['url'])) + "\" />\n")
        last_name = s['name']
    opml_file.write("</body>\n</opml>\n")

def create_csv_file(country_code, country_name, stations):
  with open('output/csv/' + generate_filename(country_code,country_name) + '.csv', 'w', encoding='utf-8') as csv_file:
    csv_file.write("\"Name\",\"URL\"\n")
    last_name = ""
    for s in stations:
      if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == country[0]) and (s['codec'] == 'MP3'):
        csv_file.write("\"" + s['name'].replace("\"","\"\"") + "\",\"" + clean_url(s['url']) + "\"\n")
        last_name = s['name']


def create_html_file(countries, stations):
  with open('output/internet_radio_stations.htm', 'w', encoding='utf-8') as html_file:
    html_file.write("<html>\n<head>\n<title>Internet Radio Stations</title>\n</head>\n")
    html_file.write("<body>\n")
    html_file.write("<h1>Internet Radio Stations</h1>")
    html_file.write("<h2>Countries</h2>")
    html_file.write("<ul>\n")
    for country in countries:
      if (len(country[0]) > 0):
        html_file.write("<li><a href='#" + country[0] + "'>" + country[0] + " " + country[1] + "</a></li>\n")
      else:
        html_file.write("<li><a href='#" + country[0] + "'>Unspecified</a></li>\n")
    html_file.write("</ul>\n")
    html_file.write("<hr />\n")
    html_file.write("<h2>Radio Stations by Country</h2>\n")
    for country in countries:
      if (len(country[0]) > 0):
        html_file.write("<h3><a name='" + country[0] + "'>" + country[0] + " " + country[1] + "</a></h3>")
      else:
        html_file.write("<h3><a name='unspecified'>Unspecified</a></h3>")
      html_file.write("<ul>\n")
      last_name = ""
      for s in stations:
        if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == country[0]) and (s['codec'] == 'MP3'):
          html_file.write("<li><a href='" + clean_url(s['url']) + "'>" + s['name'] + "</a></li>")
        last_name = s['name']
      html_file.write("</ul>\n")
    html_file.write("</body>\n</html>\n")

def create_csv_file_all(countries, stations):
  with open('output/internet_radio_stations.csv', 'w', encoding='utf-8') as csv_file:
    csv_file.write("\"Name\",\"URL\",\"Country\"\n")
    for country in countries:
      last_name = ""
      for s in stations:
        if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == country[0]) and (s['codec'] == 'MP3'):
          csv_file.write("\"" + s['name'].replace("\"","\"\"") + "\",\"" + clean_url(s['url']) + "\",\"" + s['country'].replace("\"","\"\"") + "\"\n")
        last_name = s['name']


print("Reading stations...")
stations = read_stations()
print(" - " + str(len(stations)) + " stations found")

print("Parsing Countries...")
countries = parse_countries(stations)

print("Creating CSV file...")
create_countries_csv_file(countries)

print("Creating TXT file...")
create_countries_txt_file(countries)

print("Creating HTML file...")
create_html_file(countries, stations)

print("Creating mu3, pls and opml files for each country...")
for country in countries:
  print(" - " + country[0])
  create_m3u_file(country[0], country[1], stations)
  create_pls_file(country[0], country[1], stations)
  create_opml_file(country[0], country[1], stations)
  create_csv_file(country[0], country[1], stations)
  

print("Creating CSV file of all stations")
create_csv_file_all(countries,stations)