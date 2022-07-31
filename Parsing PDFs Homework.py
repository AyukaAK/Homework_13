#!/usr/bin/env python
# coding: utf-8

# # Parsing PDFs Homework
# 
# With the power of pdfminer, pytesseract, Camelot, and Tika, let's analyze some documents!
# 
# > If at any point you think, **"I'm close enough, I'd just edit the rest of it in Excel"**: that's fine! Just make a note of it.
# 
# ## A trick to use again and again
# 
# ### Approach 1
# 
# Before we get started: when you want to take the first row of your data and set it as the header, use this trick.

# In[2]:


import pandas as pd


# In[3]:


df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[4]:


# Set the first column as the columns
df.columns = df.loc[0]

# Drop the first row
df = df.drop(0)

df


# 🚀 Done!
# 
# ### Approach 2
# 
# Another alternative is to use `.rename` on your columns and just filter out the columns you aren't interested in. This can be useful if the column name shows up multiple times in your data for some reason or another.

# In[5]:


# Starting with the same-ish data...
df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'fruit name', 'likes' ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[6]:


df = df.rename(columns={
    0: 'fruit name',
    1: 'likes'
})
df = df[df['fruit name'] != 'fruit name']
df


# 🚀 Done!
# 
# ### Useful tips about coordinates
# 
# If you want to grab only a section of the page [Kull](https://jsoma.github.io/kull/#/) might be helpful in finding the coordinates.
# 
# > **Alternatively** run `%matplotlib notebook` in a cell. Afterwards, every time you use something like `camelot.plot(tables[0]).show()` it will get you nice zoomable, hoverable versions that include `x` and `y` coordinates as you move your mouse.
# 
# Coordinates are given as `"left_x,top_y,right_x,bottom_y"` with `(0,0)` being in the bottom left-hand corner.
# 
# Note that all coordinates are strings, for some reason. It won't be `[1, 2, 3, 4]` it will be `['1,2,3,4']`
# 
# # Camelot questions
# 
# The largest part of this assignment is **mostly Camelot work**. As tabular data is usually the most typical data you'll be working with, it's what I'm giving you!
# 
# It will probably be helpful to read through [Camelot's advanced usage tips](https://camelot-py.readthedocs.io/en/master/user/advanced.html), along with the notebook I posted in the homework assignment.
# 
# ## Prison Inmates
# 
# Working from [InmateList.pdf](InmateList.pdf), save a CSV file that includes every inmate.
# 
# * Make sure your rows are *all data*, and you don't have any people named "Inmate Name."
# 

# In[1]:


import camelot


# In[4]:


#it says no files but there are! so you do flavor="stream"
tables = camelot.read_pdf("InmateList.pdf", flavor="stream", pages="1-16")
tables


# In[47]:


tables[15].df


# In[7]:


import pandas as pd


# In[58]:


# combine dataframes of all 16 pages
df = pd.concat([
    tables[0].df,
    tables[1].df,
    tables[2].df,
    tables[3].df,
    tables[4].df,
    tables[5].df,
    tables[6].df,
    tables[7].df,
    tables[8].df,
    tables[9].df,
    tables[10].df,
    tables[11].df,
    tables[12].df,
    tables[13].df,
    tables[14].df,
    tables[15].df
], ignore_index=True)
df


# In[59]:


df = df.rename(columns={
    0: 'ICN #',
    1: 'Inmate Name',
    2: 'null',
    3: 'Facility',
    4: 'Booking Date',
    5: 'null2'
})
df = df[df['ICN #'] != 'ICN #']
df


# In[60]:


df = df.drop(columns=['null', 'null2'])


# In[61]:


#drop any rows that have unnecessary values in the rebounds columns
df = df[df.Facility != "Erie County Sheriff's Office"]


# In[62]:


df = df[df.Facility != "Inmate Roster"]


# In[63]:


df.columns = df.columns.str.replace('ICN #', 'ICN_number')


# In[64]:


df = df[df.ICN_number != "Created On:"]


# In[65]:


df


# In[66]:


df.to_csv('InmateList.csv', index=False)


# ## WHO resolutions
# 
# Using [A74_R13-en.pdf](A74_R13-en.pdf), what ten member countries are given the highest assessments?
# 
# * You might need to have two separate queries, and combine the results: that last page is pretty awful!
# * Always rename your columns
# * Double-check that your sorting looks right......
# * You can still get the answer even without perfectly clean data

