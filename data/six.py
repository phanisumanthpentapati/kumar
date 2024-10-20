import pygame as py
import random
import time


class cricket:
    start_button = py.Rect(535, 507, 200, 60)
    startbuttoncolor = "red"
    starttextcolor = "white"

    Title_rect = py.Rect(300, 250, 700, 100)
    r = 0
    toss_button_heads = py.Rect(300, 400, 200, 60)
    toss_button_tails = py.Rect(700, 400, 200, 60)
    bat_button = py.Rect(300, 500, 200, 60)
    ball_button = py.Rect(700, 500, 200, 60)

    # Input box for overs
    input_box = py.Rect(500, 400, 200, 50)
    input_active = False
    input_text = ''


py.init()

# screen
screen = py.display.set_mode((1300, 750))
# images
bgimg = py.image.load('imagebg.jpg')
imgwd, imght = screen.get_size()
bgimg = py.transform.scale(bgimg, (imgwd, imght))
homebgimg = py.image.load("wickets images.jpg")
homebgimg = py.transform.scale(homebgimg, (imgwd, imght))

# batsman images
batsman = py.image.load("batsman-removebg-preview.png")
batsman = py.transform.scale(batsman, (70, 90))
# bowler images
bowler = py.image.load("bowler-removebg-preview.png")
bowler = py.transform.scale(bowler, (65, 80))
# ball images
ball = py.image.load("cricket-ball-vector-illustration-removebg-preview.png")
ball = py.transform.scale(ball, (10, 10))

# Coin images for heads and tails
coin_heads = py.image.load("C:/path/to/your/image/head-removebg-preview.png")
coin_heads = py.transform.scale(coin_heads, (100, 100))
coin_tails = py.image.load("C:/path/to/your/image/tails-removebg-preview.png")
coin_tails = py.transform.scale(coin_tails, (100, 100))

# fonts
startfont = py.font.SysFont("Comic Sans", 50)
smallfont = py.font.SysFont("Comic Sans", 30)

ht = 370
wd = 645

# flags
ball_click = False
toss_result = None
toss_winner = None
team_choice = None
overs_choice = None
overs_played = 0
coin_flip_anim = False
coin_side = None
flip_duration = 2000  # 2 second animation duration

# Flip interval
flip_interval = 100  # Flip every 100 milliseconds

# functions
def ballgo(ht):
    if ht != 300:
        return ht - 0.5
    else:
        return ht


def ballhit(wd):
    if wd != 100:
        return wd - 0.5
    else:
        return wd


def titleFunc():
    py.time.wait(100)
    colors = ["red", "green", "violet", "pink", "yellow", "blue", "black", "orange", 'white']
    cricket.r = (cricket.r + 1) % len(colors)
    py.draw.rect(screen, "white", cricket.Title_rect, border_radius=10)
    titleText = startfont.render("CRICKET SIMULATOR", True, colors[cricket.r])
    screen.blit(titleText, (370, 260))
    py.draw.rect(screen, cricket.startbuttoncolor, cricket.start_button, border_radius=20)
    startText = startfont.render("START", True, cricket.starttextcolor)
    screen.blit(startText, (550, 500))


def tossFunc():
    py.draw.rect(screen, "white", cricket.toss_button_heads, border_radius=10)
    headsText = smallfont.render("HEADS", True, "black")
    screen.blit(headsText, (347, 410))

    py.draw.rect(screen, "white", cricket.toss_button_tails, border_radius=10)
    tailsText = smallfont.render("TAILS", True, "black")
    screen.blit(tailsText, (750, 410))


def batOrBallFunc():
    py.draw.rect(screen, "white", cricket.bat_button, border_radius=10)
    batText = smallfont.render("BAT", True, "black")
    screen.blit(batText, (360, 515))

    py.draw.rect(screen, "white", cricket.ball_button, border_radius=10)
    ballText = smallfont.render("BOWL", True, "black")
    screen.blit(ballText, (760, 515))


def drawOversInput():
    py.draw.rect(screen, "white", cricket.input_box, border_radius=10)
    oversText = smallfont.render(cricket.input_text, True, "black")
    screen.blit(oversText, (cricket.input_box.x + 10, cricket.input_box.y + 10))

    instruction_text = smallfont.render("Enter the number of overs:", True, "black")
    screen.blit(instruction_text, (480, 350))


# Animation for coin flip
def coinFlipAnim():
    global coin_side, coin_flip_anim, toss_result
    # Alternate between heads and tails during the flip
    if py.time.get_ticks() % (flip_interval * 2) < flip_interval:
        coin_side = coin_heads
    else:
        coin_side = coin_tails

    screen.blit(coin_side, (600, 300))
    py.display.update()

    # Stop the animation after `flip_duration` and show the result
    if py.time.get_ticks() - flip_start_time >= flip_duration:
        coin_flip_anim = False
        # Final result (display the result based on toss_result)
        if toss_result == "heads":
            coin_side = coin_heads
        else:
            coin_side = coin_tails
        screen.blit(coin_side, (600, 300))
        py.display.update()
        py.time.delay(1000)  # Pause for 1 second to display the result


# states
HOME = 0
TOSS = 1
DECISION = 2
OVER_INPUT = 3
GAME = 4
state = HOME
flip_start_time = None

# mainloop
while True:
    # events
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()

        if state == HOME:
            if event.type == py.MOUSEBUTTONDOWN:
                if cricket.start_button.collidepoint(event.pos):
                    state = TOSS

        elif state == TOSS:
            if event.type == py.MOUSEBUTTONDOWN:
                if cricket.toss_button_heads.collidepoint(event.pos) or cricket.toss_button_tails.collidepoint(event.pos):
                    # Start coin flip animation
                    coin_flip_anim = True
                    flip_start_time = py.time.get_ticks()
                    toss_result = random.choice(["heads", "tails"])

        elif state == DECISION:
            if event.type == py.MOUSEBUTTONDOWN:
                if toss_winner == "Team A":
                    if cricket.bat_button.collidepoint(event.pos):
                        team_choice = "Team A chose to bat"
                        state = OVER_INPUT
                    elif cricket.ball_button.collidepoint(event.pos):
                        team_choice = "Team A chose to bowl"
                        state = OVER_INPUT
                elif toss_winner == "Team B":
                    if cricket.bat_button.collidepoint(event.pos):
                        team_choice = "Team B chose to bat"
                        state = OVER_INPUT
                    elif cricket.ball_button.collidepoint(event.pos):
                        team_choice = "Team B chose to bowl"
                        state = OVER_INPUT

        elif state == OVER_INPUT:
            if event.type == py.MOUSEBUTTONDOWN:
                if cricket.input_box.collidepoint(event.pos):
                    cricket.input_active = True
                else:
                    cricket.input_active = False

            if event.type == py.KEYDOWN:
                if cricket.input_active:
                    if event.key == py.K_RETURN:
                        try:
                            overs_choice = int(cricket.input_text)
                            state = GAME
                        except ValueError:
                            cricket.input_text = ''  # Reset input on invalid entry
                    elif event.key == py.K_BACKSPACE:
                        cricket.input_text = cricket.input_text[:-1]
                    else:
                        cricket.input_text += event.unicode

    # draw screens
    if state == HOME:
        screen.blit(homebgimg, (0, 0))
        titleFunc()

    elif state == TOSS:
        screen.fill("green")
        tossFunc()

        # Check if coin flip animation is active
        if coin_flip_anim:
            coinFlipAnim()
        else:
            # Display the final toss result after the animation
            if toss_result == "heads":
                screen.blit(coin_heads, (600, 300))
                toss_winner = "Team A"
            else:
                screen.blit(coin_tails, (600, 300))
                toss_winner = "Team B"
            state = DECISION  # Move to decision phase

    elif state == DECISION:
        screen.fill("lightblue")
        decision_text = f"{toss_winner} won the toss"
        decision_render = smallfont.render(decision_text, True, "black")
        screen.blit(decision_render, (400, 350))
        batOrBallFunc()

    elif state == OVER_INPUT:
        screen.fill("lightyellow")
        drawOversInput()

    elif state == GAME:
        screen.blit(bgimg, (0, 0))
        screen.blit(batsman, (615, 265))
        screen.blit(bowler, (615, 360))
        if ball_click:
            ht = ballgo(ht)

            if ht == 300:
                wd = ballhit(wd)
            screen.blit(ball, (wd, ht))
        screen.blit(batsman, (80, 290))

        # Display overs and team choice
        overs_text = smallfont.render(f"Overs: {overs_choice}", True, "black")
        screen.blit(overs_text, (50, 50))

        team_choice_text = smallfont.render(f"{team_choice}", True, "black")
        screen.blit(team_choice_text, (50, 100))

    py.display.update()

py.quit()
