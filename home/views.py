
import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import operator

from django.shortcuts import render
from django.template import loader
import random
from .models import Player,Owner
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

def get_match(url):
  player_template = {"pid":"0","name":"","is_captain":"0","team_name":"","out_by":"None","runs_scored":"0","balls_faced":"0","fours":"0","sixes":"0","strike_rate":"0","overs":"0","maiden":"0","runs_given":"0","wickets":"0","no_balls":"0","wide_balls":"0","CROST":"0","extras":"0","points":"0"}
  with open(os.path.join(BASE, "matches.json"),"r") as f:
    matches = json.load(f)
  # matches = {"match": []}
  # pprint(matches)
  # print matches['match'][0]['match_name']

  # Scorecard = open('scorecard.html')
  Scorecard = requests.get(url).text

  Soup = BeautifulSoup(Scorecard,"html.parser")
  # print soup
  match_name = Soup.find('h1',class_="cb-nav-hdr cb-font-18 line-ht24").get_text()
  match_name = match_name[:match_name.find('- Live Cricket Score, Commentary')].strip()

  for match in matches['match']:
    if match_name == match['match_name']:
      print "Match already exists..."
      return match

  match = {}
  match['match_name'] = match_name
  match['url'] = url[url.find('cricket-scorecard/')+18:]




  Inning1 = Soup.find_all('div',id="innings_1")[0]
  Inning1_batting = Inning1.find_all('div',class_="cb-col cb-col-100 cb-ltst-wgt-hdr")[0]
  Inning1_bowling = Inning1.find_all('div',class_="cb-col cb-col-100 cb-ltst-wgt-hdr")[1]
  Inning1_batting = Inning1_batting.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms")
  Inning1_bowling = Inning1_bowling.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms ")
  Score = Inning1.find_all('span',class_="pull-right")
  score = Score[0].get_text()
  if '-' in score:
    score = score[:score.find('-')]
  team_name = Inning1.find('span').get_text()
  if 'Innings' in team_name:
    team_name = team_name[:team_name.find(' Innings')]
  match['team1_name'] = team_name
  match['team1_score'] = score



  # Inning 1 Start

  Inning1_batting_info = []
  for b in Inning1_batting:
    # pprint(b)
    batsman = {}
    name = b.find('a',class_="cb-text-link")
    if name:
      pid = name['href'][10:]
      batsman['pid'] = str(pid[:pid.find('/')])
      batsman['name'] = str(name.get_text()).strip()
      if '(' in batsman['name']:
        batsman['name'] = batsman['name'][:batsman['name'].find('(')].strip()
    out_by = b.find('span',class_="text-gray")
    if out_by:
      batsman['out_by'] = str(out_by.get_text()).strip()
    runs = b.find('div',class_="cb-col cb-col-8 text-right text-bold")
    if runs:
      batsman['runs'] = str(runs.get_text()).strip()
    all_others = b.find_all('div',class_="cb-col cb-col-8 text-right")
    if len(all_others)>0:
      batsman['balls'] = str(all_others[0].get_text()).strip()
      batsman['fours'] = str(all_others[1].get_text()).strip()
      batsman['sixes'] = str(all_others[2].get_text()).strip()
      batsman['sr'] = str(all_others[3].get_text()).strip()

    # print all_other
    if len(batsman) > 0:
      Inning1_batting_info.append(batsman)



  Inning1_bowling_info = []
  for b in Inning1_bowling:
    bowler = {}
    name = b.find('a',class_="cb-text-link")
    if name:
      pid = name['href'][10:]
      bowler['pid'] = str(pid[:pid.find('/')])
      bowler['name'] = str(name.get_text()).strip()
      if '(' in bowler['name']:
        bowler['name'] = bowler['name'][:bowler['name'].find('(')].strip()
    wickets = b.find('div',class_="cb-col cb-col-8 text-right text-bold")
    if wickets:
      bowler['wickets'] = str(wickets.get_text()).strip()
    runs_given = b.find('div',class_="cb-col cb-col-10 text-right")
    if runs_given:
      bowler['runs_given'] = str(runs_given.get_text()).strip()
    all_others = b.find_all('div',class_="cb-col cb-col-8 text-right")
    # print all_others
    if len(all_others)>0:
      bowler['overs'] = str(all_others[0].get_text()).strip()
      bowler['maiden'] = str(all_others[1].get_text()).strip()
      bowler['no_balls'] = str(all_others[2].get_text()).strip()
      bowler['wide_balls'] = str(all_others[3].get_text()).strip()
      # bowler['economy'] = str(all_others[5].get_text()).strip()
    # print bowler
    if len(bowler) > 0:
      Inning1_bowling_info.append(bowler)



  # Inning 2 Start


  Inning2 = Soup.find_all('div',id="innings_2")[0]
  Inning2_batting = Inning2.find_all('div',class_="cb-col cb-col-100 cb-ltst-wgt-hdr")[0]
  Inning2_bowling = Inning2.find_all('div',class_="cb-col cb-col-100 cb-ltst-wgt-hdr")[1]
  Inning2_batting = Inning2_batting.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms")
  Inning2_bowling = Inning2_bowling.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms ")
  Score = Inning2.find_all('span',class_="pull-right")
  score = Score[0].get_text()
  if '-' in score:
    score = score[:score.find('-')]
  team_name = Inning2.find('span').get_text()
  if 'Innings' in team_name:
    team_name = team_name[:team_name.find(' Innings')]
  match['team2_name'] = team_name
  match['team2_score'] = score






  Inning2_batting_info = []
  for b in Inning2_batting:
    # pprint(b)
    batsman = {}
    name = b.find('a',class_="cb-text-link")
    if name:
      pid = name['href'][10:]
      batsman['pid'] = str(pid[:pid.find('/')])
      batsman['name'] = str(name.get_text()).strip()
      if '(' in batsman['name']:
        batsman['name'] = batsman['name'][:batsman['name'].find('(')].strip()
    out_by = b.find('span',class_="text-gray")
    if out_by:
      batsman['out_by'] = str(out_by.get_text()).strip()
    runs = b.find('div',class_="cb-col cb-col-8 text-right text-bold")
    if runs:
      batsman['runs'] = str(runs.get_text()).strip()
    all_others = b.find_all('div',class_="cb-col cb-col-8 text-right")
    if len(all_others)>0:
      batsman['balls'] = str(all_others[0].get_text()).strip()
      batsman['fours'] = str(all_others[1].get_text()).strip()
      batsman['sixes'] = str(all_others[2].get_text()).strip()
      batsman['sr'] = str(all_others[3].get_text()).strip()

    # print all_other
    if len(batsman) > 0:
      Inning2_batting_info.append(batsman)



  Inning2_bowling_info = []
  for b in Inning2_bowling:
    bowler = {}
    name = b.find('a',class_="cb-text-link")
    if name:
      pid = name['href'][10:]
      bowler['pid'] = str(pid[:pid.find('/')])
      bowler['name'] = str(name.get_text()).strip()
      if '(' in bowler['name']:
        bowler['name'] = bowler['name'][:bowler['name'].find('(')].strip()
    wickets = b.find('div',class_="cb-col cb-col-8 text-right text-bold")
    if wickets:
      bowler['wickets'] = str(wickets.get_text()).strip()
    runs_given = b.find('div',class_="cb-col cb-col-10 text-right")
    if runs_given:
      bowler['runs_given'] = str(runs_given.get_text()).strip()
    all_others = b.find_all('div',class_="cb-col cb-col-8 text-right")
    # print all_others
    if len(all_others)>0:
      bowler['overs'] = str(all_others[0].get_text()).strip()
      bowler['maiden'] = str(all_others[1].get_text()).strip()
      bowler['no_balls'] = str(all_others[2].get_text()).strip()
      bowler['wide_balls'] = str(all_others[3].get_text()).strip()
      # bowler['economy'] = str(all_others[5].get_text()).strip()
    # print bowler
    if len(bowler) > 0:
      Inning2_bowling_info.append(bowler)

  # print match
  # print json.dumps(matches,sort_keys=True,indent=4, separators=(',', ': '))
  players = {}
  Players = Soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm")
  Players1 = Players[1].find_all('a')
  Players2 = Players[3].find_all('a')
  # for p in Players1:
  #   print p
  # for p in Players2:
  #   print p
  for p in Players1:
    player = player_template.copy()
    pid = p['href'][10:]
    pid = str(pid[:pid.find('/')])
    players[pid] = player
  for p in Players2:
    player = player_template.copy()
    pid = p['href'][10:]
    pid = str(pid[:pid.find('/')])
    players[pid] = player



  # print players
  for p in Inning1_batting_info:
    if p['pid'] in players:
      players[p['pid']]['name'] = p['name']
      players[p['pid']]['balls_faced'] = p['balls']
      players[p['pid']]['fours'] = p['fours']
      players[p['pid']]['sixes'] = p['sixes']
      players[p['pid']]['runs_scored'] = p['runs']
      players[p['pid']]['out_by'] = p['out_by']
      players[p['pid']]['strike_rate'] = p['sr']
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_playing:
        players[p['pid']]['pid'] = p['pid']
      else:
        players[p['pid']]['pid'] = '-1'
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_captain:
        players[p['pid']]['is_captain'] = "1"



  for p in Inning1_bowling_info:
    if p['pid'] in players:
      players[p['pid']]['name'] = p['name']
      players[p['pid']]['maiden'] = p['maiden']
      players[p['pid']]['overs'] = p['overs']
      players[p['pid']]['no_balls'] = p['no_balls']
      players[p['pid']]['runs_given'] = p['runs_given']
      players[p['pid']]['wickets'] = p['wickets']
      players[p['pid']]['wide_balls'] = p['wide_balls']
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_playing:
        players[p['pid']]['pid'] = p['pid']
      else:
        players[p['pid']]['pid'] = '-1'
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_captain:
        players[p['pid']]['is_captain'] = "1"


  for p in Inning2_batting_info:
    if p['pid'] in players:
      players[p['pid']]['name'] = p['name']
      players[p['pid']]['balls_faced'] = p['balls']
      players[p['pid']]['fours'] = p['fours']
      players[p['pid']]['sixes'] = p['sixes']
      players[p['pid']]['runs_scored'] = p['runs']
      players[p['pid']]['out_by'] = p['out_by']
      players[p['pid']]['strike_rate'] = p['sr']
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_playing:
        players[p['pid']]['pid'] = p['pid']
      else:
        players[p['pid']]['pid'] = '-1'
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_captain:
        players[p['pid']]['is_captain'] = "1"


  for p in Inning2_bowling_info:
    if p['pid'] in players:
      players[p['pid']]['name'] = p['name']
      players[p['pid']]['maiden'] = p['maiden']
      players[p['pid']]['overs'] = p['overs']
      players[p['pid']]['no_balls'] = p['no_balls']
      players[p['pid']]['runs_given'] = p['runs_given']
      players[p['pid']]['wickets'] = p['wickets']
      players[p['pid']]['wide_balls'] = p['wide_balls']
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_playing:
        players[p['pid']]['pid'] = p['pid']
      else:
        players[p['pid']]['pid'] = '-1'
      if Player.objects.filter(Pid=p['pid']).count()==1 and Player.objects.get(Pid=p['pid']).Is_captain:
        players[p['pid']]['is_captain'] = "1"



  match['players'] = players
  matches["match"].append(match)


  with open(os.path.join(BASE, "matches.json"),'w') as f:
    json.dump(matches,f)
  return match



