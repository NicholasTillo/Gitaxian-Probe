
(define (problem example3)
(:domain gitaxianprobe)

(:objects
    c_grizzlybear1  c_goblin1  c_grizzlybear2 - creature
    l_mountain1  l_plains1 - land 
    s_lightning_bolt1 s_lightning_bolt2 s_chaplains_blessing1 - spell
    
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



;lands
(is_in_hand l_mountain1)
(is_land_colour l_mountain1 red) 

(is_in_hand l_plains1)
(is_land_colour l_plains1 white) 

 

	;Creatures


(is_summoning_sick c_grizzlybear1)
(is_creature_colour c_grizzlybear1 green) 
(= (toughness c_grizzlybear1)2)
(= (max_toughness c_grizzlybear1)2)
(= (power c_grizzlybear1)2)
(= (converted_mana_cost c_grizzlybear1)2)

(is_summoning_sick c_grizzlybear2)
(is_creature_colour c_grizzlybear2 green) 
(= (toughness c_grizzlybear2)2)
(= (max_toughness c_grizzlybear2)2)
(= (power c_grizzlybear2)2)
(= (converted_mana_cost c_grizzlybear2)2)

;World
(= (current_life_total_player)3)
(= (current_life_total_enemy)3)
(current_phase main) 
(can_pass)



;Spells
(is_in_hand s_lightning_bolt1)
(is_spell_colour s_lightning_bolt1 red)
(= (spell_converted_mana_cost s_lightning_bolt1) 1)
(= (spell_value s_lightning_bolt1) 3)
(spell_effect deal s_lightning_bolt1)

(is_in_hand s_lightning_bolt2)
(is_spell_colour s_lightning_bolt2 red)
(= (spell_converted_mana_cost s_lightning_bolt2) 1)
(= (spell_value s_lightning_bolt2) 3)
(spell_effect deal s_lightning_bolt2)

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
(and(<=(current_life_total_enemy)0)
;(and(is_dead c_grizzlybear1)))
)

)
)



