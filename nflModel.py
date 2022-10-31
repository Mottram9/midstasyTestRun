##Load packages
import pandas as pd
from enum import Flag
from statistics import mean, stdev 
# import matplotlib as mpl 
# import matplotlib.pyplot as plt
# from pandasgui import show

use_local = True

if use_local:
    data = pd.read_csv('2021playbyplay.csv.gz', compression = 'gzip', low_memory = False)
else:
    YEAR = 2022
    data = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp/'\
                    'play_by_play_' + str(YEAR) + '.csv.gz',
                    compression= 'gzip', low_memory= False)

data = data.loc[data.season_type=='REG']

player_dict = {}

class PlayerType(Flag):
    RB = 1
    WR = 2
    QB = 4
    
class PlayerClass:
    
    completed_pass_count = 0
    total_pass_count = 0
    rb_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rb_rz_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    wr_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    wr_rz_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    qb_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    qb_rz_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
    def __init__(self, id, name, team):
        self.id = id
        self.name = name
        self.team = team
        
    def __str__(self) -> str:
        return f'{self.name}, {self.team}: {self.get_bindex_rb()}, {self.get_bindex_wr()}, {self.get_bindex_qb()}'
    
    def update_type(self, type):
        if hasattr(self, 'type'):
            self.type |= type
        else:
            self.type = type
    
    def add_rb_value(self, week):
        self.rb_values[week - 1] += 1
        self.update_type(PlayerType.RB)

    def add_rb_rz (self, week):
        self.rb_rz_values[week - 1] += 1
        self.update_type(PlayerType.RB)
        
    def add_wr_value(self, week):
        self.wr_values[week - 1] += 1
        self.update_type(PlayerType.WR)

    def add_wr_rz (self, week):
        self.wr_rz_values[week - 1] += 1
        self.update_type(PlayerType.WR)
        
    def add_qb_value(self, week, completed):
        self.qb_values[week - 1] += 1
        self.update_type(PlayerType.QB)
        
        if completed:
            completed_pass_count = completed_pass_count + 1
        
        total_pass_count = total_pass_count + 1
            

    def add_qb_rz (self, week):
        self.qb_rz_values[week - 1] += 1
        self.update_type(PlayerType.QB)
        
    def get_stdev_rb(self):
        return stdev(self.rb_values)

    def get_mean_rb(self):
        return mean(self.rb_values)

    def get_total_rb(self):
        return sum(self.rb_values)

    def get_bindex_rb (self):
        return (0.5*mean(self.rb_values))+(2*mean(self.rb_rz_values))+(0.03*sum(self.rb_values))

    def get_bindex_qb (self):
        return (0.2*mean(self.qb_values))+(1.5*mean(self.qb_rz_values))+(0.03*sum(self.qb_values))

    def get_bindex_wr (self):
        return (mean(self.wr_values))+(2.5*mean(self.wr_rz_values))+(0.06*sum(self.wr_values))
        
    def get_stdev_wr(self):    
        return stdev(self.wr_values)

    def get_total_wr(self):
        return sum(self.wr_values)

    def get_mean_wr(self):
        return mean(self.wr_values)
    
    def get_stdev_qb(self):
        return stdev(self.qb_values)

    def get_total_qb(self):
        return sum(self.qb_values)

    def get_mean_qb(self):
        return mean(self.qb_values)
   
    def get_completed_pass_percent(self):
        return self.completed_pass_count / self.total_pass_count
   
    def is_type(self, player_type):
        return self.type & player_type == player_type

    def to_csv_output(self):
        return f'{self.name},{self.team},{self.get_bindex_rb()},{self.get_bindex_wr()},{self.get_bindex_qb()}\n'
    
   ##FIX def to_csv_output(self):
        ##return f'{self.name},{self.team},{self.get_type_string()},{self.get_bindex_rb()+self.get_bindex_wr()+self.get_bindex_qb()}\n'
        
