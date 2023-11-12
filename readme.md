# Internet Radio Stations M3U and PLS Creator

The contained script takes the JSON output of the "Radio Browser" project (https://www.radio-browser.info/) and turns it into a country-coded collection of M3U and PLS formatted files for import into retro applications such as WinAmp.

The JSON file can be sourced from a call to one of the Radio Browser servers - such as the one below:
http://de1.api.radio-browser.info/json/stations

The script creates a CSV and TXT file of country codes, and a M3U and PLS file for each country code with the MP3 radio stations in that country. Look in the /output/m3u and /output/pls directories for the files!

The included M3U and PLS files (zipped) were generated on 2023-11-12.

I wrote this for my own purposes - feel free to modify!
