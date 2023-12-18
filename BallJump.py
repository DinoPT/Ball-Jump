#Lecture 2
from codecs import backslashreplace_errors
from platform import platform
from select import select
from threading import Timer
from pygame import mixer
import pygame
import random
import math
#import PyParticles

#Global variables

#Gravity Definition (Global Variable)
gravity = (math.pi, 0.002)

#Variables for the defined colours
black = (0,0,0) 
white = (255,255,255)
#This is to control the amount of loops per second that the game will run at to 60 
fps = 60

#Boolean variable responsible to check if the player is still jumping (True) or falling (False)
jump=False

#variables that are used to store changed values of x and y coordinates, later used for the calculation of player's coordinates in functions
y_change = 0
x_change = 0

#Number of platforms the game should produce
num_platforms = 10

#Number of particles created for the space background
space_particles = []

#maximum value for the x coordinates generated to create platforms
max_x = 500

#maximum value for the y coordinates generated to create platforms
max_y = 600

#y coordinate referencing the middle of the screen
screen_centre = 250

#Dimensions of the rectangle platforms generated
rect_width = 150
rect_height = 10

#Array that store the coordinates for the creation of platforms
coordinates = []

#Actual list of the rectangle platforms
platforms = []

#Indications for the creation of the player's character
player_size = 30
player_x = 170
player_y = 400

#Functions
#Calculates the resultant position when two forces are applied to a particle.
    #In this case - gravity and directional force.
def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    #Hypotenuse joins the two forces together.
    length = math.hypot(x,y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return(angle, length)

#Locate the particle next to the mouse click
def findParticle(particles, x, y):
    if math.hypot(particles.x-x, particles.y-y) <= particles.size:
        return particles

#Prints background stars/particles
def Background_print():    
    p1 = SpaceParticle((150, 50), 15)
    p1.display()

#This function is responsible for appending to the player it's physics and the display on the game
def PlayerCreate():
    player.display()

def SpaceCreate():
#Creates several random particles from the class "SpaceParticle" for our background, resembling stars in space
    num_space_particles = 200
    for n in range(num_space_particles):
        size = random.randint(1,4)
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)

        #Give Particles random speed and direction
        star = SpaceParticle((x,y),size)
        star.speed = random.random()/10
        star.angle = random.uniform(0,math.pi*2)
        space_particles.append(star)

def CoordinatesGenerator():
    #our first entry in the list will always be a predeterminated platform so the player doesn't just fall out of bounds.
    #Parameters           x           y              w            h
    coordinates.append([player.x-50, player.y + 100, rect_width, rect_height])
    for i in range (num_platforms):
        #Array that store the coordinates for the creation of platforms
        #Since to draw a platform pygame needs 4 coordinates, we are inputing that the top left corner should be in x=145, y=480 and that it should be width = 150 and height = 10
        #                       x                            y                 w            h
        coordinates.append([random.randint(0,max_x),random.randint(0,max_y),rect_width,rect_height])

def DrawPlatforms():
#THE ERROR WITH THIS IS THAT THE COORDINATES ARE SUBDIVIDED INTO OTHER ENTRIES INSTEAD OF HAVING THE COMPLETE INFORMATION BEING INTRODUCED
    for i in range(len(coordinates)):
        #draws the platforms generated
        #edge width (ew) and border radius (br) parameters only added to make platforms more rounder and nor fully filled with colour for cosmetic reasons
        #                                    
        #                                                            ew  br
        rect_platform = pygame.draw.rect(screen,white,coordinates[i], 1, 2)
        #Add each platform to the list
        platforms.append(rect_platform)

def StarBehaviour():
    for star in space_particles:
        star.move()
        star.display()
        star.bounce()

def BackgroundMusic():

    #Initializes the mixer that will manage the music being played in the level.
    mixer.init()

    #Load audio file
    mixer.music.load('Music\catinspace_hq.mp3')

    print("music started playing....")

    #Set preferred volume
    mixer.music.set_volume(0.2)

    #Play the music, using -1 as a parameter to loop the track
    mixer.music.play(-1)

