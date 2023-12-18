#Lecture 2
import pygame
import math
from pickle import TRUE                       
import random

class Environment:
    gravity = (math.pi, 0.02)

    def addFunctions(self, function_list):
        for f in function_list:
            #try and get function, provide default value in place of failure
            (n, func) = self.function_dictionary.get(f, (-1, None))
            #single particle functions
            if n == 1:
                self.particle_functions1.append(func)
            elif n == 2:
                self.particle_functions2.append(func)
            else:
                print ("No function found called %s" %f)   

    def __init__(self, width, height, player_x, player_y, y_change, rect_platforms):
        self.width = width
        self.height = height
        self.particles = []
        self.colour = (255,255,255)
        self.mass_of_air = 0.5
        self.jump = False
        self.gravity = (math.pi, 0.005)
        self.x = player_x
        self.y = player_y
        #set up empty functions for enabled features
        self.particle_functions1 = []
        self.particle_functions2 = []

        #add possible functions
        self.function_dictionary = {
            'move': (1, lambda p: p.move()),
            'drag': (1, lambda p: p.addDrag()),
            'jumping': (1, lambda p: p.jumping(self.y,p,y_change)),
            'bounce': (1, lambda p: self.bounce(p)), #bounce is called in environment
            'collide': (1, lambda p: p.checkCollisions(rect_platforms, self.jump, p, y_change))
        }                             
    def addParticles(self,n=1, **kargs):
        for i in range (n):
            #try and get an argument from kargs, if it fails, it will generate a random attribute instead
            size = kargs.get('size',random.randint(10,20))
            mass = kargs.get('mass',random.randint(100,200))
            x = kargs.get('x',random.uniform(size,self.width-size))
            y = kargs.get('y',random.uniform(size,self.height-size))
            
            #create the particle
            p = Particle((x,y),size, mass)
            

            #apply additional attributes
            p.speed = kargs.get('speed',random.random())
            p.angle = kargs.get('angle',random.uniform(0, math.pi*2))
            p.colour = kargs.get('colour',(0,0,255))
            p.drag = (p.mass/(p.mass + self.mass_of_air))**p.size

            self.particles.append(p)

        #Checks player's and platform's position and when to execute a jump
    def jumping(self,y_pos, particle, y_change): #put (self,y_pos)  otherwise
        #Preset value of how far the player can jump
        y_pos = particle.y
        jump_height = 9
        gravity_jump = 0.2
        if particle.jump:
            y_change = -jump_height 
            particle.jump = False

        y_pos += y_change #y_pos += y_change
        y_change += gravity_jump
        return y_pos

    #checks for collisions with platforms
    def checkCollisions(rect_platforms, j, particle, y_change):
        #Calling the global variables "player_x" and "player_y" declared above into the function
    
        #Tells us the direction of the player and controls how much moviment is done per frame
        #if y_change as a negative value, we are executing a "up" moviment, while if it is positive we are going "down" on the screen
        for i in range(len(rect_platforms)):
            #pygame's built-in rectangle collision detect tool, checks if any points that overlap between 2 defined rectangles
            if rect_platforms[i].colliderect([particle.x, particle.y + 24.5, 30 ,10]) and particle.jump == False and y_change > 0:
                j = True
        return j


    def move(self, particle):
        particle.x += math.sin(self.angle) * self.speed
        particle.y -= math.cos(self.angle) * self.speed

    def bounce(self, particle):
        #East Coast:
        if particle.x > self.width - particle.size:
            #Implements elasticity to reduce speed on bounce
            particle.speed *= particle.elasticity
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = -particle.angle
        #West Coast:
        elif particle.x < particle.size:
            particle.speed *= particle.elasticity
            #Sticks to the wall
            particle.x = 2* particle.size - particle.x
            #Reverses the angle
            particle.angle = -particle.angle
        #Deep South:
        elif particle.y > self.height - particle.size:
            particle.speed *= particle.elasticity
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
        #North
        elif particle.y < particle.size:
            particle.speed *= particle.elasticity
            particle.y = 2* particle.size - particle.y
            particle.angle = math.pi - particle.angle

    #Calculates the resultant position when two forces are applied to a particle.
    #In this case - gravity and directional force.

    def update(self):
        for i, particle in enumerate(self.particles):
             for f in self.particle_functions1:
                f(particle)
            #Particles other than the selected particle move
            #call two particle functions, if any
        if(self.particle_functions2 != []):

                                
            for particle2 in self.particles[i+1:]:
                for f in self.particle_functions2:
                    f(particle, particle2)
    
    #Locate the particle next to the mouse click
    def findParticle(self, coords):
        x,y = coords
        for p in self.particles:
            if math.hypot(p.x-x, p.y-y) <= p.size:
                return p

def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    #Hypotenuse joins the two forces together.
    length = math.hypot(x,y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return(angle, length)

    

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

    def display(self,screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
    
    #This function is used in thus class to prevent that the background particles will move out of screen,
    #instead bouncing and changing directory while maintaining it's momentum
    def bounce(self,width,height):
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

    #Move function: 
    def move(self):
        #Weights the particle with the drag:
        self.ParticleSpeed *= self.drag
        ##Adds the weight of gravity when the particle moves:
        (self.angle, self.ParticleSpeed) = addVectors(self.angle, self.ParticleSpeed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.ParticleSpeed
        self.y -= math.cos(self.angle) * self.ParticleSpeed

