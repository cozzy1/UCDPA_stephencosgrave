#!/usr/bin/env python
# coding: utf-8

# In[240]:


import pandas as pd
import bs4 as bs
import urllib.request
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns


# In[241]:


players_list = []
# This is a function to add players
# This allows flexibility to the program. For example if we wanted to add Josh Allen or Patrick Mahomes
# to the conversation, we can recycle this code


# In[242]:


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


# In[243]:


# Add Tom Brady Data Frame


# In[244]:


add_player('df',r"C:\Users\DRPhones41\.jupyter\sportsref_download_TB.csv","Tom Brady") #Call 'Add_Player' function from above

dftb = pd.read_csv("dfname_update.csv") #Read from generic csv

#Need to rename the columns. TD could mean Passing, Rushing or Receiving, so I'm renaming them to help differentiate

dftb.columns = ['Col','Player_Name', 'Rk', 'Year', 'Date', 'Game Number', 'Week', 'Age', 'Tm', 'Location', 'Opp', 'Result',  'GS',
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


# In[245]:


# Add Peyton Manning Data Frame


# In[246]:


add_player('df',r"C:\Users\DRPhones41\.jupyter\sportsref_download_PM.csv","Peyton Manning")
dfpm = pd.read_csv("dfname_update.csv")

#dfpm = dfpm.drop([0],axis = 1)

dfpm.columns = ['Col','Player_Name','Rk','Year','Date', 'Game Number', 'Week', 'Age', 'Tm', 'Location', 'Opp', 'Result','GS',
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


# In[247]:


# Combine the two Data Frames to one big one


# In[248]:


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


# In[249]:


len(np.unique(pd_combined.Year))


# In[250]:


# Webscraping data


# In[251]:


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


# In[252]:


#Format data types
dfws = dfws.astype({
    'Year' : 'int',
    'Winner' : 'string',
    'Runner Up' : 'string'
})

print(dfws)


# In[253]:


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


# In[254]:


# Join the scraped data to the combined dataframe

# Initially tried this - result = pd.concat([pd_combined, dfws], join="outer")
#print(result) - but that did not combine correctly

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


# In[255]:


# Check formatting types
result.dtypes


# In[256]:


# Rename columns and re-format data types within joined dataframe

result.rename(columns = {'Year_x':'Year', 'Year_y':'Year_Join'}, inplace = True)

# The use of % in the original data prevented formatting to happen. Replace % signs with blanks, and then format data types
result = result.replace({'%': ''}, regex=True)

# Format below data types
result = result.astype({
'TeamKey' : 'string',
'Player_Name' : 'string',
'Rk' : 'int',
'Year' : 'int',
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


# In[257]:


result.head()


# In[258]:


# Based on the above dataframe, i set out to create some charts to illustrate the respective careers of both players
# in relation to each other


# In[259]:


# Charts below will show 0 values where a player missed an entire season.  To replace these 0 values with 'None' would
# cause the above table to stop working - "Cannot convert non-finite values (NA or inf) to integer"


# In[260]:


sns.scatterplot(x="Rk", y="Passing Yds", hue="Player_Name", data=result)

plt.title("Yards per game")
plt.xlabel = ('Passing Yards')
plt.ylabel = ('Games')
fig.set_size_inches(12, 8)


# In[261]:


# This chart illustrates the unpredictability of the league, from one game to the next - for both players - with
# wildly different passing yards from game-to-game


# In[262]:


sns.lineplot(x="Year", y="Passing TD", hue="Player_Name", data=result)
         
plt.title("Passing Touchdowns per game")
plt.show()


# In[263]:


# This shows us that Peyton Manning was always capable of great TD seasons, and always scored highly, whereas Tom Brady was
# never as prolific, in that regard

# While a statistically brilliant season, in which he threw for 55 Touchdowns, the 2013-14 season saw Peyton Manning
# fall to the Seattle Seahawks in the Superbowl


# In[264]:


sns.lineplot(x='Year', y='Passing Att', data=result,
          #fit_reg=False,
          hue='Player_Name',
          #col = 'Year',
          #col_order='Year',
          #row = 'Player_Name'
          )
plt.show()

sns.lineplot(x='Year', y='Passing Cmp', data=result,
          #fit_reg=False,
          hue='Player_Name',
          #col = 'Year',
          #col_order='Year',
          #row = 'Player_Name'
          )
plt.show()


# In[265]:


# The above two graphs show remarkable consistency in relation to Passing Attempts to Completions.  This shows us
# that both QBs were capable of producing, regardless of the state of their receiving corps, or Offensive Lines

# The most noteworthy thing from this graph, is that Tom Brady's passing attempts have risen, as he's gotten older.
# Generally, a QBs arm capacity/strength decreases with age, and he is tasked with throwing less, but Brady has bucked 
# that trend


# In[ ]:





# In[266]:


sns.lmplot(x='Year', y='Passing Cmp%', data=result,
          #fit_reg=False,
          hue='Player_Name',
          #col = 'Year',
          #col_order='Year',
          #row = 'Player_Name'          
          )
plt.show()


# In[267]:


playerlabel1 = ""

yearlyplayers = []
yearlyyears = []
YearlyPassingYds = []
YearlyPassingAtt = []
YearlyPassingCmp = []
YearlyPassingCmpPct = []
YearlyPassingYPA = []

CareerPassingYds = []
CareerPassingAtt = []
CareerPassingCmp = []
CareerPassingCmpPct = []

# Formula template to get the Yards Per statistics
# n and d are just variable names, used in Stack Overflow. Where the formula is dividing by zero, return zero, this stops 
# errors from occurring

def getperstats(n, d):
    return n / d if d else 0

# For each player in our players_list (from the template at the very top). Go through them one by one
# Create all the variables for year and career. Year ones will help go through the result DF
# Once it moves on to a new player, these will reset to zero because theyre IN the for loop

for pl in players_list:
    new_year = 1
    year1 = 0
    year2 = 0
    yearm1 = 0
    yearp1 = 0
   
    i_yearlypassingyds = 0
    i_yearlypassingatt = 0
    i_yearlypassingcmp = 0
    i_yearlypassingtd = 0
    i_yearlypassingypa = 0
   
    i_careerpassingyds = 0
    i_careerpassingatt = 0
    i_careerpassingcmp = 0
    i_careerpassingtd = 0
   
   
    for row4 in result.index:
        playerlabel1 = result.iloc[row4]['Player_Name']
        passingyardslabel = result.iloc[row4]['Passing Yds']
        rushingydslabel = result.iloc[row4]['Rushing Yds']
           
# If the player in results is equal to the player name from the players list, tally up career stats
        if pl == playerlabel1:
            
            i_careerpassingyds = i_careerpassingyds + result.iloc[row4]['Passing Yds']
            i_careerpassingatt = i_careerpassingatt + result.iloc[row4]['Passing Att']
            i_careerpassingcmp = i_careerpassingcmp + result.iloc[row4]['Passing Cmp']
            i_careerpassingtd = i_careerpassingtd + result.iloc[row4]['Passing TD']

            year2 = year1
            year1 = result.iloc[row4]['Year']
            yearm1 = year1-1
           
            if year1!=year2:

                i_yearlypassingypa= getperstats(i_yearlypassingyds,i_yearlypassingatt)

               
                yearlyyears.append(yearm1)
                yearlyplayers.append(playerlabel1)
                #yearlyyears.append(year1)
                YearlyPassingYds.append(i_yearlypassingyds)
                YearlyPassingAtt.append(i_yearlypassingatt)
                YearlyPassingCmp.append(i_yearlypassingcmp)
                YearlyPassingYPA.append(i_yearlypassingypa)

               
                i_yearlypassingyds = result.iloc[row4]['Passing Yds']
                i_yearlypassingatt = result.iloc[row4]['Passing Att']
                i_yearlypassingcmp = result.iloc[row4]['Passing Cmp']
                #i_yearlypassingypa = result.iloc[row4]['Passing Y/A']
            elif year1==year2:
                i_yearlypassingyds = i_yearlypassingyds + result.iloc[row4]['Passing Yds']
                i_yearlypassingatt = i_yearlypassingatt + result.iloc[row4]['Passing Att']
                i_yearlypassingcmp = i_yearlypassingcmp + result.iloc[row4]['Passing Cmp']
                #i_yearlypassingypa = i_yearlypassingypa + result.iloc[row4]['Passing Y/A']

               
    print(pl)
    print(i_yearlypassingyds)
    
    CareerPassingYds.append(i_careerpassingyds)
    CareerPassingAtt.append(i_careerpassingatt)
    CareerPassingCmp.append(i_careerpassingcmp)

    i_careerpassingpct = round(i_careerpassingcmp/i_careerpassingatt,2)
    CareerPassingCmpPct.append(i_careerpassingpct)


# In[268]:


#Create dictionaries for all players using the lists populated above

careerdict = { 'Name' :  players_list,
             'PassYds' : CareerPassingYds,
             'PassAtt' : CareerPassingAtt,
             'PassCmp' : CareerPassingCmp,
             'PassRte' : CareerPassingCmpPct

             }


# In[269]:


yearlydict = { 'Name' :  yearlyplayers,
             'Years': yearlyyears,
             'PassYds' : YearlyPassingYds,
             'PassAtt' : YearlyPassingAtt,
             'PassCmp' : YearlyPassingCmp,
             'PassYPA' : YearlyPassingYPA

             }


# In[270]:


#Create dataframes from those dictionaries

careerddf = pd.DataFrame(careerdict)
careerddf.head()


# In[271]:


yearlydf = pd.DataFrame(yearlydict)
yearlydf.head()


# In[272]:


print(yearlydf)


# In[273]:


print("---------------------------------------------------------")
print("--------------------END OF TOTALS------------------------")
print("---------------------------------------------------------")


# In[274]:


statssum = result[['Player_Name','Year','Passing Att','Passing Cmp','Passing Yds','Passing TD','Passing Int']].groupby('Player_Name').sum()
statsmean = round(result[['Player_Name','Year','Passing Att','Passing Cmp','Passing Yds','Passing TD','Passing Int']].groupby('Player_Name').mean(),2)
statsmedian = result[['Player_Name','Year','Passing Att','Passing Cmp','Passing Yds','Passing TD','Passing Int']].groupby('Player_Name').median()


# In[275]:


print("SUM STATISTICS........................")
print(statssum)
print("MEAN STATISTICS........................")
print(statsmean)
print("MEDIAN STATISTICS........................")
print(statsmedian)


# In[276]:


# Get sum of all rows as a new row in Dataframe
total = result.sum()
total.name = 'Total'
# Assign sum of all rows of DataFrame as a new Row
total = total.append(total.transpose())
print(total)

print("---------------------------------------------------------")
print("--------------------END OF STATS-------------------------")
print("---------------------------------------------------------")


# In[277]:


total.head()


# In[278]:


sns.lineplot(x='Years',
            y='PassYPA',
            data=yearlydf,
             hue='Name'
            #fit_reg=False,
            #col = 'Year',
            #col_order='Year',
            #row = 'Player_Name'
          )
plt.show()


# In[279]:


sns.lmplot(x='Year',
          y='Passing Cmp%',
          data=result,
          hue='Player_Name'      
          )
plt.show()


# In[280]:


sns.barplot(x = 'PassYds',
            y = 'Name',
            hue = 'Name',
            data = careerddf
           )

plt.show()


# In[281]:


sns.scatterplot(x = 'PassYds',
            y = 'Name',
            hue = 'Name',
            data = careerddf)
plt.show()


# In[282]:


sns.lmplot(x='Years',
          y='PassYPA',
          data=yearlydf,
          hue='Name'      
          )
plt.show()

print("------------------------------------------------GRAPHS---------------------------")


# In[283]:


sns.pairplot(careerddf, hue ='Name')
# to show
plt.show()


# In[284]:


sns.pairplot(yearlydf, hue ='Name')
# to show
plt.show()


# In[285]:


yearlydict2 = { 'Name' :  yearlyplayers,
             'PassAtt' : YearlyPassingAtt
             
             }

yearlydf2 = pd.DataFrame(yearlydict2)
yearlydf2.head()

sns.pairplot(yearlydf2, hue ='Name')
# to show
plt.show()


# In[ ]:





# In[ ]:




