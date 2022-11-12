import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('test_area_nogit/worm.png').convert_alpha()
print(sprite_sheet_image)
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
print(sprite_sheet)

BG = (50, 50, 50)
BLACK = (0, 0, 0)



# animation for sprite
animations = {"move": None,
			 "jump": None,
			}
run_animation_list = []
run_animation_frames = 4 
jump_animation_list = []
jump_animation_frames = 11
update_tick = pygame.time.get_ticks()
update_cooldown = 100
frame =0

for x in range(run_animation_frames):
	run_animation_list.append(sprite_sheet.get_image(x, 32, 32, 5, BLACK))


for x in range(run_animation_frames,run_animation_frames+jump_animation_frames):
	jump_animation_list.append(sprite_sheet.get_image(x, 32, 32, 1, BLACK))

animations["move"] = run_animation_list
animations["jump"] = jump_animation_list
print(animations)

run = True
while run:

	#update background
	screen.fill(BG)

	#show frame images
	current_time = pygame.time.get_ticks()
	if current_time - update_tick >= update_cooldown:
		frame +=1
		update_tick = current_time
		if frame == len(run_animation_list):
			frame = 0

	#screen.blit(jump_animation_list[frame],(0,0))
	screen.blit(run_animation_list[frame],(0,0))
#
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()