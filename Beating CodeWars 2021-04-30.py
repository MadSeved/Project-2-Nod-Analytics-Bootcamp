#
# Libraries needed
#


from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import time
import numpy as np
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")



#
# Getting the kata URL's
#


# Given that the webpage uses "infinite" scrolling we'll need to scroll down to the bottom of the page in order to access
# all kata URL's

url = "https://www.codewars.com/kata/search/python?q=&&beta=false"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extracting the information from the page and turning it into a beautiful soup
variable = driver.page_source
soup = bs(variable)

# Making a list of all URL's beloning to the katas
kata_url = ["https://www.codewars.com/" + i["href"] for i in soup.select("div.item-title > a", href = True)]


#
# Scraping
#


# The lists bellow will become our columns in the DataFrame. 

developer=[]
collection_kata_part_of=[]
kata_name=[]
kata_rank=[]
publish_date=[]
times_attemped=[]
times_skipped=[]
total_code_submissions=[]
total_times_completed=[]
total_times_completed_python=[]
total_stars=[]
percentage_of_votes_with_positive=[]
total_very_satisfied=[]
total_somewhat_satisfied=[]
total_not_satisfied=[]
total_rank_assessments=[]
average_assessed_rank=[]
highest_assessed_rank=[]
lowest_assessed_rank=[]
tags=[]

# We access every kata URL and scrape it. The multiple try/except statements are needed to compensate for the fact that
# the CSS select statements sometime points to non-existing objects at different pages.

