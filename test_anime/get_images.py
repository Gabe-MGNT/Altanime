import requests
import pandas as pd
import json
import urllib
import os
import time
import random
df = pd.read_csv("anime.csv")
df["images"] = ""



def main():
    for index, row in df.iterrows():
        if row["images"] != "":
            continue
        id_anime = row["id"]
        
        if not os.path.exists("img/"+str(id_anime)):
                    os.makedirs("img/"+str(id_anime))
        else:
                    print("skipped")
                    continue
        url_api = "https://api.jikan.moe/v4/anime/"+str(id_anime)+"/pictures"
        response = requests.get(url_api)
        if response.status_code == 404:
              continue
        json_object = json.loads(response.text)


        images = json_object["data"]
        try :
            nique(id_anime, images)
        except Exception as e:
            continue

        

def nique(id_anime, images):
    nb = 0
    for image in images:
            nb += 1
            for name, url_image in (image["jpg"]).items():

                    

                print(name, url_image)
                urllib.request.urlretrieve(url_image, "img/"+str(id_anime)+"/"+name+"-"+str(nb)+".jpg")
                print("Attendre 2s ou 5s")
                time.sleep(random.randint(5,7))
                print("Fin attente")
                


if  __name__ == "__main__":
    main()