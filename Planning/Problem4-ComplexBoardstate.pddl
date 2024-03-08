(define (problem example4)
(:domain gitaxianprobe)

(:objects
    player
)

(:init

)

(:goal
 and(<=(current_enemy_health)0)

)
(:metric maximize
(current_player_health)
)
)
