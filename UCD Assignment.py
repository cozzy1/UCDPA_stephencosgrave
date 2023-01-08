#!/usr/bin/env python
# coding: utf-8

# In[490]:


import pandas as pd
import bs4 as bs
import urllib.request
import numpy as np
import csv
import matplotlib.pyplot as plt


# In[491]:


players_list = []
# Function to add player
# This allows flexibility to the program. For example if we wanted to add Josh Allen or Patrick Mahomes
# to the conversation, we can recycle this code


# In[492]:


def add_player (dfname,link,player):

    dfname = pd.read_csv(link)
    
    dflength = (len(dfname) -1) 
    dfname = dfname[0:dflength] #Removes totals from bottom
    
    new_header = dfname.iloc[0] #grab the first row for the header
    dfname = dfname[1:dflength] #take the data less the header row
    dfname.columns = new_header #set the header row as the df header

    dfname.insert(0,"Player_Name", player) #Add player ID column
    players_list.append(player) #Add player name to list
    dfname.to_csv("dfname_update.csv") #export to generic csv
    
    print(players_list)
    print("---------------------------------------------------------")
    print("---------------------END OF FUNCTION---------------------")
    print("---------------------------------------------------------")


# In[493]:


# Add Tom Brady Data Frame


# In[494]:


add_player('df',r"C:\Users\DRPhones41\.jupyter\sportsref_download_TB.csv","Tom Brady") #Call 'Add_Player' function from above

dftb = pd.read_csv("dfname_update.csv") #Read from generic csv

#Need to rename the columns. TD could mean Passing, Rushing or Receiving, so I'm renaming them
dftb.columns = ['First_Column','Player_Name', 'Rk', 'Year', 'Date', 'Game Number', 'Week', 'Age', 'Tm', 'Location', 'Opp', 'Result',  'GS',
                'Passing Cmp',  'Passing Att',  'Passing Cmp%', 'Passing Yds', 'Passing TD', 'Passing Int', 'Passing Rate',  'Passing Sk', 'Passing Yds_1', 'Passing Y/A', 'Passing AY/A',
                'Rushing Att', 'Rushing Yds',  'Rushing Y/A',  'Rushing TD',
                'Receiving Tgt', 'Receiving Rec', 'Receiving Yds',  'Receiving Y/R','Receiving TD','Receiving Ctch%','Receiving Y/Tgt', 'Scoring TD', 'Scoring Pts', 'Scoring Sk',
                'Tackle Solo', 'Tackle Ast', 'Tackle Comb', 'Tackle TFL', 'Tackle QBHits',
                'Fumble Fmb', 'Fumble FL', 'Fumble FF', 'Fumble FR', 'Fumble Yds', 'Fumble TD',
                'Punting Pnt','Punting Yds', 'Punting Y/P','Punting RetYds','Punting Net','Punting NY/P','Punting TB','Punting TB%','Punting In20', 'Punting In20%','Punting Blck',
                'Off Snap Num', 'Off Snap Pct',
                'Def Snap Num', 'Def Snap Pct',
                'St Snap Num', 'St Snap Pct',
                'Status']


#Delete rows to match up
dftb = dftb.drop(dftb.columns[[35, 36, 37, 38 ,39, 40, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]],axis = 1)
# Removing column 64, as 'status' is not required, and its inclusion causes errors

print(dftb.columns)
dftb.to_csv('dftb_update.csv')        

print("---------------------------------------------------------")
print("---------------------END OF TOM BRADY--------------------")
print("---------------------------------------------------------")


# In[495]:


# Add Peyton Manning Data Frame


# In[496]:


add_player('df',r"C:\Users\DRPhones41\.jupyter\sportsref_download_PM.csv","Peyton Manning")
dfpm = pd.read_csv("dfname_update.csv")

#dfpm = dfpm.drop([0],axis = 1)

dfpm.columns = ['First_Column','Player_Name','Rk','Year','Date', 'Game Number', 'Week', 'Age', 'Tm', 'Location', 'Opp', 'Result','GS',
                'Passing Cmp','Passing Att','Passing Cmp%', 'Passing Yds','Passing TD','Passing Int','Passing Rate','Passing Sk','Passing Yds_1','Passing Y/A','Passing AY/A',
                'Rushing Att','Rushing Yds','Rushing Y/A','Rushing TD',
                'Receiving Tgt','Receiving Rec', 'Receiving Yds','Receiving Y/R', 'Receiving TD', 'Receiving Ctch%', 'Receiving Y/Tgt',
                'Scoring TD','Scoring Pts',
                'Fumble Fmb','Fumble FL', 'Fumble FF', 'Fumble FR', 'Fumble Yds', 'Fumble TD',
                'Off Snap Num',	'Off Snap Pct',
                'Def Snap Num', 'Def Snap Pct',
                'St Snap Num', 'St Snap Pct',
                'Status']


#Delete rows to match up
dfpm = dfpm.drop(dfpm.columns[[47]],axis = 1)
print(dfpm)
dfpm.to_csv('dfpm_update.csv')

print("---------------------------------------------------------")
print("---------------------END OF PEYTON MANNING---------------")
print("---------------------------------------------------------")


