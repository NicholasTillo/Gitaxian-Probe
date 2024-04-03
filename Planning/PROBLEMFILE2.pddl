
(define (problem example2)
(:domain gitaxianprobe)

(:objects
    c_knight1 c_grizzlybear2 c_goblin1 c_aegis_turtle1 - creature
    l_forest1  l_island1 - land 
)

(:init

;hand
	
;creature bear 1
(is_in_hand c_knight1)
(is_owned_by_player c_knight1)
(is_creature_colour c_knight1 green) 
;stats
(= (toughness c_knight1)2)
(= (max_toughness c_knight1)2)
(= (power c_knight1)2)
(= (converted_mana_cost c_knight1)2)
(has_vigilance c_knight1)


(is_in_hand c_aegis_turtle1)
(is_owned_by_player c_aegis_turtle1)
(is_creature_colour c_aegis_turtle1 blue) 
;stats
(= (toughness c_aegis_turtle1)5)
(= (max_toughness c_aegis_turtle1)5)
(= (power c_aegis_turtle1)0)
(= (converted_mana_cost c_aegis_turtle1)1)



;lands
(is_in_hand l_forest1)
(is_in_hand l_island1)


(is_land_colour l_forest1 green) 
(is_land_colour l_island1 blue) 
 

	;Creatures


(is_summoning_sick c_goblin1)
(is_creature_colour c_goblin1 red)
(= (toughness c_goblin1)1)
(= (max_toughness c_goblin1)1)
(= (power c_goblin1)1)
(= (converted_mana_cost c_goblin1)1)

(is_summoning_sick c_grizzlybear2)
(is_creature_colour c_grizzlybear2 green) 
(= (toughness c_grizzlybear2)2)
(= (max_toughness c_grizzlybear2)2)
(= (power c_grizzlybear2)2)
(= (converted_mana_cost c_grizzlybear2)2)


;World
(= (current_life_total_player)8)
(= (current_life_total_enemy)4)
(current_phase main) 
(can_pass)



(=(available_mana white)0)
(=(available_mana blue)0)
(=(available_mana green)0)
(=(available_mana black)0)
(=(available_mana red)0)
(=(available_mana_total)0)
)


(:goal
(and(<=(current_life_total_enemy)0)
)

)
)


