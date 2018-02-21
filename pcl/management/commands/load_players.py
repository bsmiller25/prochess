from django.core.management.base import BaseCommand, CommandError
from pcl.models import Division, Team, Player
from django.conf import settings

import pandas as pd
import numpy as np


class Command(BaseCommand):
    help = 'Loads Teams'
    def handle(self, *args, **options):
        

        teams = Team.objects.all()
        for team in teams:
            print('Loading team: {}'.format(team.name))
            name = "-".join(team.name.lower().split(' '))
            name = name.replace('st-','saint-')
            url = 'https://www.prochessleague.com/{}.html'.format(name)

            try:
                roster = pd.read_html(url, header=0)[1]
                roster = roster.replace('-', roster.replace(['-'], [None]))
                
                for index, row in roster.iterrows():
                    print('Loading player: {}'.format(row['Name']))
                    p = {'name': row['Name'],
                         'team': team,
                         'rating': row['Rating'],
                         'perf': row['Perf']
                    }
                    Player.objects.update_or_create(name=p['name'],
                                                    defaults=p)
            except KeyError:
                roster = pd.read_html(url, header=1)[1]
                roster = roster.replace('-', roster.replace(['-'], [None]))
                
                for index, row in roster.iterrows():
                    print('Loading player: {}'.format(row['Name']))
                    p = {'name': row['Name'],
                         'team': team,
                         'rating': row['Rating'],
                         'perf': row['Perf']
                    }
                    Player.objects.update_or_create(name=p['name'],
                                                    defaults=p)