def index(request):
  context = {'message': 'Ma nigga ma nigga..Youre home'}
  return render(request,'home/index.html',context)


def resetdb(request):
  players_list = {}
  with open('finallist.txt') as f:
    for line in f:
      a = [b.strip() for b in line.rstrip().split(",")]
      players_list[a[0]] = a

  all_players = Player.objects.all()
  for p in all_players:
    pid = p.Pid
    p.Basevalue = players_list[pid][3]
    p.Player_type = players_list[pid][4]
    p.Team_name = 'NUL'
    p.Points = 0
    p.save()
  all_owners = Owner.objects.all()
  for o in all_owners:
    o.Remaining_cash = 3500
    o.Points = 0
    o.save()
  return render(request,'home/resetdb.html')


def teams(request):
  with open(os.path.join(BASE, "matches.json"), "r") as f:
    matches = json.load(f)

  if request.method == 'POST':
    if 'update_points' in request.POST:
      team_name_map = {'Sunrisers Hyderabad': 'SRH',
                        'Royal Challengers Bangalore': 'RCB' ,
                        'Rising Pune Supergiant': 'RPS' ,
                        'Mumbai Indians': 'MIN' ,
                        'Kolkata Knight Riders': 'KKR' ,
                        'Kings XI Punjab': 'KXP' ,
                        'Gujarat Lions': 'GJL' ,
                        'Delhi Daredevils': 'DDD' }
      all_players = Player.objects.all()
      all_players.update(Points=0)
      all_owners = Owner.objects.all()
      all_owners.update(Points=0)

      for match in matches['match']:
        if int(match['team1_score'])> int(match['team2_score']):
          winner_team = str(match['team1_name'])
          loser_team = str(match['team2_name'])
        else:
          winner_team = str(match['team2_name'])
          loser_team = str(match['team1_name'])
        winner_team_obj = Owner.objects.get(Team_name=team_name_map[winner_team])
        winner_team_obj.Points += 100
        winner_team_obj.save()

        loser_team_obj = Owner.objects.get(Team_name=team_name_map[loser_team])
        loser_team_obj.Points -= 50
        loser_team_obj.save()

        for player in match['players']:
          for p in all_players:
            if player == p.Pid:
              p.Points += int(match['players'][player]['points'])
              p.save()
              team = Owner.objects.get(Team_name=p.Team_name)
              team.Points += int(match['players'][player]['points'])
              team.save()

  all_players = Player.objects.all()
  all_owners = Owner.objects.all()
  all_owners = sorted(all_owners,key=operator.attrgetter('Points'),reverse=True)

  context = {
    'all_players': all_players,
    'all_owners' : all_owners,
    'matches' : matches,
  }
  return render(request,'home/teams.html',context)