x=0
for i in kata_url:
    # The print statement is a way to keep track of progress
    print(x)
    soup = bs(requests.get(i).content)
    
    try:
        developer.append(soup.select("#shell_content > div.px-0.w-full > div > div.w-full.md\:w-5\/12 > div.mt-1.mb-3 > a.ml-4.mr-0")[0].text)
    except:
        developer.append("Anonymous")
    collection_kata_part_of.append(soup.select("#shell_content > div.px-0.w-full > div > div.w-full.md\:w-5\/12 > div.mt-1.mb-3 > a.mr-0.js-add-to-collection.ml-2 > span")[0].text)
    
    kata_name.append(soup.select("h4")[0].text)
    
    kata_rank.append(soup.select("#shell_content > div.px-0.w-full > div > div.w-full.md\:w-5\/12 > div.flex.items-center > div > div > span")[0].text)
    
    try:
        publish_date.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td.p-1.text-right")[0].text)
    except:
        try:
            publish_date.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td.p-1.text-right")[0].text)
        except:
            publish_date.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td.p-1.text-right")[0].text)
    
    try:
        times_attemped.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.p-1.text-right")[0].text)
    except:
        try:
            times_attemped.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.p-1.text-right")[0].text)
        except:
            try:
                times_attemped.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.p-1.text-right")[0].text)
            except:    
                times_attemped.append(np.nan)
    
    try:
        times_skipped.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td.p-1.text-right")[0].text)
    except:
        try:
            times_skipped.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td.p-1.text-right")[0].text)
        except:
            times_skipped.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td.p-1.text-right")[0].text)
    try:
        total_code_submissions.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td.p-1.value.text-right")[0].text)
    except:
        try:
            total_code_submissions.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td.p-1.value.text-right")[0].text)
        except:
            total_code_submissions.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td.p-1.value.text-right")[0].text)
    
    try:
        total_times_completed.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td.p-1.text-right")[0].text)
    except:
        try:
            total_times_completed.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td.p-1.text-right")[0].text)
        except:
            total_times_completed.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td.p-1.text-right")[0].text)
    
    total_times_completed_python.append(soup.select("#shell_content > div.px-0.w-full > div > div.w-full.md\:w-5\/12 > div.mt-1.mb-3 > span:nth-child(5)")[0].text)
    
    total_stars.append(soup.select("#shell_content > div.px-0.w-full > div > div.w-full.md\:w-5\/12 > div.mt-1.mb-3 > a.mr-0.js-add-code-challenge-star > span")[0].text)
    
    percentage_of_votes_with_positive.append(soup.select("#shell_content > div.px-0.w-full > div > div.w-full.md\:w-5\/12 > div.mt-1.mb-3 > span:nth-child(4) > span")[0].text)
    
    try:
        total_very_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td.p-1.text-right")[0].text)
    except:
        try:
            total_very_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td.p-1.text-right")[0].text)
        except:
            total_very_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(2) > td.p-1.text-right")[0].text)
    
    try:
        total_somewhat_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td.p-1.text-right")[0].text)
    except:
        try:
            total_somewhat_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td.p-1.text-right")[0].text)
        except:
            total_somewhat_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td.p-1.text-right")[0].text)
    try:
        total_not_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td.p-1.text-right")[0].text)
    except:
        try:
            total_not_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td.p-1.text-right")[0].text)
        except:
            total_not_satisfied.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(4) > td.p-1.text-right")[0].text)
    
    try:
        total_rank_assessments.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(5) > td.p-1.text-right")[0].text)
        average_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(6) > td.p-1.text-right")[0].text)
        highest_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(7) > td.p-1.text-right")[0].text)
        lowest_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(6) > div > div:nth-child(2) > table > tbody > tr:nth-child(8) > td.p-1.text-right")[0].text)
    except:
        try:
            total_rank_assessments.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(5) > td.p-1.text-right")[0].text)
            average_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(6) > td.p-1.text-right")[0].text)
            highest_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(7) > td.p-1.text-right")[0].text)
            lowest_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(5) > div > div:nth-child(2) > table > tbody > tr:nth-child(8) > td.p-1.text-right")[0].text)
        except:
            try:
                total_rank_assessments.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(5) > td.p-1.text-right")[0].text)
                average_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(6) > td.p-1.text-right")[0].text)
                highest_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(7) > td.p-1.text-right")[0].text)
                lowest_assessed_rank.append(soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(4) > div > div:nth-child(2) > table > tbody > tr:nth-child(8) > td.p-1.text-right")[0].text)
            except:
                total_rank_assessments.append(np.nan)
                average_assessed_rank.append(np.nan)
                highest_assessed_rank.append(np.nan)
                lowest_assessed_rank.append(np.nan)
    tags.append(", ".join(re.findall('([A-Z][a-z]+)', soup.select("#shell_content > div.w-full.mt-2 > div:nth-child(2) > div.mt-15px")[0].text)))
    x+=1
    
    
    
#
# Cleaning Data and DataFrame
#


# Creaing a new column containing all votes as an integer
total_votes = list(range(len(total_very_satisfied)))
for i in range(len(total_very_satisfied)):
    total_votes[i] = int(total_very_satisfied[i]) + int(total_somewhat_satisfied[i]) + int(total_not_satisfied[i])

# The next two paragraphs makes sure that these columns display the information in the way we want to
total_times_completed_python_real=list(range(len(total_very_satisfied)))
x=0
for i in total_times_completed_python:
    total_times_completed_python_real[x]=i.split()[0]
    x+=1
    
percentage_of_votes_with_positive_real=list(range(len(total_very_satisfied)))
x=0
for i in percentage_of_votes_with_positive:
    percentage_of_votes_with_positive_real[x]=i.split()[0]
    x+=1

# As the webscraping provide data as strings we need to change the object types to integers if necessarry.
x=0
for i in total_stars:
    total_stars[x] = int(i)
    x+=1
    
x=0
for i in collection_kata_part_of:
    collection_kata_part_of[x] = int(i)
    x+=1
    
x=0
for i in times_attemped:
    times_attemped[x] = int(i)
    x+=1
    
x=0
for i in times_skipped:
    times_skipped[x] = int(i)
    x+=1

x=0
for i in total_code_submissions:
    total_code_submissions[x] = int(i)
    x+=1
    
x=0
for i in total_times_completed:
    total_times_completed[x] = int(i)
    x+=1
    
x=0
for i in total_votes:
    total_votes[x] = int(i)
    x+=1
    
x=0
for i in total_very_satisfied:
    total_very_satisfied[x] = int(i)
    x+=1
    
x=0
for i in total_somewhat_satisfied:
    total_somewhat_satisfied[x] = int(i)
    x+=1
    
x=0
for i in total_not_satisfied:
    total_not_satisfied[x] = int(i)
    x+=1
    
x=0
for i in total_rank_assessments:
    total_rank_assessments[x] = float(i)
    x+=1
    
x=0
for i in percentage_of_votes_with_positive_real:
    percentage_of_votes_with_positive_real[x] = int(i[:-1])
    x+=1
    
df=pd.DataFrame({"kata name":kata_name, "developer":developer, "kata rank":kata_rank, "publish date":publish_date, "total stars":total_stars, "no. collections kata part of":collection_kata_part_of, "times attempted":times_attemped, "times skipped":times_skipped, "total code submissions":total_code_submissions, "total times completed":total_times_completed, "total times completed (P)":total_times_completed_python_real, "percentage of votes with positive feedback [%]":percentage_of_votes_with_positive_real, "total votes":total_votes, "total very satisfied":total_very_satisfied, "total somewhat satisfied":total_somewhat_satisfied, "total not satisfied":total_not_satisfied, "total rank assessment":total_rank_assessments, "average assessed rank":average_assessed_rank, "highest assessed rank":highest_assessed_rank, "lowest assessed rank":lowest_assessed_rank, "tags":tags})

# Saving the DataFrame as a csv
df.to_csv(r'C:\\Users\\kebbe\\Nod Coding\\Week 4\\Day 4\\Projekt\Beating CodeWars.csv', index=False)



#
# EDA: Data Analysis Engineering for Max Experience gain analysis
#


# Making a new DataFrame that is used later on
eda_df = pd.DataFrame()

eda_df["kata name"] = df["kata name"]
eda_df["kata rank"] = df["kata rank"]
eda_df["developer"] = df["developer"]
eda_df["completions/attempts"] = df["total times completed"] / df["times attempted"]
eda_df["completions/submissions"] = df["total times completed"] / df["total code submissions"]
eda_df["skips/attempts"] = df["times skipped"] / df["times attempted"]
eda_df["average of comp/att and comp/sub"] = (eda_df["completions/attempts"] + eda_df["completions/submissions"])/2



#
# EDA: Fun Fact analysis
#


# Which developer have made the most katas?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.groupby("developer", as_index=False).count().sort_values(by="kata name", ascending = False).head(10), x="developer", y="kata name")
ma_plot.set(ylabel="Count")
ma_plot.set(xlabel="Developer")
ma_plot.set(title="Top 10 developers who made the most katas")
plt.show()


# Which developer with at least 10 katas have the most average amount of stars?
a=df.groupby("developer", as_index=False).count()
b=a.loc[a["kata name"]>=10]
c=list(b["developer"])


plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.loc[df["developer"].isin(c)].groupby("developer", as_index=False).mean().sort_values(by="total stars", ascending = False).head(10), x="developer", y="total stars")
ma_plot.set(ylabel="Average amount of stars")
ma_plot.set(xlabel="Developer")
ma_plot.set(title="Top 10 developers that has at least ten katas who have the highest average amount of stars")
plt.show()


# Which devoloper with at least 10 katas have the highest average positive assessment?
a=df.groupby("developer", as_index=False).count()
b=a.loc[a["kata name"]>=10]
c=list(b["developer"])

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.loc[df["developer"].isin(c)].groupby("developer", as_index=False).mean().sort_values(by="percentage of votes with positive feedback [%]", ascending = False).head(10), x="developer", y="percentage of votes with positive feedback [%]")
ma_plot.set(ylabel="Average positive assessment [%]")
ma_plot.set(xlabel="Developer")
ma_plot.set(title="Top 10 developers that has at least ten katas who have the highest average positive assessment [%]")
plt.show()


# What is the kata rank distribution among all katas?

ma_plot = df.groupby("kata rank", as_index=False).count()[["kata rank", "kata name"]].plot.pie(y="kata name", autopct="%1.1f%%", figsize=(17,13), labels=["1 kyu", "2 kyu", "3 kyu", "4 kyu", "5 kyu", "6 kyu", "7 kyu", "8 kyu"])
ma_plot.set(ylabel="")
plt.legend("")
plt.title("Rank distribution among katas")
plt.show()


# Which kata is part of most no. collections?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.sort_values(by="no. collections kata part of", ascending=False).head(10), x="kata name", y="no. collections kata part of")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("The number of collections a kata is part of (Top 10)")
ma_plot.set(ylabel="no. collections kata is part of")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which devoloper has the highest amount of katas that's part of collections?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.groupby("developer", as_index=False).sum().sort_values(by="no. collections kata part of", ascending=False).head(10), x="developer", y="no. collections kata part of")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("The sum of all collections this developers katas are part of (Top 10)")
ma_plot.set(ylabel="Sum of no. collections kata is part of")
ma_plot.set(xlabel="Developer")
plt.show()

# Making this additional plot due to the odd nature of the result
plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.groupby("developer", as_index=False).sum().sort_values(by="no. collections kata part of", ascending=False).tail(5), x="developer", y="no. collections kata part of")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("The sum of all collections this developers katas are part of (Bottom 5)")
ma_plot.set(ylabel="Sum of no. collections kata is part of")
ma_plot.set(xlabel="Developer")
plt.show()



# How has the amount of katas published per year increased?

count_2013=0
count_2014=0
count_2015=0
count_2016=0
count_2017=0
count_2018=0
count_2019=0
count_2020=0
count_2021=0
for i in df["publish date"]:
    if i[-4:]=="2013":
        count_2013+=1
    elif i[-4:]=="2014":
        count_2014+=1
    elif i[-4:]=="2015":
        count_2015+=1
    elif i[-4:]=="2016":
        count_2016+=1
    elif i[-4:]=="2017":
        count_2017+=1
    elif i[-4:]=="2018":
        count_2018+=1
    elif i[-4:]=="2019":
        count_2019+=1
    elif i[-4:]=="2020":
        count_2020+=1
    elif i[-4:]=="2021":
        count_2021+=1

plt.figure(figsize=(14,10))
ma_plot=sns.lineplot(x=["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"], y=[count_2013, count_2014, count_2015, count_2016, count_2017, count_2018, count_2019, count_2020, count_2021])
plt.title("Number of katas published over the years")
ma_plot.set(ylabel="no. of katas")
ma_plot.set(xlabel="Year")
plt.show()


# Which rank has the highest average percentage of votes with positive feedback?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.groupby("kata rank", as_index=False).mean().sort_values(by="percentage of votes with positive feedback [%]", ascending=False), x="kata rank", y="percentage of votes with positive feedback [%]")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("The average percentage of positive feedback per rank")
ma_plot.set(ylabel="Percentage of votes with positive feedback")
ma_plot.set(xlabel="Kata rank")
plt.show()


# Which kata has the least percentage of votes with positive feedback and also at least 1000 attempts?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=df.loc[df["times attempted"] >= 1000].sort_values(by="percentage of votes with positive feedback [%]").head(10), x="kata name", y="percentage of votes with positive feedback [%]")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("The katas with lowest percentage of positive feedback (bottom 10) and at least 1000 attempts")
ma_plot.set(ylabel="Percentage of votes with positive feedback")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which kata has the highest and lowest skipped/attempts? (can be sorted by rank)

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="skips/attempts", ascending= False).head(10), x="kata name", y="skips/attempts")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the highest skips/attempt")
ma_plot.set(ylabel="skips/attempt")
ma_plot.set(xlabel="Kata name")
plt.show()

