#! /usr/bin/env python
import sys
import argparse
from weather import Weather

class WeatherReport:
    def __init__(self, location):
        self.get_report(location)   

    def get_report(self, location): 
        self.show_location(location)
        [self.show_weather(day) for day in self.get_days(self.locate(location))]

    def locate(self, location):
        return Weather().lookup_by_location(location)

    def get_days(self, place):
        days = []
        [self.get_day(days, item['date'], item['low'], item['high'], item['text']) for item in place.forecast()]
        return days

    def get_day(self, days, date, low, high, text): 
        days.append([date, self.get_celsius(low), self.get_celsius(high), text])

    def get_celsius(self, temperature):
        return (int(temperature) - 32) * 5.0/9.0

    def show_weather(self, day):
        from_to = "%d-%d" % (day[1], day[2])
        print " "*2 + "%s:" % (day[0]), from_to.rjust(5) + u'\u00b0' + "C -", "%s" % (day[3])

    def show_location(self, location):
        print "-" * 50
        feedback = "10-day forecast for " + location.capitalize()
        print feedback.center(50)
        print "-" * 50


if __name__ == "__main__":
    parser = argparse.ArgumentParser('tdwreport')
    parser.add_argument('-l', '--location', default="sarajevo", help='get forecast for this location')
    args = parser.parse_args()
    report = WeatherReport(args.location)