#Checks player's and platform's position and when to execute a jump
def jumping(y_pos): #put (self,y_pos)  otherwise
    #Preset value of how far the player can jump
    jump_height = 9
    #referencing both global variables declared above
    global jump
    global y_change
    gravity_jump = 0.2

    if jump:
        y_change = -jump_height 
        jump = False

    y_pos += y_change #y_pos += y_change
    y_change += gravity_jump
    return y_pos

#checks for collisions with platforms
def checkCollisions(rect_platforms, j, p):
    #Calling the global variables "player_x" and "player_y" declared above into the function
    
    #Tells us the direction of the player and controls how much moviment is done per frame
    #if y_change as a negative value, we are executing a "up" moviment, while if it is positive we are going "down" on the screen
    global y_change
    for i in range(len(rect_platforms)):
        #pygame's built-in rectangle collision detect tool, checks if any points that overlap between 2 defined rectangles
        if rect_platforms[i].colliderect([p.x, p.y + 24.5, 30 ,10]) and jump == False and y_change > 0:
            j = True
    return j

#A loss condition if the player falls off the platforms and out of bounds.
def GameOver():
    #checks if the player has a y coordinate higher than the max screen height, meaning out of the screen
    if player.y >600:
        print("You fell and lost the game.")
        running = False
        pygame.quit()

#handles the positioning of platforms as the player progresses and his y coordinate changes into more negative values (character goes higher on screen)
def update_platforms(coordinates, y_pos, y_change):
    #CoordinatesGenerator() #to re-generate more platforms
    if y_pos < screen_centre and y_change < 0:
        #going through all of the platforms editing their y value
        for i in range(len(coordinates)):
            coordinates[i][i] -= y_change
        else: #just to get out of this loop
            pass
    
    for i in range(len(coordinates)):
        if coordinates[i][i] < 500:
           coordinates[i] = [random.randint(0,max_x),random.randint(0,max_y),rect_width,rect_height]
    return coordinates

#Classes
#Creating a Class: Creating a class for an object means it can be edited later
class SpaceParticle:
    #Defines the attribute "elasticity" that we will use for bounce
    elasticity = 0.75
    #Fucntions passed to the object
    def __init__(self, coords, size):
        x,y = coords 
        self.x = x
        self.y = y
        self.size = size 
        self.colour = (random.randint(10,255), random.randint(10,255), random.randint(10,255))
        self.thickness = 0
        self.speed = 0.1
        self.angle = 0
    #Display function: takes arguments and draws a circle

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
    
    #This function is used in thus class to prevent that the background particles will move out of screen,
    #instead bouncing and changing directory while maintaining it's momentum
    def bounce(self):
        #East Coast:
        if self.x > width - self.size:
            #Implements elasticity to reduce speed on bounce
            self.speed *= self.elasticity
            self.x = width - self.size
            self.angle = -self.angle
        #West Coast:
        elif self.x < self.size:
            self.speed *= self.elasticity
            #Sticks to the wall
            self.x = self.size
            #Reverses the angle
            self.angle = -self.angle
        #Deep South:
        elif self.y > height - self.size:
            self.speed *= self.elasticity
            self.y = height - self.size
            self.angle = math.pi - self.angle
        #North
        elif self.y < self.size:
            self.speed *= self.elasticity
            self.y = self.size
            self.angle = math.pi - self.angle


#Creating a Class: Creating a class for an object means it can be edited later
class Particle:
    #Defines Drag and Elasticity
    drag = 0.999
    elasticity = 0.75

    #Fucntions passed to the object
    def __init__(self, coords, size):
        x,y = coords 
        self.x = x
        self.y = y
        self.size = size 
        self.colour = (random.randint(10,255), random.randint(10,255), random.randint(10,255))
        self.thickness = 0
        #Moviments speed when the player controls it
        self.MovimentSpeed = 3
        #Speed as a dragged particle
        self.ParticleSpeed = 0.1
        self.angle = 0
    #Display function: takes arguments and draws a circle
    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

