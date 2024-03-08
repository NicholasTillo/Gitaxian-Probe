(define (problem example3)
(:domain gitaxianprobe)

(:objects
    player1 player2 - player
	c_grizzlybear1 c_grizzleybear2 c_goblin1 c_goblin2 c_goblin3 c_goblin4 c_dross_crocodile1 c_dross_crocodile1 c_dross_crocodile1 c_aegis_turtle1 c_knight1 c_knight2 - creature

l_forest1 l_mountain1 l_mountain2 l_swamp1 - land
)

(:init
(is_land_colour l_forest1 green) 
(is_land_colour l_swamp1 black) 
(is_land_colour l_mountain1 red) 
(is_land_colour l_mountain2 red)

;enemy creatures
(is_creature_colour c_grizzlybear1 green) 
	(= (toughness C_grizzlybear1)2)
(= (power c_grizzlybear1)2)
(= (converted_mana_cost c_grizzlybear1)2)

(is_creature_colour c_goblin1 red) 
(has_haste c_goblin1)
	(= (toughness c_goblin1)1)
(= (power c_goblin1)1)
(= (converted_mana_cost c_goblin1)1)

(is_creature_colour c_goblin2 red) 
(has_haste c_goblin2 )
	(= (toughness c_goblin2 )1)
(= (power c_goblin2 )1)
(= (converted_mana_cost c_goblin2 )1)

(is_creature_colour c_dross_crocodile1 black) 
	(= (toughness c_dross_crocodile1)5)
(= (power c_dross_crocodile1)1)
(= (converted_mana_cost c_dross_crocodile1)4)

(is_creature_colour c_knight1 white) 
(has_vigilance c_knight1)
	(= (toughness c_knight1)2)
(= (power c_knight1)2)
(= (converted_mana_cost c_knight1)2)
;player Creatures 
(is_in_hand c_grizzlybear2)
(is_creature_colour c_grizzlybear2green) 
	(= (toughness c_grizzlybear2)2)
(= (power c_grizzlybear2)2)
(= (converted_mana_cost c_grizzlybear2)2)

(is_in_hand c_goblin3)
(is_creature_colour c_goblin3 red) 
(has_haste c_goblin3)
	(= (toughness c_goblin3)1)
(= (power c_goblin3)1)
(= (converted_mana_cost c_goblin3)1)

(is_in_hand c_goblin4)
(is_creature_colour c_goblin4red) 
(has_haste c_goblin4)
	(= (toughness c_goblin4)1)
(= (power c_goblin4)1)
(= (converted_mana_cost c_goblin4)1)

(is_in_hand c_dross_crocodile2)
(is_creature_colour c_dross_crocodile2 black) 
	(= (toughness c_dross_crocodile2)5)
(= (power c_dross_crocodile2)1)
(= (converted_mana_cost c_dross_crocodile2)4)

(is_owned_by_player c_knight2)
(has_vigilance c_knight2)
	(= (toughness c_knight2)2)
(= (power c_knight2)2)
(= (converted_mana_cost c_knight2)2)

is_owned_by_player c_aegis_turtle1)
	(= (toughness c_aegis_turtle1)5)
(= (power c_aegis_turtle1)0)
(= (converted_mana_cost c_aegis_turtle1)1)

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

