#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import bs4 as bs
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# In[30]:


#To compare stats for Tom Brady and Peyton Manning, two of the greatest Quarterbacks to ever play in the NFL


# In[ ]:


# I have created csv files with the required data, using information found on Pro Football Reference, for both players
# I will import both of these, and merge them together, to create a data table containing information on both of
# their careers


# In[31]:


#Import Tom Brady game data and add column for Player Name

dftb = pd.read_csv(r"C:\Users\DRPhones41\.jupyter\Tom_Brady_Data .csv")
dftb.insert(0,"Player_Name", "Tom Brady")


# In[32]:


dftb.head()


# In[33]:


#print to test

print(dftb)


# In[34]:


#Import Peyton Manning game data and add column for Player Name

dfpm = pd.read_csv(r"C:\Users\DRPhones41\.jupyter\Peyton_Manning_Data.csv")
dfpm.insert(0,"Player_Name", "Peyton Manning")


# In[35]:


#print to test

print(dfpm)


# In[36]:


#Combine to one data frame

pd_combined = pd.concat([dftb, dfpm])


# In[37]:


pd_combined.head()


# In[38]:


#Replace null values and change special characters in 'Location' column

pd_combined["Location"].fillna('H', inplace = True)
pd_combined["Location"] = pd_combined["Location"].replace("@","A")


# In[39]:


pd_combined.head()


# In[40]:


#Replace all other null values with zero

pd_combined.fillna("0", inplace = True)
pd_combined.head()


# In[41]:


#Format data types

pd_combined = pd_combined.astype({
'Year' : 'string',
'Week' : 'string',
'Tm' : 'string',
'Location' : 'string',
'Opp' : 'string',
'Result' : 'string',
'GS' : 'string'
})


# In[43]:


print(pd_combined)


# In[58]:


#Get GameID for PD_Combined data frame

pdc_row_count = 0
game_key_pdc = []
pdc_game_key = ""


# In[59]:


for t in pd_combined.itertuples():
    yearvalue_pdc = pd_combined.iloc[pdc_row_count]['Year']
    teamvalue_pdc = pd_combined.iloc[pdc_row_count]['Tm']
    pdc_row_count = pdc_row_count + 1

    pdc_game_key = teamvalue_pdc + yearvalue_pdc
    game_key_pdc.append(pdc_game_key)
    
pd_combined.insert(0,"TeamKey", game_key_pdc)


# In[60]:


print(pd_combined)


# In[84]:


#Webscrape from below URL to get additional information

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


# In[85]:


#Format data types
dfws = dfws.astype({
    'Year' : 'int',
    'Winner' : 'string',
    'Runner Up' : 'string'
})

print(dfws)


# In[86]:


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
    elif name_long == "Denver Broncos":
        winners_short.append("DEN")
        champion = "DEN"
    elif name_long == "Indianapolis Colts":
        winners_short.append("IND")
        champion = "IND"
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


# In[87]:


print(dfws)


# In[88]:


#Drop pointless columns
dfws = dfws.drop(columns=['Number','Attendance','Location','Winners Share','Final Score'])


# In[89]:


print(dfws)


# In[90]:


dfws.insert(1,"Season", season)
dfws.insert(2,"Name_Short", winners_short)
dfws.insert(0,"Team_key", game_key_tuple)

print(game_key_tuple)


# In[ ]:




