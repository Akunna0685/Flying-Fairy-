import random
import sys
import pygame
from pygame.locals import *


# Global Variables for the game
window_width = 1000
window_height = 699

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
grassfloor = 'grass.png'
background_image = 'Crystal cave.jpg'
fairyplayer_image = 'Fairy.png'
fairyground_image = 'base.png'





def fairygame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    fairyground = 0
    tempheight = 100

    print(horizontal)
    print(vertical)

    # Generating two grass for blitting on window
    first_grass = createGrass()
    second_grass = createGrass()

    # List containing lower grass
    down_grass = [
        {'x': window_width + 300 - tempheight,
         'y': first_grass[1]['y']},
        {'x': window_width + 300 - tempheight + (window_width / 2),
         'y': second_grass[1]['y']},
    ]

    # List Containing upper pipes
    up_grass = [
        {'x': window_width + 300 - tempheight,
         'y': first_grass[0]['y']},
        {'x': window_width + 200 - tempheight + (window_width / 2),
         'y': second_grass[0]['y']},
    ]

    grassVelX = -4  # pipe velocity along x

    fairy_velocity_y = -9  # bird velocity
    fairy_Max_Vel_Y = 10
    fairy_Min_Vel_Y = -8
    fairyAccY = 1

    # velocity while flapping
    fairy_fly_velocity = -8

    # It is true only when the bird is flapping
    fairy_flying = False
    while True:

        # Handling the key pressing events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    fairy_velocity_y = fairy_fly_velocity
                    fairy_flying = True

        # This function will return true if the flappybird is crashed
        game_over = isGameOver(horizontal, vertical, up_grass, down_grass)

        if game_over:
            return

        # check for your_score
        playerMidPos = horizontal + game_images['Fairy'].get_width() / 2
        for grass in up_grass:
            grassMidPos = grass['x'] + game_images['grassimage'][0].get_width() / 2
            if grassMidPos <= playerMidPos < grassMidPos + 4:
                # Printing the score
                your_score += 1
                print(f"Your your_score is {your_score}")

        if fairy_velocity_y < fairy_Max_Vel_Y and not fairy_flying:
            fairy_velocity_y += fairyAccY

        if fairy_flying:
            fairy_flying = False
        playerHeight = game_images['Fairy'].get_height()
        vertical = vertical + min(fairy_velocity_y, elevation - vertical - playerHeight)

        # move pipes to the left
        for uppergrass, lowergrass in zip(up_grass, down_grass):
            uppergrass['x'] += grassVelX
            lowergrass['x'] += grassVelX

        # Add a new pipe when the first is about
        # to cross the leftmost part of the screen
        if 0 < up_grass[0]['x'] < 5:
            newgrass = createGrass()
            up_grass.append(newgrass[0])
            down_grass.append(newgrass[1])

        # if the pipe is out of the screen, remove it
        if up_grass[0]['x'] < -game_images['grassimage'][0].get_width():
            up_grass.pop(0)
            down_grass.pop(0)

        # Lets blit our game images now
        window.blit(game_images['Crystal cave'], (0, 0))
        for upperGrass, lowerGrass in zip(up_grass, down_grass):
            window.blit(game_images['grassimage'][0],
                        (upperGrass['x'], upperGrass['y']))
            window.blit(game_images['grassimage'][1],
                        (lowerGrass['x'], lowerGrass['y']))

        window.blit(game_images['base'], (fairyground, 600))
        window.blit(game_images['Fairy'], (horizontal, vertical))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Refreshing the game window and displaying the score.
        pygame.display.update()

        # Set the framepersecond
        framepersecond_clock.tick(framepersecond)


        #clock = pygame.time.Clock()
        #pygame.display.flip()
        #clock.tick(30)


def isGameOver(horizontal, vertical, up_grass, down_grass):
    if vertical > elevation - 25 or vertical < 0:
        return True

    # Checking if bird hits the upper pipe or not
    for grass in up_grass:
        grassHeight = game_images['grassimage'][0].get_height()
        if (vertical < grassHeight + grass['y']
                and abs(horizontal - grass['x']) < game_images['grassimage'][0].get_width()):
            return True

    # Checking if bird hits the lower pipe or not
    for grass in down_grass:
        if (vertical + game_images['Fairy'].get_height() > grass['y']
                and abs(horizontal - grass['x']) < game_images['grassimage'][0].get_width()):
            return True

    return False

def createGrass():
                offset = window_height / 3
                grassHeight = game_images['grassimage'][0].get_height()

                # generating random height of pipes
                y2 = offset + random.randrange(0,int(window_height - game_images['base'].get_height() - 1.2 * offset))
                grassX = window_width + 10
                y1 = grassHeight - y2 + offset
                grass = [
                    # upper Pipe
                    {'x': grassX, 'y': -y1},

                    # lower Pipe
                    {'x': grassX, 'y': y2}
                ]
                return grass



if __name__ == "__main__":
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock= pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flying Fairy Game')

    # Load all the images which we will use in the game
    # images for displaying score
    game_images['scoreimages'] = (
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha()
    )
    game_images['Fairy'] = pygame.image.load(fairyplayer_image).convert_alpha()
    game_images['base'] = pygame.image.load(fairyground_image).convert_alpha()
    game_images['Crystal cave'] = pygame.image.load(background_image).convert_alpha()
    game_images['grassimage'] = (pygame.transform.rotate(pygame.image.load(grassfloor)
                                                        .convert_alpha(),
                                                        180),
                                pygame.image.load(grassfloor).convert_alpha())

    print("WELCOME TO THE FAIRY FOREST GAME")
    print("Press space or enter to start the game")


    while True:

        # sets the coordinates of flappy bird
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['Fairy'].get_height()) / 2)



        # for selevel
        fairyground = 0

        print(horizontal)
        print(vertical)
        while True:
            for event in pygame.event.get():

                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

                    # Exit the program
                    sys.exit()

                # If the user presses space or up key,
                # start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    fairygame()

                # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['Crystal cave'], (0, 0))
                    window.blit(game_images['Fairy'], (horizontal, vertical))
                    window.blit(game_images['base'], (fairyground, 600))

                    # Just Refresh the screen
                    pygame.display.update()

                    framepersecond_clock.tick(framepersecond)