#Screen init
background_colour = black
(width, height) = (500, 600)
#background = pygame.image.load(image_file)
#background = pygame.transform.scale(background, (width,height))
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Ball Jump')
screen.fill(background_colour)

#Creates the variable player using the class Particle and assigns value to the particle speed and angle
player = Particle((player_x,player_y),player_size)
player.ParticleSpeed = random.random()/2
player.angle = random.uniform(0,math.pi*2)

#player = PyParticles.Environment

#Uses the Space Particles class to draw stars that bounce all around in the background
SpaceCreate()

#Plays music infinitely while the game is running
BackgroundMusic()

#Calls the functions that generates random values to coordinates and populates the array which stores them
CoordinatesGenerator()

#Prints out the game objects
Background_print()

#pygame.draw.circle(screen, (255,0,150), (150,50), 35, 7)

#Prints screen
pygame.display.flip()


#Game Loop
running = True
grab_player = None
##Initialises relative X and Y to 0
relativeX, relativeY = (0,0)

while running:
    #This function in pygame will make so that the segment it is placed on will never run more that x frames per second
    #as such putting it on the game run loop with 60, will make our game have the maximum frame rate of 60 per second.
    pygame.time.Clock().tick(fps)

    screen.fill(background_colour)

    #Assigns the behaviours such as move and bounce to the star particles
    StarBehaviour()

    #Draws the platforms created on the screen
    DrawPlatforms()
        
    #player and the physics attributed to it being initialized    
    PlayerCreate()

    #This keeps updating players "y" coordinates which determines how high he is in our game, it will keep making sure jump keeps getting triggered and our player going higher or lower when appropriate
    player.y = jumping(player.y)

    #platforms = update_platforms(coordinates, player.y, y_change)

    #This keeps updating the player's x axis, meaning it is responsible for the constant left and right moviment
    player.x += x_change
    #Will output if true or false depending if it made a collision with a platform, in the case it didn't jump will be de-activated making the player fall out of bounds and lose the game
    jump = checkCollisions(platforms, jump, player)

    #Game Loop
    pygame.display.flip()
    for event in pygame.event.get():
        #Player horizontal moviment using the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -player.MovimentSpeed
            if event.key == pygame.K_RIGHT:
                x_change = player.MovimentSpeed
        
        #Once the key is release it will stop all moviment
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = 0

        #Gets the mouse position
        #Calls the find particle function
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = event.pos 
            #Changes the clicked particle to be selected  
            grab_player = findParticle(player, mouseX, mouseY)
            #grab_particle.colour = (255, 255, 255)
        


        #needs fixing
        #Change the colour of the player
        if event.type == pygame.K_TAB:
            player.colour = (random.randint(10,255), random.randint(10,255), random.randint(10,255))

    #Releases the particle when the mouse is released

    #Any of the grab code needs to be outside the event.get() otherwise it will only grab when there is an event such as clicking or moving


    if event.type == pygame.MOUSEBUTTONUP:
            
        if grab_player:
        #Applies relative force to the selected particle when moved
            grab_player.angle = math.atan2(relativeY, relativeX) + 0.5*math.pi
            grab_player.speed = math.hypot(relativeX, relativeY) * 0.1
        grab_player = None

        #THE HAND OF GOD - moves selected particle when mouse moves.
    if grab_player and event.type == pygame.MOUSEMOTION:

        #Relatve X and Relative Y: How much the particle has moved in the last frames
        (relativeX, relativeY) = event.rel
        (mouseX, mouseY) = event.pos
        grab_player.x = mouseX
        grab_player.y = mouseY

    #if the player falls into the void the game will display that you lost, stop running and quit
    GameOver()

    if event.type == pygame.QUIT:
        print("You quit the game.")
        running = False
        pygame.quit()
