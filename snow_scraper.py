import requests
from bs4 import BeautifulSoup
import io
from datetime import date, timedelta, datetime

#configs
export_path = '/home/gregory/PycharmProjects/snow_scraper/historical_snow_reports/'

region_resort_dict = {}
region_resort_dict['colorado'] = ['vail', 'beaver-creek', 'breckenridge', 'arapahoe-basin-ski-area', 'keystone']
region_resort_dict['california'] = ['heavenly-mountain-resort', 'kirkwood', 'northstar-california']
region_resort_dict['utah'] = ['park-city-mountain-resort']
region_resort_dict['british-columbia'] = ['whistler-blackcomb']
region_resort_dict['northern-alps'] = ['courchevel', 'les-arcs-bourg-st-maurice', 'tignes']
region_resort_dict['vorarlberg'] = ['lech-zuers-am-arlberg']
region_resort_dict['valais'] = ['verbier']
region_resort_dict['trentino'] = ['madonna-di-campiglio']

list_view_type = 'list#view'

years = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009']

historical_snowfall_url_template = 'http://www.onthesnow.com/<region>/<resort>/historical-snowfall.html?y=<year>&v=<view>'

class ResortSnowFallEntry:
    resort = None
    yearly_entries = {}

    def __init__(self, resort):
        self.resort = resort

    def add_annual_entry(self, annual_entry):
        self.yearly_entries[annual_entry.year] = annual_entry

    def resort_report(self):
        output = io.StringIO()
        #i picked 2016 to ensure we include leap day
        d1 = date(2016,1,1)
        d2 = date(2016,12,31)
        diff = d2 - d1
        days = [d1 + timedelta(x) for x in range(diff.days + 1)]

        #header
        output.write(self.resort+',')
        for day in days:
            output.write(day.strftime('%b %d') + ',')
        output.write('\n')

        for year, entries in sorted(self.yearly_entries.items()):
            output.write(year + ',')
            for day in days:
                try:
                    the_date = date(int(year), day.month, day.day)
                except:
                    #this is what happens when you try to create a leap day for a non leap year
                    output.write('n/a,')
                    continue
                if the_date in entries.daily_entries:
                    output.write(entries.daily_entries[the_date].new_snowfall_in_inches.replace('in.','') + ',')
                elif the_date > date.today():
                    output.write('n/a,')
                else:
                    output.write('0,')
            output.write('\n')

        return output.getvalue()

class AnnualSnowFallEntry:
    year = None
    daily_entries = {}

    def __init__(self, year):
        self.year = year

    def add_daily_entry(self, daily_entry):
        self.daily_entries[daily_entry.date] = daily_entry

class DailySnowFallEntry:
    date = None
    new_snowfall_in_inches = None
    season_total_snowfall = None
    base_depth = None

    def __init__(self, html_row):
        #probably should refer to the headers for this
        self.date = datetime.strptime(html_row[0].string, '%b %d, %Y').date()
        self.new_snowfall_in_inches = html_row[1].string
        self.season_total_snowfall = html_row[2].string
        self.base_depth = html_row[3].string


def build_url(url_template, resort, region, view_type, year):
    url = url_template.replace('<resort>',resort)
    url = url.replace('<region>', region)
    url = url.replace('<year>', year)
    url = url.replace('<view>',view_type)
    return url

def main():
    for region, resorts in region_resort_dict.items():
        for resort in resorts:
            resort_entry = ResortSnowFallEntry(resort)
            for year in years:
                year_entry = AnnualSnowFallEntry(year)


                r = requests.get(build_url(historical_snowfall_url_template,resort,region,list_view_type,year))
                soup = BeautifulSoup(r.text, 'html.parser')

                for each in soup.find_all('tr'):
                    if each is not None:
                        row = each.find_all('td')
                        if row != []:
                            year_entry.add_daily_entry(DailySnowFallEntry(row))

                resort_entry.add_annual_entry(year_entry)

            f = open(export_path + resort + '.txt', 'w')
            f.write(resort_entry.resort_report())
            f.close()

if __name__ == "__main__":
    main()