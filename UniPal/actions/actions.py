# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import sys
import re
import pandas as pd
import os
import numpy as np

import certifi
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

from datetime import time, datetime, date

from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
from urllib.request import urlopen

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction

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

class ActionResetTimetableSlots(Action):
    
    def name(self) -> Text:
        return "action_resetTimetableSlots"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # reset slots about type, semester, year, period 
        return [SlotSet("exams", False),SlotSet("grad_studies_type", None), SlotSet("semester", None), SlotSet("academic_year", None), SlotSet("exam_period", None)]


class ActionResetAnnouncementSlot(Action):
    
    def name(self) -> Text:
        return "action_resetAnnouncementSlot"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # reset slots about type, semester, year, period 
        return [SlotSet("num_of_announcements", None)]

class ActionResetSlots(Action):
    
    def name(self) -> Text:
        return "action_resetSlots"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # reset slots about type, semester, year, period 
        # FollowupAction("action_resetAnnouncementSlot")
        # FollowupAction("action_resetTimetableSlots")

        return [SlotSet("num_of_announcements", None), SlotSet("exams", False), SlotSet("grad_studies_type", None), SlotSet("semester", None), SlotSet("academic_year", None), SlotSet("exam_period", None) ]



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


# class ActionUniClassSchedule(Action):
    
#     def name(self) -> Text:
#         return "action_uni_class_schedule"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         url = "https://www.di.uoa.gr/studies/undergraduate/schedules"

#         grad_stud_type = tracker.get_slot('grad_studies_type')
#         # exams


#         return []

class ActionUniPalServices(Action):
    
    def name(self) -> Text:
        return "action_UniPal_services"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=" \n \n I can provide the following services/information:\n1. Announcements\n2. Exams Schedule\n3. Class Timetable\n4. University Contact/Location/Access Info\n5. University Staff Contact Details\n6. Psychological Support Information\n")

        return []

# class Buttons_yearPeriodType(Action):
#     def name(self) -> Text:
#         return "action_button_year"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         buttons = []
#         #append the response of API in the form of title and payload
#         programme_type_list = [ "PPS", "PMS" ]
#         type_list = ["Undergraduate", "Postgraduate"]
#         "/inform{\"grad_studies_type\":\"" + prog + "\"}"
#         for prog,prog_name in zip(programme_type_list,type_list):
#             buttons.append({"title": f"{prog_name}" , "payload": "/request_exam_schedule{\"grad_studies_type\":\"" + prog + "\"}", "value": prog})

#         #then display it using dispatcher
        
#         dispatcher.utter_message(text= "Choose study programme type" , buttons=buttons)     
    
#         return []    

class Button_Year(Action):
    def name(self) -> Text:
        return "action_button_year"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        year_list = [ f"{i:02d}" for i in range(9,22) ]
        
        # for y in year_list:
            # buttons.append({"title": f"20{y}-20{int(y)+1}" , "payload": '/request_exam_schedule{"academic_year":"{y}"}'})

        #then display it using dispatcher
        # dispatcher.utter_message(text= "Choose year" , buttons=buttons)     
        dispatcher.utter_message(text="Choose the academic year:\n(2009-2021)")
        return []    

class Button_Period(Action):
    def name(self) -> Text:
        return "action_button_period"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        period_list=[ "jan", "jun", "sep" ]
        period_list_full=["January", "June", "September"] 
        
        # for p,pf in zip(period_list, period_list_full):
            # buttons.append({"title": f"{pf}" , "payload": '/inform_period{"exam_period":"{p}"}'})

        #then display it using dispatcher
        # dispatcher.utter_message(text= "Choose exam period" , buttons=buttons)     
        dispatcher.utter_message(text= "Choose exam period:\n(January, June or September)")  
        return []    


class Button_Period_Semester(Action):
    def name(self) -> Text:
        return "action_button_period_semester"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        exams_flag=tracker.get_slot("exams")
        if exams_flag:
            dispatcher.utter_message(text= "Choose exam period:\n(January, June or September)")  
        else:
            dispatcher.utter_message(text= "Choose studies semester:\n(Spring or Winter)") 
        return []    

