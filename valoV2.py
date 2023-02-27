import pygame, sys
from pygame.locals import *
import math
pygame.init()

# MAP SET UP

tile_image = pygame.image.load('tile2.png')
tile_size = tile_image.get_width()
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
game_map = load_map('mapV1')

map_size = len(game_map[0])


# DISPLAY SET UP

screen_width = 700
screen = pygame.display.set_mode((screen_width, screen_width))
# to be set at screen_width, screen_width


# PLAYER SET UP

player_image =  pygame.image.load('player.png')
player_image.set_colorkey((255,255,255))
player_rect = pygame.Rect(500,50,50,50)
speed = 5
moving_right = False
moving_left = False
moving_up = False
moving_down = False
player_loc = [player_rect.x,player_rect.y]
player_angle = math.pi
FOV = math.pi / 2
HALF_FOV = FOV / 2
true_scroll = [player_loc[0],player_loc[1]]

# FPS COUNTER

fps = pygame.time.Clock()
font = pygame.font.SysFont("Arial" , 18 , bold = True)
def fps_counter():
    FPS = str(int(fps.get_fps()))
    fps_t = font.render(FPS , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))


# TILE RECTS
tile_rects = []
y = 0
for row in game_map:
    x = 0
    for tile in row:
        if tile == '1':
             tile_rects.append(pygame.Rect(x * tile_size , y * tile_size  , tile_size, tile_size))
        x += 1
    y += 1

while True:
    screen.fill((255,255,0))

    # SCROLLING

    true_scroll[0] += (player_rect.x-true_scroll[0] - (screen_width / 2)) / 20
    true_scroll[1] += (player_rect.y-true_scroll[1] - (screen_width / 2)) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # TILE BLIT

    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(tile_image, (x*tile_size - scroll[0] , y*tile_size - scroll[1]))
            x += 1
        y += 1


    # COLLITIONS AND MOVEMENT

    collisions = []
    if moving_left == True:
        player_rect.x -= speed
        player_loc[0] -= speed
    if moving_right == True:
        player_rect.x += speed
        player_loc[0] += speed
    for tile in tile_rects:
        if player_rect.colliderect(tile):
            collisions.append(tile)
    for tile in collisions:
        if moving_left == True:
            player_rect.left = tile.right
        if moving_right == True:
            player_rect.right = tile.left
        player_loc[0] = player_rect.x
    collisions = []
    if moving_up == True:
        player_rect.y -= speed
        player_loc[1] -= speed
    if moving_down == True:
        player_rect.y += speed
        player_loc[1] += speed
    for tile in tile_rects:
        if player_rect.colliderect(tile):
            collisions.append(tile)
    for tile in collisions:
        if moving_up == True:
            player_rect.top = tile.bottom
        if moving_down == True:
            player_rect.bottom = tile.top
        player_loc[1] = player_rect.y
    screen.blit(player_image, (player_rect.x-scroll[0],player_rect.y-scroll[1]))


     # PLAYER ANGLE

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if ((player_rect.x-scroll[0] + 25) - mouse_x) == 0:
        if (player_rect.y-scroll[1] + 25) < mouse_y:
            player_angle = (3 * math.pi) / 2
        if (player_rect.y-scroll[1] + 25) > mouse_y:
            player_angle = math.pi / 2
    elif ((player_rect.y-scroll[1] + 25) - mouse_y) == 0:
        if (player_rect.x-scroll[0] + 25) > mouse_x:
            player_angle = math.pi
        if (player_rect.x-scroll[0] + 25) < mouse_x:
            player_angle = 0
    else:
        player_angle = math.atan(((player_rect.y-scroll[1] + 25) - mouse_y) / ((player_rect.x-scroll[0] + 25) - mouse_x))
        if (player_rect.y-scroll[1] + 25) > mouse_y and (player_rect.x-scroll[0] + 25) < mouse_x:
            player_angle = -1 * player_angle
        if (player_rect.y-scroll[1] + 25) > mouse_y and (player_rect.x-scroll[0] + 25) > mouse_x:
            player_angle =  math.pi - player_angle
        if (player_rect.y-scroll[1] + 25) < mouse_y and (player_rect.x-scroll[0] + 25) > mouse_x:
            player_angle = math.pi - player_angle
        if (player_rect.y-scroll[1] + 25) < mouse_y and (player_rect.x-scroll[0] + 25) < mouse_x:
            player_angle = (2 * math.pi) - player_angle
    player_angle = -1 * player_angle


     # LEFT-RIGHT ANGLE

    left_angle = player_angle - HALF_FOV
    if left_angle < (-2 * math.pi):
        left_angle = left_angle + (2 * math.pi)
    right_angle = player_angle + HALF_FOV
    if right_angle > 0:
        right_angle = right_angle - (2 * math.pi)
    pygame.draw.line(screen, (255, 0, 0), ((player_rect.x-scroll[0] + 25), (player_rect.y-scroll[1] + 25)), ((player_rect.x-scroll[0] + 25) + (math.cos(right_angle) * 500),  (player_rect.y-scroll[1] + 25) + (math.sin(right_angle) * 500)), 2)
    pygame.draw.line(screen, (255, 0, 0), ((player_rect.x-scroll[0] + 25), (player_rect.y-scroll[1] + 25)), ((player_rect.x-scroll[0] + 25) + (math.cos(left_angle) * 500),  (player_rect.y-scroll[1] + 25) + (math.sin(left_angle) * 500)), 2)


    ########### RAYCASTING ###########

    # ALL THE TILES IN RANGE

    right_bound = player_rect.x + (screen_width / 4)
    left_bound = player_rect.x - (screen_width / 4)
    down_bound = player_rect.y + (screen_width / 4)
    up_bound = player_rect.y - (screen_width / 4)
    rects = []
    for tile in tile_rects:
        if left_bound < (tile.left + 150) and right_bound > (tile.right - 150 ) and up_bound < (tile.top + 150) and down_bound > (tile.bottom - 150) :
            rects.append(
                        (
                        ((tile.left - scroll[0]), (tile.top - scroll[1])),
                        ((tile.left - scroll[0] + tile_size), (tile.top - scroll[1])),
                        ((tile.left - scroll[0] + tile_size), (tile.top - scroll[1] + tile_size)),
                        ((tile.left - scroll[0]), (tile.top - scroll[1] + tile_size))
                        )
                        )

    # ALL THE TILES IN ANGLE

    slopes = {}
    finalpoints = []
    for rect in rects:
        for point in rect:
            if ((player_rect.x-scroll[0] + 25) - point[0]) == 0:
                if (player_rect.y-scroll[1] + 25) < point[1]:
                    point_angle = (3 * math.pi) / 2
                if (player_rect.y-scroll[1] + 25) > point[1]:
                    point_angle = math.pi / 2
            elif ((player_rect.y-scroll[1] + 25) - point[1]) == 0:
                if (player_rect.x-scroll[0] + 25) > point[0]:
                    point_angle = math.pi
                if (player_rect.x-scroll[0] + 25) < point[0]:
                    point_angle = 0
            else:
                point_angle = math.atan(((player_rect.y-scroll[1] + 25) - point[1]) / ((player_rect.x-scroll[0] + 25) - point[0]))
                if (player_rect.y-scroll[1] + 25) > point[1] and (player_rect.x-scroll[0] + 25) < point[0]:
                    point_angle = -1 * point_angle
                if (player_rect.y-scroll[1] + 25) > point[1] and (player_rect.x-scroll[0] + 25) > point[0]:
                    point_angle =  math.pi - point_angle
                if (player_rect.y-scroll[1] + 25) < point[1] and (player_rect.x-scroll[0] + 25) > point[0]:
                    point_angle = math.pi - point_angle
                if (player_rect.y-scroll[1] + 25) < point[1] and (player_rect.x-scroll[0] + 25) < point[0]:
                    point_angle = (2 * math.pi) - point_angle
            point_angle = -1 * point_angle
            if player_angle < (-1 * ((math.pi * 2) - HALF_FOV)) or player_angle > (-1 * HALF_FOV):

                    if point_angle > left_angle or point_angle < right_angle:
                        finalpoints.append(point)
            else:
                if point_angle < right_angle and point_angle > left_angle:
                    finalpoints.append(point)
            slopes[point] = point_angle

    # TILE GRIDS

    verticals = []
    x = -1 * scroll[0]
    x = x - tile_size
    for i in range(int(map_size) + 3):
        verticals.append(x)
        pygame.draw.line(screen, (0,255,0), (x , 10), (x , 590), 2)
        x = x + tile_size

    horizontals = []
    y = -1 * scroll[1]
    y = y - tile_size
    for i in range(int(map_size) + 3):
        horizontals.append(y)
        pygame.draw.line(screen, (0,255,0), (10 , y), (590 , y), 2)
        y = y + tile_size

    # INTERSECTIONS OF EACH POINT

    polycoords = {}
    for point in finalpoints:

        if ((player_rect.x-scroll[0] + 25) - point[0]) == 0:
            pass
        elif ((player_rect.y-scroll[1] + 25) - point[1]) == 0:
            pass

        else:
            m = ((player_rect.y-scroll[1] + 25) - point[1]) / ((player_rect.x-scroll[0] + 25) - point[0])

            ########### VERTICALS ###############


            if (player_rect.x-scroll[0] + 25) > point[0]:
                for i in verticals:
                    if i < (player_rect.x-scroll[0] + 25):
                        x = i
            if (player_rect.x-scroll[0] + 25) < point[0]:
                for i in verticals:
                    if i > (player_rect.x-scroll[0] + 25):
                        x = i
                        break
            y = (m * (x - point[0])) + point[1]

            Y = y
            if y not in horizontals:
                for i in horizontals:
                    if i < y:
                        Y = i

            if (player_rect.x-scroll[0] + 25) > point[0]:
                Xcoord = int((x + scroll[0]) / tile_size) - 1
            if (player_rect.x-scroll[0] + 25) < point[0]:
                Xcoord = int((x + scroll[0]) / tile_size)

            Ycoord = int((Y + scroll[1]) / tile_size)
            if Ycoord == map_size:
                Ycoord -= 1


            if (player_rect.x-scroll[0] + 25) > point[0]:
                V_E_X = x - (tile_size * (map_size/8))
                V_E_Y = (m * (V_E_X - point[0])) + point[1]
            else:
                V_E_X = x + (tile_size * (map_size/8))
                V_E_Y = (m * (V_E_X - point[0])) + point[1]

            if game_map[Ycoord][Xcoord] != "0" or (x,y) in finalpoints:
                (V_X, V_Y) = (x,y)
                #pygame.draw.line(screen, (0,255,0), (x,y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)), 4)
            else:
                first = True
                for i in range(int(map_size)):
                    if (player_rect.x-scroll[0] + 25) > point[0]:
                        x -= tile_size
                        y = (m * (x - point[0])) + point[1]
                        Y = y
                        if y not in horizontals:
                            for i in horizontals:
                                if i < y:
                                    Y = i
                        Ycoord = int((Y + scroll[1]) / tile_size)
                        if (player_rect.x-scroll[0] + 25) > point[0]:
                            Xcoord = int((x + scroll[0]) / tile_size) - 1
                        if (player_rect.x-scroll[0] + 25) < point[0]:
                            Xcoord = int((x + scroll[0]) / tile_size)

                        if Ycoord == map_size:
                            Ycoord -= 1
                        if game_map[Ycoord][Xcoord] != "0" or (x,y) in finalpoints:
                            if first:
                                (V_X, V_Y) = (x,y)
                                first = False
                            #pygame.draw.line(screen, (0,255,0), (x,y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)), 4)

                            break
                    if (player_rect.x-scroll[0] + 25) < point[0]:
                        x += tile_size
                        y = (m * (x - point[0])) + point[1]
                        Y = y
                        if y not in horizontals:
                            for i in horizontals:
                                if i < y:
                                    Y = i
                        Ycoord = int((Y + scroll[1]) / tile_size)
                        if (player_rect.x-scroll[0] + 25) > point[0]:
                            Xcoord = int((x + scroll[0]) / tile_size) - 1
                        if (player_rect.x-scroll[0] + 25) < point[0]:
                            Xcoord = int((x + scroll[0]) / tile_size)
                        if Ycoord == map_size:
                            Ycoord -= 1
                        if game_map[Ycoord][Xcoord] != "0" or (x,y) in finalpoints:
                            #pygame.draw.line(screen, (0,255,0), (x,y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)), 4)
                            if first:
                                (V_X, V_Y) = (x,y)
                                first = False
                            break

            ################# HOrizontals ######################

            if (player_rect.y-scroll[1] + 25) > point[1]:
                for i in horizontals:
                    if i < (player_rect.y-scroll[1] + 25):
                        y = i

            if (player_rect.y-scroll[1] + 25) < point[1]:
                for i in horizontals:
                    if i > (player_rect.y-scroll[1] + 25):
                        y = i
                        break

            x = ((y - point[1]) / m) + point[0]

            X = x
            if x not in verticals:
                for i in verticals:
                    if i < x:
                        X = i

            if (player_rect.y-scroll[1] + 25) > point[1]:
                Ycoord = int((y + scroll[1]) / tile_size) - 1
            if (player_rect.y-scroll[1] + 25) < point[1]:
                Ycoord = int((y + scroll[1]) / tile_size)

            Xcoord = int((X + scroll[0]) / tile_size)
            if Xcoord == map_size:
                Xcoord -= 1

            if (player_rect.y-scroll[1] + 25) > point[1]:
                H_E_Y = y - (tile_size * (map_size/8))
                H_E_X = ((H_E_Y - point[1]) / m) + point[0]

            else:
                H_E_Y = y + (tile_size * (map_size/8))
                H_E_X = ((H_E_Y - point[1]) / m) + point[0]



            if game_map[Ycoord][Xcoord] != "0" or (x,y) in finalpoints:
                (H_X, H_Y) = (x,y)
                #pygame.draw.line(screen, (255,0,0), (x,y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)))
            else:
                first = True
                for i in range(int(map_size)):
                    if (player_rect.y-scroll[1] + 25) > point[1]:
                        y -= tile_size
                        x = ((y - point[1]) / m) + point[0]
                        X = x
                        if x not in verticals:
                            for i in verticals:
                                if i < x:
                                    X = i

                        if (player_rect.y-scroll[1] + 25) > point[1]:
                            Ycoord = int((y + scroll[1]) / tile_size) - 1
                        if (player_rect.y-scroll[1] + 25) < point[1]:
                            Ycoord = int((y + scroll[1]) / tile_size)
                        Xcoord = int((x + scroll[0]) / tile_size)
                        if Xcoord == map_size:
                            Xcoord -= 1
                        if game_map[Ycoord][Xcoord] != "0" or (x,y) in finalpoints:
                            #pygame.draw.line(screen, (255,0,0), (x,y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)))
                            if first:
                                (H_X, H_Y) = (x,y)
                                first = False
                            break
                    if (player_rect.y-scroll[1] + 25) < point[1]:
                        y += tile_size
                        x = ((y - point[1]) / m) + point[0]
                        X = x
                        if x not in verticals:
                            for i in verticals:
                                if i < x:
                                    X = i
                        if (player_rect.y-scroll[1] + 25) > point[1]:
                            Ycoord = int((y + scroll[1]) / tile_size) - 1
                        if (player_rect.y-scroll[1] + 25) < point[1]:
                            Ycoord = int((y + scroll[1]) / tile_size)
                        Xcoord = int((X + scroll[0]) / tile_size)
                        if Xcoord == map_size:
                            Xcoord -= 1
                        if game_map[Ycoord][Xcoord] != "0" or (x,y) in finalpoints:
                            if first:
                                (H_X, H_Y) = (x,y)
                                first = False
                            #pygame.draw.line(screen, (255,0,0), (x,y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)))
                            break

            # FINDING SHORTEST

            dist_V = math.sqrt((((player_rect.y-scroll[1] + 25) - V_Y) ** 2) + (((player_rect.x-scroll[0] + 25) - V_X) ** 2))
            dist_H = math.sqrt((((player_rect.y-scroll[1] + 25) - H_Y) ** 2) + (((player_rect.x-scroll[0] + 25) - H_X) ** 2))
            if dist_H < dist_V:
                (F_X, F_Y) = (H_X,H_Y)
            else:
                (F_X, F_Y) = (V_X, V_Y)

            dist_E_V = math.sqrt((((player_rect.y-scroll[1] + 25) - V_E_Y) ** 2) + (((player_rect.x-scroll[0] + 25) - V_E_X) ** 2))
            dist_E_H = math.sqrt((((player_rect.y-scroll[1] + 25) - H_E_Y) ** 2) + (((player_rect.x-scroll[0] + 25) - H_E_X) ** 2))
            if dist_E_H < dist_E_V:
                (F_E_X, F_E_Y) = (H_E_X, H_E_Y)
            else:
                (F_E_X, F_E_Y) = (V_E_X, V_E_Y)
            #pygame.draw.line(screen , (255,0,255) , (F_X, F_Y), ((player_rect.x-scroll[0] + 25),(player_rect.y-scroll[1] + 25)))
            polycoords[point] = ((F_X,F_Y), ((F_E_X, F_E_Y)))

    polycoordslist = list(polycoords.values())
    slopelist2 = list(slopes.keys())
    polycoordslist2 = list(polycoords.keys())
    for point in slopelist2:
        if point not in polycoordslist2:
            del slopes[point]
    slopeslist = list(slopes.values())
    slopeslist.sort()
    if player_angle < (-1 * ((math.pi * 2) - HALF_FOV)) or player_angle > (-1 * HALF_FOV):
        pass

    else:
        first = True
        polypoints = []
        for slope in slopeslist:
            point = list(slopes.keys())[list(slopes.values()).index(slope)]
            if first:
                pygame.draw.circle(screen, (255,0,0), polycoords[point][0], 4)
                pygame.draw.circle(screen, (255,0,0), polycoords[point][1], 4)
                polypoints.append(polycoords[point][0])
                polypoints.append(polycoords[point][1])
                first = False
            else:
                polypoints.append(polycoords[point][0])
                polypoints.append(polycoords[point][1])
                pygame.draw.polygon(screen, (255,255,255), (polypoints[0],polypoints[1],polypoints[3],polypoints[2]))
                del polypoints[0]
                del polypoints[0]
    #print(list(slopes.keys())[list(slopes.values()).index(min(slopes.values()))])


    # EVENTS

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                moving_up = True
            if event.key == K_s:
                moving_down = True
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                moving_up = False
            if event.key == K_s:
                moving_down = False


    fps_counter()
    pygame.display.update()
    fps.tick(60)
