(define (domain gitaxianprobe)

; TO RUN ON ONLINE EDITOR:
; select this domain file & any of the problem files,
; solve with the ENHSP planner.

; note that this file will not run with any of the other planners.

; importing many requirements that are supported by ENHSP!
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

; define the types of objects that we will be using in this domain
; and within the problem files.
; all of these relate to concepts integral to MTG gameplay.
(:types
	creature
	spell
	land
	player
	colour 
	spell_effect
	phase
)

; define constants that will remain static no matter the problem,
; such as the colours that one can tap their lands for,
; the effect of the spells we implemented,
; and all the game phases of MTG.
(:constants 
    white blue black red green - colour
    heal deal - spell_effect
    main attack block endP opponentAttack opponentBlock opponentEnd - phase
)

; define the predicates that will act on objects,
; these will help us define states within our domain.
(:predicates

    ; globals
    (current_phase ?phase - phase)
    (have_played_land)
    (can_pass)
    
    ; the following predicates will act on all types of card objects...
    (is_in_hand ?card) 
    (is_owned_by_player ?card)
    
    ; only lands and creatures get tapped, not spells. 
    (is_tapped ?card)
    
    ; applies to creatures
    (is_dead ?creature - creature)
    (is_creature_colour ?creature - creature ?colour - colour)
    (is_summoning_sick ?creature - creature) 
    (is_attacking ?creature - creature) 
    (is_blocking ?creature - creature)
    (is_blocked ?creature - creature) 
    (has_vigilance ?creature - creature)
    (has_haste ?creature - creature)
    
    ; applies to spells
    (spell_effect ?effect - spell_effect ?spell - spell)
    (is_spell_colour ?spell - spell ?colour - colour)
    
    ; applies to lands
    (is_land_colour ?land - land ?colour - colour)
)

; the use of functions in our domains will help us define
; numeric values used in MTG. 
(:functions 

    ; values regarding creatures
    (toughness ?creature - creature) 
    (max_toughness ?creature - creature)
    (power ?creature - creature) 
    (converted_mana_cost ?creature - creature) 
    
    ; values to keep track of how much mana the player has
    (available_mana ?colour - colour)
    (available_mana_total)
    
    ; these will keep track of the health of the player and opponent
    (current_life_total_player)
    (current_life_total_enemy)
    
    ; values related to the functionality of spells
    (spell_value ?spell - spell)
    (spell_converted_mana_cost ?spell - spell)
)

; allows the player to play a land
(:action play_land
     :parameters (?land - land)
     :precondition 
        (and 	
            (current_phase main) 
            (is_in_hand ?land)
            (not(have_played_land))
            (>=(current_life_total_player)0)
        )
     :effect 
        (and 
            (not(is_in_hand ?land))
            (have_played_land) 
            (is_owned_by_player ?land)
        )
)

; returns creatures to the status of not blocking / not attacking, and max health
; once combat is over; i.e. in the end phase of the player.
; this action also processes damage towards an opponent, if a creature was unblocked
(:action clean_up
    :parameters (?creature - creature)
    :precondition 
        (and 
            (current_phase endP)
            (or
                (is_attacking ?creature)(is_blocking ?creature)
            )
        )
    :effect
        (and 
            (when
                (is_blocking ?creature)
                (not(is_blocking ?creature))
            )
            (when
                (and
                    (not(is_blocked ?creature))(is_attacking ?creature)
                ) 
                (decrease (current_life_total_enemy) (power ?creature))
            )
            (not(is_attacking ?creature))
            (not(is_blocked ?creature))
            (assign(toughness ?creature)(max_toughness ?creature))
        )
)

; allows the turn to pass after the clean_up is complete
; essentially ensures that all creatures have the correct status
; assigned to them by the time the phase ends.
(:action clear 
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
                        (is_dead ?creature)
                    )
                )
            )
        )
        
    :effect
        (and 
            (can_pass)
        )
)

; this action will force all of the opponent's creatures to block
; since we did not implement functionality for the opponent, as that is 
; outside the scope of this assignment.
(:action all_opp_creatures_block
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
                        (is_dead ?creature)
                    )
                )
            )
        )
    :effect
    (and (can_pass))
)

; performs the same core functionalities as clean_up action
; except for the opponent's creatures!
(:action opponent_clean_up
    :parameters (?creature - creature)
    :precondition 
        (and 
            (current_phase opponentEnd)
            (or
                (is_attacking ?creature)
                (is_blocked ?creature)
                (is_blocking ?creature)
            )
        )
    :effect
        (and 
            (not(is_blocking ?creature))
            (when 
                (and
                    (is_attacking ?creature) 
                    (not(is_blocked ?creature))
                ) 
                (decrease (current_life_total_player) (power ?creature))
            )
            (not(is_attacking ?creature))
            (not(is_blocked ?creature))
            (assign(toughness ?creature)(max_toughness ?creature)))
)

; checks that the game is able to be passed after the opponent
; has cleaned up all their creatures and processed their damage.
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
        (and 
            (can_pass)
        )
)

