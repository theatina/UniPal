
from ctypes.wintypes import HENHMETAFILE
from datetime import time, datetime, date
import pandas as pd
import sys
import re
import os
import certifi
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()
import numpy as np

import certifi
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

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
    
    
def ActionUniExamSchedule():
    
    url = "https://www.chatzi.org/dit-schedule/"
    #/pps/jan/1819"

    # page = urlopen(url)
    # html = page.read().decode("utf-8")
    # soup = BeautifulSoup(html, "html.parser")

    # schedule_path = "https://www.chatzi.org/dit-schedule/"
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
    academic_year = 2014
    if len(str(academic_year))>2:
        academic_year = int(str(academic_year)[-2:])
        academic_year=int(str(academic_year).zfill(2))

    acad_years=str(academic_year-1).zfill(2)+"-"+str(academic_year).zfill(2)

    # print(grad_stud_type, semester, academic_year)
    # file_url = os.path.join(schedule_path, f"")
    # file_url = "https://www.chatzi.org/dit-schedule/examsched_PMS_sep21.xls"
    
    file_url = f"https://www.chatzi.org/dit-schedule/{acad_years}/examsched_{grad_stud_type}_{period}{int(academic_year)}.xls"
    # file_url = f"https://www.chatzi.org/dit-schedule/#/{grad_stud_type}/{exams}/{academic_year}"
    print(file_url)

    timetable_df = pd.read_excel(file_url)
    print(timetable_df)

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
    # print(timetable_df["Date"])
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


def ActionUniStaffInfo():
    announcements_url = "https://www.di.uoa.gr/staff/"
    uoa_url = "https://www.di.uoa.gr"

    # DEP:      announcements_url + ?field_staff_specialty_target_id=7
    # EDIP:     announcements_url + ?field_staff_specialty_target_id=8
    # ETEP:     announcements_url + ?field_staff_specialty_target_id=30
    # SECRET:   announcements_url + ?field_staff_specialty_target_id=29
    info_dict={}
    for specialty_id in [7,8,30,29]:
        # if secretary, display them separately, first
        # if specialty_id==29:
        #     print("\n--> Secretary:")
        page = urlopen(announcements_url+f"?field_staff_specialty_target_id={specialty_id}")
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

    # with open(r"staff.txt", "w", encoding="utf-8") as writer:

        for st_id in info_dict.keys():
            
            staff_str=f"{info_dict[st_id]['Name']}: {info_dict[st_id]['Number']} - {info_dict[st_id]['MailAddress']} ({info_dict[st_id]['StaffType']})"
            print(staff_str)
            # writer.write(staff_str+"\n")

    return None


def ActionUniAccessInfo():
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
    print(f"Contact/Location Information: \n{contact}")
    
    access = soup.find_all('div', attrs={"class":"paragraph paragraph--type--bp-simple paragraph--view-mode--default paragraph--id--1712"})
    access=access[0].get_text()
    access=re.sub(" +"," ",access)
    access=re.sub("\n+","\n", access)
    access_lines=access.split("\n")
    access_lines=[a_line.strip() for a_line in access_lines[3:]]
    access="\n".join(access_lines)
    print(f"University Access: \n{access}")

    # loc = soup.find_all('div', attrs={"class":"paragraph paragraph--type--bp-view paragraph--view-mode--default paragraph--id--1710"})
    # loc=loc[0].get_text()
    # loc=re.sub(" +"," ",loc)
    # loc=re.sub("\n+","\n", loc)
    # print(f"Location: {loc}")

    
    return None

def ActionUniClassSchedule():
    
    url = "https://www.di.uoa.gr/announcements"
    #/pps/jan/1819"

    # page = urlopen(url)
    # html = page.read().decode("utf-8")
    # soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # tags=soup.find_all('a')
    # for t in tags:
    #     print(t.get_text())

    # schedule_path = "https://www.chatzi.org/dit-schedule/"
    # year_list = [ f"{i:02d}{i+1:02d}" for i in range(9,22) ]
    # semester_list = [ "winter", "spring" ]

    # grad_stud_type = tracker.get_slot('grad_studies_type')
    # exams = tracker.get_slot('exams')
    # semester = tracker.get_slot('semester')
    # academic_year = tracker.get_slot('academic_year')

    # exit()
    grad_stud_type = "PPS"
    semester = "winter"
    # semester = "winter"
    academic_year = 2022
    if len(str(academic_year))>2:
        academic_year = int(str(academic_year)[-2:])
        academic_year=int(str(academic_year).zfill(2))

    acad_years=str(academic_year).zfill(2)+"-"+str(academic_year+1).zfill(2)
    acad_years_sem=str(academic_year).zfill(2)+str(academic_year+1).zfill(2)

    # print(grad_stud_type, semester, academic_year)
    # file_url = os.path.join(schedule_path, f"")
    # file_url = "https://www.chatzi.org/dit-schedule/examsched_PMS_sep21.xls"
    
    file_url = f"https://www.di.uoa.gr/schedule/{acad_years}/timetable_{grad_stud_type}_{semester}{acad_years_sem}.xls"
    print(file_url)

    timetable_df = pd.read_excel(file_url)
    timetable_df.to_csv("timetableTest.csv", index=False, header=True)
    
    # print(timetable_df.head)
    # exit()
    
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
        else:
            df.columns=["Time", "Main", "A_1", "A_2", "B_", "C", "D", "E_", "ST", "Z_"]
        # print(df.columns)

    
    weekday_num_to_name={1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday"}
    class_sched_dict={}
    for weekday,df in enumerate(weekday_df):
        for (c_name,c_items) in df.iteritems():
            if c_name in lecture_halls or ("Online" in timetable_df.values):
                # print(c_name)
                if "Online" in timetable_df.values:
                    hall_name="Online"
                else:
                    hall_name=lecture_halls[c_name]
                lects=c_items.values.tolist()
                # print(len(lects),len(df["Time"]))
                # print(lects)
                lects=[ item.split("\n") if type(item)==str else item for item in lects ]
                # print(lects)
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
        print_str+="\n"

    print(print_str)
    return None
    



'''
____________________________________________________________________________________
'''

# main

# ActionUniPsychoSupportInfo()
# ActionUniAnnouncements()
# ActionUniClassSchedule()
ActionUniExamSchedule()
# ActionUniStaffInfo()
# ActionUniAccessInfo()
# ActionUniRetrieveAllFiles()
# ActionUniAcademicTimetable()