# In[497]:


# Combine the two Data Frames to one big one


# In[498]:


#Combine to one data frame
pd_combined = pd.concat([dftb, dfpm])

#Replace null values and change special characters in 'Location' column
pd_combined["Location"].fillna('H', inplace = True)
pd_combined["Location"] = pd_combined["Location"].replace("@","A")

#Replace null values and change special characters in 'Played' column
pd_combined["GS"].fillna('Played', inplace = True)
pd_combined[['GS']] = pd_combined[['GS']].replace({'\*': 'Played'}, regex=True)

#Replace all other null values with zero.
pd_combined.fillna("0", inplace = True)

#Format below data types
pd_combined = pd_combined.astype({
'Year' : 'string',
'Week' : 'string',
'Tm' : 'string',
'Location' : 'string',
'Opp' : 'string',
'Result' : 'string',
'GS' : 'string'
})

#Get GameID for PD_Combined data frame
pdc_row_count = 0
game_key_pdc = []
pdc_game_key = ""

for t in pd_combined.itertuples():
    yearvalue_pdc = pd_combined.iloc[pdc_row_count]['Year']
    teamvalue_pdc = pd_combined.iloc[pdc_row_count]['Tm']
    pdc_row_count = pdc_row_count + 1

    pdc_game_key = teamvalue_pdc + yearvalue_pdc
    game_key_pdc.append(pdc_game_key)

pd_combined.insert(0,"TeamKey", game_key_pdc)


#Print and export to test
print(pd_combined)
pd_combined.to_csv('pd_combined.csv')

print("---------------------------------------------------------")
print("---------------------END OF COMBINED FRAME---------------")
print("---------------------------------------------------------")


# In[499]:


# Webscraping data


# In[500]:


#Webscrape from below URL
source = urllib.request.urlopen('https://www.skysports.com/nfl/news/34693/10735320/list-of-nfl-super-bowl-winners').read()
soup = bs.BeautifulSoup(source,'lxml')

table = soup.table
table = soup.find('table')
table_rows = table.find_all('tr')
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
   
dfws = pd.read_html(str(table))[0]
print(type(dfws))


# In[501]:


#Format data types
dfws = dfws.astype({
    'Year' : 'int',
    'Winner' : 'string',
    'Runner Up' : 'string'
})

print(dfws)


# In[502]:


#Get GameID for dfws data frame
season = []
winners_short = []
game_key = []

irow = 0
name_long = ""
champion = ""
for row1 in dfws.itertuples():
    #Superbowl happens in calendar year of prior season so new column is needed
    name_long = dfws.iloc[irow]['Winner']
    if name_long == "Tampa Bay Buccaneers":
        winners_short.append("TAM")
        champion = "TAM"
    elif name_long == "New England Patriots":
        winners_short.append("NWE")
        champion = "NWE"
    elif name_long == "New England":
        winners_short.append("NWE")
        champion = "NWE"
    elif name_long == "Denver Broncos":
        winners_short.append("DEN")
        champion = "DEN"
    elif name_long == "Indianapolis Colts":
        winners_short.append("IND")
        champion = "IND"
    elif name_long == "Arizona Cardinals":
        winners_short.append("ARI")
        champion = "ARI"
    elif name_long == "Chicago Bears":
        winners_short.append("CHI")
        champion = "CHI"
    elif name_long == "Green Bay Packers":
        winners_short.append("GNB")
        champion = "GNB"
    elif name_long == "New York Giants":
        winners_short.append("NYG")
        champion = "NYG"
    elif name_long == "Detroit Lions":
        winners_short.append("DET")
        champion = "DET"
    elif name_long == "Washington Commanders":
        winners_short.append("WAS")
        champion = "WAS"
    elif name_long == "Philadelphia Eagles":
        winners_short.append("PHI")
        champion = "PHI"
    elif name_long == "Pittsburgh Steelers":
        winners_short.append("PIT")
        champion = "PIT"
    elif name_long == "Los Angeles Rams":
        winners_short.append("LAR")
        champion = "LAR"
    elif name_long == "San Francisco 49ers":
        winners_short.append("SFO")
        champion = "SFO"
    elif name_long == "Cleveland Browns":
        winners_short.append("CLE")
        champion = "CLE"
    elif name_long == "Dallas Cowboys":
        winners_short.append("DAL")
        champion = "DAL"
    elif name_long == "Kansas City Chiefs":
        winners_short.append("KAN")
        champion = "KAN"
    elif name_long == "Los Angeles Chargers":
        winners_short.append("LAC")
        champion = "LAC"
    elif name_long == "Denver Broncos":
        winners_short.append("DEN")
        champion = "DEN"
    elif name_long == "New York Jets":
        winners_short.append("NYJ")
        champion = "NYJ"
    elif name_long == "Las Vegas Raiders":
        winners_short.append("LVR")
        champion = "LVR"
    elif name_long == "Tennessee Titans":
        winners_short.append("TEN")
        champion = "TEN"
    elif name_long == "Buffalo Bills":
        winners_short.append("BUF")
        champion = "BUF"
    elif name_long == "Minnesota Vikings":
        winners_short.append("MIN")
        champion = "MIN"
    elif name_long == "Atlanta Falcons":
        winners_short.append("ATL")
        champion = "ATL"
    elif name_long == "Miami Dolphins":
        winners_short.append("MIA")
        champion = "MIA"
    elif name_long == "New Orleans Saints":
        winners_short.append("NOR")
        champion = "NOR"
    elif name_long == "Cincinnati Bengals":
        winners_short.append("CIN")
        champion = "CIN"
    elif name_long == "Seattle Seahawks":
        winners_short.append("SEA")
        champion = "SEA"
    elif name_long == "Carolina Panthers":
        winners_short.append("CAR")
        champion = "CAR"
    elif name_long == "Jacksonville Jaguars":
        winners_short.append("JAX")
        champion = "JAX"
    elif name_long == "Baltimore Ravens":
        winners_short.append("BAL")
        champion = "BAL"
    elif name_long == "Houston Texans":
        winners_short.append("HOU")
        champion = "HOU"
    else:
        winners_short.append("Default")
        champion = ""
   
    winners_short_tuple = tuple(winners_short)
   
    yearvalue = dfws.iloc[irow]['Year']
    irow = irow +1
    newseason = yearvalue-1
    season.append(newseason)

    teamkey = str(champion)+str(yearvalue)
    game_key.append(teamkey)

    game_key_tuple = tuple(game_key)
    
    #Drop unrelated columns