# Pretty pointless plot
plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="skips/attempts", ascending= False).tail(10), x="kata name", y="skips/attempts")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the lowest skips/attempt")
ma_plot.set(ylabel="skips/attempt")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which kata has the highest and lowest completed/attempts? (can be sorted by rank

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="completions/attempts", ascending= False).head(10), x="kata name", y="completions/attempts")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the highest completions/attempt")
ma_plot.set(ylabel="completions/attempt")
ma_plot.set(xlabel="Kata name")
plt.show()

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="completions/attempts", ascending= False).tail(10), x="kata name", y="completions/attempts")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the lowest completions/attempt")
ma_plot.set(ylabel="completions/attempt")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which kata has the highest and lowest completed/submissions? (can be sorted by rank)

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="completions/submissions", ascending= False).head(10), x="kata name", y="completions/submissions")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the highest completions/submissions")
ma_plot.set(ylabel="completions/submissions")
ma_plot.set(xlabel="Kata name")
plt.show()

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="completions/submissions", ascending= False).tail(10), x="kata name", y="completions/submissions")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the lowest completions/submissions")
ma_plot.set(ylabel="completions/attempt")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which kata has the highest average of completed/attempts + completed/submissions? (can be sorted by rank)

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.sort_values(by="average of comp/att and comp/sub", ascending= False).head(10), x="kata name", y="average of comp/att and comp/sub")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 katas with the highest average of comp/att and comp/sub")
ma_plot.set(ylabel="average of comp/att and comp/sub")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which rank 5 kata has the highest average of completed/attempts + completed/submissions?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.loc[eda_df["kata rank"]=="5 kyu"].sort_values(by="average of comp/att and comp/sub", ascending= False).head(10), x="kata name", y="average of comp/att and comp/sub")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Top 10 rank 5 katas with the highest average of comp/att and comp/sub")
ma_plot.set(ylabel="average of comp/att and comp/sub")
ma_plot.set(xlabel="Kata name")
plt.show()


# Which kata rank has the highest and lowest average completed/attempts?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.groupby("kata rank", as_index=False).mean().sort_values(by="skips/attempts", ascending= False).head(10), x="kata rank", y="skips/attempts")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Kata ranks with the highest/lowest average skips/attempt")
ma_plot.set(ylabel="skips/attempt")
ma_plot.set(xlabel="Kata rank")
plt.show()


# Which kata rank has the highest and lowest average skipped/attempts?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.groupby("kata rank", as_index=False).mean().sort_values(by="completions/attempts", ascending= False).head(10), x="kata rank", y="completions/attempts")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Kata ranks with the highest/lowest average completions/attempt")
ma_plot.set(ylabel="completions/attempt")
ma_plot.set(xlabel="Kata rank")
plt.show()


# Which kata rank has the highest and lowest average completed/submissions?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.groupby("kata rank", as_index=False).mean().sort_values(by="completions/submissions", ascending= False).head(10), x="kata rank", y="completions/submissions")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Kata ranks with the highest/lowest average completions/submissions")
ma_plot.set(ylabel="completions/submissions")
ma_plot.set(xlabel="Kata rank")
plt.show()


# Which kata rank has the highest average of completed/attempts + completed/submissions?

plt.figure(figsize=(14,10))
ma_plot=sns.barplot(data=eda_df.groupby("kata rank", as_index=False).mean().sort_values(by="average of comp/att and comp/sub", ascending= False).head(10), x="kata rank", y="average of comp/att and comp/sub")
ma_plot.set_xticklabels(ma_plot.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.title("Kata ranks with the highest/lowest average of average of comp/att and comp/sub")
ma_plot.set(ylabel="average of comp/att and comp/sub")
ma_plot.set(xlabel="Kata rank")
plt.show()