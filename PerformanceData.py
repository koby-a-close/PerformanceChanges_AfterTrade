# PerformanceData.py
# Created 01/07/2020 by KAC

# import warnings filter
from warnings import simplefilter

# ignore all future warnings
simplefilter(action='ignore', category=Warning)

# Load packages
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

from prettytable import PrettyTable
from pybaseball import team_pitching, team_batting

# Team info
df_team_data = pd.ExcelFile('/Users/Koby/PycharmProjects/PerformanceChange_AfterTrade/Input/Teams.xlsx')
df_Teams = df_team_data.parse(sheet_name='Records', header=0)

dict_2017 = dict(zip(df_Teams['Team'], df_Teams['wp2017']))
dict_2018 = dict(zip(df_Teams['Team'], df_Teams['wp2018']))
dict_2019 = dict(zip(df_Teams['Team'], df_Teams['wp2019']))
team_dict = {'2017': dict_2017, '2018': dict_2018, '2019': dict_2019}

# Player info
df_trade_data = pd.ExcelFile('/Users/Koby/PycharmProjects/PerformanceChange_AfterTrade/Input/Trades.xlsx')

# Comparisons for baters
df_2019Batters = df_trade_data.parse(sheet_name='2019Batter', header=0)
df_2018Batters = df_trade_data.parse(sheet_name='2018Batter', header=0)
df_2017Batters = df_trade_data.parse(sheet_name='2017Batter', header=0)
df_Batters = pd.concat([df_2019Batters, df_2018Batters, df_2017Batters], ignore_index=True)
df_Batters['Year'] = df_Batters['Year'].astype(str)

df_Batters['delta_wOBA'] = df_Batters['New wOBA'] - df_Batters['Old wOBA']
df_Batters['delta_wRC+'] = df_Batters['New wRC+'] - df_Batters['Old wRC+']
df_Batters['delta_team_WinPerc'] = np.zeros(shape=(len(df_Batters), 1))

for i in range(len(df_Batters)):
    year = df_Batters['Year'][i]
    old_team = df_Batters['Old Team'][i]
    new_team = df_Batters['New Team'][i]
    old_wp = team_dict[year][old_team]
    new_wp = team_dict[year][new_team]
    df_Batters['delta_team_WinPerc'][i] = new_wp - old_wp

# Plots and regression stats for batters
x_wOBA = df_Batters['delta_wOBA']
x_wRC = df_Batters['delta_wRC+']
y_WinPerc = df_Batters['delta_team_WinPerc']

batter_results_wOBA = sm.OLS(y_WinPerc,sm.add_constant(x_wOBA)).fit()
print(batter_results_wOBA.summary())
plt.scatter(x_wOBA, y_WinPerc)
X_plot = np.linspace(0,1,100)
plt.plot(x_wOBA, batter_results_wOBA.fittedvalues)
plt.show()

batter_results_wRC = sm.OLS(y_WinPerc,sm.add_constant(x_wRC)).fit()
print(batter_results_wRC.summary())
plt.scatter(x_wRC, y_WinPerc)
X_plot = np.linspace(0,1,100)
plt.plot(x_wRC, batter_results_wRC.fittedvalues)
plt.show()

# Comparisons for pitchers
df_2019Pitchers = df_trade_data.parse(sheet_name='2019Pitcher', header=0)
df_2018Pitchers = df_trade_data.parse(sheet_name='2018Pitcher', header=0)
df_2017Pitchers = df_trade_data.parse(sheet_name='2017Pitcher', header=0)
df_Pitchers = pd.concat([df_2019Pitchers, df_2018Pitchers, df_2017Pitchers], ignore_index=True)
df_Pitchers['Year'] = df_Pitchers['Year'].astype(str)

df_Pitchers['delta_FIP-'] = df_Pitchers['New FIP-'] - df_Pitchers['Old FIP-']
df_Pitchers['delta_SIERA'] = df_Pitchers['New SIERA'] - df_Pitchers['Old SIERA']
df_Pitchers['delta_team_WinPerc'] = np.zeros(shape=(len(df_Pitchers), 1))

for i in range(len(df_Pitchers)):
    year = df_Pitchers['Year'][i]
    old_team = df_Pitchers['Old Team'][i]
    new_team = df_Pitchers['New Team'][i]
    old_wp = team_dict[year][old_team]
    new_wp = team_dict[year][new_team]
    df_Pitchers['delta_team_WinPerc'][i] = new_wp - old_wp

x_FIP = df_Pitchers['delta_FIP-']
x_SIERA = df_Pitchers['delta_SIERA']
y_WinPercentage = df_Pitchers['delta_team_WinPerc']

pitcher_results_FIP = sm.OLS(y_WinPercentage,sm.add_constant(x_FIP)).fit()
print(pitcher_results_FIP.summary())
plt.scatter(x_FIP, y_WinPercentage)
X_plot = np.linspace(0,1,100)
plt.plot(x_FIP, pitcher_results_FIP.fittedvalues)
plt.show()

pitcher_results_SIERA = sm.OLS(y_WinPercentage,sm.add_constant(x_SIERA)).fit()
print(pitcher_results_SIERA.summary())
plt.scatter(x_SIERA, y_WinPercentage)
X_plot = np.linspace(0,1,100)
plt.plot(x_SIERA, pitcher_results_SIERA.fittedvalues)
plt.show()

