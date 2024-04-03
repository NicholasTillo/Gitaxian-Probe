
(define (problem example1)
(:domain gitaxianprobe)

(:objects
	c_grizzlybear1  c_grizzlybear2 c_grizzlybear3 c_grizzlybear4 c_grizzlybear5 - creature
    l_forest1 l_forest2 - land 
)

(:init
(is_in_hand c_grizzlybear1)
(is_owned_by_player c_grizzlybear1)
(is_creature_colour c_grizzlybear1 green) 


(is_in_hand c_grizzlybear3)
(is_owned_by_player c_grizzlybear3)
(is_creature_colour c_grizzlybear3 green) 

(is_in_hand c_grizzlybear5)
(is_owned_by_player c_grizzlybear5)
(is_creature_colour c_grizzlybear5 green) 

(is_in_hand l_forest1)
(is_in_hand l_forest2)

(is_land_colour l_forest1 green) 
(is_land_colour l_forest2 green) 


(= (toughness c_grizzlybear1)2)
(= (max_toughness c_grizzlybear1)2)
(= (power c_grizzlybear1)2)
(= (converted_mana_cost c_grizzlybear1)2)

(= (toughness c_grizzlybear3)2)
(= (max_toughness c_grizzlybear3)2)
(= (power c_grizzlybear3)2)
(= (converted_mana_cost c_grizzlybear3)2)


(= (toughness c_grizzlybear5)2)
(= (max_toughness c_grizzlybear5)2)
(= (power c_grizzlybear5)2)
(= (converted_mana_cost c_grizzlybear5)2)


(is_summoning_sick c_grizzlybear2)
(is_creature_colour c_grizzlybear2 green) 
(= (toughness c_grizzlybear2)2)
(= (max_toughness c_grizzlybear2)2)
(= (power c_grizzlybear2)2)
(= (converted_mana_cost c_grizzlybear2)2)

(is_summoning_sick c_grizzlybear4)
(is_creature_colour c_grizzlybear4 green) 
(= (toughness c_grizzlybear4)2)
(= (max_toughness c_grizzlybear4)2)
(= (power c_grizzlybear4)2)
(= (converted_mana_cost c_grizzlybear4)2)


(= (current_life_total_player)7)
(= (current_life_total_enemy)6)
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
;(and(<=(toughness c_grizzlybear2)0) (current_phase opponentEnd)
;(and(not(is_alive c_grizzlybear2)))
;(and(not(is_in_hand c_grizzlybear3)) (is_dead c_grizzlybear3))
;(and(flag)
;(and(not(is_attacking c_grizzlybear2))(current_phase opponentEnd))
;(and(not(is_attacking c_grizzlybear2))(<=(toughness c_grizzlybear2)0))
;(and (not (is_in_hand c_grizzlybear1))(not (is_in_hand c_grizzlybear3))
;(and (current_phase opponentAttack))
 ;(and(>=(available_mana green)2))
)
)
)




