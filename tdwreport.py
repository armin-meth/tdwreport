#! /usr/bin/env python
import argparse
import requests
from weather import Weather
from weather import models

class WeatherReport(Weather):
    def __init__(self, location):
        Weather.__init__(self)
        self.get_report(location)   

    def get_report(self, location): 
        self.show_location(location)
        [self.show_weather(day) for day in self.get_days(self.lookup_by_location(location))]

    def lookup_by_location(self, location):
        url = "%s?q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='%s') and u='c' &format=json" % (self.URL, location)
        results = self._call(url)
        return results

    def get_days(self, place):
        days = []
        [self.get_day(days, item['date'], item['low'], item['high'], item['text']) for item in place.forecast()]
        return days

    def get_day(self, days, date, low, high, text):
        days.append([date, int(low), int(high), text])

    def show_weather(self, day):
        from_to = "%d-%d" % (day[1], day[2])
        print " "*2 + "%s:" % (day[0]), from_to.rjust(5) + u'\u00b0' + "C -", "%s" % (day[3])

    def show_location(self, location):
        print "-" * 50
        feedback = "10-day forecast for " + location.capitalize()
        print feedback.center(50)
        print "-" * 50

    def _call(self, url):
        results = requests.get(url).json()
        if int(results['query']['count']) > 0:
            wo = models.weather_obj.WeatherObject(results['query']['results']['channel'])
            return wo
        else:
            print 'No results found.'
            quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser('tdwreport')
    parser.add_argument('-l', '--location', default="sarajevo", help='get forecast for this location')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    report = WeatherReport(args.location)
