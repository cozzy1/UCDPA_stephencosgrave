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


# In[ ]:




