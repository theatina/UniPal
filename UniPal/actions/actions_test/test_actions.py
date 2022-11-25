from ctypes.wintypes import HENHMETAFILE
from datetime import time, datetime, date
import pandas as pd
import sys
import re
import os
import numpy as np

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
    # print({ann['href'].split("/")[-1]:ann.contents[0]  for ann in (links) if ann['href'].split("/")[-1].isnumeric() }  )
    # ann_list = [ item:ann.contents if item.isnumeric() for ann in links for item in ann['href'].split(os.sep)   ]
    ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split("/") if item.isnumeric()  }
    if not ann_list:
        ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  }

    ann_list_sorted = {k: v for k, v in sorted(ann_list.items(), key=lambda item: item[0])}

    top=10
    text_all = f"Here are the {top} most recent NKUA Announcements:"
    for i,num in enumerate(list(ann_list_sorted.keys())[:top]):

        # print(ann)
        name = ann_list_sorted[num]
        if announcements_url[-1]=="/":
            link_path=f"{announcements_url}{str(num)}"
        else:
            link_path=f"{announcements_url}/{str(num)}"
        # link_path = os.path.join(announcements_url,str(num))
        announcement_text = f"{i+1}. {name} ({link_path})"
        if "\\" in link_path:
            link_path.replace("\\","/")
            print(link_path)
        page = urlopen(link_path)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        summary=soup.find_all("div", attrs={"class":"clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item"})
        print(summary[1].get_text())
        # links_raw = soup.find_all('a')


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
    
    
def ActionUniExamSchedule():
    
    url = "https://www.chatzi.org/dit-schedule/"
    #/pps/jan/1819"

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    schedule_path = "https://www.chatzi.org/dit-schedule/"
    year_list = [ f"{i:02d}{i+1:02d}" for i in range(9,22) ]
    semester_list = [ "winter", "spring" ]
    exams_list = [ "jan", "jun", "sep" ]
    programme_list = [ "pps", "pms", "full" ]


    # grad_stud_type = tracker.get_slot('grad_studies_type')
    # exams = tracker.get_slot('exams')
    # semester = tracker.get_slot('semester')
    # academic_year = tracker.get_slot('academic_year')

    grad_stud_type = "PPS"
    period = "jan"
    # semester = "winter"
    academic_year = 2020
    if len(str(academic_year))>2:
        academic_year = int(str(academic_year)[-2:])

    acad_years=str(academic_year-1)+"-"+str(academic_year)

    # print(grad_stud_type, semester, academic_year)
    # file_url = os.path.join(schedule_path, f"")
    # file_url = "https://www.chatzi.org/dit-schedule/examsched_PMS_sep21.xls"
    
    file_url = f"https://www.chatzi.org/dit-schedule/{acad_years}/examsched_{grad_stud_type}_{period}{int(academic_year)}.xls"
    # file_url = f"https://www.chatzi.org/dit-schedule/#/{grad_stud_type}/{exams}/{academic_year}"
    print(file_url)

    timetable_df = pd.read_excel(file_url)
    

    # Πρόγραμμα Εξετάσεων Προπτυχιακών Μαθημάτων Χειμερινής Περιόδου 2021 -> Date -> Date
    # Unnamed: 1 -> Time1
    # Unnamed: 2 -> Time2
    # Unnamed: 3 -> Time3
    # Unnamed: 3 -> Time4
    # timetable_df.rename(columns={"Πρόγραμμα Εξετάσεων Προπτυχιακών Μαθημάτων Χειμερινής Περιόδου 2021":"Date", "Unnamed: 1": "Time1", "Unnamed: 2": "Time2", "Unnamed: 3": "Time3"}, inplace=True)
    if 'Unnamed: 4' in list(timetable_df.columns):
        timetable_df.columns=["Date", "Time1", "Time2", "Time3", "Time4"]
    else:
        timetable_df.columns=["Date", "Time1", "Time2", "Time3"]
        # timetable_df.rename(columns={"Unnamed 4": "Time4"}, inplace=True)
    # print(type(timetable_df["Date"][2]))
    # print(timetable_df["Date"][2].date().strftime('%A %d-%m-%y'))
    timetable_df["Date"] = timetable_df["Date"].apply(lambda x: x.date().strftime('%A %d-%m-%Y') if isinstance(x, datetime) else x)
    print(timetable_df["Date"])
    timetable_df.to_csv(f"exams{grad_stud_type}{period}{academic_year}Timetable.csv", index=False, header=True)


    # print(timetable_df.columns)
    mes=timetable_df

    #TODO: list of classes arranged alphabetically - date(day, date) - time
    # timetable_df[timetable_df == 7]

    
    all_classes=list(set([c for sublist in timetable_df.iloc[1:,1:].values for c in sublist if type(c)==str]))

    all_classes=sorted(all_classes)
    class_str=""
    for element in all_classes:
        i, c = np.where(timetable_df == element)
        class_str+=f"{element} -> {timetable_df.iloc[i[0],0]}, {timetable_df.iloc[0,c[0]]}\n" 

    print (class_str)
    return class_str




'''
____________________________________________________________________________________
'''

# main

# ActionUniPsychoSupportInfo()
ActionUniAnnouncements()
# ActionUniClassSchedule()
# ActionUniExamSchedule()