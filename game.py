import pygame
import base
import bird
import pipe


pygame.init()
WIDTH, HEIGHT = 288, 512
BG_IMG = pygame.image.load('assets/bg.png')
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
VELOCITY = -2
THRESHOLDS = {
    'base': -337,
    'pipe': 72
}
FONT = pygame.font.SysFont("Arial", 12)


def main():
    b = bird.Bird()
    first_base = base.Base(0, VELOCITY)
    bases = [first_base]
    first_pipe = pipe.Pipe(512, VELOCITY)
    pipes = [first_pipe]
    framecounter = 0
    score = 0
    distance = 0
    flag = 0
    activate = False

    clock = pygame.time.Clock()
    run = 1

    # main loop
    while run:

        # Pipes and bases spawning
        if pipes[-1].x < THRESHOLDS['pipe']:
            pipes.append(pipe.Pipe(288, VELOCITY))
        elif pipes[0].x + pipes[0].sprite1.get_width() < 0:
            flag = 0
            pipes.pop(0)
        if bases[-1].x < 0:
            bases.append(base.Base(bases[-1].x + bases[-1].sprite.get_width(), VELOCITY))
        elif bases[0].x < THRESHOLDS['base']:
            bases.pop(0)

        # Score/distance count
        if flag == 0:
            if pipes[0].x < 144:
                score += 1
                flag = 1
        distance -= VELOCITY / 10

        # Updating and drawing
        SCREEN.blit(BG_IMG, (0, 0))
        b.update()
        b.draw(SCREEN)
        for p in pipes:
            p.update()
            p.draw(SCREEN)
        for bs in bases:
            bs.update()
            bs.draw(SCREEN)
        scr = FONT.render('Score : ' + str(score), True, (0, 0, 0))
        dist = FONT.render('Distance : ' + str(round(distance)), True, (0, 0, 0))
        SCREEN.blit(scr, (0, 0))
        SCREEN.blit(dist, (0, 15))

        # Animation
        if framecounter > 12:
            framecounter = 0
            b.img_count = 0
        if framecounter > 9:
            b.img_count = 1
        elif framecounter > 6:
            b.img_count = 2
        elif framecounter > 3:
            b.img_count = 1
        framecounter += 1

        # Update display
        pygame.display.flip()

        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b.jump()
                if event.key == pygame.K_d:
                    activate = not activate
                if event.key == pygame.K_ESCAPE:
                    run = 0

        # Collision detection
        for p in pipes:
            if p.collide(b):
                run = 0
        if b.rect.bottom > 400 or b.y < -50:
            run = 0

        # Clock tick
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()