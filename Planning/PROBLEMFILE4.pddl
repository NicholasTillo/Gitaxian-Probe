
(define (problem example4)
(:domain gitaxianprobe)

(:objects
    c_knight1 c_dross_crocodile1 c_dross_crocodile2 c_knight2 c_goblin1 - creature
    l_mountain1  l_plains1 l_swamp1  l_mountain2 - land 
    s_lightning_bolt1  s_chaplains_blessing1 - spell
    
)

(:init

;hand
	

(is_in_hand c_goblin1)
(is_owned_by_player c_goblin1)
(is_creature_colour c_goblin1 red) 
;stats
(= (toughness c_goblin1)1)
(= (max_toughness c_goblin1)1)
(= (power c_goblin1)1)
(= (converted_mana_cost c_goblin1)1)
(has_haste c_goblin1)



(is_owned_by_player c_dross_crocodile1)
(is_creature_colour c_dross_crocodile1 black) 
;stats
(= (toughness c_dross_crocodile1)1)
(= (max_toughness c_dross_crocodile1)1)
(= (power c_dross_crocodile1)5)
(= (converted_mana_cost c_dross_crocodile1)4)

(is_in_hand c_knight1)
(is_owned_by_player c_knight1)
(is_creature_colour c_knight1 white) 
;stats
(= (toughness c_knight1)2)
(= (max_toughness c_knight1)2)
(= (power c_knight1)2)
(= (converted_mana_cost c_knight1)2)
(has_vigilance c_knight1)







;lands
(is_in_hand l_mountain1)
(is_land_colour l_mountain1 red) 

(is_in_hand l_mountain2)
(is_land_colour l_mountain2 red) 

(is_in_hand l_plains1)
(is_land_colour l_plains1 white) 

(is_in_hand l_swamp1)
(is_land_colour l_swamp1 white) 

 

	;Creatures


(is_summoning_sick c_dross_crocodile2)
(is_creature_colour c_dross_crocodile2 black) 
(= (toughness c_dross_crocodile2)1)
(= (max_toughness c_dross_crocodile2)1)
(= (power c_dross_crocodile2)5)
(= (converted_mana_cost c_dross_crocodile2)4)


(is_summoning_sick c_knight2)
(is_creature_colour c_knight2 white) 
(= (toughness c_knight2)2)
(= (max_toughness c_knight2)2)
(= (power c_knight2)2)
(= (converted_mana_cost c_knight2)2)
(has_vigilance c_knight2)

;World
(= (current_life_total_player)6)
(= (current_life_total_enemy)12)
(current_phase main) 
(can_pass)



;Spells
(is_in_hand s_lightning_bolt1)
(is_spell_colour s_lightning_bolt1 red)
(= (spell_converted_mana_cost s_lightning_bolt1) 1)
(= (spell_value s_lightning_bolt1) 3)
(spell_effect deal s_lightning_bolt1)


(is_in_hand s_chaplains_blessing1)
(is_spell_colour s_chaplains_blessing1 white)
(= (spell_converted_mana_cost s_chaplains_blessing1) 1)
(= (spell_value s_chaplains_blessing1) 5)
(spell_effect heal s_chaplains_blessing1)



(=(available_mana white)0)
(=(available_mana blue)0)
(=(available_mana green)0)
(=(available_mana black)0)
(=(available_mana red)0)
(=(available_mana_total)0)
)


(:goal
(and(<=(current_life_total_enemy)(current_life_total_player))
;(and(is_dead c_grizzlybear1)))
)

)
)



