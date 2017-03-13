from django.shortcuts import render
from django.template import loader
from .models import Player,Owner

def index(request):
  context = {'message': 'Ma nigga ma nigga..Youre home'}
  return render(request,'home/index.html',context)


def teams(request):
  context={}
  return render(request,'home/teams.html',context)

def matches(request):
  context={}
  return render(request,'home/matches.html',context)

def auction(request):

  all_owners = Owner.objects.all()
  all_players = Player.objects.all()
  teams = {}
  # Put all sold players in teams
  team_names = {
    'SRH': 'Sunrisers Hyderabad',
    'RCB': 'Royal Challengers Bangalore',
    'RPS': 'Rising Pune Supergiants',
    'MIN': 'Mumbai Indians',
    'KKR': 'Kolkata Knight Riders',
    'KXP': 'Kings XI Punjab',
    'GJL': 'Gujarat Lions',
    'DDD': 'Delhi Daredevils'
  }
  for owner in all_owners:
    teams[team_names[owner.Team_name]] = []
  for player in all_players:
    if player.Team_name in team_names:
      player_info = {}
      player_info['name'] = str(player.Name)
      player_info['team_name'] = str(player.Team_name)
      player_info['basevalue'] = str(player.Basevalue)
      if str(player.Nationality) == 'IN':
        player_info['nationality'] = "Indian"
      else:
        player_info['nationality'] = "Foreigner"
      if str(player.Player_type) == 'BA':
        player_info['player_type'] = "Batsman"
      elif str(player.Player_type) == 'BO':
        player_info['player_type'] = "Bowler"
      elif str(player.Player_type) == 'WK':
        player_info['player_type'] = "Wicket Keeper"
      elif str(player.Player_type) == 'AR':
        player_info['player_type'] = "All Rounder"
      teams[team_names[player.Team_name]].append(player_info)
  print teams
  context = {
    'teams': teams,

  }
  return render(request,'home/auction.html',context)