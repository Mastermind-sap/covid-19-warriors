import pygame
import random
import math

# initialising Pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Covid-19 warriors")
icon = pygame.image.load("cross.png")
icon = pygame.transform.scale(icon, (1000, 1000))
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background.jpg")

# Sound
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Doctor
doctorImg = pygame.image.load("doctor.png")
doctorImg = pygame.transform.scale(doctorImg, (100, 100))
doctorX = 370
doctorY = 480
doctorX_change = 0

# Corona
coronaImg = []
coronaX = []
coronaY = []
coronaY_change = []
num_of_corona = 4
for i in range(num_of_corona):
    coronaImg.append(pygame.image.load("corona.png"))
    coronaImg[i] = pygame.transform.scale(coronaImg[i], (50, 50))
    coronaX.append(random.randint(0, 750))
    coronaY.append(0)
    coronaY_change.append(+random.randint(1, 3))

# Injection
injectionImg = []
injectionX = []
injectionY = []
injection_state = []
num_of_injection = len(injectionImg)
injectionImg.append(pygame.image.load("injection.png"))
injectionImg[0] = pygame.transform.scale(injectionImg[0], (50, 50))
injectionX.append(1000)
injectionY.append(480)
injectionY_change = -2
injection_state.append("ready")

# Score

score_value = 0
dead = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 40)


def show_score(x, y):
    score = font.render("Recovered : " + str(score_value) + "\nFatalities : " + str(dead), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("KEEP SUPPORTING THE DOCTORS!", True, (255, 0, 0))
    screen.blit(over_text, (50, 250))
    # pygame.mixer.music.stop()


def isCollision(coronaX, coronaY, injectionX, injectionY):
    distance = math.sqrt(math.pow(coronaX - injectionX, 2) + (math.pow(coronaY - injectionY, 2)))
    if distance < 27:
        return True
    else:
        return False


def doctor(x, y):
    screen.blit(doctorImg, (x, y))


def corona(x, y, i):
    screen.blit(coronaImg[i], (x, y))


def fire_injection(x, y, i):
    global injection_state
    injection_state[i] = "fire"
    screen.blit(injectionImg[i], (x, y - 20))


t = 0
key_check = True
# Game loop
running = True
while running:
    # Changing background color:RGB (max=255)
    screen.fill((100, 100, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if key_check:
            # if keystroke is pressed check whether left or right
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    doctorX_change = -6
                if event.key == pygame.K_RIGHT:
                    doctorX_change = +6
                if event.key == pygame.K_SPACE:
                    for i in range(num_of_injection + 1):
                        if injection_state[i] == "ready":
                            injectionX[i] = doctorX
                            fire_injection(injectionX[i], injectionY[i], i)
                            bulletSound = pygame.mixer.Sound("laser.wav")
                            bulletSound.play()
                            break
                        elif i == num_of_injection:
                            num_of_injection += 1
                            injectionImg.append(pygame.image.load("injection.png"))
                            injectionImg[i + 1] = pygame.transform.scale(injectionImg[i + 1], (50, 50))
                            injectionX.append(1000)
                            injectionY.append(480)
                            injection_state.append("ready")
                            injectionX[i + 1] = doctorX
                            fire_injection(injectionX[i + 1], injectionY[i + 1], (i + 1))
                            bulletSound = pygame.mixer.Sound("laser.wav")
                            bulletSound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    doctorX_change = 0
    # adding boundary for the movement of doctor

    # Type 1:doctor goes from one end to other end
    # if doctorX>=800:
    #     doctorX = 0
    # elif doctorX<=0:
    #     doctorX = 800

    # Type 2:doctor goes to the original position
    # if doctorX>=800 or doctorX<=0:
    #     doctorX =370

    # Type 3:doctor cannot move
    if doctorX >= 750:
        doctorX = 750
    elif doctorX <= 0:
        doctorX = 0

    doctorX += doctorX_change
    doctor(doctorX, doctorY)

    # Corona movement
    for i in range(num_of_corona):

        # Game Over
        if (coronaY[i] > 430) and (coronaX[i] < (doctorX + 50)) and (coronaX[i] > (doctorX - 50)):
            for j in range(num_of_corona):
                coronaY[j] = 2000
            game_over_text()
            motivateSound = pygame.mixer.Sound("motivate.wav")
            motivateSound.play()
            key_check = False
            t += 1
            
            if t >= 1100:
                running = False
            break

        coronaY[i] += coronaY_change[i]
        corona(coronaX[i], coronaY[i], i)

        if coronaY[i] == 600:
            coronaY[i] = 0
            coronaX[i] = random.randint(0, 750)
            dead += 1

        # Collision
        for j in range(num_of_injection + 1):
            collision = isCollision(coronaX[i], coronaY[i], injectionX[j], injectionY[j])
            if collision:
                explosionSound = pygame.mixer.Sound("explosion.wav")
                explosionSound.play()
                injectionY[j] = 480
                injectionX[j] = 1000
                injection_state[j] = "ready"
                score_value += 1
                coronaY[i] = 0
                coronaX[i] = random.randint(0, 750)
            # Injection movement
            if injectionY[j] <= 0:
                injectionY[j] = 480
                injectionX[j] = 1000
                injection_state[j] = "ready"
            if injection_state[j] == "fire":
                fire_injection(injectionX[j], injectionY[j], j)
                injectionY[j] += injectionY_change

    show_score(textX, testY)

    pygame.display.update()
