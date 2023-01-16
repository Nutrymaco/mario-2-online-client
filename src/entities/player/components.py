from dataclasses import dataclass as component


@component
class Player:
	movement_speed = 2
	jump_speed = 5
	jump_count = 0
	is_jumping = False
