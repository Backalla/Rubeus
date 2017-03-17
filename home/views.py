from django.shortcuts import render
from django.template import loader
import random
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
  prev = None
  current = None
  show_unsold = False
  selected_player_type = 'BA'
  error = ""
  if request.method == "POST":
    print request.POST
    if 'current_pid' in request.POST:
      prev = request.POST['current_pid']
    if request.POST['action'] == 'next':
      selected_player_type = request.POST['player_type']
      if 'sold_to_team_name' in request.POST:
        if request.POST['sold_to_team_name']=='UNS':
          current_pid = request.POST['current_pid']
          current_player_object = Player.objects.get(Pid=current_pid)
          current_player_object.Basevalue = current_player_object.Basevalue*2
          current_player_object.Team_name = 'UNS'
          current_player_object.save()
        elif request.POST['sold_to_team_name']!='UNS' and request.POST['sold_amount']:

          current_pid = request.POST['current_pid']
          sold_to_team_name = request.POST['sold_to_team_name']
          current_player_object = Player.objects.get(Pid=current_pid)
          sold_to_team_object = Owner.objects.get(Team_name=sold_to_team_name)
          if sold_to_team_object.Remaining_cash >= int(request.POST['sold_amount']):
            current_player_object.Team_name = sold_to_team_name
            current_player_object.Basevalue = int(request.POST['sold_amount'])
            current_player_object.save()
            sold_to_team_object.Remaining_cash = sold_to_team_object.Remaining_cash - int(request.POST['sold_amount'])
            sold_to_team_object.save()
          else:
            error = "You cannot buy this player. Insufficient funds remaining."
        elif request.POST['sold_to_team_name'] != 'NUL' and not request.POST['sold_amount']:
          error = "Please enter sold amount."
      if 'show_unsold' in request.POST:
        show_unsold = True
        available_players = Player.objects.filter(Player_type=selected_player_type, Team_name='UNS')
      else:
        available_players = Player.objects.filter(Player_type=selected_player_type, Team_name='NUL')
      if len(available_players) == 0:
        error = "No players left!!"
        current = '0'
      else:
        current = random.choice(list(available_players)).Pid
      if error:
        print error
        current = request.POST['current_pid']
    elif request.POST['action'] == 'search':
      search_term = request.POST['search_player']
      search_player_object = Player.objects.filter(Name=search_term)
      if len(search_player_object) == 0:
        error = "Player not found. Please check the name and search again."
      else:
        current = Player.objects.get(Name=search_term).Pid
    elif request.POST['action'] == "previous" and not error:
      current = request.POST['previous_pid']
      current_player_object = Player.objects.get(Pid=current)
      current_player_object.Basevalue /= 2
      current_player_object.save()
      prev = None
  all_owners = Owner.objects.all()
  all_players = Player.objects.all()
  context = {
    "all_owners": all_owners,
    "all_players": all_players,
    "current":current,
    "prev": prev,
    "selected_player_type":selected_player_type,
    "error":error,
    "show_unsold":show_unsold,
  }
  return render(request,'home/auction.html',context)