def matches(request):
  context={}
  all_players = Player.objects.all()
  all_owners = Owner.objects.all()
  with open(os.path.join(BASE, "matches.json"), "r") as f:
    matches = json.load(f)


  context={
    "matches":matches,
    "all_players":all_players,
    "all_owners":all_owners,
  }
  return render(request,'home/matches.html',context)



def editmatches(request):
  context={}
  error = None
  if request.method == "POST":
    print request.POST
    if 'add_match' in request.POST and request.POST['add_match'] == "True":
      url = str(request.POST['url'])
      try:
        get_match(url)
      except Exception as e:
        print e
        error = "No scorecard found.."
    if 'edit_match' in request.POST:
      new_info = {}
      for info in request.POST:
        if '__' in info:
          new_info[tuple(str(info).split('__'))] = str(request.POST[info])
      with open(os.path.join(BASE, "matches.json"), "r") as f:
        matches = json.load(f)
      match_name = request.POST['edit_match']
      for match in matches['match']:
        if match['match_name'] == match_name:
          for pid,attr in new_info:
            match['players'][pid][attr] = new_info[(pid,attr)]


      with open(os.path.join(BASE, "matches.json"), 'w') as f:
        json.dump(matches, f)

    if 'update_points' in request.POST and request.POST['update_points'] == "True":
      with open(os.path.join(BASE, "matches.json"), "r") as f:
        matches = json.load(f)
      for match in matches['match']:
        for pid in match['players']:
          player = match['players'][pid]


          if int(player['pid']) == -1:
            points = 0
          else:
            points = 0
            # print player['name'],
            # 1run = 1 point
            points += int(player['runs_scored'])

            # 75 to 99 = 50 bonus points
            if int(player['runs_scored']) >= 75 and int(player['runs_scored']) < 100:
              points+= 50

            # >= 100 runs = points boubled
            if int(player['runs_scored']) >= 100:
              points += int(player['runs_scored'])

            # 1 wicket = 30 points
            points += 30*int(player['wickets'])

            # 1 CROST = 15 points
            points += 15*int(player['CROST'])

            # 1 maiden over = 50 points
            points += 50*int(player['maiden'])

            # 3+ wickets = 100 points
            if int(player['wickets']) > 3:
              points += 100

            # hattrick, 6 fours and 6 sixes
            points += int(player['extras'])

            # -20 for duck
            if player['out_by'] != 'None' and player['runs_scored'] == '0':
              points -= 20

            # -20 if runs given > 40
            if int(player['runs_given']) > 40:
              points -= 20

            if int(player['is_captain']) == 1:
              points *= 2
          player['points'] = str(points)
      with open(os.path.join(BASE, "matches.json"), 'w') as f:
        json.dump(matches, f)




  all_players = Player.objects.all()
  all_owners = Owner.objects.all()
  with open(os.path.join(BASE, "matches.json"), "r") as f:
    matches = json.load(f)


  context={
    "matches":matches,
    "all_players":all_players,
    "all_owners":all_owners,
    "error":error,
  }
  return render(request,'home/editmatches.html',context)

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













