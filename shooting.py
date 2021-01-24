import pygame
import sys
import random
from time import sleep

padWidth = 480
padHeight = 640
rockImage = ['rock01.png','rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
             'rock06.png', 'rock07.png','rock08.png', 'rock09.png', 'rock10.png', \
             'rock11.png','rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
             'rock16.png','rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
             'rock21.png','rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
             'rock26.png','rock27.png', 'rock28.png', 'rock29.png', 'rock30.png']
explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']

def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text,(10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('놓친 운석 수:' + str(count), True, (255, 0, 0))
    gamePad.blit(text,(350,0))

# 게임 메세지 출력
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('NanumGothic.ttf',80)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()       #베경 음악 정지
    gameOverSound.play()            #게임 오버 사운드 재생s
    sleep(2)
    pygame.mixer.music.play(-1)     #배경 음악 재생
    runGame()

# 전투기가 운석과 충돌했을떄 메세지 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')

# 게임 오버 메시지 보이기
def gameOver():
    global gamePad
    writeMessage('게임 오버!')

#게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
# 게임 초기화
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')            # 게임 이름
    background = pygame.image.load('background.png')    # 배경 그림
    fighter = pygame.image.load('fighter.png')          # 전투기 그림
    missile = pygame.image.load('missile.png')          # 미사일 그림
    explosion = pygame.image.load('explosion.png')      # 폭발 그림
    pygame.mixer.music.load('music.wav')                # 배경 음악
    pygame.mixer.music.play(-1)                         # 배경음악 재생
    missileSound = pygame.mixer.Sound('missile.wav')    # 미사일 사운드
    gameOverSound = pygame.mixer.Sound('gameover.wav')  # 게임 오버 사운드
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound

    # 전투기 미사일에 운석이 맞았을 경우 TRUE
    isShot = False
    shotCount = 0
    rockPassed = 0
    
    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치 (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX= 0

    # 무기 좌표 리스트
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 운석 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: # 게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:      # 전투기 왼쪽으로 이동
                    fighterX -= 5
                    
                elif event.key == pygame.K_RIGHT:   # 전투기 오른쪽으로 이동
                    fighterX += 5

                elif event.key == pygame.K_SPACE:   # 미사일 발사
                    missileSound.play()             # 미사일 사운드
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:    # 방향기를 때면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                        
        drawObject(background, 0, 0)

        # 전투기 위치 조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()
                
            
        drawObject(fighter, x, y)

    
        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):     # 미사일 요소에 대해 반복함
                bxy[1] -= 10                        # 총알의 y좌표 - 10 (위로 이동)
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:                     # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy)       # 미사일 제거
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        rockY += rockSpeed                          # 운석 아래로 움직임

        # 운석 맞춘 점수 표시
        writeScore(shotCount)
        
        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        # 놓친 운석 수 표시
        writePassed(rockPassed)

        if rockPassed == 3:
            gameOver()          #운석 3개 놓치면 게임오버
            
        # 운석을 맞춘 경우
        if isShot:
            #운석 폭발
            drawObject(explosion, rockX, rockY)     # 운석 폭발 그림 출력
            destroySound.play()                     # 운석 폭발 사운드
            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            #운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10
            
        drawObject(rock, rockX, rockY)              # 운석 그리기

        pygame.display.update()                     # 게임화면을 다시그림

        clock.tick(60)

    pygame.quit()

initGame()
runGame()