class Button_Semester(Action):
    def name(self) -> Text:
        return "action_button_semester"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        semester_list=[ "winter", "spring"]
        
        # for p,pf in zip(period_list, period_list_full):
            # buttons.append({"title": f"{pf}" , "payload": '/inform_period{"exam_period":"{p}"}'})

        #then display it using dispatcher
        # dispatcher.utter_message(text= "Choose exam period" , buttons=buttons)     
        dispatcher.utter_message(text= "Choose studies semester:\n(Spring or Winter)")  
        return []   

class Button_Programme(Action):
    def name(self) -> Text:
        return "action_button_programme"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = []
        #append the response of API in the form of title and payload
        programme_type_list = [ "PPS", "PMS" ]
        type_list = ["Undergraduate", "Postgraduate"]
        
        # for prog,prog_name in zip(programme_type_list,type_list):
            # buttons.append({"title": f"{prog_name}" , "payload": '/inform_programme{"grad_studies_type":"{prog}"}'})

        #then display it using dispatcher
        
        # dispatcher.utter_message(text= "Choose study programme type:" , buttons=buttons)  
        dispatcher.utter_message(text= "Choose study programme type:\n(Undergraduate or Postgraduate)")   
    
        return []                                 

# working well (due to different .xls format): 19-20, 20-21, 21-22, 22-23 
class ActionUniClassSchedule(Action):
    def name(self) -> Text:
        return "action_uni_class_schedule"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # schedule_path = "https://www.chatzi.org/dit-schedule/"
        # year_list = [ f"{i:02d}{i+1:02d}" for i in range(9,22) ]
        # semester_list = [ "winter", "spring" ]

        grad_stud_type = tracker.get_slot('grad_studies_type')
        exams = tracker.get_slot('exams')
        semester = tracker.get_slot('semester')
        academic_year = tracker.get_slot('academic_year')
        if academic_year==None:
            academic_year=21

        if len(str(academic_year))>2:
            academic_year = int(str(academic_year)[-2:])
            academic_year=int(str(academic_year).zfill(2))

        acad_years=str(academic_year).zfill(2)+"-"+str(academic_year+1).zfill(2)
        acad_years_sem=str(academic_year).zfill(2)+str(academic_year+1).zfill(2)

        # print(grad_stud_type, semester, academic_year)
        # file_url = os.path.join(schedule_path, f"")
        # file_url = "https://www.chatzi.org/dit-schedule/examsched_PMS_sep21.xls"
        
        file_url = f"https://www.di.uoa.gr/schedule/{acad_years}/timetable_{grad_stud_type}_{semester}{acad_years_sem}.xls"
        # print(file_url)

        timetable_df = pd.read_excel(file_url)
        # timetable_df.to_csv("timetableTest.csv", index=False, header=True)
        
        # print(timetable_df["Δευτέρα"].values)
        x=13
        Monday_df=timetable_df[:x]
        Tuesday_df=timetable_df[x+3:(x+3)+x].reset_index(drop=True)
        Wednesday_df=timetable_df[(x+3)+x+1+3:(x+3)*2+x].reset_index(drop=True)
        Thursday_df=timetable_df[(x+3)*2+x+1+3:(x+3)*3+x].reset_index(drop=True)
        Friday_df=timetable_df[(x+3)*3+x+1+3:].reset_index(drop=True)


        # print(Monday_df, Tuesday_df, Wednesday_df, Thursday_df, Friday_df)
        # columns ["Main", "A_1", "A_2", "B_", "C", "D", "E_", "ST", "Z_"]
        lecture_halls={"Main":"Αμφιθέατρο", "A_1":"Α1", "A_2":"Α2", "B_":"Β", "C":"Γ", "D":"Δ", "E_":"Ε", "ST":"ΣΤ", "Z_":"Ζ" }
        weekday_df=[Monday_df, Tuesday_df, Wednesday_df, Thursday_df, Friday_df]
        for df in weekday_df:
            if "Online" in timetable_df.values:
                col_names=["Time"]
                col_names.extend([f"Online{i}" for i in range(1,len(timetable_df.columns))])
                df.columns=col_names
            elif len(df.columns)==9:
                df.columns=["Time", "Main", "A_1", "A_2", "B_", "C", "D", "ST", "Z_"]
            else:
                df.columns=["Time", "Main", "A_1", "A_2", "B_", "C", "D", "E_", "ST", "Z_"]
                # print(df.columns)

        
        weekday_num_to_name={1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday"}
        class_sched_dict={}
        for weekday,df in enumerate(weekday_df):
            for (c_name,c_items) in df.iteritems():
                if c_name in lecture_halls or ("Online" in timetable_df.values):
                    if "Online" in timetable_df.values:
                        hall_name="Online"
                    else:
                        hall_name=lecture_halls[c_name]
                    lects=c_items.values.tolist()
                    # print(len(lects),len(df["Time"]))
                    lects=[ item.split("\n") if type(item)==str else item for item in lects ]
                    for l_ind,l in enumerate(lects):
                        if type(l)==list and len(l)>1:
                            # if len(l)>3:
                            #     print(l)
                            class_name=l[0].strip()
                            class_type=l[1].strip()
                            professors=l[2:]

                            weekday_name=weekday_num_to_name[weekday+1]
                            if class_name not in class_sched_dict:
                                class_sched_dict[class_name]={}
                                class_sched_dict[class_name]["Type"]=class_type
                                class_sched_dict[class_name]["Professors"]=professors
                                class_sched_dict[class_name]["Timetable"]={}

                            if weekday_name not in class_sched_dict[class_name]["Timetable"]:
                                class_sched_dict[class_name]["Timetable"][weekday_name]={}
                                class_sched_dict[class_name]["Timetable"][weekday_name]["Hall"]=hall_name
                                # print(class_name, df["Time"].values[l_ind])
                                class_sched_dict[class_name]["Timetable"][weekday_name]["Start"]=df["Time"].values[l_ind].split("-")[0]
                                class_sched_dict[class_name]["Timetable"][weekday_name]["End"]=df["Time"].values[l_ind].split("-")[1]
                            
                            # if class_sched_dict[class_name]["Timetable"][weekday_name]["End"]!=None:
                                # class_sched_dict[class_name]["Timetable"][weekday_name]["Start"]=df["Time"].values[l.index].split("-")[0]
                            class_sched_dict[class_name]["Timetable"][weekday_name]["End"]=df["Time"].values[l_ind].split("-")[1]
                            
                    # print(hall_name, lects)
        class_sched_dict = dict(sorted(class_sched_dict.items()))
        # print(class_sched_dict)
        print_str=""
        for i,k in enumerate(class_sched_dict):
            print_str+=f"{k} ({class_sched_dict[k]['Type']} | {', '.join(class_sched_dict[k]['Professors'])})\n"
            for day in class_sched_dict[k]['Timetable']:
                print_str+=f"{day}: {class_sched_dict[k]['Timetable'][day]['Hall']} | {class_sched_dict[k]['Timetable'][day]['Start']}-{class_sched_dict[k]['Timetable'][day]['End']}\n"
            print_str+=" \n"
        
        dispatcher.utter_message(f"\nFound this timetable ({grad_stud_type,semester,acad_years}) : \n{print_str} \n \n ")
        # print(print_str)
        return []

class ActionUniExamSchedule(Action):
    
    def name(self) -> Text:
        return "action_uni_exam_schedule"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        period_list = [ "jan", "jun", "sep" ]
        programme_type_list = [ "PPS", "PMS" ]

        grad_stud_type = tracker.get_slot('grad_studies_type')
        exams = tracker.get_slot('exams')
        period = tracker.get_slot('exam_period')
        academic_year = tracker.get_slot('academic_year')
        if academic_year==None:
            academic_year=22
        
        academic_year=int(str(academic_year)[-2:]) if len(str(academic_year))>2 else int(str(academic_year))

        acad_years=str(int(academic_year)-1).zfill(2)+"-"+str(academic_year).zfill(2)
        file_url = f"https://www.chatzi.org/dit-schedule/{acad_years}/examsched_{grad_stud_type}_{period}{str(academic_year).zfill(2)}.xls"
        # print(file_url)
        timetable_df = pd.read_excel(file_url)
    
        # Πρόγραμμα Εξετάσεων Προπτυχιακών Μαθημάτων Χειμερινής Περιόδου 2021 -> Date -> Date
        # Unnamed: 1 -> Time1
        # Unnamed: 2 -> Time2
        # Unnamed: 3 -> Time3
        # Unnamed: 3 -> Time4
        # timetable_df.rename(columns={"Πρόγραμμα Εξετάσεων Προπτυχιακών Μαθημάτων Χειμερινής Περιόδου 2021":"Date", "Unnamed: 1": "Time1", "Unnamed: 2": "Time2", "Unnamed: 3": "Time3"}, inplace=True)
        if 'Unnamed: 5' in list(timetable_df.columns):
        # better make a general rule about multiple column counts
            timetable_df.columns=["Date", "Time1", "Time2", "Time3", "Time4","Time5"]
        elif 'Unnamed: 4' in list(timetable_df.columns):
            timetable_df.columns=["Date", "Time1", "Time2", "Time3", "Time4"]
        elif 'Unnamed: 3' in list(timetable_df.columns):
            timetable_df.columns=["Date", "Time1", "Time2", "Time3"]
        else:
            timetable_df.columns=["Date", "Time1", "Time2"]
            # timetable_df.rename(columns={"Unnamed 4": "Time4"}, inplace=True)
        # print(type(timetable_df["Date"][2]))
        # print(timetable_df["Date"][2].date().strftime('%A %d-%m-%y'))
        timetable_df["Date"] = timetable_df["Date"].apply(lambda x: x.date().strftime('%A %d-%m-%Y') if isinstance(x, datetime) else x)
        # timetable_df.to_csv(f"exams{grad_stud_type}{exams}{academic_year}Timetable.csv", index=False, header=True)

        #list of classes arranged alphabetically - date(day, date) - time
        all_classes=list(set([c for sublist in timetable_df.iloc[1:,1:].values for c in sublist if type(c)==str]))

        all_classes=sorted(all_classes)
        class_str=""
        for num,element in enumerate(all_classes):
            i, c = np.where(timetable_df == element)
            class_str+=f"{num+1}. {element} -> {timetable_df.iloc[i[0],0]}, {timetable_df.iloc[0,c[0]]}\n" 

        dispatcher.utter_message(f"\nFound this timetable: \n{class_str}\n")
        
        #TODO: insert buttons for subject choice ?
        return []

class ActionUniClassExamTimetable(Action):
    def name(self) -> Text:
        return "action_class_exam_timetable"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        exams_flag=tracker.get_slot("exams")
        if exams_flag:
            return [FollowupAction("action_uni_exam_schedule")]
        else:
            return [FollowupAction("action_uni_class_schedule")]
        

class ActionCheckExamsFormSlots(Action):
    def name(self) -> Text:
        return "action_correct_examform_slots"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gradType={"PPS":"Undergraduate", "PMS":"Postgraduate"}
        grad_stud_type=tracker.get_slot("grad_studies_type")
        period=tracker.get_slot("exam_period")
        semester=tracker.get_slot("semester")
        per={"jan":"January", "jun":"June", "sep":"September"}
        academic_year=tracker.get_slot("academic_year")
        
        # get_entities
        # check_entities=["user_name", "exams", "grad_studies_type", "exam_period", "semester", "academic_year"]
        # for entity_name in check_entities:
        #     entity_val=next(tracker.get_latest_entity_values(entity_name), None)
            
        #     dispatcher.utter_message(f"{entity_name}: {entity_val}")

        # exams = tracker.get_slot("exams")
        # exams_str="exams" if exams else "classes"

        exams_slot=tracker.get_slot("exams")
        intent=tracker.latest_message['intent'].get('name')
        # dispatcher.utter_message(f"Intent: {intent}")
        # dispatcher.utter_message(f"{exams_slot},{type(exams_slot)==type(True)}")
        if intent not in ["request_exam_schedule", "request_class_schedule"]:
            if exams_slot:
                exam_flag_value=True
                exams=True
                exams_str="exams"
                per_sem="period"
            else:
                exam_flag_value=False
                exams=False
                exams_str="classes"
                per_sem="semester"
        else:
            if intent=="request_exam_schedule":
                exam_flag_value=True
                exams=True
                exams_str="exams"
                per_sem="period"
            else:
                exam_flag_value=False
                exams=False
                exams_str="classes"
                per_sem="semester"
        
        if academic_year!=None and not exams and int(academic_year) not in [19,20,21,2019,2020,2021]:
            academic_year=None
            dispatcher.utter_message(f"The year must be either 2019, 2020 or 2021 !\n")
        

        if exams:
            list_to_fill=[grad_stud_type, period, academic_year]
        else:
            list_to_fill=[grad_stud_type, semester, academic_year]
        
        if None in list_to_fill:
            username=tracker.get_slot("user_name")
            dispatcher.utter_message(f"\nYou haven't chosen the type and/or year and/or {per_sem} of the {exams_str} {username} =)\nI will now help you fill the necessary information, is that ok?")
            return [SlotSet("exams",exam_flag_value)]
        
        
        if exams:
            ac_year=int(str(academic_year)[-2:]) if len(str(academic_year))>2 else int(str(academic_year))
            file_url = f"https://www.chatzi.org/dit-schedule/{ac_year-1:02d}-{ac_year:02d}/examsched_{grad_stud_type}_{period}{ac_year}.xls"
            dispatcher.utter_message(f"\nYou have chosen to see the {gradType[grad_stud_type]} {exams_str} timetable of {per[period]} for the year '{ac_year}, does anything need correction?\n(file: {file_url})")
        # timetable_df=pd.read_excel(file_url)
        else:
            ac_year=int(str(academic_year)[-2:]) if len(str(academic_year))>2 else int(str(academic_year))
            file_url = f"https://www.di.uoa.gr/schedule/{str(ac_year).zfill(2)}-{str(int(ac_year+1)).zfill(2)}/timetable_{grad_stud_type}_{semester}{str(ac_year).zfill(2)}{str(ac_year+1).zfill(2)}.xls"
            dispatcher.utter_message(f"\nYou have chosen to see the {gradType[grad_stud_type]} {exams_str} timetable of {semester} for the year '{ac_year}, does anything need correction?\n(file: {file_url})")

    
        return [SlotSet("exams",exam_flag_value)]


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
        
        num_of_anns = tracker.get_slot('num_of_announcements')
        if num_of_anns==None:
            dispatcher.utter_message("You haven't chosen the number of announcements, so I'm gonna show you the first 10 =)\n")
            num_of_anns=10
        else:
            num_of_anns=int(num_of_anns)

        ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split("/") if item.isnumeric()  }
        if not ann_list:
            ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  }

        ann_list_sorted = {k: v for k, v in sorted(ann_list.items(), key=lambda item: item[0])}
        
        announcement_text=""
        text_all = f"Here are the {num_of_anns} most recent NKUA Announcements:"
        for i,num in enumerate(list(ann_list_sorted.keys())[:num_of_anns]):
            name = ann_list_sorted[num]
            if announcements_url[-1]=="/":
                link_path=f"{announcements_url}{str(num)}"
            else:
                link_path=f"{announcements_url}/{str(num)}"
            # link_path = os.path.join(announcements_url,str(num))
            announcement_text+=f"\n\n{i+1}. {name} ({link_path})"
            page = urlopen(link_path)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            summary=soup.find_all("div", attrs={"class":"clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item"})

            announcement_text+=f"\nSummary: {summary[1].get_text()}"
        
        dispatcher.utter_message(announcement_text)
        dispatcher.utter_message(f"")
        dispatcher.utter_message(f"\nFor further information and announcements, you can visit the University's Announcements Page here: {announcements_url}\n")

        return []


