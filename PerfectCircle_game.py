import pygame
import math

# initialize pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Draw a Circle")

# set up the font
font = pygame.font.SysFont(None, 30)

# set up the colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up the variables
score = 0
best_score = 0
ideal_radius = 200
ideal_area = math.pi * ideal_radius ** 2
distance = 0
last_mouse_pos = None
last_click_time = None
max_click_interval = 0.5  # seconds
min_distance_to_point = 20  # pixels
color = GREEN

# set up the game loop
running = True
while running:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get the mouse position
    mouse_pos = pygame.mouse.get_pos()

    # check if the mouse button is pressed
    if pygame.mouse.get_pressed()[0]:
        # calculate the distance from the center of the screen to the mouse position
        distance = math.sqrt((mouse_pos[0] - 250) ** 2 + (mouse_pos[1] - 250) ** 2)

        # check if the mouse is too close to the circle's edge
        if distance >= ideal_radius - 10:
            color = RED
        else:
            color = GREEN

        # calculate the area of the drawn circle
        area = math.pi * distance ** 2

        # calculate the percentage difference between the drawn circle and the ideal circle
        percentage_difference = abs(ideal_area - area) / ideal_area * 100
        percentage_similarity = 100 - percentage_difference
        score = int(percentage_similarity)

        # check if the score is higher than the best score
        if score > best_score:
            best_score = score

        # check if the mouse is too close to a point
        if last_mouse_pos is not None:
            distance_to_point = math.sqrt((mouse_pos[0] - last_mouse_pos[0]) ** 2 +
                                          (mouse_pos[1] - last_mouse_pos[1]) ** 2)
            if distance_to_point < min_distance_to_point:
                color = RED

        # check if the mouse is moving too slowly
        if last_click_time is not None:
            elapsed_time = pygame.time.get_ticks() - last_click_time
            elapsed_distance = ((mouse_pos[0] - last_mouse_pos[0]) ** 2 +
                                (mouse_pos[1] - last_mouse_pos[1]) ** 2) ** 0.5
            if elapsed_time > 0:
                velocity = elapsed_distance / elapsed_time
            else:
                velocity = 0

            #velocity = elapsed_distance / elapsed_time
            if velocity < 100:
                color = RED

        # update the last mouse position and click time
        last_mouse_pos = mouse_pos
        last_click_time = pygame.time.get_ticks()

    # draw the screen
    screen.fill(WHITE)
    pygame.draw.circle(screen, color, mouse_pos, 10, 10)
    pygame.draw.circle(screen, BLACK, (250, 250), ideal_radius, 1)
    score_text = font.render("Score: {}%".format(score), True, BLACK)
    best_score_text = font.render("Best Score: {}%".format(best_score), True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(best_score_text, (10, 40))
    pygame.display.update()

# quit pygame
pygame.quit()