dfws = dfws.drop(columns=['Number','Attendance','Location','Winners Share','Final Score'])
   

dfws.insert(1,"Season", season)
dfws.insert(2,"Name_Short", winners_short)
dfws.insert(0,"Team_key", game_key_tuple)

print(game_key_tuple)
print(dfws)


print("---------------------------------------------------------")
print("---------------------END OF Webscrape--------------------")
print("---------------------------------------------------------")


# In[503]:


#df2 = dfws.iloc[1]['Year']

#result = pd.concat([pd_combined, dfws], join="outer")
#print(result)

result = pd_combined.merge(
    dfws,
    left_on = "TeamKey",
    right_on = "Team_key",
    how = "left"
    )
#Replace null values and change special characters in 'Location' column
#Replace all other null values with zero. 
result.fillna("0", inplace = True)

print("---------------------------------------------------------")
print("---------------------END OF JOIN-------------------------")
print("---------------------------------------------------------")


# In[504]:


result.rename(columns = {'Year_x':'Year', 'Year_y':'Year_Join'}, inplace = True)

#This took forever to figure out. % in the original data prevented formatting to happen. Replace % signs with nothing
result = result.replace({'%': ''}, regex=True)

#Format below data types
result = result.astype({
'TeamKey' : 'string',
'Player_Name' : 'string',
'Rk' : 'string',
'Year' : 'string',
'Date' : 'string',
'Game Number' : 'string',
'Week' : 'string',
'Age' : 'string',
'Tm' : 'string',
'Location' : 'string',
'Opp' : 'string',
'Result' : 'string',
'GS' : 'string',
'Passing Cmp' : 'float',
'Passing Att' : 'int',
'Passing Cmp%' : 'float',
'Passing Yds' : 'int',
'Passing TD' : 'int',
'Passing Int' : 'int',
'Passing Rate' : 'float',
'Passing Sk' : 'int',
'Passing Yds_1' : 'int',
'Passing Y/A' : 'float',
'Passing AY/A' : 'float',
'Rushing Att' : 'int',
'Rushing Yds' : 'int',
'Rushing Y/A' : 'float',
'Rushing TD' : 'int',
'Receiving Tgt' : 'int',
'Receiving Rec' : 'int',
'Receiving Yds' : 'int',
'Receiving Y/R' : 'float',
'Receiving TD' : 'int',
'Receiving Ctch%' : 'float',
'Receiving Y/Tgt' : 'float',
'Scoring TD' : 'int',
'Scoring Pts' : 'int',
'Fumble Fmb' : 'int',
'Fumble FL' : 'int',
'Fumble FF' : 'int',
'Fumble FR' : 'int',
'Fumble Yds' : 'int',
'Fumble TD' : 'int',
'Off Snap Num' : 'int',
'Off Snap Pct' : 'float',
'Def Snap Num' : 'int',
'Def Snap Pct' : 'float',
'St Snap Num' : 'int',
'St Snap Pct' : 'float',
'Team_key' : 'string',
'Season' : 'string',
'Name_Short' : 'string',
'Winner' : 'string',
'Runner Up' : 'string',
'MVP' : 'string'
})

print(result)
result.to_csv('result_JOIN.csv')


# In[505]:


result.head()


# In[506]:


statssum = result[['Player_Name','Year','Passing Att','Passing Cmp','Passing Yds','Passing TD','Passing Int']].groupby('Player_Name').sum()
print(statssum)


# In[507]:


statsmean = result[['Player_Name','Year','Passing Att','Passing Cmp','Passing Yds','Passing TD','Passing Int']].groupby('Player_Name').mean()
print(statsmean)


# In[ ]:




