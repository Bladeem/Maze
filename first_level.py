import sys

import pygame

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
cell_size = 50
world_width = len(world_data[0])
world_height = len(world_data)
WALL_IMAGE = pygame.image.load("dirt.png")
WALL_IMAGE = pygame.transform.scale(WALL_IMAGE, (cell_size, cell_size))
PATH_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)

player_x = 1
player_y = 1
player_speed = 1
player_image = pygame.image.load("mario.png")
player_image = pygame.transform.scale(player_image, (cell_size, cell_size))
player_rect = player_image.get_rect()

pygame.init()

screen = pygame.display.set_mode((world_width * cell_size, world_height * cell_size))

monster_x = 3
monster_y = 8
monster_speed = 1
monster_direction = "right"
monster_image = pygame.image.load("rabbit.png")
monster_image = pygame.transform.scale(monster_image, (50, 50))
monster_rect = monster_image.get_rect()

gold_list = [(2, 3), (4, 7), (7, 3)]
gold_score = 0
gold_image = pygame.image.load("coin.png")
gold_image = pygame.transform.scale(gold_image, (cell_size/1.5, cell_size/2))

winning_cell = (8, 5)

running = True
game_over = False
game_won = False

MONSTER_MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MONSTER_MOVE_EVENT, 500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and world_data[player_y][player_x - 1] == 0:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT and world_data[player_y][player_x + 1] == 0:
                player_x += player_speed
            elif event.key == pygame.K_UP and world_data[player_y - 1][player_x] == 0:
                player_y -= player_speed
            elif event.key == pygame.K_DOWN and world_data[player_y + 1][player_x] == 0:
                player_y += player_speed
        elif event.type == MONSTER_MOVE_EVENT:
            if monster_direction == "right":
                if world_data[monster_y][monster_x + 1] == 0:
                    monster_x += 1
                else:
                    monster_direction = "left"
        #    elif monster_direction == "down":
        #        if world_data[monster_y + 1][monster_x] == 0:
        #            monster_y += monster_speed
        #        else:
        #            monster_direction = "left"
            elif monster_direction == "left":
                if world_data[monster_y][monster_x - 1] == 0:
                    monster_x -= 1
                else:
                    monster_direction = "right"
         #   elif monster_direction == "up":
         #       if world_data[monster_y - 1][monster_x] == 0:
         #           monster_y -= monster_speed
         #       else:
         #           monster_direction = "right"

    if (player_x, player_y) in gold_list:
        gold_list.remove((player_x, player_y))
        gold_score += 1

    if player_x == monster_x and player_y == monster_y:
        game_over = True
    if (player_x, player_y) == winning_cell:
        game_won = True


   # screen.fill((0, 0, 0))
    screen.blit(player_image, (50, 50))
    screen.blit(monster_image, (50, 50))

    for row in range(world_height):
        for col in range(world_width):
            cell_value = world_data[row][col]
            if cell_value == 1:
                screen.blit(WALL_IMAGE, (col * cell_size, row * cell_size))
            else:
                pygame.draw.rect(screen, PATH_COLOR, (col * cell_size, row * cell_size, cell_size, cell_size))

    player_rect.topleft = (player_x * cell_size, player_y * cell_size)
    screen.blit(player_image, player_rect)
  #  pygame.draw.rect(screen, (0, 255, 0), (monster_x * cell_size, monster_y * cell_size, cell_size, cell_size))

    monster_rect = (monster_x * cell_size, monster_y * cell_size)
    screen.blit(monster_image, monster_rect)
    pygame.draw.circle(screen, (0, 0, 255 ),
                       (winning_cell[0] * cell_size + cell_size // 2, winning_cell[1] * cell_size + cell_size // 2),
                       cell_size // 5)

    if game_over:
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Oyun Bitti Canavara Yakalandınız!!", True, (255, 0, 0))
        screen.blit(game_over_text, (50, world_height * cell_size // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()
    if game_won:
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Tebrikler Oyunu Kazandınız...", True, (0, 255, 0))
        screen.blit(game_over_text, (50, world_height * cell_size // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    for gold in gold_list:
        screen.blit(gold_image, (gold[0] * cell_size + 8, gold[1] * cell_size + 15))

  #  for gold in collected_gold:
  #      pygame.draw.circle(screen, (0, 255, 0),
  #                          (gold[0] * cell_size + cell_size // 2, gold[1] * cell_size + cell_size // 2),
  #                          cell_size // 3)

    font = pygame.font.Font(None, 36)
    gold_score_text = font.render(f"Skor: {gold_score}", True, (255, 255, 255))
    screen.blit(gold_score_text, (10, 10))

    pygame.display.update()

pygame.quit()
