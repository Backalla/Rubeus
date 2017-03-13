from __future__ import unicode_literals

from django.db import models

class Player(models.Model):
  Pid = models.CharField(max_length=10,primary_key=True)
  Name = models.CharField(max_length=100)
  Basevalue = models.PositiveIntegerField()
  PLAYER_TYPE_CHOICES = (
    ('BA','Batsman'),
    ('BO','Bowler'),
    ('WK','Wicket Keeper'),
    ('AR','All Rounder'),
  )
  Player_type = models.CharField(max_length=2,choices=PLAYER_TYPE_CHOICES,default='BA')
  NATIONALITY_CHOICES = (
    ('IN','Indian'),
    ('FO','Foreigner'),
  )
  Nationality = models.CharField(max_length=2,choices=NATIONALITY_CHOICES,default='IN')
  Team_name = models.CharField(max_length=3,default="NUL")

  def __str__(self):
    return self.Name

class Owner(models.Model):
  Name = models.CharField(max_length=100)
  TEAM_CHOICES = (
    ('SRH','Sunrisers Hyderabad'),
    ('RCB','Royal Challengers Bangalore'),
    ('RPS','Rising Pune Supergiants'),
    ('MIN', 'Mumbai Indians'),
    ('KKR', 'Kolkata Knight Riders'),
    ('KXP', 'Kings XI Punjab'),
    ('GJL', 'Gujarat Lions'),
    ('DDD', 'Delhi Daredevils'),
  )
  Team_name = models.CharField(max_length=3,choices=TEAM_CHOICES,default='SRH')
  Points = models.PositiveIntegerField(default=0)
  Remaining_cash = models.PositiveIntegerField(default=3500)
  def __str__(self):
    return self.Name+" - "+self.Team_name

