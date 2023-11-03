## load packages

import pandas as pd
from enum import Flag
from statistics import mean, stdev 

## Read play by play dataset

## NFL season year to pull

YEAR = 2023

## Upcoming NFL Week

FantasyWeekIs = 9

##RostersOnly = No if it's Tuesday, else = Yes


RostersOnly = 'Yes'

## Last n weeks to include in calculations for player scores

n_weeks_included = 18

data_pbp = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp/' \
                   'play_by_play_' + str(YEAR) + '.csv.gz',
                   compression= 'gzip', low_memory= False)

xxxx = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp_participation/pbp_participation_' + str(YEAR) + '.csv')

yyyy = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/players/players.csv')

from espn_api.football import League

league = League(league_id=1471217, year = 2023, espn_s2 = 'AEAlGBHWzC6C11wr2NGZuz7v7aS6d1ziyHIqw5UepPnZtS9v%2FTX8E4MnAAwdlV9%2FVoH4fSX1wMvZc0uFxPVqGclKy22xbFakCJVIsbwdj0n1EXevS8lzYGMkBrPsa%2BDhkQbCu1HQweEtU%2F6PUNcX8ElKTZXbkpieZWmeaBzwr2PvFDNmVtFrfoxX0llqlnjGXG0irUc6liDjKiKcv4%2BDudmqDju3W%2FZqbldzBlRWSpwUSPnDFh36zvwmb%2BkEkffkATES8ZjNCVe%2F6sWMdVg3gFIPtjJkVXBaE%2F2vmddCQbaDQQ%3D%3D', swid = '{FEA2C37D-CFAE-4161-B882-4BE389FF2041}')

def checkIfRomanNumeral(numeral):
    numeral = {c for c in numeral.upper()}
    validRomanNumerals = {c for c in "MDCLXVI()"}
    return not numeral - validRomanNumerals

def create():
    ret = []
    for matchups in league.box_scores(FantasyWeekIs):
      h = []
      g= []
      for player in matchups.home_lineup:
          split = player.name.split()
          last = split[len(split) -  1]
          team = player.proTeam
          slot = player.slot_position
          if checkIfRomanNumeral(last) == True:
              last = *split,_ = split
              last = split[len(split) -  1]
          if 'Jr' in last or 'Sr' in last:
              last = *split,_ = split
              last = split[len(split) -  1]
          team = team.replace('OAK', 'LV')
          team = team.replace('LAR', 'LA')
          team = team.replace('WSH', 'WAS')
          h.append(last + ',' + team + ',' + slot)
      ret.append(h)
      for player in matchups.away_lineup:
          split = player.name.split()
          last = split[len(split) -  1]
          team = player.proTeam
          slot = player.slot_position
          if checkIfRomanNumeral(last) == True:
              last = *split,_ = split
              last = split[len(split) -  1]
          if 'Jr' in last or 'Sr' in last:
              last = *split,_ = split
              last = split[len(split) -  1]
          team = team.replace('OAK', 'LV')
          team = team.replace('LAR', 'LA')
          team = team.replace('WSH', 'WAS')
          g.append(last + ',' + team + ',' + slot)
      ret.append(g)
    return ret

def make():
    ret = []
    for matchups in league.box_scores(FantasyWeekIs):
        ret.append(matchups.home_team)
        ret.append(matchups.away_team)
    return ret

player_outputs = [] 
player_outputs = create()
header_outputs = make()

# data_pbp = pd.read_csv('play_by_play_2022.csv.gz', compression = 'gzip', low_memory = False)

##Filter for regular season only

data_pbp = data_pbp.loc[data_pbp.season_type=='REG']

## Create empty dict for player scores

player_dict = {}

##PlayerType class, player attributes, values, and class specific methods

class PlayerType(Flag):
    RB = 1
    WR = 2
    QB = 4
    
