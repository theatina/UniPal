# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import sys
import re
import pandas as pd
import os
from datetime import time, datetime, date
import numpy as np

from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
from urllib.request import urlopen

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionGreetUser(Action):
    
    def name(self) -> Text:
        return "action_greet_user"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text = "Hi, Pal!")

        return []


class ActionUniPsychoSupportInfo(Action):
    
    def name(self) -> Text:
        return "action_uni_psychoSupport_info"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "https://www.uoa.gr/foitites/symboyleytikes_ypiresies/monada_psychokoinonikis_parembasis/"

        phone1 = "2103688226 (University Club, Athens)"
        phone2 = "2107275580 (University Campus)"
        # info = 
        text = f"If you feel like you need support, you can call {phone1} or {phone2} for further information or visit {url}"
        dispatcher.utter_message(text)

        return []


class ActionUniClassSchedule(Action):
    
    def name(self) -> Text:
        return "action_uni_class_schedule"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "https://www.di.uoa.gr/studies/undergraduate/schedules"

        grad_stud_type = tracker.get_slot('grad_studies_type')
        # exams


        return []


class Button_Year(Action):
    def name(self) -> float:
        return "action_button_year"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[float, Any]) -> List[Dict[float, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        year_list = [ f"{i:02d}" for i in range(9,22) ]
        
        for y in year_list:
            buttons.append({"title": f"20{y}-20{y+1}" , "payload": "/inform_year{{'academic_year':y}}", "value": y})

        #then display it using dispatcher
        dispatcher.utter_message(text= "Choose year" , buttons=buttons)     
        return []    

class Button_Period(Action):
    def name(self) -> float:
        return "action_button_period"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[float, Any]) -> List[Dict[float, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        period_list=[ "jan", "jun", "sep" ]
        period_list_full=["January", "June", "September"] 
        
        for p,pf in zip(period_list, period_list_full):
            buttons.append({"title": f"{pf}" , "payload": "/inform_period{{'exam_period':p}}", "value": p})

        #then display it using dispatcher
        dispatcher.utter_message(text= "Choose exam period" , buttons=buttons)     
        return []             

class Button_Programme(Action):
    def name(self) -> Text:
        return "action_button_year"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        programme_type_list = [ "PPS", "PMS" ]
        type_list = ["Undergraduate", "Postgraduate"]
        
        for prog,prog_name in zip(programme_type_list,type_list):
            buttons.append({"title": f"{prog_name}" , "payload": "/inform_programme{{'grad_studies_type':prog}}", "value": prog})

        #then display it using dispatcher
        dispatcher.utter_message(text= "Choose study programme type" , buttons=buttons)     
        return []                                 

class ActionUniExamSchedule(Action):
    
    def name(self) -> Text:
        return "action_uni_exam_schedule"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "https://www.chatzi.org/dit-schedule/"
        #/pps/jan/1819"

        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        schedule_path = "https://www.chatzi.org/dit-schedule/"
        year_list = [ f"{i:02d}{i+1:02d}" for i in range(9,22) ]
        # print(year_list)
        # semester_list = [ "winter", "spring" ]
        exams_list = [ "jan", "jun", "sep" ]
        programme_type_list = [ "PPS", "PMS" ]

    
        grad_stud_type = tracker.get_slot('grad_studies_type')
        grad_stud_type=grad_stud_type
        exams = tracker.get_slot('exams')
        semester = tracker.get_slot('semester')
        academic_year = tracker.get_slot('academic_year')
        acad_years=f"{academic_year-1}{academic_year}"

        # print(grad_stud_type, semester, academic_year)
        file_url = os.path.join(schedule_path, f"")
        # file_url = "https://www.chatzi.org/dit-schedule/20-21/examsched_PPS_jan21.xls"
        file_url = f"https://www.chatzi.org/dit-schedule/{acad_years}/examsched_{grad_stud_type}_{exams}{academic_year}.xls"
        
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
        # timetable_df.to_csv(f"exams{grad_stud_type}{exams}{academic_year}Timetable.csv", index=False, header=True)

        #list of classes arranged alphabetically - date(day, date) - time
        all_classes=list(set([c for sublist in timetable_df.iloc[1:,1:].values for c in sublist if type(c)==str]))

        all_classes=sorted(all_classes)
        class_str=""
        for element in all_classes:
            i, c = np.where(timetable_df == element)
            class_str+=f"{element} -> {timetable_df.iloc[i[0],0]}, {timetable_df.iloc[0,c[0]]}\n" 

        # print (class_str)
    
        dispatcher.utter_message(f"\nFound this timetable {class_str}\n")
        
        #TODO: insert buttons for subject choice
        return []


class ActionUniAnnouncements(Action):
    
    def name(self) -> Text:
        return "action_uni_announcements"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        announcements_url = "https://www.di.uoa.gr/announcements"
        uoa_url = "https://www.di.uoa.gr"

        page = urlopen(announcements_url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        links_raw = soup.find_all('a')

        links = [ link for link in links_raw if "/announcements/" in link['href']  ]
        
        ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  }

        num_of_anns = int(tracker.get_slot('num_of_announcements'))
        ann_list_sorted = {k: v for k, v in sorted(ann_list.items(), key=lambda item: item[0])[:num_of_anns]}

        text_all = f"Here are the {num_of_anns} most recent NKUA Announcements:"
        for i,num in enumerate(ann_list_sorted):
            name = ann_list_sorted[num]
            link_path = os.path.join(announcements_url,str(num))
            announcement_text = f"{i+1}. {name} ({link_path})"
            dispatcher.utter_message(announcement_text)
        
        dispatcher.utter_message(f"\nFor further information and announcements, you can visit the University's Announcements Page here: {announcements_url}\n")

        return []