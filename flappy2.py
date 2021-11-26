import pygame, sys, random 

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,600))
	screen.blit(floor_surface,(floor_x_pos + 400,600))

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (70,bird_rect.centery))
	return new_bird,new_bird_rect

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (600,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (600,random_pipe_pos - 200))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 2
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 700:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		return False

	return True

pygame.init
gravity = 0.25
bird_movement = 0
game_active = True
screen = pygame.display.set_mode((400,700))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (70,350))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1600)
pipe_height = [250,400,550]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (200,300))

while True : 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE : 
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bird_rect.center = (70,350)
                pipe_list.clear()
                bird_movement = 0
                bird_movement -= 6

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    
    screen.blit(bg_surface,(0,0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
    
    else:
        screen.blit(game_over_surface,game_over_rect)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -400:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)