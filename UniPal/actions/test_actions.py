from datetime import time
import pandas as pd
import sys
import re
import os

from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
from urllib.request import urlopen
import requests

def ActionUniPsychoSupportInfo():
    url = "https://www.uoa.gr/foitites/symboyleytikes_ypiresies/monada_psychokoinonikis_parembasis/"

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # clean_text = [ re.sub("\s+"," ",line) for line in soup.contents if line not in [ "", " " ] ]
    # for i,line in enumerate(clean_text):
    #     print(f"{i} -> {line}")
    print(print(soup.prettify()))

    # phone = 
    # info = 
    text = f"If you feel like you need support, you can call "

def visit_link(url):
    webbrowser.open(url)

def ActionUniAnnouncements():
    announcements_url = "https://www.di.uoa.gr/announcements"
    uoa_url = "https://www.di.uoa.gr"

    page = urlopen(announcements_url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    links_raw = soup.find_all('a')

    links = [ link for link in links_raw if "/announcements/" in link['href']  ]
    
    # ann_list = [ item:ann.contents for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  ]
    ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  }

    ann_list_sorted = {k: v for k, v in sorted(ann_list.items(), key=lambda item: item[0])}

    print(ann_list_sorted)
    text_all = f"Here are the 10 most recent NKUA Announcements:"
    for i,num in enumerate(ann_list_sorted):
        # print(ann)
        name = ann_list_sorted[num]
        link_path = os.path.join(announcements_url,str(num))
        announcement_text = f"{i+1}. {name} ({link_path})"
        print(announcement_text)
    
    print(f"\nFor further information and announcements, you can visit the University's Announcements Page here: {announcements_url}\n")


def ActionUniClassSchedule():
    url = "https://www.chatzi.org/dit-schedule/"
    #/pps/jan/1819"

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    schedule_path = "https://www.chatzi.org/dit-schedule/"
    # year_list = [ f"{i:02d}{i+1:02d}" for i in range(9,22) ]
    exam_year_list = [ f"{i:02d}" for i in range(10,23) ]
    class_year_list = [ f"{i:02d}{i+1:02d}" for i in range(9,22) ]
    url_year_list = [ f"{i:02d}-{i+1:02d}" for i in range(9,22) ]
    # print(exam_year_list, class_year_list, url_year_list)
    
    semester_list = [ "winter", "spring" ]
    exams_list = [ "jan", "jun", "sep" ]
    programme_list = [ "PPS", "PMS" ]

    # https://www.chatzi.org/dit-schedule/20-21/timetable_PPS_winter2021.xls
    # https://www.chatzi.org/dit-schedule/20-21/timetable_PPS_spring2021.xls
    # https://www.chatzi.org/dit-schedule/19-20/timetable_PPS_spring1920.xls
   
    # https://www.chatzi.org/dit-schedule/20-21/timetable_PMS_winter2021.xls

    # https://www.chatzi.org/dit-schedule/20-21/timetable_winter2021.xls
    # https://www.chatzi.org/dit-schedule/20-21/timetable_spring2021.xls

    
    # https://www.chatzi.org/dit-schedule/20-21/examsched_PPS_jan21.xls
    # https://www.chatzi.org/dit-schedule/20-21/examsched_PPS_jun21.xls
    # https://www.chatzi.org/dit-schedule/20-21/examsched_PPS_sep21.xls
    # https://www.chatzi.org/dit-schedule/20-21/examsched_PMS_sep21.xls

    # grad_stud_type = input("\nInsert graduate study programme type: ")
    # semester = input("\nInsert semester of study: ")

    # academic_year = input("\nInsert academic year: ")[-2:]

    # if grad_stud_type in grad_stud_type:
    #     filename = f"timetable_{grad_stud_type}_{semester}{academic_year}"
    # else:
    #     filename = f"timetable_{semester}{academic_year}"
    # print(filename)

    # file_url = os.path.join()
    file_url = "https://www.chatzi.org/dit-schedule/20-21/examsched_PPS_jan21.xls"

    timetable_df = pd.read_excel(file_url)

    for index, column in enumerate(timetable_df):
        print(f"Column no. {index}:\n {timetable_df[column].unique()}\n\n")
    
    





'''
____________________________________________________________________________________
'''

# main

# ActionUniPsychoSupportInfo()
# ActionUniAnnouncements()
ActionUniClassSchedule()