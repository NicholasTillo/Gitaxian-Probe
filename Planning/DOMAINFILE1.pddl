
(define (domain gitaxianprobe)
(:requirements 
:typing 
:negative-preconditions 
:fluents
:conditional-effects 
:universal-preconditions
:existential-preconditions
:strips
:equality
:disjunctive-preconditions
:adl

)

(:types
	creature
	spell
	land
	player
	colour 
	spell_effect
	phase
)

(:constants 
white blue black red green - colour
heal deal - spell_effect
main attack block endP opponentAttack opponentBlock opponentEnd - phase
)

(:predicates

;All Cards Have Each Of These
(is_in_hand ?card) 

;Usually just lands and creatures 
(is_tapped ?card)
(is_owned_by_player ?card)


;Creature
(is_dead ?creature - creature)
(is_creature_colour ?creature - creature ?colour - colour)
(is_summoning_sick ?creature - creature) 
(is_attacking ?creature - creature) 
(is_blocking ?creature - creature)
(is_blocked ?creature - creature) 
(has_vigilance ?creature - creature)
(has_haste ?creature - creature)

;Spells
(spell_effect ?effect - spell_effect ?spell - spell)
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
(max_toughness ?creature - creature) 
(power ?creature - creature) 
(converted_mana_cost ?creature - creature) 
(available_mana ?colour - colour)
(available_mana_total)
(current_life_total_player)
(current_life_total_enemy)
(spell_value ?spell - spell)
(spell_converted_mana_cost ?spell - spell)
)


(:action play_land
 :parameters (?land - land)
 :precondition (and 	
(current_phase main) 
(is_in_hand ?land)
(not(have_played_land))
(>=(current_life_total_player)0))
 :effect (and 
(not(is_in_hand ?land))
(have_played_land) 
(is_owned_by_player ?land)

)
)

(:action clean_up
:parameters (?creature - creature)
:precondition 
(and 
    (current_phase endP)
    (or(is_attacking ?creature)(is_blocking ?creature))
)
        
:effect
(and 
    (when(is_blocking ?creature)(not(is_blocking ?creature)))
    (when(and(not(is_blocked ?creature))(is_attacking ?creature)) (decrease (current_life_total_enemy) (power ?creature)))
    (not(is_attacking ?creature))
    (not(is_blocked ?creature))
    (assign(toughness ?creature)(max_toughness ?creature)))
)

( :action clear 
:parameters ()
:precondition 
    (and
        (not(can_pass))
        (current_phase endP)
        (forall(?creature - creature)
            (and
                (not(is_attacking ?creature))
                (not(is_blocking ?creature))
                (or
                    (is_owned_by_player ?creature)
                    (not(is_tapped ?creature))
                    (is_dead ?creature))
                )
            )
        )
    
:effect
(and (can_pass))
)

( :action all_opp_creatures_block
:parameters ()
:precondition
(and
    (current_phase block)
    (not(can_pass))
    (forall (?creature - creature)
            (and
                (>(toughness ?creature)0)
                (or
                    (is_owned_by_player ?creature)
                    (is_tapped ?creature)
                    (is_blocking ?creature)
                    (forall (?c - creature) (not(is_attacking ?c)))
                    (is_dead ?creature))
                )
        )
    )
    
:effect
(and (can_pass))
)


(:action opponent_clean_up
:parameters (?creature - creature)
:precondition 
    (and 
        (current_phase opponentEnd)
        (or(is_attacking ?creature)(is_blocked ?creature)(is_blocking ?creature))
    )
:effect
    (and 
        (not(is_blocking ?creature))
        (when (and(is_attacking ?creature) (not(is_blocked ?creature))) (decrease (current_life_total_player) (power ?creature)))
        (not(is_attacking ?creature))
        (not(is_blocked ?creature))
        (assign(toughness ?creature)(max_toughness ?creature)))
    )

( :action opponent_clear 
:parameters ()
:precondition 
    (and
        (not(can_pass))
        (current_phase opponentEnd)
        (forall(?creature - creature)
            (and
                (not(is_attacking ?creature))
                (not(is_blocking ?creature))
        
            )
        )
    )
:effect
(and (can_pass))
)

(:action tap_land 
 :parameters (?land - land ?c - colour)
 :precondition (and 
    (>(current_life_total_player)0)
    (not(is_in_hand ?land))
    (not(is_tapped ?land))
    (is_land_colour ?land ?c))
 :effect (and  
 (increase(available_mana ?c)1)
 (increase(available_mana_total)1)
 (is_tapped ?land)

)
)

(:action play_creature
 :parameters (?creature - creature ?c - colour)
 :precondition 
(and 
	; technicalities with player
    (>(current_life_total_player)0)
    (current_phase main)
    (is_in_hand ?creature)
    (is_creature_colour ?creature ?c)

; checking enough to pay for a creature
(>= (available_mana_total)(converted_mana_cost ?creature)) 
(>= (available_mana ?c) 1)
)
 :effect 
(and
		; defining summoning sickness
	(when (has_haste ?creature) (not(is_summoning_sick ?creature)))
    (when (not(has_haste ?creature)) (is_summoning_sick ?creature))
	(decrease (available_mana ?c) 1)
	(decrease (available_mana_total)(converted_mana_cost ?creature))

	(not(is_in_hand ?creature))
	(not(is_dead ?creature))
)
)

(:action attack_opponent 
 :parameters (?creature - creature)
 :precondition (and
    (>(current_life_total_player) 0)
    (is_owned_by_player ?creature)
    (not(is_tapped ?creature))
    (not(is_summoning_sick ?creature))
    (current_phase attack)
    (not(is_in_hand ?creature))
    (not(is_dead ?creature)))

 :effect (and 
(when(not(has_vigilance ?creature))(is_tapped ?creature))
(is_attacking ?creature)
(not(is_blocked ?creature))
)
)

(:action player_block_creature
 :parameters(?attacking_creature ?blocking_creature - creature)
 :precondition(and
			(>(current_life_total_player) 0)
			(current_phase opponentBlock)
			
			(is_attacking ?attacking_creature)
            (not(is_blocked ?attacking_creature))
            (not(is_dead ?attacking_creature))
            
            (not(is_blocking ?blocking_creature))
			(not(is_tapped ?blocking_creature))
            (not(is_dead ?blocking_creature))
            (not(is_in_hand ?blocking_creature))
            (is_owned_by_player ?blocking_creature)
            )
    
 :effect(and
            (decrease(toughness ?attacking_creature)(power ?blocking_creature))
            (decrease(toughness ?blocking_creature)(power ?attacking_creature))
			(is_blocked ?attacking_creature)
			(is_blocking ?blocking_creature)
			(not(can_pass))
)
)

(:action kill_creature 
 :parameters(?c - creature)
 :precondition(and(<= (toughness ?c)0))
 :effect(and(assign(toughness ?c)(max_toughness ?c))(is_dead ?c)) 

)


(:action can_pass_from_block
:parameters()
:precondition(and
            (>(current_life_total_player) 0)
			(current_phase opponentBlock)
			(forall(?creature - creature)
                (and
                    (>(toughness ?creature)0)
                )
			)
			)
:effect(and(can_pass)))


(:action can_pass_from_main
:parameters()
:precondition(and
            (>(current_life_total_player) 0)
			(current_phase main)
			(forall(?creature - creature)
                (and
                    (>(toughness ?creature)0)
                )
			)
			)
:effect(and(can_pass))




)

(:action opponent_block_creature
 :parameters(?attacking_creature ?blocking_creature - creature)
 :precondition(and
			(>(current_life_total_player) 0)
			(is_attacking ?attacking_creature)
			(not(is_blocking ?blocking_creature))
			(not(is_tapped ?blocking_creature))
            (not(is_blocked ?attacking_creature))
            (current_phase block)
            (not(is_dead ?attacking_creature))
            (not(is_dead ?blocking_creature))
            (not(is_owned_by_player ?blocking_creature))
            )
            
 :effect(and
            (decrease(toughness ?attacking_creature)(power?blocking_creature))
            (decrease(toughness ?blocking_creature)(power ?attacking_creature))
			(is_blocked ?attacking_creature)
			(is_blocking ?blocking_creature)
)
)
(:action pass
:parameters ()
:precondition (and  
    (can_pass)
    (>(current_life_total_player) 0)
    )
:effect (and

    (assign (available_mana white) 0)
    (assign (available_mana blue) 0)
    (assign (available_mana black) 0)
    (assign (available_mana red) 0)
    (assign (available_mana green) 0)
    (assign (available_mana_total) 0)
    
    
(when(current_phase main)
(and(not(current_phase main))
    (current_phase attack)
    (can_pass)
    (not (have_played_land))
    
))

(when(current_phase attack)
(and
    (not(current_phase attack))(current_phase block)
    (not(can_pass))
)

)
(when(current_phase block)
    (and
        (not(current_phase block))
        (current_phase endP)
        (not (can_pass))
    )
)
 ; create another action to check if all creatures are either blocking or not blocking
 ; for all creatures not owned by the player they must either be blocking or tapped

(when(current_phase endP)
(and
    (not(current_phase endP))
    (current_phase opponentAttack)
    (not(can_pass))
)
)


(when(current_phase opponentAttack)
(and
    (not(current_phase opponentAttack))(current_phase opponentBlock)
    (can_pass))
)

(when(current_phase opponentBlock)
(and(not(current_phase opponentBlock))(current_phase opponentEnd) (not(can_pass)))
)

(when(current_phase opponentEnd)
(and
    (not(current_phase opponentEnd))(current_phase main)
    (can_pass)

)
))
)               


(:action untap_player_cards
:parameters (?card)
:precondition
    (and
        (current_phase opponentEnd)
        (is_owned_by_player ?card)
        (or(is_tapped ?card)(is_summoning_sick ?card))
    )
:effect
    (and
        (not (is_tapped ?card))
        (not (is_summoning_sick ?card))
    )
)


(:action untap_opponent_cards
:parameters (?creature - creature)
:precondition
    (and
        (current_phase endP)
        (not(is_owned_by_player ?creature))
        (or(is_tapped ?creature)(is_summoning_sick ?creature))
    )
:effect
    (and
        (not (is_tapped ?creature))
        (not (is_summoning_sick ?creature))
    )
)

(:action play_spell
 :parameters( ?colour - colour ?spell - spell ?target)
 :precondition(and
    (>=(current_life_total_player)0)
    (is_in_hand ?spell)
    (current_phase main)
    (>=(toughness ?target)0)
    (is_spell_colour ?spell ?colour)
    (>= (available_mana_total)(spell_converted_mana_cost ?spell)) 
    (>= (available_mana ?colour) 1)
    )
 :effect(and
    ;pay mana
    (decrease (available_mana ?colour) 1)
	(decrease (available_mana_total)(spell_converted_mana_cost ?spell))
    
    (not(can_pass))
    (not(is_in_hand ?spell))
    
    ;Effects
    (when
        (spell_effect deal ?spell)
        (decrease(toughness ?target)(spell_value ?spell))
    )
    (when
        (spell_effect heal ?spell)
        (increase(current_life_total_player)(spell_value ?spell))
        )
    ;(when
    ;    (spell_effect deal ?spell)
    ;    (decrease(toughness ?target)(spell_value ?spell))
    ;    )
    ;(when
    ;    (and
    ;        (spell_effect deal ?spell)
    ;    )   
    ;
    ;(decrease(current_life_total_player)(spell_value ?spell))
    ;)
    )
)


;ENEMY BASED ACTIONS

(:action enemy_attack
:parameters (?creature1 - creature)
:precondition(and
             (not(is_attacking ?creature1))
             (not(is_owned_by_player ?creature1))
             (not(is_dead ?creature1))
             (not(is_summoning_sick ?creature1))
             (current_phase opponentAttack)
             (not(is_tapped ?creature1))
             )
:effect(and
    (is_attacking ?creature1)
    (not(is_blocked ?creature1))
(when
    (not(has_vigilance ?creature1)) 
    (is_tapped ?creature1))
)
)

( :action all_opp_creatures_attack
:parameters ()
:precondition
(and
    (current_phase opponentAttack)
    (forall (?creature - creature)
            (or
                (is_owned_by_player ?creature)
                (is_attacking ?creature)
                (is_dead ?creature))
            )
        )
    
:effect
(and (can_pass))
)


)
