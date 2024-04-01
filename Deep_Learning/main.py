
import json
import tensorflow as tf
import keras
from keras import layers
from numpy import random
import numpy as np
import requests
import time 
import flatdict
import itertools


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
        return None
    
   
    
def gather_data():
    #try to see if the data.json is already there (Which is should be)
    try: 
            x = open('data.json', 'r+', encoding='utf-8')
            return json.load(x)
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

        return wanted_list
    



def preprocessing(pdata): 
    """
    Need to remove all of the variables that stop it from being a inhomogenous vector. 
    Making it so all vectors are of the same length by padding the keywords and colours. 
    """
    #First the colours, 
    current = pdata.pop('colors')
    for i in ["W","U","B","R","G"]:
        if i in current:
            pdata["has_"+i] = True
        else: 
            pdata["has_"+i] = False

    #Then Colour Identities
    current = pdata.pop('color_identity')
    for i in ["W","U","B","R","G"]:
        if i in current:
            pdata["has_"+i+"_identity"] = True
        else: 
            pdata["has_"+i+"_identity"] = False

    #Then the Keywords. 
    current = pdata.pop('keywords')

    all_keywords = ["Deathtouch", "Defender", "Double strike", "Enchant", "Equip", "Mill", 
                    "First strike", "Flash", "Flying", "Haste", "Hexproof", "Indestructible", 
                    "Intimidate", "Landwalk", "Lifelink", "Protection", "Reach", "Shroud", 
                    "Trample", "Vigilance", "Ward", "Fight", "Banding", "Rampage", 
                    "Cumulative upkeep", "Flanking", "Phasing", "Buyback", "Shadow", "Cycling", 
                    "Scry", "Echo", "Horsemanship", "Fading", "Kicker", "Flashback", "Madness", 
                    "Fear", "Morph", "Amplify", "Provoke", "Storm", "Fateseal", "Affinity", 
                    "Entwine", "Clash", "Modular", "Sunburst", "Bushido", "Soulshift", "Splice", 
                    "Offering", "Ninjutsu", "Epic", "Convoke", "Dredge", "Transmute", "Bloodthirst", 
                    "Haunt", "Replicate", "Forecast", "Graft", "Recover", "Ripple", "Split second", 
                    "Suspend", "Vanishing", "Delve", "Frenzy", "Gravestorm", "Transfigure", 
                    "Champion", "Changeling", "Evoke", "Hideaway", "Prowl", "Proliferate", 
                    "Detain", "Populate", "Transform", "Reinforce", "Conspire", 
                    "Will of the council", "Council's dilemma", "Persist", "Wither", "Bolster", 
                    "Retrace", "Devour", "Exalted", "Unearth", "Cascade", "Manifest", "Support", 
                    "Investigate", "Meld", "Goad", "Exert", "Explore", "Annihilator", "Level Up", 
                    "Assemble", "Rebound", "Totem armor", "Surveil", "Infect", "Adapt", "Amass", 
                    "Learn", "Battle Cry", "Living weapon", "Venture into the dungeon", "Undying", 
                    "Connive", "Miracle", "Soulbond", "Overload", "Scavenge", "Open an Attraction", 
                    "Roll to Visit Your Attractions", "Unleash", "Convert", "Cipher", "Incubate", 
                    "Evolve", "Extort", "Fuse", "Bestow", "Tribute", "Hidden agenda", "Outlast", 
                    "Prowess", "Dash", "Exploit", "Menace", "Renown", "Awaken", "Myriad", 
                    "Discover", "Surge", "Collect evidence", "Skulk", "Emerge", "Escalate", 
                    "Melee", "Crew", "Fabricate", "Partner", "Suspect", "Undaunted", "Improvise", 
                    "Aftermath", "Ascend", "Assist", "Mentor", "Afterlife", "Riot", "Spectacle", 
                    "Escape", "Companion", "Mutate", "Encore", "Boast", "Foretell", "Daybound", 
                    "Nightbound", "Disturb", "Cleave", "Training", "Compleated", "Reconfigure", 
                    "Blitz", "Casualty", "Enlist", "Ravenous", "Squad", "Prototype", "Living metal", 
                    "More Than Meets the Eye", "For Mirrodin!", "Toxic", "Backup", "Bargain", 
                    "Craft", "Disguise", "Solved"]

    for i in all_keywords:
        
        if i in current:
            pdata["has_keyword_"+i] = True
        else: 
            pdata["has_keyword_"+i] = False

    current = pdata.pop('games')
    for i in ["paper","mtgo","arena"]:
        if i in current:
            pdata["is_in_"+i] = True
        else: 
            pdata["is_in_"+i] = False

    current = pdata.pop('finishes')
    for i in ["nonfoil","foil"]:
        if i in current:
            pdata["is_finish_"+i] = True
        else: 
            pdata["is_finish_"+i] = False

    # remember to pop the salt score because it is no longer at the end
              
    return pdata

def gather_ready_data(pdata, grouping):
    #try to see if the data.json is already there (Which is should be)
    #pdata is the data we will make the file on if it does not already exsist. 
    #Grouping which section of the data it is, will return the corresponding arrays
    try: 
        ERRORxERROR
        if grouping == "training":
            x = open('training_data.json', 'r+', encoding='utf-8')
            y = open('training_data_labels.json', 'r+', encoding='utf-8')
        elif grouping == "validation":
            x = open('validation_data.json', 'r+', encoding='utf-8')
            y = open('validation_data_labels.json', 'r+', encoding='utf-8')
        elif grouping == "testing":
            x = open('testing_data.json', 'r+', encoding='utf-8')
            y = open('testing_data_labels.json', 'r+', encoding='utf-8')
        return np.array(json.load(x)) , np.array(json.load(y))
    #If not, make it, 
    except:
        final_list = []
        y_vec = []
        counter = 0
        for i in pdata:
            # list_vals =  np.array(list(i.values()))
            clean_dict = preprocessing(i) 
            no_dict_list_vals = flatdict.FlatDict(clean_dict, delimiter = ".")
            y_vec.append(no_dict_list_vals.pop("salt"))

            list_vals = list(no_dict_list_vals.values())
            np_list = reduce_list(list_vals)

            final_list.append(np_list) 
            counter += 1
            print(counter)
        
        #print this to a file!
        if grouping == "training":
            with open('training_data.json', 'w', encoding='utf-8') as f:
                json.dump(final_list, f, ensure_ascii=False, indent=4)
            with open('training_data_labels.json', 'w', encoding='utf-8') as f:
                json.dump(y_vec, f, ensure_ascii=False, indent=4)
        elif grouping == "validation":
            with open('validation_data.json', 'w', encoding='utf-8') as f:
                json.dump(final_list, f, ensure_ascii=False, indent=4)
            with open('validation_data_labels.json', 'w', encoding='utf-8') as f:
                json.dump(y_vec, f, ensure_ascii=False, indent=4)
        elif grouping == "testing":
            with open('testing_data.json', 'w', encoding='utf-8') as f:
                json.dump(final_list, f, ensure_ascii=False, indent=4)
            with open('testing_data_labels.json', 'w', encoding='utf-8') as f:
                json.dump(y_vec, f, ensure_ascii=False, indent=4)

        return np.array(final_list), np.array(y_vec)



def split_data(p_data):
    random.shuffle(p_data)
    length = len(p_data)
    k1 = int((length * 7)/10)
    k2 = int((length * 9)/10)
    training = p_data[:k1]
    validation = p_data[k1:k2]
    testing = p_data[k2:]


    return training, validation, testing



def reduce_list(plist):

    flat_list = []
    
    for xs in plist:
        if(type(xs) == list):
            for x in xs:
                flat_list.append(x)
        else:
            flat_list.append(xs)
            
    return flat_list
    

def make_deep_learning():
    inputs = keras.Input(shape=(41,))
    dense = layers.Dense(64, activation="relu")(inputs)
    dense2 = layers.Dense(64, activation="relu")(dense)
    outputs = layers.Dense(10)(dense2)
    model = keras.Model(inputs=inputs, outputs=outputs, name="mnist_model")


    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=keras.optimizers.RMSprop(),
        metrics=[keras.metrics.SparseCategoricalAccuracy()],
    )
    model.summary()
    model.save("path_to_my_model.keras")


def main():
    data = gather_data()
    training,validation,testing  = split_data(data)
    print(len(data))
    print(len(training))
    print(len(validation))
    print(len(testing))


    #Gather both the data, and the labels for the training data. 
    data_file,y_vec = gather_ready_data(training, "training")
    print(data_file.shape)
    print(y_vec.shape)
    data_file_validation,y_vec_validation = gather_ready_data(validation, "validation")
    data_file_testing,y_vec_testing = gather_ready_data(testing, "testing")


    

    

    
main()