def try_add_player(id, name, team):
    if id not in player_dict:
        player_dict[id] = PlayerClass(id, name, team)
        
def try_add_wr(csv_row):
    if pd.isna(csv_row.receiver_id) == False:
        try_add_player(csv_row.receiver_id, csv_row.receiver, csv_row.posteam)
        player_dict[csv_row.receiver_id].add_wr_value(csv_row.week)

def try_add_rb(csv_row):
    if pd.isna(csv_row.rusher_id) == False:
        try_add_player(csv_row.rusher_id, csv_row.rusher, csv_row.posteam)
        player_dict[csv_row.rusher_id].add_rb_value(csv_row.week)

def try_add_rb_rz(csv_row):
    if pd.isna(csv_row.rusher_id) == False:
        if csv_row.yardline_100<=20:
            try_add_player(csv_row.rusher_id, csv_row.rusher, csv_row.posteam)
            player_dict[csv_row.rusher_id].add_rb_rz(csv_row.week)
    
def try_add_qb(csv_row):
    if pd.isna(csv_row.passer_player_id) == False:
        try_add_player(csv_row.passer_player_id, csv_row.passer_player_name, csv_row.posteam)
        player_dict[csv_row.passer_player_id].add_qb_value(csv_row.week, csv_row.is_completed)

def try_add_qb_rz(csv_row):
    if pd.isna(csv_row.passer_player_id) == False:
        if csv_row.yardline_100<=20:
            try_add_player(csv_row.passer_player_id, csv_row.passer_player_name, csv_row.posteam)
            player_dict[csv_row.passer_player_id].add_qb_rz(csv_row.week)

def try_add_wr_rz(csv_row):
    if pd.isna(csv_row.receiver_id) == False:
        if csv_row.yardline_100<=20:
            try_add_player(csv_row.receiver_id, csv_row.receiver, csv_row.posteam)
            player_dict[csv_row.receiver_id].add_wr_rz(csv_row.week)
        
for _, value in data.iterrows():
    try_add_wr(value)
# for _, value in data.iterrows():
    try_add_rb(value)
# for _, value in data.iterrows():
    try_add_qb(value)
# for _, value in data.iterrows():
    try_add_rb_rz(value)
# for _, value in data.iterrows():
    try_add_qb_rz(value)
# for _, value in data.iterrows():
    try_add_wr_rz(value)    
    
    
f = open('test_nflmodel.csv', 'w')
f.write('player,team,carry score,target score,passing score\n')
for key in player_dict:
    f.write(player_dict[key].to_csv_output())
f.flush()
f.close()

print(len(player_dict))
print('COMPLETE')

# WRTable1 = pd.DataFrame(WRdictTest)
# WRTable1 = WRTable1.T
# WRTable2 = pd.DataFrame(WRTable1.mean(axis = 1))
# WRTable3 = pd.DataFrame(WRTable1.std(axis = 1))
# WRTable4 = pd.DataFrame(WRTable1.sum(axis = 1))
# WRTable1['total'] = WRTable4
# WRTable1['mean'] = WRTable2
# WRTable1['stdev'] = WRTable3
# # WRTable1['RZmean'] = RZ_WRTable2
# # WRTable1['RZstdev'] = RZ_WRTable3
# show(WRTable1)










##Statistics example

# for key in WRdictTest:
#     print(key)
#     print(stdev(WRdictTest[key]))
#     print(sum(WRdictTest[key]))

##Create and fill the RB Dictionary for weekly carries array

# RBdictTest = {}

# for k, val in data.iterrows():
#     if pd.isna(val.rusher)==False:
#         if (val.rusher) in RBdictTest:
#             pass
#         else:
#             RBdictTest[val.rusher] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#         RBdictTest[val.rusher][val.week-1] +=1

##Statistics example

# for k in RBdictTest:
#     print(k)
#     print(stdev(RBdictTest[k]))
#     print(sum(RBdictTest[k]))

