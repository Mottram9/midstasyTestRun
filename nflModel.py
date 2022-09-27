##Load packages

import pandas as pd

from statistics import mean, stdev 

import matplotlib as mpl 

import matplotlib.pyplot as plt

from pandasgui import show

##Read 2021 play by play dataset

data = pd.read_csv('2021playbyplay.csv.gz', compression = 'gzip', low_memory = False)

##Filter for regular season only

data = data.loc[data.season_type=='REG']

##Create and fill the WR Dictionary for weekly targets array

WRdictTest = {}
dictNames = {}
WRrankList = {}

for key, value in data.iterrows():
    if pd.isna(value.receiver_id)==False:
        if (value.receiver_id) in WRdictTest:
            pass
        else:
            WRdictTest[value.receiver_id] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dictNames[value.receiver_id] = value.receiver
        WRdictTest[value.receiver_id][value.week-1] +=1
        for key in WRdictTest:
            print(dictNames[key])




    





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


print('COMPLETE')


