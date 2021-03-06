from django.test import TestCase
from home.models import Player
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
  p.save()