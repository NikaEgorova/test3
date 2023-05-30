import sys
import cfg
import pygame
import modules.Levels as Levels
import time


'''Начать определенный уровень'''
def startLevelGame(level, screen, font):
    clock = pygame.time.Clock() #створення "годинника",який допоможу відслідковувати час
    SCORE = 0 # змінна з рахунком
    q_pressed = 0
    wall_sprites = level.setupWalls(cfg.SKYBLUE)# фукнція setupWalls прописана у Levels, вона створює стіни, передається лише колір 
    gate_sprites = level.setupGate(cfg.WHITE)# фукнція setupGate прописана у Levels, вона створює ворота, передається лише колір 
    hero_sprites, ghost_sprites = level.setupPlayers(cfg.HEROPATH, [cfg.BlinkyPATH, cfg.ClydePATH, cfg.InkyPATH, cfg.PinkyPATH])# створення спрайтів'''
    food_sprites = level.setupFood(cfg.YELLOW, cfg.WHITE)# створення їжі
    redfood_sprites = level.setupRedFood(cfg.RED,cfg.YELLOW, cfg.WHITE)#створення червоної їжі
    is_clearance = False # виграв/ не виграв
    while True:    
        redcherry = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.changeSpeed([cfg.sple, 0])
                        hero.is_move = True
                        cfg.direc = 'l'
                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.changeSpeed([cfg.spri, 0])
                        hero.is_move = True
                        cfg.direc = 'r'
                elif event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.changeSpeed([0,cfg.spup])
                        hero.is_move = True
                        cfg.direc = 'u'
                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, cfg.spdown])
                        hero.is_move = True
                        cfg.direc = 'd'
                elif event.key == pygame.K_q:
                    if q_pressed < 3:
                        q_pressed += 1
                        if hero.is_move == False:
                            if cfg.direc == 'r':
                                hero.rect.x = hero.rect.x + 60
                            elif cfg.direc == 'l':
                                hero.rect.x = hero.rect.x - 60
                            elif cfg.direc == 'u':
                                hero.rect.y = hero.rect.y - 60
                            elif cfg.direc == 'd':
                                hero.rect.y = hero.rect.y + 60
                        else:
                            if cfg.direc == 'r':
                                hero.rect.x = hero.rect.x + 30
                            elif cfg.direc == 'l':
                                hero.rect.x = hero.rect.x - 30
                            elif cfg.direc == 'u':
                                hero.rect.y = hero.rect.y - 30
                            elif cfg.direc == 'd':
                                hero.rect.y = hero.rect.y + 30
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    hero.is_move = False
        screen.fill(cfg.BLACK) #заливка бекграунду
        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites,1)# оновлення позиція гравця   
        hero_sprites.draw(screen)# намалювати плеєра
        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)# якщо гравець і монета зіткнулись, монета зникає
            redfood_eaten = pygame.sprite.spritecollide(hero,redfood_sprites,True)
            if  len(redfood_eaten)> 0:
                cherrytime = 0
                redfood_eaten.clear()
                while cherrytime < 10000:
                    redcherry = True
                    cherrytime += 1
        SCORE += len(food_eaten)# а до рахунку прибавляється 1
        wall_sprites.draw(screen)# намалювати стіни
        gate_sprites.draw(screen)# намалювати ворота
        food_sprites.draw(screen)# намалювати їжу
        redfood_sprites.draw(screen)
        for ghost in ghost_sprites:
            # Случайное движение призраков (плохой эффект и ОШИБКА)
            '''
            res = ghost.update(wall_sprites, None)
            while not res:
                ghost.changeSpeed(ghost.randomDirection())
                res = ghost.update(wall_sprites, None)
            '''
            # Укажите путь призрака
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc0 = ghost.tracks_loc[0] + 1
                elif ghost.role_name == 'Clyde':
                    loc0 = 2
                else:
                    loc0 = 0
                ghost.changeSpeed(ghost.tracks[loc0][0: 2])
            ghost.update(wall_sprites, None,0)
        ghost_sprites.draw(screen)
        score_text = font.render("Score: %s" % SCORE, True, cfg.RED)
        screen.blit(score_text, [10, 10])
        if len(food_sprites) == 0:
            is_clearance = True
            break
        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            print(redcherry)
            if redcherry == False:
                is_clearance = False
                break
        pygame.display.flip()
        clock.tick(10)
    return is_clearance


'''Показать текст'''
def showText(screen, font, is_clearance, flag=False):
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'# або текст геймовер або перемога
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]#або тут або там
    surface = pygame.Surface((400, 200))# якесь поле
    surface.set_alpha(10)# прозрачність
    surface.fill((128, 128, 128))# заливка кольором
    screen.blit(surface, (100, 200))# відобразити сюрфейс на екрані
    texts = [font.render(msg, True, cfg.WHITE),
            font.render('Press ENTER to continue or play again.', True, cfg.WHITE),
            font.render('Press ESCAPE to quit.', True, cfg.WHITE)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            main(initialize())
                    else:
                        main(initialize())
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


'''инициализация'''
def initialize():
    pygame.init()
    icon_image = pygame.image.load(cfg.ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pacman')
    return screen


'''Основная функция'''
def main(screen):
    #pygame.mixer.init()
    #pygame.mixer.music.load(cfg.BGMPATH)
    #pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(cfg.FONTPATH, 18)
    font_big = pygame.font.Font(cfg.FONTPATH, 24)
    for num_level in range(1, Levels.NUMLEVELS+1):
        level = getattr(Levels, f'Level{num_level}')()
        is_clearance = startLevelGame(level, screen, font_small)
        if num_level == Levels.NUMLEVELS:
            showText(screen, font_big, is_clearance, True)
        else:
            showText(screen, font_big, is_clearance)


'''run'''
if __name__ == '__main__':
    main(initialize())
