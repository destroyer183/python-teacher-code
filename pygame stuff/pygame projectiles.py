import math
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# load images
background_image = pygame.image.load("outer_space.jpg")
ship_image = pygame.image.load("ship.png")
fireball_image = pygame.image.load("fireball.jpg")
asteroid_image = pygame.image.load("asteroid.png")

# get image dimensions
# NEW/DIFFERENT WAY TO GET IMAGE/BOUNDING BOX DIMENSIONS
ship_width = ship_image.get_rect().width
ship_height = ship_image.get_rect().height

# OLD WAY TO GET IMAGE/BOUNDING BOX DIMENSIONS
asteroid_box = asteroid_image.get_rect()
asteroid_width = asteroid_box.width
asteroid_height = asteroid_box.height

fireball_width = fireball_image.get_rect().width
fireball_height = fireball_image.get_rect().height

# store locations of all graphics
fireball_x = -5000
fireball_y = -5000

# put the ship halfway and at the bottom of the screen
ship_x = WIDTH / 2 - ship_width / 2
ship_y = HEIGHT - ship_height

# put the asteroid at the top middle of the screen
asteroid_x = WIDTH / 2 - asteroid_width / 2
asteroid_y = 0

# give the asteroid health so that it has to be hit multiple times
# before being destroyed
asteroid_health = 10

play_game = True

###############################
# New stuff for projectile
###############################
fireball_fired = False
FIREBALL_SPEED = 3
fireball_x_speed = 0
fireball_y_speed = 0

# game loop
while play_game == True:

    # get keyboard inputs
    pygame.event.get()
    keys = pygame.key.get_pressed()

    # check if escape key was pressed to exit the program
    if keys[pygame.K_ESCAPE]:
        play_game = False

    # ship movement code
    if keys[pygame.K_w]:
        ship_y = ship_y - 5
    if keys[pygame.K_s]:
        ship_y = ship_y + 5
    if keys[pygame.K_a]:
        ship_x = ship_x - 5
    if keys[pygame.K_d]:
        ship_x = ship_x + 5

    # fire projectile code - press the spacebar, and the
    # fireball wasn't already fired
    if keys[pygame.K_SPACE] and fireball_fired == False:
        # calculate the direction to shoot the fireball
        # step 1:  calculate the vertical distance, "rise"
        rise = asteroid_y - ship_y

        # step 2: calculate the horizontal distance, "run"
        run = asteroid_x - ship_x

        # step 3: calculate the hypotenuse
        hypotenuse = math.sqrt(rise*rise + run*run)

        # step 4: calculate the speed of the projectile
        fireball_x_speed = run / hypotenuse * FIREBALL_SPEED
        fireball_y_speed = rise/ hypotenuse * FIREBALL_SPEED

        # step 5: move the fireball to the ship so it looks
        # like the ship is shooting it
        fireball_x = ship_x
        fireball_y = ship_y

        # step 6: "turn on" the fireball
        fireball_fired = True

    # draw my graphics with the background first
    screen.blit(background_image, (0,0))

    screen.blit(ship_image, (ship_x, ship_y))
    screen.blit(asteroid_image, (asteroid_x, asteroid_y))

    # draw the projectile IF it has been fired
    if fireball_fired == True:
        screen.blit(fireball_image, (fireball_x, fireball_y))

        # move the fireball if it's fired
        fireball_x = fireball_x + fireball_x_speed
        fireball_y = fireball_y + fireball_y_speed
       
        # let the user shoot the fireball again if the fireball
        # has flown off the screen
        if fireball_x > WIDTH or fireball_x + fireball_width < 0 or fireball_y + fireball_height < 0 or fireball_y > HEIGHT:
            fireball_fired = False

        # collision detection: check if the fireball hits the
        # asteroid
        asteroid_box = pygame.Rect(asteroid_x, asteroid_y,
                            asteroid_width, asteroid_height)

        fireball_box = pygame.Rect(fireball_x, fireball_y,
                            fireball_width, fireball_height)

        # if they hit, asteroid is destroyed
        if asteroid_box.colliderect(fireball_box):

            # reduce the asteroid's health BEFORE checking if it is destroyed
            asteroid_health = asteroid_health - 1

            # when the asteroid runs out of health, move it away
            if asteroid_health <= 0:
                asteroid_x = -10000
                asteroid_y = -10000

            fireball_x = -5000
            fireball_y = -5000
            fireball_fired = False
   
    pygame.display.update()

pygame.quit()
exit()