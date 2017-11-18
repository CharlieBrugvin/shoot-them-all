
#size of the window, in pixel
window_width = 1280#1024
window_height = 720#576
fullscreen = False
#number of columns
nbColumn = 14

#size of the elements
ship_width = window_width/nbColumn
ship_height = ship_width/1.5

invader_width = ship_width
invader_height = ship_height

laser_width = ship_width/8
laser_height = laser_width*3

#speed of the elements, in px/iteration
invader_speed_min = 0.03
invader_speed_max = 0.3

white_laser_speed_min = 1
white_laser_speed_max = 3
red_laser_speed = 4

#invader behaviour
invader_probality_shooting = 0.002
probability_of_second_invader_popping = 0.25
penality_if_invader_succeed = 5

#laser dammage
laser_dammage_against_ship = 3
laser_dammage_against_invader = 40

#texts
text_score_size = 40

#list of the events
# "type of the event" -> the duration of it, is seconds
dictEvent = {
	"ship_shooted" : 0.5,
	"ship_shot" : 1, #when the ship fire
	"invader_killed" : 1,
	"invader_succeed" : 3,
	"invader_shot" : 1
}
