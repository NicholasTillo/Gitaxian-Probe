import numpy
#have to pip install this one
from pgmpy.factors.discrete import TabularCPD 
from pgmpy.models import BayesianNetwork
import pgmpy
#Exploring PGMPY to see if its worth over manually coding numpy. 
model = BayesianNetwork()

#Add all nodes of Bayseian Network 
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

model.add_edges_from(all_edges)

#Begin to add the CPD's to the Baysian.


#Player Deck Archetype 
player_arch_CPD = TabularCPD('deck_archetype',4, [[64/300], 
                                                  [83/300], 
                                                  [130/300], 
                                                  [23/300]],
                        evidence=[], evidence_card=[],
                        state_names={'deck_archetype': ['Aggro', 'Control', 'Midrange', 'Combo']})
#Add it to the model
model.add_cpds(player_arch_CPD)


#Black in Player Colour Identity
player_black_CPD = TabularCPD('has_black',2, [[144/300], [156/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_black': ['True', 'False']})
#Add it to the model
model.add_cpds(player_black_CPD)


#Red in Player Colour Identity
player_red_CPD = TabularCPD('has_red',2, [[148/300], [152/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_red': ['True', 'False']})
#Add it to the model
model.add_cpds(player_red_CPD)


#White in Player Colour Identity
player_white_CPD = TabularCPD('has_white',2, [[126/300], [174/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_white': ['True', 'False']})
#Add it to the model
model.add_cpds(player_white_CPD)


#Green in Player Colour Identity
player_green_CPD = TabularCPD('has_green',2, [[123/300], [177/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_green': ['True', 'False']})
#Add it to the model
model.add_cpds(player_green_CPD)


#Blue in Player Colour Identity
player_blue_CPD = TabularCPD('has_blue',2, [[140/300], [160/300]],
                        evidence=[], evidence_card=[],
                        state_names={'has_blue': ['True', 'False']})
#Add it to the model
model.add_cpds(player_blue_CPD)


#Number of lands on opponent's board
opp_lands_CPD = TabularCPD('num_opp_lands', 3, [[69/300], [132/300], [99/300]],
                        evidence=[], evidence_card=[],
                        state_names={'num_opp_lands': ['0-2', '3-5', '6-8']})
#Add it to the model
model.add_cpds(opp_lands_CPD)


#Opponent's current health
# opp_health_CPD = TabularCPD('opp_current_health', 4, [[[[8/300],[11/300],[9/300]],[[15/300],[18/300],[2/300]]], [[[14/300],[10/300],[6/300]],[[11/300],[6/300],[2/300]]], [[[39/300],[26/300],[3/300]],[[45/300],[11/300],[6/300]]], [[[13/300],[7/300],[2/300]],[[23/300],[10/300],[3/300]]]],
#                         evidence=['has_red', 'player_creatures_on_board'], evidence_card=[2,3],
#                         state_names={'opp_current_health': ['0-5', '6-10', '11-15', '16-20'],
#                                      'has_red':['True', 'False'],
#                                      'player_creatures_on_board':['0-2','3-5','6-8']})
opp_health_CPD = TabularCPD('opp_current_health', 4, [[8/74,11/54,9/20,15/94,18/45,2/13], 
                                                      [14/74,10/54,6/20,11/94,6/45,2/13], 
                                                      [39/74,26/54,3/20,45/94,11/45,6/13], 
                                                      [13/74,7/54,2/20,23/94,10/45,3/13]],
                        evidence=['has_red', 'player_creatures_on_board'], evidence_card=[2,3],
                        state_names={'opp_current_health': ['0-5', '6-10', '11-15', '16-20'],
                                     'has_red':['True', 'False'],
                                     'player_creatures_on_board':['0-2','3-5','6-8']})


#Add it to the model
model.add_cpds(opp_health_CPD)


#Player Lands On Board
player_land_CPD = TabularCPD('num_player_lands', 3, [[47/123, 119/177],
                                                     [53/123,41/177],
                                                     [23/123,17/177]],
                            evidence=['has_green'], evidence_card=[2],
                            state_names={'num_player_lands': ['0-2','3-5','6-8'],
                                         'has_green': ["True","False"]}
                            )
model.add_cpds(player_land_CPD)

#instants and Sorceries
instant_sorceries_CPD = TabularCPD('num_player_instants_and_sorceries_played', 3, [[23/140, 132/160],
                                                                                    [75/140,20/160],
                                                                                    [42/140,8/160]],
                            evidence=['has_blue'], evidence_card=[2],
                            state_names={'num_player_instants_and_sorceries_played': ['0-2','3-5','6-8'],
                                         'has_blue': ["True","False"]}
                            )
model.add_cpds(instant_sorceries_CPD)

#Num Cards IN Player Hand
num_cards_in_player_hand_CPD = TabularCPD('player_cards_in_hand', 3, [[2/140, 48/160],
                                                                        [55/140,93/160],
                                                                        [83/140,19/160]],
                            evidence=['has_blue'], evidence_card=[2],
                            state_names={'player_cards_in_hand': ['0-2','3-5','6-7'],
                                         'has_blue': ["True","False"]}
                            )
model.add_cpds(num_cards_in_player_hand_CPD)

#Num Cards In Opponents Hand
num_cards_in_opponent_hand_CPD = TabularCPD('opp_cards_in_hand', 3, [[89/144, 41/156],
                                                                    [35/144,92/156],
                                                                    [20/144,23/156]],
                            evidence=['has_black'], evidence_card=[2],
                            state_names={'opp_cards_in_hand': ['0-2','3-5','6-7'],
                                         'has_black': ["True","False"]}
                            )
model.add_cpds(num_cards_in_opponent_hand_CPD)


# player_health_CPD = TabularCPD('player_current_health', 4, [[[[[3/300],[0/300],[1/300]],[[9/300],[4/300],[1/300]]],[[[3/300],[2/300],[2/300]],[[13/300],[3/300],[2/300]]]],[[[[9/300],[4/300],[0/300]],[[11/300],[2/300],[0/300]]],[[[9/300],[8/300],[3/300]],[[13/300],[6/300],[2/300]]]],[[[[14/300],[4/300],[0/300]],[[15/300],[5/300],[1/300]]],[[[13/300],[7/300],[3/300]],[[12/300],[6/300],[0/300]]]],[[[[24/300],[8/300],[0/300]],[[22/300],[7/300],[0/300]]],[[[17/300],[6/300],[2/300]],[[19/300],[5/300],[0/300]]]]],
#                         evidence=['has_black', 'has_white', 'opp_creatures_on_board'], evidence_card=[2,2,3],
#                         state_names={'player_current_health': ['0-5', '6-10', '11-15', '16-20'],
#                                      'has_black':['True', 'False'],
#                                      'has_white':['True', 'False'],
#                                      'opp_creatures_on_board':['0-2','3-5','6-8']})
# #Add it to the model
# model.add_cpds(player_health_CPD)

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
#Add it to the model
model.add_cpds(player_health_CPD)


#Player Winning
# player_winning_CPD = TabularCPD('player_winning', 2, [[12 /300,6/300,2/300,0/300,
#                                                        9/300,8/300,8/300,3/300,
#                                                        16/300,13/300,9/300,5/300,
#                                                        12/300,19/300,3/300,23/300],
#                                                         [9/300,13/300,16/300,15/300,
#                                                         4/300,9/300,7/300,14/300,
#                                                         0/300,2/300,13/300,17/300,
#                                                         1/300,0/300,9/300,23/300]],
#                             evidence=['player_current_health','opp_current_health'], evidence_card=[4,4],
#                             state_names={'player_winning': ['True','False'],
#                                          'player_current_health': ["0-5","6-10","11-15","16-20"],
#                                          'opp_current_health': ["0-5","6-10","11-15","16-20"]}
#                             )
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
model.add_cpds(player_winning_CPD)

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
model.add_cpds(number_player_creatures_CPD)


#Player Non Land Permenants
player_nonland_permenants_CPD = TabularCPD('player_nonland_permenants_on_board', 3, [[11/14,24/50, 15/48, 8/13, 42/50,34/80,15/35,7/10],
                                                                                     [3/14,18/50, 27/48,  3/13, 8/50 ,34/80,17/35,3/10],
                                                                                     [0/14,8/50, 6/48,   2/13, 0/50 ,12/80,3/35,0/10]],
                            evidence=['has_white','deck_archetype'], evidence_card=[2,4],
                            state_names={'player_nonland_permenants_on_board': ["0-2","3-5","6-8"],
                                         'has_white': ["True","False"],
                                         'deck_archetype': ['Aggro', 'Control', 'Midrange', 'Combo']}
                            )
model.add_cpds(player_nonland_permenants_CPD)


#Opponents Creatures on Board
opp_creatures_board_CPD = TabularCPD('opp_creatures_on_board', 3, [[3/22,7/24,16/23, 14/56,25/54, 9/22, 14/50,8/25,3/24],
                                                                   [5/22,11/24,7/23, 25/56,19/54, 12/22,22/50,13/25,19/24],
                                                                   [14/22,6/24,0/23, 17/56,10/54, 1/22, 14/50,4/25,2/24]],
                            evidence=['num_opp_lands','opp_cards_in_hand'], evidence_card=[3,3],
                            state_names={'opp_creatures_on_board': ["0-2","3-5","6-8"],
                                         'num_opp_lands': ["0-2","3-5","6-8"],
                                         'opp_cards_in_hand': ["0-2","3-5","6-7"]}
                            )
model.add_cpds(opp_creatures_board_CPD)





#Check if model is valid. 

print(model.get_parents("opp_creatures_on_board"))
print(model.check_model())


#Load it into a VE Object. 
inference = pgmpy.inference.VariableElimination(model)





