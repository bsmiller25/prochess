from django.core.management.base import BaseCommand, CommandError
from pcl.models import Division, Team
from django.conf import settings

import pandas as pd
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    help = 'Loads Teams'
    def handle(self, *args, **options):
        url = 'https://www.prochessleague.com/teams.html'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        all_teams = pd.read_html(str(soup.findAll("table")[0]), header=0)[0]
        
        divisions = Division.objects.all()
        for div in divisions:
            print('Loading teams for {} Division'.format(div.name))
            try:
                teams = all_teams['{} Division'.format(div.name)]
            except KeyError:
                teams = all_teams['{} Divison'.format(div.name)]

            for team in teams:
                print('Loading {}'.format(team))
                t = {'name': team,
                     'division': div,
                     }
                Team.objects.update_or_create(name=t['name'],
                                              defaults=t)
