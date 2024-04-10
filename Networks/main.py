import numpy
#have to pip install this one
from pgmpy.factors.discrete import TabularCPD 
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
import pgmpy
#Exploring PGMPY to see if its worth over manually coding numpy. 
model = BayesianNetwork()

#Add all nodes of Bayesian Network 
model.add_node("player_winning")
model.add_node("player_cards_in_hand")
model.add_node("player_current_health")
model.add_node("num_opp_lands")
model.add_node("num_player_lands")
model.add_node("deck_archetype")
model.add_node("opp_current_health")
model.add_node("player_nonland_permenants_on_board")
model.add_node("player_creatures_on_board")
model.add_node("opp_creatures_on_board")
model.add_node("has_white")
model.add_node("has_blue")
model.add_node("has_black")
model.add_node("has_red")
model.add_node("has_green")
model.add_node("opp_cards_in_hand")
model.add_node("num_player_instants_and_sorceries_played")

# Add the edges between each node, also according to the Bayesian Network
# Edges are directed: parent -> child
all_edges = [("player_current_health", "player_winning"),
             ("opp_current_health", "player_winning"),
             ("player_creatures_on_board", "opp_current_health"),
             ("has_black", "player_creatures_on_board"),
             ("has_green", "player_creatures_on_board"),
             ("has_white", "player_nonland_permenants_on_board"),
             ("deck_archetype", "player_nonland_permenants_on_board"),
             ("has_red", "opp_current_health"),
             ("has_black", "opp_cards_in_hand"),
             ("has_black", "player_current_health"),
             ("has_green", "num_player_lands"),
             ("has_blue", "num_player_instants_and_sorceries_played"),
             ("has_blue", "player_cards_in_hand"),
             ("has_white", "player_current_health"),
             ("opp_creatures_on_board", "player_current_health"),
             ("player_cards_in_hand", "player_creatures_on_board"),
             ("opp_cards_in_hand", "opp_creatures_on_board"),
             ("num_opp_lands", "opp_creatures_on_board"),
            ]

# Add all the edges to our modelled network...
model.add_edges_from(all_edges)

#Begin to add the CPD's to the Bayesian.

"""
    Each CPD is in the following format:
    (
        '(node name that the CPD is in regards to)', (num. categories of main node states),
        [CP values], ['(name of evidence nodes, if any)'], [(ordered state values for the evidence)],
        ['(ordered state names for the evidence)']
    )

    More information can be found here, referencing the documentation:
    https://pgmpy.org/factors/discrete.html
"""
#Player Deck Archetype 
player_arch_CPD = TabularCPD('deck_archetype',4, [[64/300], 
                                                  [83/300], 
                                                  [130/300], 
                                                  [23/300]],
                        evidence=[], evidence_card=[],
                        state_names={'deck_archetype': ['Aggro', 'Control', 'Midrange', 'Combo']})
model.add_cpds(player_arch_CPD)  #Add it to the model


