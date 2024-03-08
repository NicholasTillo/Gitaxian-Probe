(define (problem example2)
(:domain gitaxianprobe)

(:objects
    player1 player2 - player
	c_grizzlybear1 c_grizzlybear2 c_grizzlybear3 c_grizzlybear4 c_aegis_turtle1- creature
	S_lightning_bolt1 s_lightning_bolt2 - spells
    l_forest1 l_mountain1 l_island1 - land 

)

(:init
	;hand
(is_in_hand c_grizzlybear4)
(is_in_hand c_aegis_turtle1)
(is_in_hand l_forest1)
(is_in_hand l_mountain1)
(is_in_hand l_island1)
(is_in_hand s_lightning_bolt1)
(is_in_hand s_lightning_bolt2)


(is_land_colour l_forest1 green) 
(is_land_colour l_island1 blue) 
(is_land_colour l_mountain1 red) 

	;Creatures
(is_creature_colour c_grizzlybear1 green) 
(is_creature_colour c_grizzlybear2 green) 
(is_creature_colour c_grizzlybear3 green) 
(is_creature_colour c_grizzlybear4 green) 
(is_creature_colour c_aegis_turtle1 blue) 

	(= (toughness C_grizzlybear1)2)
(= (toughness C_grizzlybear2)2)
(= (toughness C_grizzlybear3)2)
(= (toughness C_grizzlybear4)2)
(= (toughness c_aegis_turtle1)5)
(= (power c_grizzlybear1)2)
(= (power c_grizzlybear2)2)
(= (power c_grizzlybear3)2)
(= (power c_grizzlybear4)2)
(= (power c_aegis_turtle1)0)
(= (converted_mana_cost c_grizzlybear1)2)
(= (converted_mana_cost c_grizzlybear2)2)
(= (converted_mana_cost c_grizzlybear3)2)
(= (converted_mana_cost c_grizzlybear4)2)
(= (converted_mana_cost c_aegis_turtle1))

;Spells
(is_spell_colour s_lightning_bolt1 red)
(is_spell_colour s_lightning_bolt2 red)
(= (spell_converted_mana_cost s_lightning_bolt1) 1)
(= (spell_converted_mana_cost s_lightning_bolt2) 1)
(= (spell_value s_lightning_bolt1) 3)
(= (spell_value s_lightning_bolt1) 3)
(= (spell_value s_lightning_bolt2) 3)
(spell_effect deal s_lightning_bolt1)
(spell_effect deal s_lightning_bolt2)

;World
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