class ActionUniStaffInfo(Action):
    
    def name(self) -> Text:
        return "action_uni_staff_info"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        staff_url = "https://www.di.uoa.gr/staff/"

        # DEP:      announcements_url + ?field_staff_specialty_target_id=7
        # EDIP:     announcements_url + ?field_staff_specialty_target_id=8
        # ETEP:     announcements_url + ?field_staff_specialty_target_id=30
        # SECRET:   announcements_url + ?field_staff_specialty_target_id=29
        info_dict={}
        for specialty_id in [7,8,30,29]:
            # if secretary, display them separately, first
            # if specialty_id==29:
            #     print("\n--> Secretary:")
            page = urlopen(staff_url+f"?field_staff_specialty_target_id={specialty_id}")
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            links_raw = soup.find_all('div', attrs={"class":"col col-xs-12 col-sm-12 col-md-6 col-lg-4"})
            
            for i,l in enumerate(links_raw):
                staff_id=int(l.find_all('a')[0]["href"].split("/")[-1])
                info_dict[staff_id]={}

                # Name
                name=l.find_all('a')[0].get_text()
                name=name.strip()

                # Phone Number
                ph_num=l.find_all("div", attrs={"class":"field-content people-phone"} )[0].get_text()
                ph_num=ph_num.strip()
                ph_num=re.sub(" ","",ph_num)

                # Email Address
                mail_add=l.find_all("div", attrs={"class":"email"} )[0].get_text()
                mail_add=mail_add.strip()
                mail_parts=mail_add.split(' ')
                # username + @di.uoa.gr 
                mail_add=f"{mail_parts[0]}@di.uoa.gr"
                
                # Stuff Type
                stuff_type=l.find_all("div", attrs={"class":"field-content people-speciality"})[0].get_text()
                stuff_type=stuff_type.strip()

                info_dict[staff_id]["Name"]=name
                info_dict[staff_id]["StaffType"]=stuff_type
                # info_dict[staff_id]["Level"]=lvl
                info_dict[staff_id]["MailAddress"]=mail_add
                info_dict[staff_id]["Number"]=ph_num

                # if secretary, display them separately, first
                # if specialty_id==29:
                    # print(f"{name}: {ph_num} - {mail_add} ({stuff_type})")

        staff_str="Here is the contact information of Uni's Staff:\n"
        for st_id in info_dict.keys():
            
            staff_str+=f"{info_dict[st_id]['Name']}: {info_dict[st_id]['Number']} - {info_dict[st_id]['MailAddress']} ({info_dict[st_id]['StaffType']})\n"
            # print(staff_str)
        
        dispatcher.utter_message(staff_str)
        dispatcher.utter_message(f"")
        dispatcher.utter_message(f"\nFor further staff information, you can visit the University's Staff Page here: {staff_url}\n")

        return []