# In[155]:


tables = camelot.read_pdf("A74_R13-en.pdf", flavor="stream", pages="1-5")
tables


# In[156]:


tables[0].df


# In[157]:


df = pd.concat([
    tables[0].df,
    tables[1].df,
    tables[2].df,
], ignore_index=True)
df


# In[158]:


#colum names
df = df.rename(columns={
    0: 'Members and',
    1: 'WHO scale',
})
df = df[df['Members and'] != 'Members and']
df


# In[159]:


# rename the columns
df.columns = df.columns.str.replace('Members and', 'Members_and_Associate Members')
df.columns = df.columns.str.replace('WHO scale', 'WHO_scale_for_2022_2023_per')
df


# In[160]:


#drop any rows that have unnecessary values in the rebounds columns
df = df[df.WHO_scale_for_2022_2023_per != "for 2022–2023"]
df = df[df.WHO_scale_for_2022_2023_per != "%"]


# In[164]:


df.shape


# In[179]:


df.head()


# In[167]:


#add two rows from the bad last page by looking at it below- just two countries
df = df.append({'Members_and_Associate Members' : 'Zambia',
                    'WHO_scale_for_2022_2023_per' : 0.0090} , 
                    ignore_index=True)
df = df.append({'Members_and_Associate Members' : 'Zimbabwe',
                    'WHO_scale_for_2022_2023_per' : 0.0050} , 
                    ignore_index=True)


# In[168]:


df.shape


# In[175]:


df


# In[172]:


df.dtypes


# In[174]:


df['WHO_scale_for_2022_2023_per'] = df['WHO_scale_for_2022_2023_per'].astype(float)


# In[171]:


df.sort_values(by='WHO_scale_for_2022_2023_per', ascending=True)
df


# In[170]:


#only the last page for the reference
tables = camelot.read_pdf("A74_R13-en.pdf", flavor="stream", pages="6")
tables[0].df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## The Avengers
# 
# Using [THE_AVENGERS.pdf](THE_AVENGERS.pdf), approximately how many lines does Captain America have as compared to Thor and Iron Man?
# 
# * Character names only: we're only counting `IRON MAN` as Iron Man, not `TONY`.
# * Your new best friend might be `\n`
# * Look up `.count` for strings

# In[ ]:





# In[ ]:





# ## COVID data
# 
# Using [covidweekly2721.pdf](covidweekly2721.pdf), what's the total number of tests performed in Minnesota? Use the Laboratory Test Rates by County of Residence chart.
# 
# * You COULD pull both tables separately OR you could pull them both at once and split them in pandas.
# * Remember you can do things like `df[['name','age']]` to ask for multiple columns

# In[ ]:





# ## Theme Parks
# 
# Using [2019-Theme-Index-web-1.pdf](2019-Theme-Index-web-1.pdf), save a CSV of the top 10 theme park groups worldwide.
# 
# * You can clean the results or you can restrict the area the table is pulled from, up to you

# In[ ]:





# ## Hunting licenses
# 
# Using [US_Fish_and_Wildlife_Service_2021.pdf](US_Fish_and_Wildlife_Service_2021.pdf) and [a CSV of state populations](http://goodcsv.com/geography/us-states-territories/), find the states with the highest per-capita hunting license holders.

# In[ ]:





# # Not-Camelot questions
# 
# You can answer these without using Camelot.

# ## Federal rules on assault weapons
# 
# Download all of the PDFs from the Bureau of Alcohol, Tobacco, Firearms and Explosives's [Rules and Regulations Library](https://www.atf.gov/rules-and-regulations/rules-and-regulations-library). Filter for a list of all PDFs that contain the word `assault weapon` or `assault rifle`.
# 
# > If you're having trouble scraping, maybe someone will be kind enough to drop a list of PDF urls in Slack?

# In[ ]:





# ## New immigration judge training materials
# 
# Extract the text from [this 2020 guide for new immigration judges](2020-training-materials-2a-201-300.pdf) and save it as a file called `training-material.txt`.
# 
# > I took this PDF from [a FOIA request](https://www.muckrock.com/foi/united-states-of-america-10/most-recent-new-immigration-judge-training-materials-120125/#comms) – but the unfortunate thing is *I actually had to remove the OCR layer to make it part of this assignment*. By default everything that goes through Muckrock gets all of the text detected!

# In[ ]:




