
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
            pdata["has_"+i] = "1"
        else: 
            pdata["has_"+i] = "0"

    #Then Colour Identities
    current = pdata.pop('color_identity')
    for i in ["W","U","B","R","G"]:
        if i in current:
            pdata["has_"+i+"_identity"] = "1"
        else: 
            pdata["has_"+i+"_identity"] = "0"

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
            pdata["has_keyword_"+i] = "1"
        else: 
            pdata["has_keyword_"+i] = "0"

    current = pdata.pop('games')
    for i in ["paper","mtgo","arena"]:
        if i in current:
            pdata["is_in_"+i] = "1"
        else: 
            pdata["is_in_"+i] = "0"

    current = pdata.pop('finishes')
    for i in ["nonfoil","foil"]:
        if i in current:
            pdata["is_finish_"+i] = "1"
        else: 
            pdata["is_finish_"+i] = "0"

    # remember to pop the salt score because it is no longer at the end
              
    return pdata

def gather_ready_data(pdata, grouping):
    
    #try to see if the data.json is already there (Which is should be)
    #pdata is the data we will make the file on if it does not already exsist. 
    #Grouping which section of the data it is, will return the corresponding arrays
    try: 
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
            for i in range(len(np_list)):
               
                if np_list[i] == True: 
                    np_list[i] = "1"
                elif np_list[i] == False:
                    np_list[i] = "0"
                if type(np_list[i]) != str:
                    np_list[i] = str(np_list[i])



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

        return np.array(final_list),np.array(y_vec)



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
    

def make_deep_learning(ptraining,p_y_vec,p_validationStuff,p_test_data,p_test_y_vec):
    #IDK WHAT VALIDATION IS USED FOR YET
    #RETURNS A KERAS MODEL. 
    #MAKES IT IF IT DOESNT EXSIST 
    try: 
        ERRORxERROR
        print("trying_to_read_model")
        model = keras.models.load_model("path_to_my_model.keras")
        print("taken")
        return model

    except:

        #Preprocess again :SOB: 
        #two options, Either splitting it on white space, or not. If we do itll 
        #make it a 2D array, which i think is larger than not. 
        #if we dont i THINK we will lose a bit of inforamtion, becuase each word wont be encoded.

        #TESTINg
        layer = keras.layers.TextVectorization(split = None)
        #layer = keras.layers.TextVectorization()


        for i in ptraining:
            layer.adapt(i)

        x = []
        for i in ptraining:
            v_text = layer(i)
            x.append(v_text)
        x = tf.stack(x)


        validatio_x = []
        
        for i in p_validationStuff[0]:
            validation_v_text = layer(i)
            validatio_x.append(validation_v_text)
        validatio_x = tf.stack(validatio_x)
        
            
        validation_full = (validatio_x,p_validationStuff[1])
        

        test_x = []
        for i in p_test_data:
            test_v_text = layer(i)
            test_x.append(test_v_text)
        predict_data =  test_x[-1]
        predict_salt = p_test_y_vec[-1]


        p_test_y_vec = p_test_y_vec[:-1]
        test_x = test_x[:-1]
        test_x = tf.stack(test_x)
    
    

        """
        inputs = keras.Input(shape = (262,))
    
        dense = layers.Dense(64, activation="relu")(inputs)
        #Do a dropout here, 
        dense2 = layers.Dense(64, activation="relu")(dense)
        
        outputs = layers.Dense(10)(dense2)
        model = keras.Model(inputs=inputs, outputs=outputs, name="mnist_model")
        """

        model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape=(262,)),
            #tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu'),
            #tf.keras.layers.Dropout(0.2),
            #tf.keras.layers.Dense(10,activation="relu"),
            tf.keras.layers.Dense(1)

        ])

        model.compile(
            #This one can either be mean absolute error, 
            #or mean squared logarithmic error. Im not sure which is better.
            #keras.losses.MeanSquaredLogarithmicError(
            #reduction="sum_over_batch_size", name="mean_squared_logarithmic_error"
            #)
        
            loss=keras.losses.MeanAbsoluteError(
                                                reduction="sum_over_batch_size", 
                                                name="mean_absolute_error"
                                                ),
            #optimizer=keras.optimizers.Adam(),
            #Reddit says adam is better, and a combination of adagrad and smn else, but idk what that smn else is so we do gradient decent. 

            optimizer=keras.optimizers.Adagrad(),
            #There are alot and alot of parameters that we need to account for in the constructor. 
            #I think the biggest one is learning rate and maybe momentum, 
            #But well see!
            metrics=[keras.metrics.MeanSquaredError(name="mean_squared_error", dtype=None)],
            #We can use a loss function as a metric, This metric is 
            #Not used when training, but only on testing. Can be the same as the loss
            #I think any regression one should work. Im just gonna use mean squared error. 
        )
        history = model.fit(
                            x, 
                            p_y_vec, 
                            #validation_data = validation_full,
                            validation_split = 0.2,
                            verbose = 1
                            #MAYBE SAMPLE WEIGHT. 
                            )
        
        results = model.evaluate(
                        test_x,
                        p_test_y_vec
                        )

        print(results)
        preditction = model.predict(predict_data)
        print(preditction)

        model.summary()
        model.save("path_to_my_model.keras")


        return model


def test_model(pmodel,p_testing_x,p_y_vec):
    test_scores = pmodel.evaluate(p_testing_x, p_y_vec, verbose=2)
    return test_scores

def main():
    #THIS SHOULDNT BE LIKE THIS, ITS VERY VERY BAD CODE QUALITY, 
    #BUT I CANT BE BOTHERED TO PUJT IT BACK INTO THE FUNCTION< 
    #TRY NOT TO TOUCH IT ITS PRONE TO EXPLOSIONS. 
    data = gather_data()
    training,validation,testing  = split_data(data)
    print(len(data))
    print(len(training))
    print(len(validation))
    print(len(testing))


    #Gather both the data, and the labels for the training data. 
    data_file_training , y_vec = gather_ready_data(training, "training")
    data_file_validation,y_vec_validation = gather_ready_data(validation, "validation")
    data_file_testing,y_vec_testing = gather_ready_data(testing, "testing")

    model = make_deep_learning(data_file_training,y_vec,(data_file_validation,y_vec_validation),data_file_testing,y_vec_testing)




    

    

    
main()