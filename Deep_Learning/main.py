
import json
import tensorflow as tf
import keras
from keras import layers
from numpy import random
import numpy as np
import requests
import time 

pteroaomrea = []

def sanitize_name(pname):
    final_name = pname.lower().replace(" ", "-").replace("'","").replace(",","").replace("í","i").replace("é","e").replace(".","")
    if "/" in pname:
        final_name = final_name.split("/")[0][:-1]
        return final_name
    else:
        return final_name

def get_salt_score(pname):
    """
    HERE GATHER ALL THE SALT SCORES BY INDIVUDALLY CARD BY CARD MAKING A PULL REQUEST TO THE 
    EDHREC JSON, PRAYING THEY DONT BLOCK MY IP 
    putting a delay in there and doing name stuff so it gets to the right card. 
    """
    #Turn name correct
    advanced_name = sanitize_name(pname)
    #Ping json edhrec for the data
    try:
        response = requests.get('https://json.edhrec.com/cards/'+advanced_name)
        #parse it (basically)
        jsonResponse = response.json()
         #Reutrn salt score
        return jsonResponse["salt"]
    except:
        pteroaomrea.append(advanced_name)
        return None
    
   
    
def gather_data():
    #try to see if the data.json is already there (Which is should be)
    try:
        ERRORxERRORxERROER 
        with open('data.json', 'w', encoding='utf-8') as f:
            return json.load(f)
    #If not, make it, 
    except:
        #Start from the larger data json
        dataRaw = open("Deeplearning/default-cards-20240302220650.json", encoding="utf-8")
        dataLoaded = json.load(dataRaw)
        #These are the keys we want,
        wanted_key = ['name', 'lang', 'released_at', 'layout', 'highres_image', 'image_status', 'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 'colors', 'color_identity', 'keywords', 'legalities', 'games', 'reserved', 'finishes', 'oversized', 'promo', 'reprint', 'variation', 'set', 'set_name', 'set_type', 'collector_number', 'digital', 'rarity', 'flavor_text', 'artist', 'border_color', 'frame', 'full_art', 'textless', 'booster', 'story_spotlight', 'edhrec_rank', 'penny_rank', 'prices']
        wanted_list = []
        already_named = {}
        #For each card
        for i in dataLoaded:
            #Only gather the wanted keys
            all_keys = i.keys()
            for x in wanted_key:
                if not x in all_keys:
                    i[x] = ""
            dict_you_want = {key: i[key] for key in wanted_key}

            #check if we have already gathered the information about it. 
            try:
                #if its already in there, then continue.
                already_named[dict_you_want["name"]] 
                print("Duplicate Found")
                continue
            except: 
                #if not, then continue. 
                pass
            #Gather the salt score for that specific card
            time.sleep(0.01)
            
            salt_score = get_salt_score(dict_you_want["name"])
            if salt_score == None:
                continue
            #Add it to the dict
            dict_you_want["salt"] = salt_score
            wanted_list.append(dict_you_want)
            already_named[dict_you_want["name"]] = 1 

        #print this to a file!
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(wanted_list, f, ensure_ascii=False, indent=4)

        print(pteroaomrea)


        return wanted_list
    


def make_deep_learning():
    pass

def split_data(p_data):
    random.shuffle(p_data)
    length = len(p_data)
    k1 = int((length * 7)/10)
    k2 = int((length * 9)/10)
    training = p_data[:k1]
    validation = p_data[k1:k2]
    testing = p_data[k2:]


    return training, validation, testing

def main():
    data = gather_data()
    training,validation,testing  = split_data(data)
    print(len(data))
    print(len(training))
    print(len(validation))
    print(len(testing))



    #inputs = keras.Input(shape=(784,))



    #model = keras.Sequential(
    #    [
    #     
    #        layers.Dense(2, activation="relu", name="layer1"),
    #        layers.Dense(3, activation="relu", name="layer2"),
    #        layers.Dense(4, name="layer3"),
    #    ]
    #)





main()