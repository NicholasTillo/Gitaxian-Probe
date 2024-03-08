import numpy
#have to pip install this one
from pgmpy.factors.discrete import TabularCPD 
from pgmpy.models import BayesianNetwork
import pgmpy
#Exploring PGMPY to see if its worth over manually coding numpy. 
model = BayesianNetwork()

#Add all nodes of Bayseian Network 
model.add_node("player_winning")
model.add_node("available_mana")
model.add_node("played_land")
model.add_node("turn_number")
model.add_node("player_cards_in_hand")
model.add_node("mulligans_taken")
model.add_node("average_mana_cost")
model.add_node("player_current_health")
model.add_node("damage_dealt_to_opponent")
model.add_node("numb_cards_drawn")
model.add_node("num_artifacts_played")
model.add_node("num_enchantments_played")
model.add_node("num_opponents_lands")
model.add_node("deck_archetype")
model.add_node("current_opponent_health")
model.add_node("creatures_on_board")
model.add_node("creautres_on_opp_board")
model.add_node("has_white")
model.add_node("has_blue")
model.add_node("has_black")
model.add_node("has_red")
model.add_node("has_green")
model.add_node("opp_cards_in_hand")
model.add_node("num_opponents_spell_countered")
model.add_node("num_instants_played")
model.add_node("num_cards_played")
model.add_node("num_opp_cards_drawn")

#add in CPD's to define relationships between nodes. 
cpd_player_winning = TabularCPD(variable = "player_winning", variable_card = 2, values = [[0.5],[0.5]])
cpd_player_winning = TabularCPD(variable = "player_winning", variable_card = 2, values = [[0.5],[0.5]])
random_init_model = BayesianNetwork.get_random_cpds(model)
print(random_init_model.check_model())

