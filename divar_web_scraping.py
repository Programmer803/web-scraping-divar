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
my_db = my_Database("Divar_2.db")
while 1==1:
    data = requests.get("https://divar.ir/s/sanandaj")



    soup = BeautifulSoup(data.content , "html.parser")
    # ****************************************

    # for d in soup.find_all("div",{"class":"book-item"}):
    #     print(d.find("a").text)

 
    
    
    # print(pic[1].find("a")["href"])

    time.sleep(2)
    print("[-]")
    pic = soup.find_all("div",{"class":"post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46"})
        
    try:
        for i in range(len(pic)):
                url = "https://divar.ir"+str(pic[i].find("a")["href"])
                
                data = requests.get(url)

                soup_ = BeautifulSoup(data.content , "html.parser")
                try:
                    info = str(soup_.find("p",{"class":"kt-unexpandable-row__value"}).text)
                except:
                    info = "None"
                info_2 = str(soup_.find("p",{"class":"kt-description-row__text kt-description-row__text--primary"}).text)
                img = soup_.find("div",{"class":"kt-carousel__slide-container"})

                img = str(img.find("img")["src"])
                title = str(soup_.find("div",{"class":"kt-page-title__title kt-page-title__title--responsive-sized"}).text)


                time_ = str(time.strftime("%Y-%m-%d-%H-%M-%S"))

                hash_ = hashlib.sha256(str(title+info+img+info_2+url).encode()).hexdigest()



                
                my_db.execute_(f"INSERT INTO divar_info VALUES('{title}','{info}','{time_}','{img}','{info_2}','{hash_}','{url}')")
                print(url)

    except:
        pass    