; allows the player to tap a land to add that land's colour to their
; mana pool (and to their total mana pool).
(:action tap_land 
     :parameters (?land - land ?c - colour)
     :precondition 
        (and 
            (>(current_life_total_player)0)
            (not(is_in_hand ?land))
            (not(is_tapped ?land))
            (is_land_colour ?land ?c)
        )
     :effect 
        (and  
         (increase(available_mana ?c)1)
         (increase(available_mana_total)1)
         (is_tapped ?land)
        )
)

; allows the player to play creatures with their current available mana,
; and on their main phase. the creatures will come in with 
; summoning sickness.
(:action play_creature
     :parameters (?creature - creature ?c - colour)
     :precondition 
        (and 
        	; technicalities with player and phase
            (>(current_life_total_player)0)
            (current_phase main)
            (is_in_hand ?creature)
            (is_creature_colour ?creature ?c)
        
            ; checking enough mana to pay for a creature
            (>= (available_mana_total)(converted_mana_cost ?creature)) 
            (>= (available_mana ?c) 1)
        )
     :effect 
        (and
        	; defining summoning sickness for creatures depending on 
        	; whether or not they have haste
        	(when (has_haste ?creature) (not(is_summoning_sick ?creature)))
            (when (not(has_haste ?creature)) (is_summoning_sick ?creature))
            
            ; using the mana to pay for the creature
        	(decrease (available_mana ?c) 1)
        	(decrease (available_mana_total)(converted_mana_cost ?creature))
            
            ; technicalities
        	(not(is_in_hand ?creature))
        	(not(is_dead ?creature))
        )
)

; indicates that a creature of the player's is attacking the opponent.
(:action attack_opponent 
     :parameters (?creature - creature)
     :precondition 
        (and
            (>(current_life_total_player) 0)
            (is_owned_by_player ?creature)
            
            ; checking that it is able to tap
            (not(is_tapped ?creature))
            (not(is_summoning_sick ?creature))
            
            (current_phase attack)
            (not(is_in_hand ?creature))
            (not(is_dead ?creature))
        )
     :effect 
        (and 
            (when
                (not(has_vigilance ?creature))
                (is_tapped ?creature)
            )
            (is_attacking ?creature)
            (not(is_blocked ?creature))
        )
)

; allows the planner to choose whether or not to block the
; opponent's attacking creature.
(:action player_block_creature
     :parameters (?attacking_creature ?blocking_creature - creature)
     :precondition
        (and
            ; technicalities
			(>(current_life_total_player) 0)
			(current_phase opponentBlock)
			
			; checking status of opponent's creatures
			(is_attacking ?attacking_creature)
            (not(is_blocked ?attacking_creature))
            (not(is_dead ?attacking_creature))
            
            ; checking status of our creature, if they are to block
            (not(is_blocking ?blocking_creature))
			(not(is_tapped ?blocking_creature))
            (not(is_dead ?blocking_creature))
            (not(is_in_hand ?blocking_creature))
            (is_owned_by_player ?blocking_creature)
        )
     :effect
         (and
            (decrease(toughness ?attacking_creature)(power ?blocking_creature))
            (decrease(toughness ?blocking_creature)(power ?attacking_creature))
			(is_blocked ?attacking_creature)
			(is_blocking ?blocking_creature)
			(not(can_pass))
        )
)

; defines death for a creature
(:action kill_creature 
     :parameters (?c - creature)
     :precondition
        (and
            (<= (toughness ?c)0)
        )
     :effect
        (and
            (assign(toughness ?c)(max_toughness ?c))
            (is_dead ?c)
        ) 
)

; checking after the player's block phase that the creatures who blocked 
; are actually dead, before passing.
(:action can_pass_from_block
    :parameters ()
    :precondition
        (and
            (>(current_life_total_player) 0)
			(current_phase opponentBlock)
			(forall(?creature - creature)
                (and
                    (>(toughness ?creature)0)
                )
			)
    	)
    :effect(and(can_pass))
)

