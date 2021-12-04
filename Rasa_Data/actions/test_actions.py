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

    page = requests.get(url)
    # html = page.read().decode("utf-8")
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.div)

    # print("examsched" in soup.prettify())

    
    # all_tags= soup.find_all(True)
    # tag_list = set( [i.name for i in all_tags] )
    # for tag in tag_list:
    #     tag_items = soup.find_all(tag)
    #     for item in tag_items:
    #         # print(item.children)
    #         for i in item.children:
    #             print(i)
    #             if "examsched" in i:
    #                 print(i)
    #     # print("examsched" in soup.prettify())

    
    # exit()
    # print(tags)

    # links_raw = soup.find_all(string="examsched #")
    # print(links_raw)
    # for i in links_raw:
    #     # if "examsched" in i and "href" in i:
    #     print(i)
    

    exit()

    links = [ link for link in links_raw  ]
    examsched_links = [ link for link_list in links_raw for link in link_list.find_all('a') if "examsched" in link['href'] ]
    timetable_links = [ link for link_list in links_raw for link in link_list.find_all('a') if "timetable" in link['href'] ]
    
    for i in examsched_links:
        print(i['href'])
    for i in timetable_links:
        print(i['href'])

    # for link in i.find_all('a'):
    #     if "examsched" in 
    #     print(link['href'])

    # ann_list = [ item:ann.contents for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  ]
    # ann_list = { int(item):str(ann.contents[0]).strip() for ann in links for item in ann['href'].split(os.sep) if item.isnumeric()  }

    # print(ann_list)



'''
____________________________________________________________________________________
'''

# main

# ActionUniPsychoSupportInfo()
# ActionUniAnnouncements()
# ActionUniClassSchedule()