##Create and fill Redzone WR dictionary for weekly targets array

# RZdata = data.loc[data.yardline_100 <= 20]

# RZ_WRdictTest = {}

# for RZkey, RZvalue in RZdata.iterrows():
#     if pd.isna(RZvalue.receiver)==False:
#         if (RZvalue.receiver) in RZ_WRdictTest:
#             pass
#         else:
#             RZ_WRdictTest[RZvalue.receiver] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#         RZ_WRdictTest[RZvalue.receiver][RZvalue.week-1] +=1

##Create and fill Redzone RB dictionary for weekly carries array

# RZ_RBdictTest = {}

# for RZk, RZval in RZdata.iterrows():
#     if pd.isna(RZval.rusher)==False:
#         if (RZval.rusher) in RZ_RBdictTest:
#             pass
#         else:
#             RZ_RBdictTest[RZval.rusher] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#         RZ_RBdictTest[RZval.rusher][RZval.week-1] +=1


##Search Engines for weekly Carries or Targets ALL & REDZONE

# print(WRdictTest.get(''))
# print(RBdictTest.get(''))
# print(RZ_WRdictTest.get(''))
# print(RZ_RBdictTest.get('Ja.Williams'))

##Convert to dataframe and show table in PandasGUI

# RZ_WRTable1 = pd.DataFrame(RZ_WRdictTest)
# RZ_WRTable1 = RZ_WRTable1.T
# RZ_WRTable2 = pd.DataFrame(RZ_WRTable1.mean(axis = 1))
# RZ_WRTable3 = pd.DataFrame(RZ_WRTable1.std(axis = 1))
# RZ_WRTable4 = pd.DataFrame(RZ_WRTable1.sum(axis = 1))
# RZ_WRTable1['total'] = RZ_WRTable4
# RZ_WRTable1['mean'] = RZ_WRTable2
# RZ_WRTable1['stdev'] = RZ_WRTable3
# show(RZ_WRTable1)

# RZ_RBTable1 = pd.DataFrame(RZ_RBdictTest)
# RZ_RBTable1 = RZ_RBTable1.T
# RZ_RBTable2 = pd.DataFrame(RZ_RBTable1.mean(axis = 1))
# RZ_RBTable3 = pd.DataFrame(RZ_RBTable1.std(axis = 1))
# RZ_RBTable4 = pd.DataFrame(RZ_RBTable1.sum(axis = 1))
# RZ_RBTable1['total'] = RZ_RBTable4
# RZ_RBTable1['mean'] = RZ_RBTable2
# RZ_RBTable1['stdev'] = RZ_RBTable3
# show(RZ_RBTable1)

# WRTable1 = pd.DataFrame(WRdictTest)
# WRTable1 = WRTable1.T
# WRTable2 = pd.DataFrame(WRTable1.mean(axis = 1))
# WRTable3 = pd.DataFrame(WRTable1.std(axis = 1))
# WRTable4 = pd.DataFrame(WRTable1.sum(axis = 1))
# WRTable1['total'] = WRTable4
# WRTable1['mean'] = WRTable2
# WRTable1['stdev'] = WRTable3
# WRTable1['RZmean'] = RZ_WRTable2
# WRTable1['RZstdev'] = RZ_WRTable3
# show(WRTable1)


# RBTable1 = pd.DataFrame(RBdictTest)
# RBTable1 = RBTable1.T
# RBTable2 = pd.DataFrame(RBTable1.mean(axis = 1))
# RBTable3 = pd.DataFrame(RBTable1.std(axis = 1))
# RBTable4 = pd.DataFrame(RBTable1.sum(axis = 1))
# RBTable1['total'] = RBTable4
# RBTable1['mean'] = RBTable2
# RBTable1['stdev'] = RBTable3
# RBTable1['RZmean'] = RZ_RBTable2
# RBTable1['RZstdev'] = RZ_RBTable3
# show(RBTable1)