class ActionUniContactLocInfo(Action):
    
    def name(self) -> Text:
        return "action_uni_contact_loc_info"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cont_loc_url = "https://www.di.uoa.gr/department/contact-location"
        uoa_url = "https://www.di.uoa.gr"

        # DEP:      announcements_url + ?field_staff_specialty_target_id=7
        # EDIP:     announcements_url + ?field_staff_specialty_target_id=8
        # ETEP:     announcements_url + ?field_staff_specialty_target_id=30
        # SECRET:   announcements_url + ?field_staff_specialty_target_id=29
        info_dict={}
        
        # if secretary, display them separately, first
        # if specialty_id==29:
        #     print("\n--> Secretary:")
        page = urlopen(cont_loc_url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        
        contact = soup.find_all('div', attrs={"class":"views-element-container clearfix block block-views block-views-blockcontact-info-block-5"})
        contact=contact[0].get_text()
        contact=re.sub(" +"," ",contact)
        contact=re.sub("\n+","\n", contact)
        contact_lines=contact.split("\n")
        contact_lines=[c_line.strip() for c_line in contact_lines[2:]]
        contact="\n".join(contact_lines)
        # print(f"Contact/Location Information: \n{contact}")
        
        access = soup.find_all('div', attrs={"class":"paragraph paragraph--type--bp-simple paragraph--view-mode--default paragraph--id--1712"})
        access=access[0].get_text()
        access=re.sub(" +"," ",access)
        access=re.sub("\n+","\n", access)
        access_lines=access.split("\n")
        access_lines=[a_line.strip() for a_line in access_lines[3:]]
        access="\n".join(access_lines)
        # print(f"University Access: \n{access}")

        # loc = soup.find_all('div', attrs={"class":"paragraph paragraph--type--bp-view paragraph--view-mode--default paragraph--id--1710"})
        # loc=loc[0].get_text()
        # loc=re.sub(" +"," ",loc)
        # loc=re.sub("\n+","\n", loc)
        # print(f"Location: {loc}")

        cont_loc_str=f"Contact/Location Information: \n{contact}"
        cont_loc_str+="\n\n" 
        cont_loc_str+=f"University Access: \n{access}"

        dispatcher.utter_message(cont_loc_str)
        dispatcher.utter_message(f"")
        dispatcher.utter_message(f"\nFor further Uni Access/Contact/Location information, you can visit the University's Page here: {cont_loc_url}\n")

        
        return []



# write action to fill all the slots from intent values after step-by-step intent filling ?!