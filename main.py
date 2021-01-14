#attempting to learn physics simulations from scratch


from math import atan, inf, sqrt, cos, sin, tan, pi as π, radians
from time import time, sleep
from random import randint as rand, choice


#        90       
#        ^        
# 180 <  +  > 0   
#        v        
#       270       


#Class Definition
class Rectangle:
  '''A rectangle encloses an area shaped like a pentagon. It is defined by an
upper and lower x range and an upper and lower y range. These are not
objects that can be placed on a screen as part of an animation.'''
  def __init__(self, x_range, y_range):
    self.x_range = x_range
    self.y_range = y_range


  def __repr__(self):
    return f'Rectangle Object, Corner 1: [{self.x_range[0]},{self.y_range[0]}], Corner 2: [{self.x_range[1]},{self.y_range[1]}]'


  def cont(self, x, y):
    '''Determines whether a given point with coordinates [x, y] lies inside
the rectangle object'''
    return self.x_range[0] <= x <= self.x_range[1] and self.y_range[0] <= y <= self.y_range[1]



  
class Circle:
  '''A circle object is defined by a radius and a pair of coordinates. When
called, a circle object takes the arguments:

Radius - the distance from the origin of the circle to its edge
Pos - the coordinates of the origin of the circle
Mom - a pair of values representing the momentum of the circle object
  in both the x and y directions.'''
  def __init__(self, radius = 5, pos = [0, 0], mom = [0, 0], mob = True):
    self.radius = radius
    self.mass = self.radius**2
    self.x_pos, self.y_pos = pos
    self.x_mom, self.y_mom = mom
    self.x_force, self.y_force = 0, 0 #Current forces acting on the circle
    self.mob = mob #Whether the circle is able to move or not. Default is True


  def cont(self, x, y):
    '''Determines whether a given point with coordinates [x, y] lies inside
the circle object.'''
    return(( x - self.x_pos)**2 + (y - self.y_pos)**2) < self.radius ** 2


  def touch_point(self, θ):
    '''determines the point on the edge of the circle object with an angle θ
from the center of the circle.'''
    return -self.radius * sin(θ) + self.x_pos, -self.radius * cos(θ) + self.y_pos
    

    