; allows passing from the main step if a spell is played.
(:action can_pass_from_main
    :parameters ()
    :precondition
        (and
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

; defines what happens when an opponent blocks one of the player's creatures!
(:action opponent_block_creature
    :parameters (?attacking_creature ?blocking_creature - creature)
    :precondition
        (and
    		(>(current_life_total_player) 0)
    		(current_phase block)
    
    		(is_attacking ?attacking_creature)
    		(not(is_blocked ?attacking_creature))
    		(not(is_dead ?attacking_creature))
    		
    		(not(is_blocking ?blocking_creature))
    		(not(is_tapped ?blocking_creature))
            (not(is_dead ?blocking_creature))
            (not(is_owned_by_player ?blocking_creature))
        )
    :effect
        (and
            ; mark damage
            (decrease(toughness ?attacking_creature)(power?blocking_creature))
            (decrease(toughness ?blocking_creature)(power ?attacking_creature))
            
            ; update status
    		(is_blocked ?attacking_creature)
    		(is_blocking ?blocking_creature)
        )
)

; allows the planner to progress from one phase to another
; if the requirements for each phase are met.
(:action pass
    :parameters ()
    :precondition 
        (and  
            (can_pass)
            (>(current_life_total_player) 0)
        )
    :effect 
        (and
            ; clear all the mana after moving from one phase to another
            (assign (available_mana white) 0)
            (assign (available_mana blue) 0)
            (assign (available_mana black) 0)
            (assign (available_mana red) 0)
            (assign (available_mana green) 0)
            (assign (available_mana_total) 0)
            
            ; moving from player's main to player's attack
            (when
                (current_phase main)
                (and
                    (not(current_phase main))
                    (current_phase attack)
                    (can_pass)
                    (not (have_played_land))
                )
            )
        
            ; moving from player's attack to player's block
            (when
                (current_phase attack)
                (and
                    (not(current_phase attack))
                    (current_phase block)
                    (not(can_pass))  ; must do checks here
                )
            )
            
            ; moving from player's block to player's end step
            (when
                (current_phase block)
                (and
                    (not(current_phase block))
                    (current_phase endP)
                    (not (can_pass))  ; must do clean-up and clear here
                )
            )
            
            ; the opponent does not play spells so they do not
            ; need a main phase...
            
            ; this will pass directly from the player's end step
            ; to the opponent's attack phase
            (when
                (current_phase endP)
                (and
                    (not(current_phase endP))
                    (current_phase opponentAttack)
                    (not(can_pass))
                )
            )
        
            ; move from opponent's attack to opponent's block phase
            (when
                (current_phase opponentAttack)
                (and
                    (not(current_phase opponentAttack))
                    (current_phase opponentBlock)
                    (can_pass)
                )
            )
        
            ; move from the opponent's block phase to their end step
            (when
                (current_phase opponentBlock)
                (and
                    (not(current_phase opponentBlock))
                    (current_phase opponentEnd)
                    (not(can_pass))
                )
            )
        
            ; pass the turn back to the player's main after the opponent's end
            (when(current_phase opponentEnd)
                (and
                    (not(current_phase opponentEnd))
                    (current_phase main)
                    (can_pass)
                )
            )
        )
)               

; allows the player to untap their cards
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
            (not(is_tapped ?card))
            (not(is_summoning_sick ?card))
        )
)

; allows the opponent to untap their cards
(:action untap_opponent_cards
    :parameters (?creature - creature)
    :precondition
        (and
            (current_phase endP)
            (not(is_owned_by_player ?creature))
            (or
                (is_tapped ?creature)
                (is_summoning_sick ?creature)
            )
        )
    :effect
        (and
            (not(is_tapped ?creature))
            (not(is_summoning_sick ?creature))
        )
)

; allows the player to play a heal or deal spell
(:action play_spell
    :parameters (?colour - colour ?spell - spell ?target)
    :precondition
        (and
            ; technicalities
            (>=(current_life_total_player)0)
            (is_in_hand ?spell)
            (current_phase main)
            (is_spell_colour ?spell ?colour)
            
            ; checking that the target creature is in play
            (>=(toughness ?target)0)
            
            ; check that we have enough mana to play the spell
            (>= (available_mana_total)(spell_converted_mana_cost ?spell)) 
            (>= (available_mana ?colour) 1)
        )
    :effect
        (and
            ; pay mana
            (decrease (available_mana ?colour) 1)
            (decrease (available_mana_total)(spell_converted_mana_cost ?spell))
            
            ; technicalities
            (not(can_pass))
            (not(is_in_hand ?spell))
            
            ; define what the corresponding spell does
            (when
                (spell_effect deal ?spell)
                (decrease(toughness ?target)(spell_value ?spell))
            )
            (when
                (spell_effect heal ?spell)
                (increase(current_life_total_player)(spell_value ?spell))
            )
        )
)

; defines the action for what it means 
; for an opponent's creature to attack.
(:action enemy_attack
    :parameters (?creature1 - creature)
    :precondition
        (and
             (not(is_attacking ?creature1))
             (not(is_owned_by_player ?creature1))
             (not(is_dead ?creature1))
             (not(is_summoning_sick ?creature1))
             (current_phase opponentAttack)
             (not(is_tapped ?creature1))
        )
    :effect
        (and
            (is_attacking ?creature1)
            (not(is_blocked ?creature1))
            (when
                (not(has_vigilance ?creature1)) 
                (is_tapped ?creature1)
            )
        )
)

; this will force the opponent to attack with all their 
; creatures whenever possible, similar to how they also
; block whenever possible.
( :action all_opp_creatures_attack
    :parameters ()
    :precondition
        (and
            (current_phase opponentAttack)
            (forall (?creature - creature)
                (or
                    (is_owned_by_player ?creature)
                    (is_attacking ?creature)
                    (is_dead ?creature)
                )
            )
        )
    :effect
        (and 
            (can_pass)
        )
)
    
)
;eof
