(define (problem example1)
(:domain gitaxianprobe)

(:objects
    Player1 player2 - player
	c_grizzlybear1 c_grizzleybear2 c_grizzleybear3 c_grizzleybear4 c_grizzleybear5 - creature
    l_forest1 l_forest2 - land 
	
)

(:init	
    (is_player player1)
    (is_enemy player2)

	(is_in_hand c_grizzlybear3)
    (is_in_hand c_grizzlybear4)
    (is_in_hand c_grizzlybear5)
    (is_in_hand l_forest1)
    (is_in_hand l_forest2)

    (is_land_colour l_forest1 green) 
    (is_land_colour l_forest2 green) 

    (is_creature_colour c_grizzlybear1 green) 
    (is_creature_colour c_grizzlybear2 green) 
    (is_creature_colour c_grizzlybear3 green) 
    (is_creature_colour c_grizzlybear4 green) 
    (is_creature_colour c_grizzlybear5 green) 

	(= (toughness C_grizzlybear1)2)
    (= (toughness C_grizzlybear2)2)
    (= (toughness C_grizzlybear3)2)
    (= (toughness C_grizzlybear4)2)
    (= (toughness C_grizzlybear5)2)
    (= (power c_grizzlybear1)2)
    (= (power c_grizzlybear2)2)
    (= (power c_grizzlybear3)2)
    (= (power c_grizzlybear4)2)
    (= (power c_grizzlybear5)2)
    (= (converted_mana_cost c_grizzlybear1)2)
    (= (converted_mana_cost c_grizzlybear2)2)
    (= (converted_mana_cost c_grizzlybear3)2)
    (= (converted_mana_cost c_grizzlybear4)2)
    (= (converted_mana_cost c_grizzlybear5)2)


    (= (current_life_total_player)20)
    (= (current_life_total_enemy)20)
    (current_phase main) 
    (is_player player1)
    (is_enemy player2)
)

(:goal
 and(<=(current_enemy_health)0)

)
(:metric maximize
(current_player_health)
)
)
