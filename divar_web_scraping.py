from bs4 import *
import requests
import time
import hashlib
import sqlite3

class my_Database():

    def __init__(self,name):
    
        # -----------------------------
        self.data_base = name
        self.connect = sqlite3.connect(self.data_base)
        self.act = self.connect.cursor()
        self.path = None
        # -----------------------------

    def get_data(self,data):

        self.act.execute(data)
        d__b = self.act.fetchall()
        self.connect.commit()
        return d__b
        
    def execute_(self,data):

        self.act.execute(data)
        self.connect.commit()
my_db = my_Database("Divar_data.db")


while True:
    data = requests.get("https://divar.ir/s/sanandaj")

    soup = BeautifulSoup(data.content , "html.parser")

    time.sleep(2)
    
    all_Ad = soup.find_all("div",{"class":"post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46"})
        
    try:
        for i in range(len(all_Ad)):
                
                # Ad page
                url = "https://divar.ir"+str(all_Ad[i].find("a")["href"])
                
                # *************************************************************
                data = requests.get(url)

                soup_ = BeautifulSoup(data.content , "html.parser")

                try:
                    info = str(soup_.find("p",{"class":"kt-unexpandable-row__value"}).text)
                except:
                    info = "None"

                # Information
                info_2 = str(soup_.find("p",{"class":"kt-description-row__text kt-description-row__text--primary"}).text)

                img = soup_.find("div",{"class":"kt-carousel__slide-container"})

                # Get image src
                img = str(img.find("img")["src"])

                # Get title
                title = str(soup_.find("div",{"class":"kt-page-title__title kt-page-title__title--responsive-sized"}).text)

                # Get time
                time_ = str(time.strftime("%Y-%m-%d-%H-%M-%S"))

                # Make hash
                hash_ = hashlib.sha256(str(title+info+img+info_2+url).encode()).hexdigest()

                # Save data in database
                my_db.execute_(f"INSERT INTO divar_info VALUES('{title}','{info}','{time_}','{img}','{info_2}','{hash_}','{url}')")

                print("[+] -> ", url)

    except:
        print("[-]")








