(define (domain gitaxianprobe)

(:requirements 
:typing 
:negative-preconditions 
:action-costs 
:fluents 
:conditional-effects 
:universal-preconditions
)

(:types
	creature
	spell
	land
	player
	colour 
	number
	spell_effect
	phase
)

(:constants 
white blue black red green - colour
heal deal - spell_effect
main attack block end opponentAttack opponentEnd - phase
)

(:predicates

;All Cards Have Each Of These
(is_in_hand ?card) 

(is_player ?player - player)
(is_enemy ?player - player)

;Usually just lands and creatures 
(is_tapped ?card)


;Creature
(is_creature_colour ?creature - creature ?colour - colour)
(is_owned_by_player ?creature - creature)
(is_summoning_sick ?creature - creature) 
(is_attacking ?creature - creature) 
(is_blocking ?creature - creature)
(is_blocked ?creature - creature) 
(has_vigilance ?creature - creature)
(has_haste ?creature - creature)



;Spells
(spell_effect ?effect - effect ?spell - spell)
(is_spell_colour ?spell - spell ?colour - colour)


;Lands
(is_land_colour ?land - land ?colour - colour)

;Globals
(current_phase ?phase - phase)
(have_played_land)

;Used for only when the opponent has attacked with all creatures. 
(can_pass) 



)
(:functions 
(toughness ?creature - creature) 
(power ?creature - creature) 
(converted_mana_cost ?creature - creature) 
(available_mana ?colour - colour)
(available_mana_total)
(current_life_total_player)
(current_life_total_enemy)
(spell_value ?spell - spell)
(spell_converted_mana_cost ?spell - spell)


(:action play_land
 :parameters (?land - land)
 :precondition (and 	
(current_phase main) 
(is_in_hand ?land)
(not(have_played_land))
(not(life_total_is n0)))
 :effect (and 
(not(is_in_hand ?land))
(
(not(have_played_land))) 
)
)

(:action tap_land 
 :parameters (?land - land, ?c - Colour)
 :precondition (and 
(not(life_total_is n0))
(not(is_in_hand ?land))
(not(is_tapped ?land))
(is_colour ?c ?land)
 :effect (and(
increase((available_mana ?colour) 1)
increase((available_mana_total) 1)
)

)
(:action play_creature
 :parameters (?creature - creature, ?n1 ?n2 - numbers, ?player - player, ?c - colour)
 :precondition 
(and 
	; technicalities with player
(>=(current_life_total_player)0)
(current_phase main)
(is_in_hand ?creature)


; checking enough to pay for a creature
(<=(converted_mana_cost ?creature)(available_mana_total)) 
(<= (available_mana ?colour) 1)
)
 :effect 
(and
		; defining summoning sickness
		(when (has_haste ?creature) (not(is_summoning_sick ?creature)))
(when (not(has_haste ?creature)) (is_summoning_sick ?creature))
)
	(decrease (available_mana ?colour) 1)
	(decrease (available_mana_total)(converted_mana_cost ?creature))
	(is_owned_by_player ?creature)
	(not(is_in_hand ?creature))

)

(:action attack_player 
 :parameters (?creature - creature ?player - player)
 :precondition (and
(>=(current_life_total_player) 0)
(is_owned_by ?creature ?player)
(not(is_summoning_sick ?creature))
(current_phase attack))
 :effect (and 
(when(not(has_vigilance ?creature))(is_tapped ?creature))
(is_attacking ?creature)
(not(is_blocked ?creature))
)

(:action pass
:parameters ()
:precondition and(
(>=(current_life_total_player) 0)
(not(current_phase opponent)))
:effect (and
(when(current_phase main)
(and
(not(current_phase main))
(current_phase attack)
(assign (available_mana white) 0)
(assign (available_mana blue) 0)
(assign (available_mana black) 0)
(assign (available_mana red) 0)
(assign (available_mana green) 0)
(assign (available_mana_total) 0)
)
(when(current_phase attack)
(and(not(current_phase attack))(current_phase block))
)
(when(current_phase block)
(and(not(current_phase block))(current_phase end))

(when(current_phase end)
(and(not(current_phase end))(current_phase opponentAttack))

(when(current_phase opponentAttack)
(and(not(current_phase opponentAttack))(current_phase opponentEnd))
)
)
)
)

)
(:action block_creature
 :parameters(?attacking_creature ?blocking_creature - creature)
 :precondition(and
			(
(>=(current_life_total_player) 0)
			(is_attacking ?attacking_creature)
			(not(is_tapped ?blocking_creature))
)
 :effect
) 
(:action play_spell
 :parameters(?spell - spell ?target)
 :precondition(and
(>=(current_life_total_player) 0)
)
 :effect(and(
(when
(and
(spell_effect heal ?spell)
(>=(toughness ?target)0)
) 
(increase(toughness ?target)(spell_value ?spell))
)
(when
(and
(spell_effect heal ?spell)
(>=(toughness ?target)0)
) 
(increase(toughness ?target)(spell_value ?spell))
)
(when
(and
(spell_effect deal ?spell)
(>=(toughness ?target)0)
) 
(decrease(toughness ?target)(spell_value ?spell))
)
(when
(and
(spell_effect deal ?spell)
(>=(toughness ?target)0)
) 
(decrease(current_life_total_player)(spell_value ?spell))
)

)

;ENEMY BASED ACTIONS

(:action enemy_attack
:parameters (?creature1 ?creature2 - creature)
:precondition(not(attacked_already))
:effect(and(
forall(?creature - creature)
		(when(not(is_owned_by_player ?creautre))
(and
(is_attacking ?creature)
(when
(not(has_vigilance ?creature))  
(is_tapped ?creature)))
			)
		(can_pass) 
		)


)