class PlayerClass:

    def __init__(self, id, name, team):
        self.id = id
        self.name = name.split('.')
        self.team = team
        self.pos = None
        self.rb_values = [0] * (FantasyWeekIs-1)
        self.rb_rz_values = [0] * (FantasyWeekIs-1)
        self.wr_values = [0] * (FantasyWeekIs-1)
        self.wr_rz_values = [0] * (FantasyWeekIs-1)
        self.qb_values = [0] * (FantasyWeekIs-1)
        self.qb_rz_values = [0] * (FantasyWeekIs-1)
        self.weekly_air_yds = [0] * (FantasyWeekIs-1)
        self.weekly_rushing_yds = [0] * (FantasyWeekIs-1)
        self.active_week = [0] * (FantasyWeekIs-1)
        self.completed_pass_count = 0
        self.total_pass_count = 0
        self.reception_count = 0
        self.rz_reception_count = 0
        
    def __str__(self) -> str:
        return f'{self.id}, {self.name}, {self.team}, {self.pos}: {self.active_week}, {self.get_total_rb()}, {self.get_total_wr()}, {self.get_total_qb()}, {self.get_mean_rz_rb()}, {self.get_mean_rz_wr()}, {self.get_mean_rz_qb()}, {self.get_bindex_rb()}, {self.get_bindex_wr()}, {self.get_bindex_qb()}'
    
    def update_type(self, type):
        if hasattr(self, 'type'):
            self.type |= type
        else:
            self.type = type
    
    def add_rb_value(self, week, rush_yds):
        self.rb_values[week - 1] += 1
        self.weekly_rushing_yds[week-1] += rush_yds
        self.update_type(PlayerType.RB)

    def add_rb_rz (self, week):
        self.rb_rz_values[week - 1] += 1
        self.update_type(PlayerType.RB)
        
    def add_wr_value(self, week, air_yds, completed):
        self.wr_values[week - 1] += 1
        self.weekly_air_yds[week-1] += air_yds
        self.update_type(PlayerType.WR)

        if completed:
            self.reception_count +=1

    def setPosition (self, position):
        self.pos = position 

    def add_wr_rz (self, week, completed):
        self.wr_rz_values[week - 1] += 1
        self.update_type(PlayerType.WR)

        if completed:
            self.rz_reception_count +=1
        
    def add_qb_value(self, week, completed, air_yds):
        self.qb_values[week - 1] += 1
        self.weekly_air_yds[week-1] += air_yds
        self.update_type(PlayerType.QB)

        if completed:
            self.completed_pass_count +=1

        self.total_pass_count += 1

    def add_qb_rz (self, week):
        self.qb_rz_values[week - 1] += 1
        self.update_type(PlayerType.QB)
                        
    def get_stdev_rb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.rb_values[itr])
            itr += 1
        try:
            stdev(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return stdev(ret[-n_weeks_included:])

    def get_mean_rb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.rb_values[itr])
            itr += 1
        try:
            mean(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return mean(ret[-n_weeks_included:])

    def get_total_rb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.rb_values[itr])
            itr += 1
        return sum(ret[-n_weeks_included:])
    
    def get_stdev_wr(self):    
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.wr_values[itr])
            itr += 1
        try:
            stdev(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return stdev(ret[-n_weeks_included:])

    def get_mean_rz_wr(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.wr_rz_values[itr])
            itr += 1
        try:
            mean(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return mean(ret[-n_weeks_included:])

    def get_mean_rz_rb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.rb_rz_values[itr])
            itr += 1
        try:
            mean(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return mean(ret[-n_weeks_included:])

    def get_mean_rz_qb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.qb_rz_values[itr])
            itr += 1
        try:
            mean(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return mean(ret[-n_weeks_included:])

    def get_total_wr(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.wr_values[itr])
            itr += 1
        return sum(ret[-n_weeks_included:])

    def get_mean_wr(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.wr_values[itr])
            itr += 1
        try:
            mean(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return mean(ret[-n_weeks_included:])
    
    def get_stdev_qb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.qb_values[itr])
            itr += 1
        try:
            stdev(ret[-n_weeks_included:])
        except:
            return 0
        else:
            return stdev(ret[-n_weeks_included:])

    def get_total_qb(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.qb_values[itr])
            itr += 1
        return sum(ret[-n_weeks_included:])

    def get_mean_qb(self):
  
        if self.total_pass_count > 8:
            ret = []
            itr = 0
            for x in self.active_week:
                if x == 1:
                    ret.append(self.qb_values[itr])
                itr += 1
            try: mean(ret[-n_weeks_included:])
            except:
                return 0
            else:
                return mean(ret[-n_weeks_included:])
        else:
            return 0
    
    def get_mean_air_yds(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.weekly_air_yds[itr])
            itr += 1
        return mean(ret[-n_weeks_included:])

    def get_mean_rush_yds(self):
        ret = []
        itr = 0
        for x in self.active_week:
            if x == 1:
                ret.append(self.weekly_rushing_yds[itr])
            itr += 1
        return mean(ret[-n_weeks_included:])

    def get_adot(self):
        if self.total_pass_count < 10:
            try:
                self.get_mean_air_yds()/self.get_mean_wr()
            except:
                return 0
            else:
                return (self.get_mean_air_yds()/self.get_mean_wr())
        else:
            return 0

    def get_adot_qb(self):
        try:
            self.get_mean_air_yds()/self.get_mean_qb()
        except:
            return 0
        else:
            return (self.get_mean_air_yds()/self.get_mean_qb())

    def get_ypc(self):
        try:
            self.get_mean_rush_yds()/self.get_mean_rb()
        except:
            return 0
        else:
            return (self.get_mean_rush_yds()/self.get_mean_rb())

    def get_completed_pass_percent(self):
        try:
            self.completed_pass_count / self.total_pass_count
        except:
            return 0
        else:
            return self.completed_pass_count / self.total_pass_count

    def get_catch_percent(self):
        try:
            (self.reception_count / sum(self.wr_values))
        except:
            return 0
        else:
            return (self.reception_count / sum(self.wr_values)) 

    def get_rz_catch_percent(self):
        try:
            (self.rz_reception_count/ sum(self.wr_rz_values))
        except:
            return 0
        else:
            return (self.rz_reception_count/ sum(self.wr_rz_values))                                                                                                                            

    def get_active_total (self):
        return sum(self.active_week)

    def get_bindex_rb (self):
        try:
        # return self.get_mean_rb() + 2*self.get_mean_rz_rb()
            (0.15*self.get_mean_rb()*self.get_ypc())+(4*self.get_mean_rz_rb())+(0.5*(self.get_mean_rb()/self.get_stdev_rb()))
        except:
            return 0
        else:
            return (0.15*self.get_mean_rb()*self.get_ypc())+(4*self.get_mean_rz_rb())+(0.5*(self.get_mean_rb()/self.get_stdev_rb()))

    def get_bindex_qb (self):
        try:
            (0.09*self.get_adot_qb()*self.get_completed_pass_percent()*self.get_mean_qb())+(3*self.get_completed_pass_percent()*self.get_mean_rz_qb())+((0.06*self.get_completed_pass_percent()*self.get_mean_qb())/self.get_stdev_qb())
        except:
            return 0
        else:
            return (0.09*self.get_completed_pass_percent()*self.get_mean_qb()*self.get_adot_qb())+(3*self.get_completed_pass_percent()*self.get_mean_rz_qb())+((0.06*self.get_completed_pass_percent()*self.get_mean_qb())/self.get_stdev_qb())

    def get_bindex_wr (self):
        try:
        # return self.get_mean_wr() + 2*self.get_mean_rz_wr()
           (0.2*self.get_catch_percent()*self.get_mean_wr()*abs(self.get_adot()))+(6.5*self.get_rz_catch_percent()*self.get_mean_rz_wr())+(self.get_mean_wr()/self.get_stdev_wr())
        except:
            return 0
        else:
            return (0.2*self.get_catch_percent()*self.get_mean_wr()*abs(self.get_adot()))+(6.5*self.get_rz_catch_percent()*self.get_mean_rz_wr())+(self.get_mean_wr()/self.get_stdev_wr())
   
    def is_type(self, player_type):
        return self.type & player_type == player_type

    def add_active(self, week):
        self.active_week[week - 1] = 1

    def to_csv_output(self):
        return f'{self.name[-1].lstrip()},{self.team},{self.pos},{self.get_total_rb()},{self.get_total_wr()},{self.get_total_qb()},{self.get_mean_rb()},{self.get_mean_wr()},{self.get_mean_qb()},{self.get_ypc()},{self.get_adot()},{self.get_adot_qb()},{self.get_completed_pass_percent()},{self.get_catch_percent()},{self.get_rz_catch_percent()},{self.get_mean_rz_rb()},{self.get_mean_rz_wr()},{self.get_mean_rz_qb()},{self.get_active_total()},{self.get_bindex_rb()},{self.get_bindex_wr()},{self.get_bindex_qb()}\n'

## Functions for filling the dict

def try_add_pos (id, position):
    if id in player_dict:
        player_dict[id].setPosition(position)

def add_pos (csv_row):
    try_add_pos(csv_row.gsis_id, csv_row.position)

def try_add_player(id, name, team):
    if id not in player_dict:
        player_dict[id] = PlayerClass(id, name, team)

def try_add_wr(csv_row):
    if pd.isna(csv_row.receiver_player_id) == False:
        if pd.isna(csv_row.air_yards) == False: 
            try_add_player(csv_row.receiver_player_id, csv_row.receiver_player_name, csv_row.posteam)
            player_dict[csv_row.receiver_player_id].add_wr_value(csv_row.week, csv_row.air_yards, csv_row.complete_pass)

def try_add_rb(csv_row):
    if pd.isna(csv_row.rusher_player_id) == False:
        if pd.isna(csv_row.rushing_yards) == False: 
            try_add_player(csv_row.rusher_player_id, csv_row.rusher_player_name, csv_row.posteam)
            player_dict[csv_row.rusher_player_id].add_rb_value(csv_row.week, csv_row.rushing_yards)

def try_add_rb_rz(csv_row):
    if pd.isna(csv_row.rusher_player_id) == False:
        if csv_row.yardline_100<=10:
            try_add_player(csv_row.rusher_player_id, csv_row.rusher_player_name, csv_row.posteam)
            player_dict[csv_row.rusher_player_id].add_rb_rz(csv_row.week)
    
def try_add_qb(csv_row):
    if pd.isna(csv_row.passer_player_id) == False:
        if pd.isna(csv_row.air_yards) == False:
            try_add_player(csv_row.passer_player_id, csv_row.passer_player_name, csv_row.posteam)
            player_dict[csv_row.passer_player_id].add_qb_value(csv_row.week, csv_row.complete_pass, csv_row.air_yards)

def try_add_qb_rz(csv_row):
    if pd.isna(csv_row.passer_player_id) == False:
        if csv_row.yardline_100<=20:
            try_add_player(csv_row.passer_player_id, csv_row.passer_player_name, csv_row.posteam)
            player_dict[csv_row.passer_player_id].add_qb_rz(csv_row.week)

def try_add_wr_rz(csv_row):
    if pd.isna(csv_row.receiver_player_id) == False:
        if csv_row.yardline_100<=20:
            try_add_player(csv_row.receiver_player_id, csv_row.receiver_player_name, csv_row.posteam)
            player_dict[csv_row.receiver_player_id].add_wr_rz(csv_row.week, csv_row.complete_pass)

## Loop through play by play to fill dict with above functions

if RostersOnly == 'No':

    for _, value in data_pbp.iterrows():
        try_add_wr(value)
        try_add_rb(value)
        try_add_qb(value)
        try_add_rb_rz(value)
        try_add_qb_rz(value)
        try_add_wr_rz(value)

    for _, value in xxxx.iterrows():
        week_string = value['nflverse_game_id'].split('_')[1]

        if pd.isna(value['offense_players']) == False: 
                for id in value['offense_players'].split(';'):
                    if id in player_dict:
                        if int(week_string) <= 18:
                            player_dict[id].add_active(int(week_string))

    for _, value in yyyy.iterrows():
        add_pos(value)

    for key in player_dict:
        print(player_dict[key])

## Write to CSV for Brom Model   

    f = open('test_nflmodel' + str(YEAR) + '.csv', 'w')
    f.write('player,team,pos,carry total,target total,pass total,carry mean,target mean,pass mean,ypc,adot,adot qb,completion pct,catch pct,RZcatch pct,RZcarry mean,RZtarget mean,RZpass mean,total active weeks,carry score,target score,passing score\n')
    for key in player_dict:
        f.write(player_dict[key].to_csv_output())
    f.flush()
    f.close()

else:
    pass

##Write to CSV for Tots Rosters

g = open('test_totsRosters.csv', 'w')
g.write(','.join(map(lambda x: x.owner + ',' + ',', header_outputs)) + '\n')
for i in range(15):
    for j in range(len(header_outputs)):
        if i < len(player_outputs[j]):
            g.write(player_outputs[j][i])
        else:
            g.write('')

        if j != 14:
            g.write(',')
    g.write('\n')
g.flush()
g.close()

print(len(player_dict))
print('COMPLETE')
print(player_outputs)
print(header_outputs)