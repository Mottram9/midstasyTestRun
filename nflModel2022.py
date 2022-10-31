## load packages

import pandas as pd
from enum import Flag
from statistics import mean, stdev 

## Read play by play dataset
YEAR = 2022
data_pbp = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp/' \
                   'play_by_play_' + str(YEAR) + '.csv.gz',
                   compression= 'gzip', low_memory= False)

xxxx = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp_participation/pbp_participation_2022.csv')

##data = pd.read_csv('2021playbyplay.csv.gz', compression = 'gzip', low_memory = False)

##Filter for regular season only

data_pbp = data_pbp.loc[data_pbp.season_type=='REG']

## Create empty dict for player scores

player_dict = {}
id_dict = {}

## Last n weeks to include in calculations for player scores

n_weeks_included = 8

##PlayerType class, player attributes, values, and class specific methods

class PlayerType(Flag):
    RB = 1
    WR = 2
    QB = 4
    
class PlayerClass:
   
    def __init__(self, id, name, team):
        self.id = id
        self.name = name
        self.team = team
        self.rb_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.rb_rz_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.wr_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.wr_rz_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.qb_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.qb_rz_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.weekly_air_yds = [0, 0, 0, 0, 0, 0, 0, 0]
        self.weekly_rushing_yds = [0, 0, 0, 0, 0, 0, 0, 0]
        self.active_week = [0, 0, 0, 0, 0, 0, 0, 0]
        self.completed_pass_count = 0
        self.total_pass_count = 0
        
    def __str__(self) -> str:
        return f'{self.id}, {self.name}, {self.team}: {self.active_week}, {self.get_total_rb()}, {self.get_total_wr()}, {self.get_total_qb()}, {self.get_mean_rz_rb()}, {self.get_mean_rz_wr()}, {self.get_mean_rz_qb()}, {self.get_bindex_rb()}, {self.get_bindex_wr()}, {self.get_bindex_qb()}'
    
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
        
    def add_wr_value(self, week, air_yds):
        self.wr_values[week - 1] += 1
        self.weekly_air_yds[week-1] += air_yds
        self.update_type(PlayerType.WR)

    def add_wr_rz (self, week):
        self.wr_rz_values[week - 1] += 1
        self.update_type(PlayerType.WR)
        
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

    def get_bindex_rb (self):
        try:
            (0.15*self.get_mean_rb()*self.get_ypc())+(3*self.get_mean_rz_rb())+(0.5*(self.get_mean_rb()/self.get_stdev_rb()))
        except:
            return 0
        else:
            return (0.15*self.get_mean_rb()*self.get_ypc())+(3*self.get_mean_rz_rb())+(0.5*(self.get_mean_rb()/self.get_stdev_rb()))

    def get_bindex_qb (self):
        try:
            (0.08*self.get_adot_qb()*self.get_completed_pass_percent()*self.get_mean_qb())+(3*self.get_completed_pass_percent()*self.get_mean_rz_qb())+((0.06*self.get_completed_pass_percent()*self.get_mean_qb())/self.get_stdev_qb())
        except:
            return 0
        else:
            return (0.08*self.get_completed_pass_percent()*self.get_mean_qb()*self.get_adot_qb())+(3*self.get_completed_pass_percent()*self.get_mean_rz_qb())+((0.06*self.get_completed_pass_percent()*self.get_mean_qb())/self.get_stdev_qb())

    def get_bindex_wr (self):
        try:
            (0.1 * self.get_mean_wr()*abs(self.get_adot()))+(4*self.get_mean_rz_wr())+(self.get_mean_wr()/self.get_stdev_wr())
        except:
            return 0
        else:
            return (0.1 * self.get_mean_wr() * abs(self.get_adot()))+(4 * self.get_mean_rz_wr()) + (self.get_mean_wr()/self.get_stdev_wr())
   
    def is_type(self, player_type):
        return self.type & player_type == player_type

    def add_active(self, week):
        self.active_week[week - 1] = 1

    def add_rookie(self):
        itr = 0
        if sum(self.active_week) == 0:
            for x in self.active_week:
                self.active_week[itr] += 1
                itr += 1


    def to_csv_output(self):
        return f'{self.name},{self.team},{self.get_total_rb()},{self.get_total_wr()},{self.get_total_qb()},{self.get_mean_rb()},{self.get_mean_wr()},{self.get_mean_qb()},{self.get_ypc()},{self.get_adot()},{self.get_adot_qb()},{self.get_completed_pass_percent()},{self.get_stdev_rb()},{self.get_stdev_wr()},{self.get_stdev_qb()},{self.get_bindex_rb()},{self.get_bindex_wr()},{self.get_bindex_qb()}\n'
    
   ##FIX def to_csv_output(self):
        ##return f'{self.name},{self.team},{self.get_type_string()},{self.get_bindex_rb()+self.get_bindex_wr()+self.get_bindex_qb()}\n'

## Functions for filling the dict

def try_add_player(id, name, team):
    if id not in player_dict:
        player_dict[id] = PlayerClass(id, name, team)

def try_add_id(csv_row):
    if csv_row.gsis_id in player_dict:
        id_dict[csv_row.pfr_id] = csv_row.gsis_id

def try_add_active(csv_row):
    if csv_row.pfr_player_id in id_dict:
        player_dict[id_dict[csv_row.pfr_player_id]].add_active(csv_row.week, csv_row.offense_snaps)

def try_add_rookie(csv_row):
    if csv_row.gsis_id in player_dict:
        player_dict[csv_row.gsis_id].add_rookie()

def try_add_wr(csv_row):
    if pd.isna(csv_row.receiver_player_id) == False:
        if pd.isna(csv_row.air_yards) == False: 
            try_add_player(csv_row.receiver_player_id, csv_row.receiver_player_name, csv_row.posteam)
            player_dict[csv_row.receiver_player_id].add_wr_value(csv_row.week, csv_row.air_yards)

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
            player_dict[csv_row.receiver_player_id].add_wr_rz(csv_row.week)

## Loop through play by play to fill dict with above functions

for _, value in data_pbp.iterrows():
    try_add_wr(value)
    try_add_rb(value)
    try_add_qb(value)
    try_add_rb_rz(value)
    try_add_qb_rz(value)
    try_add_wr_rz(value)


# Get the snap counts
for _, value in xxxx.iterrows():
    # 0 - Week Data
    week_string = value['nflverse_game_id'].split('_')[1]
    
    # 10 - Offense Data
    if pd.isna(value['offense_players']) == False: 
        # Find the player in the dictionary and add active
        for id in value['offense_players'].split(';'):
            if id in player_dict:
                player_dict[id].add_active(int(week_string))


for key in player_dict:
    print(player_dict[key])
    
## Write to CSV for useable file    
f = open('test_nflmodel2022.csv', 'w')
f.write('player,team,carry total,target total,pass total,carry mean,target mean,pass mean,ypc,adot,adot qb,completion pct,carry stdev,target stdev,pass stdev,carry score,target score,passing score\n')
for key in player_dict:
    f.write(player_dict[key].to_csv_output())
f.flush()
f.close()


print(len(player_dict))
print('COMPLETE')