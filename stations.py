import json

print("Reading Stations File")

def clean_url(url):
  return url.replace(";","")

def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def get_countries(stations):
  countries = ([(s['countrycode'].upper(), s['country']) for s in stations])
  countries = sorted(list(set(countries)))
  return countries

def create_countries_csv_file(countries):
  print("Creating Countries CSV file")
  with open('output/countries.csv', 'w', encoding='utf-8') as countries_file:
    for country in countries:
      countries_file.write("\"" + country[0] + "\",\"" + country[1] + "\"\n")

def create_countries_txt_file(countries):
  print("Creating Countries TXT file")
  with open('output/countries.txt', 'w', encoding='utf-8') as countries_file:
    for country in countries:
      countries_file.write(country[0] + " " + country[1] + "\n")

def create_m3u_file(countrycode, stations):
  print("Creating M3U file for " + countrycode)
  with open('output/m3u/radio_stations_' + countrycode + '.m3u', 'w', encoding='utf-8') as output_file:
    output_file.write("#EXTM3U\n")
    output_file.write("#PLAYLIST:Internet Radio Stations\n")
    last_name = ""
    for s in stations:
        if ((s['name'] != last_name) and s['lastcheckok'] == 1) and (s['countrycode'].upper() == countrycode) and (s['codec'] == 'MP3'):
          output_file.write("#EXTINF:-1 " + s['name'] + '\n')
          output_file.write(clean_url(s['url']) + '\n')
        last_name = s['name']


def create_pls_file(countrycode, stations):

  print("Creating PLS file for " + countrycode)

  with open('output/pls/radio_stations_' + countrycode + '.pls', 'w', encoding='utf-8') as output_file:
    output_file.write("[playlist]\n")
    i = 0
    last_name = ""
    for s in stations:
      if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == countrycode) and (s['codec'] == 'MP3'):
        i+=1
        output_file.write("File" + str(i) + "=" + clean_url(s['url']) + '\n')
        output_file.write("Title" + str(i) + "=" + s['name'] + '\n')
      last_name = s['name']
    output_file.write("NumberOfEntries=" + str(i))


def create_opml_file(countries, stations):
  
  print("Creating OPML file")

  with open('output/internet_radio_stations.opml', 'w', encoding='utf-8') as opml_file:

    opml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    opml_file.write("<opml version=\"1.0\">\n")
    opml_file.write("<head>\n<title>Internet Radio Stations</title>\n</head>\n<body>\n")
    
    for country in countries:

      opml_file.write("<outline title=\"" + encodeXMLText(country[1]) + "\" text=\"" + encodeXMLText(country[1]) + "\">\n")
      last_name = ""
      
      for s in stations:

        if (s['name'] != last_name) and (s['lastcheckok'] == 1) and (s['countrycode'].upper() == country[0]) and (s['codec'] == 'MP3'):
          opml_file.write("<outline text=\"" + encodeXMLText(s['name']) + "\" title=\"" + encodeXMLText(s['name']) + "\" type=\"audio\" url=\"" + encodeXMLText(clean_url(s['url'])) + "\" />\n")
        last_name = s['name']

      opml_file.write("</outline>\n")

    opml_file.write("</body>\n</opml>\n")


def create_html_file(countries, stations):

  print("Creating HTML file")
  
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



with open('input/stations.json', encoding='utf-8') as stations_file:
  stations = json.load(stations_file)

  countries = get_countries(stations)

  create_countries_csv_file(countries)
  create_countries_txt_file(countries)

  create_html_file(countries, stations)
  create_opml_file(countries, stations)

  for country in countries:
    create_m3u_file(country[0], stations)
    create_pls_file(country[0], stations)