class Screen:
  '''A screen object is a container for other objects. When called, a screen
object takes the arguments:

px_dims - the dimensions in πxels of the stage that will be displayed
  when self.__str__ is called.
sc_dims - the number of columns by the number of rows that will be
  returned when self.__str__ is called. This should be the size of
  your terminal window.
c_pos - the coordinates of the very center of the screen'''
  def __init__(self, px_dims = [1366, 768], sc_dims = [167, 39], c_pos = [0, 0]):
    self.sc_x, self.sc_y = sc_dims
    self.px_x, self.px_y = px_dims
    self.c_x, self.c_y = c_pos
    self.p_mat_x, self.p_mat_y = self.gen_pos_mat()
    self.objs = {} #Objects currently on the screen
    self.rects = [#Areas of the display that need updating before the screen is printed again
      Rectangle([self.p_mat_x[0], self.p_mat_x[-1]], [self.p_mat_y[0], self.p_mat_y[-1]])
    ] #For efficiency not all parts of the screen are generated every time it is printed, only the
     # parts that have changed since the last time it was printed.
    self.str = [[' ' for i in range(self.sc_x)] for i in range(self.sc_y)]
    self.render()
    

  def __str__(self):
    if self.rects:
      self.render()
    return '\n'.join([''.join(row) for row in self.str])


  def render(self):
    '''Renders the screen by rendering every cell inside an updating rectangle'''
    for py,y in enumerate(self.p_mat_y[::-1]):
      for px,x in enumerate(self.p_mat_x):
        upd = False
        for rect in self.rects:
          if rect.cont(x, y):
            upd = True
            break
        if upd:
          s = ' '
          for obj in self.objs:
            if self.objs[obj].cont(x, y):
              s = 'Ѩ'
              break
          self.str[py][px] = s
    self.rects = []
    


  def gen_pos_mat(self):
    '''Generates the x and y values of each cell in the output matrix.'''
    m = self.px_x / self.sc_x
    b = -(self.px_x >> 1)+ self.c_x + m/2
    x_values = [int(m*x+b)for x in range(self.sc_x)] 
    m = self.px_y / self.sc_y
    b = -(self.px_y >> 1)+ self.c_y + m/2
    y_values = [int(m*y+b)for y in range(self.sc_y)] 
    return x_values, y_values
        
        
    
  def add_obj(self, key, item):
    '''Adds an object, {item}, to the screen's dictionary of objects. This object
will have the unique identifier {key}'''
    self.objs [key] = item
    r = item.radius
    self.rects.append(Rectangle([item.x_pos-r,item.x_pos+r],[item.y_pos-r,item.y_pos+r]))


  def del_obj(self, key):
    '''Deletes the object with unique identifier {key} from the screen's
dictionary of objects'''
    del self.objs [key] 


  def obj_net_force(self, key, frame):
    '''Determines the total net force acting on the object with the unique
identifier {key} at the current point in time. The length of {frame}
determines the effect of gravity because gravity is weird like that.'''
    obj = self.objs [key] 
    x_force, y_force = 0, 0
    
    if obj.mob: #gravity
      y_force += obj.mass * gravity * frame

    if type(obj) == Circle:
      for ob in self.objs:
        if ob != key: #Making sure that objects dont try to interact with themselves
          o = self.objs[ob]
          if type(o) == Circle:
            x_dif, y_dif = obj.x_pos - o.x_pos, obj.y_pos - o.y_pos #distance between circles in x and y direction
            if (x_dif)**2 + (y_dif)**2 <= (obj.radius + o.radius)**2: #If the 2 circles are touching
              rec_θ = θ(x_dif, y_dif)
              x_f, y_f = xy(obj.mass*m(obj.x_mom,obj.y_mom)*cos(rec_θ+π-θ(obj.x_mom,obj.y_mom))+o.mass*m(o.x_mom,o.y_mom)*cos(rec_θ-θ(o.x_mom,o.y_mom)),rec_θ)#yum
              x_force += x_f
              y_force += y_f

    return x_force, y_force

  def accelerate(self, key):
    '''Converts the forces acting on the object with unique identifier {key} to
momentum.'''
    if self.objs [key].mob: 
      self.objs [key].x_mom += self.objs [key].x_force / self.objs [key].mass
      self.objs [key].y_mom += self.objs [key].y_force / self.objs [key].mass


  def move(self, key, time):
    '''Moves the object with unique identifier {key} by its momentum for some time.'''
    if self.objs [key].mob:
      r = self.objs[key].radius
      self.rects.append(Rectangle([self.objs[key].x_pos-r,self.objs[key].x_pos+r],[self.objs[key].y_pos-r,self.objs[key].y_pos+r]))
      self.objs [key].x_pos += self.objs [key].x_mom * time
      self.objs [key].y_pos += self.objs [key].y_mom * time
      self.rects.append(Rectangle([self.objs[key].x_pos-r,self.objs[key].x_pos+r],[self.objs[key].y_pos-r,self.objs[key].y_pos+r]))
          
    

  def time(self, time):
    '''Passes time on the screen, this is all you need to run the animation. It
has 3 stages:

1) It finds the forces acting on all the objects
2) It accelerates each object accordingly
3) It moves all objects.'''
    for key in self.objs: #finds the forces acting on each object
      if self.objs [key].mob:
        self.objs [key].x_force, self.objs [key].y_force = self.obj_net_force(key,time)
    for key in self.objs: #accelerates each object according to the forces acting on them
      if self.objs [key].mob:
        self.accelerate(key)
    for key in self.objs: #moves each object according to their velocities
      if self.objs [key].mob:
        self.move(key, time)


#Functions and stuff
def θ(x, y):
  '''Finds the angle of a vector with an x value of x and a y value of y'''
  return atan(y/x)+[π,π,2*π,0][2*(x>0)+(y>0)]
  
def m(x, y):
  '''Finds the magnitude of a vector with an x value of x and a y value of y'''
  return (x**2+y**2)**0.5

def xy(m, θ):
  '''Converts a vector with magnitude and angle to a pair of x and y values'''
  return m*cos(θ),m*sin(θ)
  




  

#Settings
global gravity
gravity = -9.8 #The rate at which objects accelerate due to gravity.

fps = 40 #Frames per second, higher fps is more demanding but increases animiation smoothness and accuracy.
frame = 1/fps

display_time = 4 #Duration of time in seconds each animation plays for before restarting

px_dims = [195, 110] #the dimensions in pixels of the display size. This should be in proportion to your monitor's display size.
sc_dims = [167, 48] #the number of columns by the number of rows of the terminal window. For me this is font size 12 in fullscreen


def main():
  screen = Screen(px_dims,sc_dims)
  screen.add_obj('left_ball', Circle(rand(4,8), [rand(20,40), rand(-40,-25)], [rand(-30,-20), rand(25,32)])) #Create 3 random balls
  screen.add_obj('right_ball', Circle(rand(4,8), [rand(-40,-20), rand(-40,-25)], [rand(20,30), rand(25,32)]))
  screen.add_obj('top_ball', Circle(rand(4,8), [rand(-20,20), rand(20,35)], [rand(1,10)*2-11, rand(-10,0)]))

  for i in range(display_time * fps):     #Runs for the set length of the animation
    s_time = int(time()*fps)#Stores the time this frame began
    try:
      screen.time(frame) #Moves the balls
    except Exception as e:
      input(e)
      obama
    print(f'{chr(10)*20}{screen}', end='')#prints the screen
    while int(time()*fps)<= s_time: #Waits until it's time to start a new frame
      'obama'#This is very important


while 1:
  main()
