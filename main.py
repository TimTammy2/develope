import pygame
import pymunk
import sys
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Volleyball Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (65, 66, 66)

# Constants
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
BALL_RADIUS = 10
FPS = 60
GRAVITY = 0.5
JUMP_HEIGHT = 15

# Scores
score_left = 0
score_right = 0

# Setup Pymunk
space = pymunk.Space()
space.gravity = (0, 500)

# Create the floor
floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_shape = pymunk.Segment(floor_body, (0, 600), (1200, 600), 5)
floor_shape.elasticity = 1.0
floor_shape.collision_type = 3  # Set collision type for floor
space.add(floor_body, floor_shape)

# Create the net
net_body = pymunk.Body(body_type=pymunk.Body.STATIC)
net_shape = pymunk.Segment(net_body, (590, 450), (590, 600), 20)
net_shape.elasticity = 0.5
space.add(net_body, net_shape)

# Create the walls
left_wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
left_wall_shape = pymunk.Segment(left_wall_body, (0, 0), (0, 600), 5)
left_wall_shape.elasticity = 1.0
space.add(left_wall_body, left_wall_shape)

right_wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
right_wall_shape = pymunk.Segment(right_wall_body, (1200, 0), (1200, 600), 5)
right_wall_shape.elasticity = 1.0
space.add(right_wall_body, right_wall_shape)

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, is_left):
        super().__init__()
        self.x = x
        self.y = y
        self.is_left = is_left
        self.jump = False
        self.vel_y = 0
        self.direction = 0

        # Create dynamic body rectangle             
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (PLAYER_WIDTH, PLAYER_HEIGHT)))
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.shape.elasticity = 0.5
        self.shape.friction = 0.5
        self.shape.collision_type = 2  # Set collision type for player
        space.add(self.body, self.shape)

    def update(self, keys, left, right, jump):
        dx = 0
        if keys[left]:
            dx = -6
            self.direction = -1
        if keys[right]:
            dx = 6
            self.direction = 1
        if keys[jump] and not self.jump:
            self.vel_y = -JUMP_HEIGHT
            self.jump = True

        self.vel_y += GRAVITY
        dy = self.vel_y
        if self.y + dy >= 543:
            dy = 543 - self.y
            self.jump = False

        self.x += dx
        self.y += dy

        if self.is_left:
            self.x = max(10, min(560, self.x))
        else:  # Boundary check for player 2
            self.x = max(620, min(1170, self.x))

        # Update the dynamic body's position
        self.body.position = self.x, self.y

    def draw(self, screen):
        if self.jump:
            if self.is_left:
                drawP1Jumping(screen, self.x, self.y)
            else:
                drawP2Jumping(screen, self.x, self.y)
        else:
            drawStanding(screen, self.x, self.y)

# Define Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_RADIUS))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, BALL_RADIUS)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = 1  # Set collision type for ball
        space.add(self.body, self.shape)

    # def update(self):
    #     pass  # No need for pygame rect update since we're using Pymunk

    def draw(self, screen):
        x, y = self.body.position
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), BALL_RADIUS)

# Drawing functions for players
def drawP1Jumping(screen, x, y):
    pygame.draw.ellipse(screen, BLACK, [0 + x, 0 + y, 20, 20], 0)
    pygame.draw.line(screen, BLACK, [x + 14, 36 + y], [10 + x, 14 + y], 3)
    pygame.draw.line(screen, BLACK, [x + 9, y + 22], [x - 3, y + 19], 3)
    pygame.draw.line(screen, BLACK, [x - 3, y + 19], [x - 6, y + 3], 3)
    pygame.draw.line(screen, BLACK, [x + 9, y + 22], [x + 26, y + 25], 3)
    pygame.draw.line(screen, BLACK, [x + 13, 36 + y], [x + 4, y + 54], 3)
    pygame.draw.line(screen, BLACK, [x + 13, 36 + y], [x + 22, y + 38], 3)
    pygame.draw.line(screen, BLACK, [x + 22, y + 38], [x + 16, y + 50], 3)

def drawP2Jumping(screen, x, y):
    pygame.draw.ellipse(screen, BLACK, [x + 0, 0 + y, 20, 20], 0)
    pygame.draw.line(screen, BLACK, [x + 6, 36 + y], [x + 10, 14 + y], 3)
    pygame.draw.line(screen, BLACK, [x + 11, y + 22], [x + 23, y + 19], 3)
    pygame.draw.line(screen, BLACK, [x + 23, y + 19], [x + 26, y + 3], 3)
    pygame.draw.line(screen, BLACK, [x + 11, y + 22], [x - 6, y + 25], 3)
    pygame.draw.line(screen, BLACK, [x + 7, 36 + y], [x + 16, y + 54], 3)
    pygame.draw.line(screen, BLACK, [x + 7, 36 + y], [x - 2, y + 38], 3)
    pygame.draw.line(screen, BLACK, [x - 2, y + 38], [x + 4, y + 50], 3)

def drawStanding(screen, x, y):
    pygame.draw.ellipse(screen, BLACK, [0 + x, 0 + y, 20, 20], 0)
    pygame.draw.line(screen, BLACK, [9 + x, 34 + y], [9 + x, 14 + y], 3)
    pygame.draw.line(screen, BLACK, [9 + x, 34 + y], [19 + x, 54 + y], 3)
    pygame.draw.line(screen, BLACK, [9 + x, 34 + y], [-1 + x, 54 + y], 3)
    pygame.draw.line(screen, BLACK, [9 + x, 14 + y], [17 + x, 34 + y], 3)
    pygame.draw.line(screen, BLACK, [9 + x, 14 + y], [1 + x, 34 + y], 3)

# Create player instances
player1 = Player(200, 543, is_left=True)
player2 = Player(1000, 543, is_left=False)

players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

ball = Ball(600, 200)

# Collision handler for ball and player
def ball_player_collision(arbiter, space, data):
    ball_shape = arbiter.shapes[0]
    player_shape = arbiter.shapes[1]
    player_body = player_shape.body

    if player_body.position.x < 600:
        ball_shape.body.velocity = (600, -300)  # Send ball to the right
    else:
        ball_shape.body.velocity = (-600, -300)  # Send ball to the left

    return True

# Add collision handler for ball and player
handler = space.add_collision_handler(1, 2)
handler.begin = ball_player_collision

# Add collision handler for ball and floor
def ball_floor_collision(arbiter, space, data):
    global score_left, score_right
    ball_position = arbiter.shapes[0].body.position
    if ball_position.x < 590:  # Left side of the net
        score_right += 1
    else:  # Right side of the net
        score_left += 1
    # Reset ball position
    ball.body.position = (600, 200)
    ball.body.velocity = (0, 0)
    return True

floor_handler = space.add_collision_handler(1, 3)
floor_handler.begin = ball_floor_collision

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player1.update(keys, pygame.K_a, pygame.K_d, pygame.K_w)
    player2.update(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)

    space.step(1 / FPS)

    # Drawing
    screen.fill((79, 220, 255))
    pygame.draw.rect(screen, GREY, (590, 450, 20, 150))
    for player in players:
        player.draw(screen)
    ball.draw(screen)

    # Draw scoreboard
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{score_left} - {score_right}", True, BLACK)
    screen.blit(score_text, (550, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

