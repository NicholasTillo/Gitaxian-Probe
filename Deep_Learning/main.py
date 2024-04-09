
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

#Keeping the randomization the same for testing.
random.seed = (180)

#For data collection purposes: 
def sanitize_name(pname):
    """
    Turning creature name strings gathered from the json, and putting them into 
    the form that the webstie will recognize. 
    """
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
    #Turn name into the correct url.
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
            #sleep for a bit to not get IP banned!
            time.sleep(0.01)
            
            salt_score = get_salt_score(dict_you_want["name"])

            if salt_score == None:
                continue
            #Add it to the dict
            dict_you_want["salt"] = salt_score
            wanted_list.append(dict_you_want)
            #add the name into a dict to keep track of duplicatres. 
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
    #Then all the games its included in. 
    current = pdata.pop('games')
    for i in ["paper","mtgo","arena"]:
        if i in current:
            pdata["is_in_"+i] = "1"
        else: 
            pdata["is_in_"+i] = "0"
    #Then the possible finished (Foil,Non-foil)
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
        #Counter for bug testing purposes. 
        #counter = 0
        #For each of the items in the dataset:
        for i in pdata:
            # list_vals =  np.array(list(i.values()))
            #Flatten Dicts 
            clean_dict = preprocessing(i) 
            no_dict_list_vals = flatdict.FlatDict(clean_dict, delimiter = ".")
            #Remove the salt score, and add that to a seperate y_vec
            y_vec.append(no_dict_list_vals.pop("salt"))
            #flatten it into a list.
            list_vals = list(no_dict_list_vals.values())
            #Call reduce list to remove all the nested lists. 
            np_list = reduce_list(list_vals)
            #Turn all the trues and falses into 1's and 0's
            #And everything else into a string. 
            for i in range(len(np_list)):
                if np_list[i] == True: 
                    np_list[i] = "1"
                elif np_list[i] == False:
                    np_list[i] = "0"
                if type(np_list[i]) != str:
                    np_list[i] = str(np_list[i])


            #add the processed data to the list. 
            final_list.append(np_list) 
            #Coutner for bugtesting purposes. 
            #counter += 1
            #print(counter)
        
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
    """ Used to partition data into 3 seperate sets, training, validation and testing"""
    random.shuffle(p_data)
    length = len(p_data)
    k1 = int((length * 7)/10)
    k2 = int((length * 9)/10)
    training = p_data[:k1]
    validation = p_data[k1:k2]
    testing = p_data[k2:]


    return training, validation, testing



def reduce_list(plist):
    """Used to get rid of nested lists. To flatten"""
    flat_list = []
    
    for xs in plist:
        if(type(xs) == list):
            for x in xs:
                flat_list.append(x)
        else:
            flat_list.append(xs)
            
    return flat_list
    


def make_layer(p_training):
    """The function that will make a text-vectorization layer that we can 
    put the individual observations into to create a deep leraning friendly vecotr 
    of 262 integers. """
    try:
        #intentionally cause an error to remake the layer.
        #ERRORxERROR

        #Attempt to load the model from file. 
        print("attempting to take layer")
        loaded_model = tf.keras.models.load_model("vector-text-model.keras")
        loaded_vectorizer = loaded_model.layers[0]
        print("got layer")

        return loaded_vectorizer

    except:
        #Create text vectorization layer
        layer = keras.layers.TextVectorization(split= None,output_mode="int")
        #The ideal code, cannot get it to be homogenounous. 
        #layer = keras.layers.TextVectorization(split="whitespace",output_sequence_length=6,output_mode="int")
        
        
        #Adapt the layer to encapsulate all the training data. 
        for i in p_training:
            layer.adapt(i)

        #Initial effor of inputting all the data in one go, without the for loop
        #Just decided to do a forloop, the additional time for running it was worth
        #The additional data we were able to transfer.

        #all_words = set()
        #counter = 0
        #for i in p_training[:5000]:
        #    print(counter)
        #    counter += 1
        #    for j in i:
        # bcuease this is coded in UTF8 for us to save the file, we have to remove the problematic characters
         #       if '\u01f5' not in j and '\u0106' not in j and '\u010d' not in j and '\u2605' not in j and '\u2610' not in j and '\u2212' not in j and '\u0142' not in j and '\u01f5' not in j and '\u01f5' not in j: 
         #           all_words.add((j))
        #print(np.array(p_training[:5000]))
        #layer.adapt((tf.stack(p_training[:5000])), batch_size="1")
        #layer.adapt((tf.stack(p_training[:5000])))
        #layer.adapt(np.array(list(all_words)))


        #Add it to a sequential model so that we are able to save it to a file
        vector_text_model = tf.keras.models.Sequential()
        vector_text_model.add(tf.keras.Input(shape=(262,)))
        vector_text_model.add(layer)
        
        #Save it to the file.
        filepath = "vector-text-model.keras"
        vector_text_model.save(filepath)

        return layer
    