#Black in Player Colour Identity
player_black_CPD = TabularCPD('has_black',2, [[144/300], [156/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_black': ['True', 'False']})
model.add_cpds(player_black_CPD)  #Add it to the model


#Red in Player Colour Identity
player_red_CPD = TabularCPD('has_red',2, [[148/300], [152/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_red': ['True', 'False']})
model.add_cpds(player_red_CPD)  #Add it to the model


#White in Player Colour Identity
player_white_CPD = TabularCPD('has_white',2, [[126/300], [174/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_white': ['True', 'False']})
model.add_cpds(player_white_CPD)  #Add it to the model


#Green in Player Colour Identity
player_green_CPD = TabularCPD('has_green',2, [[123/300], [177/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_green': ['True', 'False']})
model.add_cpds(player_green_CPD)  #Add it to the model


#Blue in Player Colour Identity
player_blue_CPD = TabularCPD('has_blue',2, [[140/300], [160/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_blue': ['True', 'False']})
model.add_cpds(player_blue_CPD)  #Add it to the model


#Number of lands on opponent's board
opp_lands_CPD = TabularCPD('num_opp_lands', 3, [[69/300], [132/300], [99/300]],
                        evidence=[], evidence_card=[],
                        state_names={'num_opp_lands': ['0-2', '3-5', '6-8']})
model.add_cpds(opp_lands_CPD)  #Add it to the model


opp_health_CPD = TabularCPD('opp_current_health', 4, [[8/74,11/54,9/20,15/94,18/45,2/13], 
                                                      [14/74,10/54,6/20,11/94,6/45,2/13], 
                                                      [39/74,26/54,3/20,45/94,11/45,6/13], 
                                                      [13/74,7/54,2/20,23/94,10/45,3/13]],
                        evidence=['has_red', 'player_creatures_on_board'], evidence_card=[2,3],
                        state_names={'opp_current_health': ['0-5', '6-10', '11-15', '16-20'],
                                     'has_red':['True', 'False'],
                                     'player_creatures_on_board':['0-2','3-5','6-8']})
model.add_cpds(opp_health_CPD)  #Add it to the model


#Player Lands On Board
player_land_CPD = TabularCPD('num_player_lands', 3, [[47/123, 119/177],
                                                     [53/123,41/177],
                                                     [23/123,17/177]],
                            evidence=['has_green'], evidence_card=[2],
                            state_names={'num_player_lands': ['0-2','3-5','6-8'],
                                         'has_green': ["True","False"]}
                            )
model.add_cpds(player_land_CPD)  #Add it to the model

#instants and Sorceries
instant_sorceries_CPD = TabularCPD('num_player_instants_and_sorceries_played', 3, [[23/140, 132/160],
                                                                                    [75/140,20/160],
                                                                                    [42/140,8/160]],
                            evidence=['has_blue'], evidence_card=[2],
                            state_names={'num_player_instants_and_sorceries_played': ['0-2','3-5','6-8'],
                                         'has_blue': ["True","False"]}
                            )
model.add_cpds(instant_sorceries_CPD)  #Add it to the model

#Num Cards in Player Hand
num_cards_in_player_hand_CPD = TabularCPD('player_cards_in_hand', 3, [[2/140, 48/160],
                                                                        [55/140,93/160],
                                                                        [83/140,19/160]],
                            evidence=['has_blue'], evidence_card=[2],
                            state_names={'player_cards_in_hand': ['0-2','3-5','6-7'],
                                         'has_blue': ["True","False"]}
                            )
model.add_cpds(num_cards_in_player_hand_CPD)  #Add it to the model

#Num Cards In Opponents Hand
num_cards_in_opponent_hand_CPD = TabularCPD('opp_cards_in_hand', 3, [[89/144, 41/156],
                                                                    [35/144,92/156],
                                                                    [20/144,23/156]],
                            evidence=['has_black'], evidence_card=[2],
                            state_names={'opp_cards_in_hand': ['0-2','3-5','6-7'],
                                         'has_black': ["True","False"]}
                            )
model.add_cpds(num_cards_in_opponent_hand_CPD)  #Add it to the model

#Player's current health
player_health_CPD = TabularCPD('player_current_health', 4, [[3/50,0/16,1/1,9/57,4/18,1/2,3/42,2/23,2/10,13/57,3/20,2/4],
                                                            [9/50,4/16,0/1,11/57,2/18,0/2,9/42,8/23,3/10,13/57,6/20,2/4],
                                                            [14/50,4/16,0/1,15/57,5/18,1/2,13/42,7/23,3/10,12/57,6/20,0/4],
                                                            [24/50,8/16,0/1,22/57,7/18,0/2,17/42,6/23,2/10,19/57,5/20,0/4]],
                        evidence=['has_black', 'has_white', 'opp_creatures_on_board'], evidence_card=[2,2,3],
                        state_names={'player_current_health': ['0-5', '6-10', '11-15', '16-20'],
                                     'has_black':['True', 'False'],
                                     'has_white':['True', 'False'],
                                     'opp_creatures_on_board':['0-2','3-5','6-8']})
model.add_cpds(player_health_CPD)  #Add it to the model

# Player winning
player_winning_CPD = TabularCPD('player_winning', 2, [[12/21,6/19,2/18,0/15,
                                                       9/13,8/17,8/15,3/17,
                                                       16/16,13/15,9/22,5/22,
                                                       12/13,19/19,3/12,23/46],
                                                        [9/21,13/19,16/18,15/15,
                                                        4/13,9/17,7/15,14/17,
                                                        0/16,2/15,13/22,17/22,
                                                        1/13,0/19,9/12,23/46]],
                            evidence=['player_current_health','opp_current_health'], evidence_card=[4,4],
                            state_names={'player_winning': ['True','False'],
                                         'player_current_health': ["0-5","6-10","11-15","16-20"],
                                         'opp_current_health': ["0-5","6-10","11-15","16-20"]}
                            )
model.add_cpds(player_winning_CPD)  #Add it to the model

#Number Player Creatures
number_player_creatures_CPD = TabularCPD('player_creatures_on_board', 3, [[5/22,3/20,12/19,3/26,5/21,  7/15,  3/26, 7/34,11/23,2/31,8/30,18/33]
                                                                          ,[6/22,12/20,4/19,11/26,7/21,7/15,  14/26,12/34,9/23,15/31,11/30,9/33],
                                                                          [11/22,5/20,3/19,12/26,9/21, 1/15,  9/26, 15/34,3/23,14/31,11/30,6/33]],
                            evidence=['has_green','has_black','player_cards_in_hand'], evidence_card=[2,2,3],
                            state_names={'player_creatures_on_board': ["0-2","3-5","6-8"],
                                         'has_green': ["True","False"],
                                         'has_black': ["True","False"],
                                         'player_cards_in_hand': ["0-2","3-5","6-7"]}
                            )
model.add_cpds(number_player_creatures_CPD)  #Add it to the model


#Player Non Land Permenants
player_nonland_permenants_CPD = TabularCPD('player_nonland_permenants_on_board', 3, [[11/14,24/50, 15/48, 8/13, 42/50,34/80,15/35,7/10],
                                                                                     [3/14,18/50, 27/48,  3/13, 8/50 ,34/80,17/35,3/10],
                                                                                     [0/14,8/50, 6/48,   2/13, 0/50 ,12/80,3/35,0/10]],
                            evidence=['has_white','deck_archetype'], evidence_card=[2,4],
                            state_names={'player_nonland_permenants_on_board': ["0-2","3-5","6-8"],
                                         'has_white': ["True","False"],
                                         'deck_archetype': ['Aggro', 'Control', 'Midrange', 'Combo']}
                            )
model.add_cpds(player_nonland_permenants_CPD)  #Add it to the model


#Opponents Creatures on Board
opp_creatures_board_CPD = TabularCPD('opp_creatures_on_board', 3, [[3/22,7/24,16/23, 14/56,25/54, 9/22, 14/50,8/25,3/24],
                                                                   [5/22,11/24,7/23, 25/56,19/54, 12/22,22/50,13/25,19/24],
                                                                   [14/22,6/24,0/23, 17/56,10/54, 1/22, 14/50,4/25,2/24]],
                            evidence=['num_opp_lands','opp_cards_in_hand'], evidence_card=[3,3],
                            state_names={'opp_creatures_on_board': ["0-2","3-5","6-8"],
                                         'num_opp_lands': ["0-2","3-5","6-8"],
                                         'opp_cards_in_hand': ["0-2","3-5","6-7"]}
                            )
model.add_cpds(opp_creatures_board_CPD)  #Add it to the model


#Check if model is valid. 
print(model.check_model())

#Load it into a VE Object. 
inference = VariableElimination(model)

#test query: an obvious one!
player_wins_query = inference.query(['player_winning'], {'player_current_health':'0-5', 'opp_current_health':'6-10'})

#chance of players winning based on the colours they play
player_wins_azur_query = inference.query(['player_winning'], {'has_red':'False', 'has_black':'False', 'has_blue':'True', 'has_green':'False', 'has_white':'True'})
player_wins_orzhov_query = inference.query(['player_winning'], {'has_red':'False', 'has_black':'True', 'has_blue':'False', 'has_green':'False', 'has_white':'True'})
player_wins_boros_query = inference.query(['player_winning'], {'has_red':'True', 'has_black':'False', 'has_blue':'False', 'has_green':'False', 'has_white':'True'})
player_wins_seles_query = inference.query(['player_winning'], {'has_red':'False', 'has_black':'False', 'has_blue':'False', 'has_green':'True', 'has_white':'True'})
player_wins_dimir_query = inference.query(['player_winning'], {'has_red':'False', 'has_black':'True', 'has_blue':'True', 'has_green':'False', 'has_white':'False'})
player_wins_izzet_query = inference.query(['player_winning'], {'has_red':'True', 'has_black':'False', 'has_blue':'True', 'has_green':'False', 'has_white':'False'})
player_wins_simic_query = inference.query(['player_winning'], {'has_red':'False', 'has_black':'False', 'has_blue':'True', 'has_green':'True', 'has_white':'False'})
player_wins_rakdos_query = inference.query(['player_winning'], {'has_red':'True', 'has_black':'True', 'has_blue':'False', 'has_green':'False', 'has_white':'False'})
player_wins_golgari_query = inference.query(['player_winning'], {'has_red':'False', 'has_black':'True', 'has_blue':'False', 'has_green':'True', 'has_white':'False'})
player_wins_gruul_query = inference.query(['player_winning'], {'has_red':'True', 'has_black':'False', 'has_blue':'False', 'has_green':'True', 'has_white':'False'})
player_wins_wubrg_query = inference.query(['player_winning'], {'has_red':'True', 'has_black':'True', 'has_blue':'True', 'has_green':'True', 'has_white':'True'})

print("Probability that an Azorius (WU) Player Wins")
print(player_wins_azur_query)
print("")
print("Probability that an Orzhov (WB) Player Wins")
print(player_wins_orzhov_query)
print("")
print("Probability that a Boros (WR) Player Wins")
print(player_wins_boros_query)
print("")
print("Probability that a Selesnya (WG) Player Wins")
print(player_wins_seles_query)
print("")
print("Probability that a Dimir (UB) Player Wins")
print(player_wins_dimir_query)
print("")
print("Probability that an Izzet (UR) Player Wins")
print(player_wins_izzet_query)
print("")
print("Probability that a Simic (UG) Player Wins")
print(player_wins_simic_query)
print("")
print("Probability that a Rakdos (BR) Player Wins")
print(player_wins_rakdos_query)
print("")
print("Probability that a Golgari (BG) Player Wins")
print(player_wins_golgari_query)
print("")
print("Probability that a Gruul (RG) Player Wins")
print(player_wins_gruul_query)
print("")
print("Probability that a Wubrg (WUBRG) Player Wins")
print(player_wins_wubrg_query)
print("")

#chance of players having nonland permanents depending on their archetype
nonland_perms_aggro_query = inference.query(['player_nonland_permenants_on_board'], {'deck_archetype':'Aggro'})
nonland_perms_white_aggro_query = inference.query(['player_nonland_permenants_on_board'], {'deck_archetype':'Aggro', 'has_white':'True'})

nonland_perms_control_query = inference.query(['player_nonland_permenants_on_board'], {'deck_archetype':'Control'})
nonland_perms_mid_query = inference.query(['player_nonland_permenants_on_board'], {'deck_archetype':'Midrange'})
nonland_perms_combo_query = inference.query(['player_nonland_permenants_on_board'], {'deck_archetype':'Combo'})

print("Nonland Permanents if Playing Aggro")
print(nonland_perms_aggro_query)
print("")
print("Nonland Permanents if Playing Aggro Including White")
print(nonland_perms_white_aggro_query)
print("")
print("Nonland Permanents if Playing Control")
print(nonland_perms_control_query)
print("")
print("Nonland Permanents if Playing Midrange")
print(nonland_perms_mid_query)
print("")
print("Nonland Permanents if Playing Combo")
print(nonland_perms_combo_query)

#The following queries relate to the home games played by us...
#Refer to the documentation for more information about this +
# analysis of the results!
game1_query = inference.query(['player_winning'], 
                              {'num_player_lands':'6-8', 
                               'player_current_health':'16-20',
                               'player_nonland_permenants_on_board':'3-5',
                               'player_cards_in_hand':'0-2',
                               'player_creatures_on_board':'3-5',
                               'num_player_instants_and_sorceries_played':'0-2',
                               'deck_archetype':'Midrange',
                               'has_black':'True',
                               'has_white':'True',
                               'has_red':'False',
                               'has_green':'False',
                               'has_blue':'False',

                               'num_opp_lands':'3-5',
                               'opp_current_health':'0-5',
                               'opp_cards_in_hand':'3-5',
                               'opp_creatures_on_board':'3-5'
                              })

game2_query = inference.query(['player_winning'], 
                              {'num_player_lands':'3-5', 
                               'player_current_health':'0-5',
                               'player_nonland_permenants_on_board':'0-2',
                               'player_cards_in_hand':'0-2',
                               'player_creatures_on_board':'0-2',
                               'num_player_instants_and_sorceries_played':'0-2',
                               'deck_archetype':'Midrange',
                               'has_black':'True',
                               'has_white':'True',
                               'has_red':'False',
                               'has_green':'False',
                               'has_blue':'False',

                               'num_opp_lands':'3-5',
                               'opp_current_health':'16-20',
                               'opp_cards_in_hand':'0-2',
                               'opp_creatures_on_board':'3-5'
                              })

game3_query = inference.query(['player_winning'], 
                              {'num_player_lands':'3-5', 
                               'player_current_health':'16-20',
                               'player_nonland_permenants_on_board':'0-2',
                               'player_cards_in_hand':'0-2',
                               'player_creatures_on_board':'0-2',
                               'num_player_instants_and_sorceries_played':'0-2',
                               'deck_archetype':'Midrange',
                               'has_black':'True',
                               'has_white':'True',
                               'has_red':'False',
                               'has_green':'False',
                               'has_blue':'False',

                               'num_opp_lands':'3-5',
                               'opp_current_health':'11-15',
                               'opp_cards_in_hand':'0-2',
                               'opp_creatures_on_board':'0-2'
                              })

print("")
print("Probability of Player Winning Game 1")
print(game1_query)

print("")
print("Probability of Player Winning Game 2")
print(game2_query)

print("")
print("Probability of Player Winning Game 3")
print(game3_query)

#eof




