import requests
from bs4 import BeautifulSoup
import re
from random import random
import operator

from django.shortcuts import render
from django.http import HttpResponse
from pcl.models import *


# Create your views here.

def index(request):
    return HttpResponse("Welcome")

def matchup(request):

    # load current matchups and players
    response = requests.get('https://www.prochessleague.com/pairings.html')
    soup = BeautifulSoup(response.text, "lxml")
    
    matchupjson = soup.find_all('script')[13].getText()
    start = matchupjson.find('inputData')
    end = matchupjson.find('Component')
    mjson = matchupjson[start:end]
    
    players = []
    matchups = []
    for i in list(range(8 * 4 * 4 * 4)):
        # get teams and matchups
        team_start = mjson.find('surname') + 13
        team_end = mjson.find('img') - 13
        team2_start = mjson.find('surname2') + 14
        team2_end = mjson.find('img2') - 13
        team = mjson[team_start:team_end]
        team2 = mjson[team2_start:team2_end]
        matchup = (team.strip(), team2.strip())
        if len(team) < 40 and len(team2) < 40:
             matchups.append(matchup)
        # get players
        player_start = mjson.find('rank') + 25
        player_end = mjson.find('rating') + 5
        name = mjson[player_start:player_end]
        player_start2 = name.find('name') + 10
        player_end2 = name.find(',') - 4
        name = name[player_start2:player_end2]
        players.append(name.strip())
        mjson = mjson[player_end:]

    matchups = list(set(matchups))
    players = list(set(players))

    
    # link to model
    matchups = [(Team.objects.get(name__icontains=matchup[0]),
                 Team.objects.get(name__icontains=matchup[1])) for matchup in matchups]

    P = []
    for player in players:
        if player == 'Christan Bauer':
            player = 'Christian Bauer'
        if player == 'Miguoel Admiraal':
            player = 'Miguel Admiraal'
        try:
            p = Player.objects.get(name__icontains=player)
        except Player.DoesNotExist:
            print('{} does not exist'.format(player))
        P.append(p)

    players = P


    # initialize weekly teams
    class WeekTeam:
        def __init__(self, players):
            self.players = players
            self.score = 0

        def __str__(self):
            return(self.players[0].player.team.name)
        __repr__ = __str__

            
    # initialize contestants
    class Contestant:
        def __init__(self, player):
            self.player = player
            self.prev_opponents = []
            self.score = 0
            self.wins = 0

        def __str__(self):
            return(self.player.name)
        __repr__ = __str__



    # define the game    
    def Game(player1, player2, rating='rating'):
        if rating == 'rating':
            p1_rating = player1.player.rating
            p2_rating = player2.player.rating
        if rating == 'perf':
            if player1.player.perf:
                p1_rating = player1.player.perf
            else:
                p1_rating = player1.player.rating
            if player2.player.perf:
                p2_rating = player2.player.perf
            else:
                p2_rating = player2.player.rating
        if rating == 'split':
            if player1.player.perf:
                p1_rating = (player1.player.rating + player1.player.perf) / 2
            else:
                p1_rating = player1.player.rating
            if player2.player.perf:
                p2_rating = (player2.player.rating + player2.player.perf) / 2
            else:
                p2_rating = player2.player.rating
                
        p1_win = 1. / (1 + 10**((p2_rating - p1_rating)/400) )
        if random() < p1_win:
            return(1, 0)
        else:
            return(0, 1)



    # link to roster
    teams = Team.objects.all()
    rosters = {team: [] for team in teams}
    
    
    for player in players:
        r = rosters[player.team]
        r.append(Contestant(player))
        rosters[player.team] = r

    # simulate matchups
    contestants = []
    weekteams = []

    for matchup in matchups:
        team1 = WeekTeam(rosters[matchup[0]])
        team2 = WeekTeam(rosters[matchup[1]])

        weekteams.append(team1)
        weekteams.append(team2)
        
        for contestant in team1.players:
            contestants.append(contestant)
            
        for contestant in team2.players:
            contestants.append(contestant)

        for sim in list(range(100)):
        # fight!
            for player in team1.players:
                for opponent in team2.players:
                    c_score, o_score = Game(player, opponent, 'split')
                    player.score += c_score
                    team1.score += c_score
                    opponent.score += o_score
                    team2.score += o_score
                
        final = {contestant.player.name: contestant.score for contestant in contestants}
        final2 = {team: team.score for team in weekteams}
        sorted_final = sorted(final.items(), key=operator.itemgetter(1))
        sorted_final2 = sorted(final2.items(), key=operator.itemgetter(1))






        
                                    
        context = {
            'matchups': matchups
        }
        
        return render(request,
                      'pcl/matchup.html',
                      context,
        )