def make_deep_learning(ptraining,p_y_vec,p_validationStuff,p_test_data,p_test_y_vec):
    """Create a deep learning model, 
    If a .keras file already exsists, then it will gather that information. 
    Otherwise it will create one train it, test it, and save it to a .keras file
    """
    try: 
        #ERRORxERROR
        #If the model exsists in the file.
        print("trying_to_read_model")
        model = keras.models.load_model('my_model.keras')
        print("taken")
        return model

    except:
        #Create the TextVectorization Layer.
        layer = make_layer(ptraining)
        
        #Apply the textVectorization layer to each of the data points. 
        x = []
        for i in ptraining:
            v_text = layer(i)
            x.append(v_text)
        print(x)
        x = tf.stack(x) #turn into tensorflow object

        #Repeat for validation set
        validatio_x = []
        
        for i in p_validationStuff[0]:
            validation_v_text = layer(i)
            validatio_x.append(validation_v_text)
        validatio_x = tf.stack(validatio_x)
        
            
        validation_full = (validatio_x,p_validationStuff[1])
        
        #Also for the test data. 
        test_x = []
        for i in p_test_data:
            test_v_text = layer(i)
            test_x.append(test_v_text)

        #The "Craterhoof" metric 
        predict_data =  tf.stack([test_x[-2]])
        predict_salt = p_test_y_vec[-2]

        #Everything but the craterhoof, 
        p_test_y_vec = p_test_y_vec[:-2]
        test_x = test_x[:-2]
        test_x = tf.stack(test_x)

        """print("Training Size")
        print(x)
        print(p_y_vec)

        print("Validation Size")
        print(validatio_x)
        print(p_validationStuff[1])

        print("Testing Size")
        print(test_x)
        print(p_test_y_vec)

        print("Prediction Size")
        print(predict_data)"""

        #Create the Sequential Model
        model = tf.keras.models.Sequential([
            tf.keras.layers.Input(name = "Input", shape=(262,)),
            tf.keras.layers.Dense(64, activation='relu',name = "Layer1"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu',name = "Layer2"),
            tf.keras.layers.Dense(1,name = "Output")

        ])


        #Compile the model, 
        #Choose loss, optimizer and metrics. 
        #more information about reasons chosen, and what the final model is, in the report. 
        model.compile(
        
            #loss=keras.losses.MeanAbsoluteError(
            #                                    reduction="sum_over_batch_size", 
            #                                    name="mean_absolute_error"
            #                                   ),
            loss=  keras.losses.MeanSquaredError(
                                                    reduction="sum_over_batch_size", name="mean_squared_error"
                                                ),
            #loss = keras.losses.MeanSquaredLogarithmicError(
            #                                               reduction="sum_over_batch_size", name="mean_squared_logarithmic_error"
            #                                            ),
            #Reddit says adam is better, and a combination of adagrad and smn else, but idk what that smn else is so we do gradient decent. 
            
            #There are alot and alot of parameters that we need to account for in the constructor. 
            #I the biggest one is learning rate, 

            #optimizer=keras.optimizers.Adagrad(learning_rate=0.5),
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            #optimizer = keras.optimizers.RMSprop(),
            
            
            metrics=[keras.metrics.MeanSquaredError(name="mean_squared_error", dtype=None)],

            #We can use a loss function as a metric, This metric is 
            #Not used when training, but only on testing. Can be the same as the loss
            #I think any regression one should work. Im just gonna use mean squared error. 
        )
        


        history = model.fit(
                            x, 
                            p_y_vec, 
                            validation_data = validation_full,
                            #validation_split = 0.2,
                            verbose = 1,
                            batch_size = 1
                            #MAYBE SAMPLE WEIGHT. 
                            )
        
        results = model.evaluate(
                        test_x,
                        p_test_y_vec,
                        batch_size = 1

                        )

        #Save Model
        #print(results)
        model.summary()
        model.save("my_model.keras")

        return model


def test_model(pmodel,p_testing_x,p_y_vec):
    test_scores = pmodel.evaluate(p_testing_x, p_y_vec, verbose=2)
    return test_scores

def main():
    """Main function of the file. 
    Will gather the data, making it if it not avaialbe.
    Partition it into training, validaitoin and testing data, 
    and will create a model and a textVectorization layer
    And then evalate it and print the results of that evaluation"""
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

    
    layer = make_layer("doesnt matter")
    
    #Prediction for the "Craterhoof Metric"
    print("Guessed By Model: ")
    print(model(layer(tf.stack([data_file_testing[-2]])))) 

    #print(layer(tf.stack([data_file_testing[-2]])))
    print("Actual Salt: ")
    #print(data_file_testing[-2])
    print(y_vec_testing[-2])
    


    

    

    
main()