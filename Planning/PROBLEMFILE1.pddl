(define (problem example1)

(:domain gitaxianprobe)

(:objects
	c_grizzlybear1  c_grizzlybear2 c_grizzlybear3 c_grizzlybear4 c_grizzlybear5 - creature
    l_forest1 l_forest2 - land 
)

(:init
    
    ; PLAYER'S CARDS
    
    ; creatures
    
    ; grizzly bear 1
    (is_in_hand c_grizzlybear1)
    (is_owned_by_player c_grizzlybear1)
    (is_creature_colour c_grizzlybear1 green) 
    
    (= (toughness c_grizzlybear1)2)
    (= (max_toughness c_grizzlybear1)2)
    (= (power c_grizzlybear1)2)
    (= (converted_mana_cost c_grizzlybear1)2)
    
    ; grizzly bear 3
    (is_in_hand c_grizzlybear3)
    (is_owned_by_player c_grizzlybear3)
    (is_creature_colour c_grizzlybear3 green) 
    
    (= (toughness c_grizzlybear3)2)
    (= (max_toughness c_grizzlybear3)2)
    (= (power c_grizzlybear3)2)
    (= (converted_mana_cost c_grizzlybear3)2)
    
    ; grizzly bear 5
    (is_in_hand c_grizzlybear5)
    (is_owned_by_player c_grizzlybear5)
    (is_creature_colour c_grizzlybear5 green) 
    
    (= (toughness c_grizzlybear5)2)
    (= (max_toughness c_grizzlybear5)2)
    (= (power c_grizzlybear5)2)
    (= (converted_mana_cost c_grizzlybear5)2)
    
    ; lands
    (is_in_hand l_forest1)
    (is_in_hand l_forest2)
    
    (is_land_colour l_forest1 green) 
    (is_land_colour l_forest2 green) 
    
    
    ; OPPONENT'S CARDS
    
    ; grizzly bear 2
    (is_summoning_sick c_grizzlybear2)
    (is_creature_colour c_grizzlybear2 green) 
    (= (toughness c_grizzlybear2)2)
    (= (max_toughness c_grizzlybear2)2)
    (= (power c_grizzlybear2)2)
    (= (converted_mana_cost c_grizzlybear2)2)
    
    ; grizzly bear 4
    (is_summoning_sick c_grizzlybear4)
    (is_creature_colour c_grizzlybear4 green) 
    (= (toughness c_grizzlybear4)2)
    (= (max_toughness c_grizzlybear4)2)
    (= (power c_grizzlybear4)2)
    (= (converted_mana_cost c_grizzlybear4)2)
    
    ; STARTING HEALTH OF PLAYER AND OPPONENT
    (= (current_life_total_player)7)
    (= (current_life_total_enemy)6)
    
    ; STARTING PHASE
    (current_phase main) 
    (can_pass)
    
    ; STARTING MANA
    (=(available_mana white)0)
    (=(available_mana blue)0)
    (=(available_mana green)0)
    (=(available_mana black)0)
    (=(available_mana red)0)
    (=(available_mana_total)0)
)

(:goal
    (and
        (<=(current_life_total_enemy)0)
    )
)

)




