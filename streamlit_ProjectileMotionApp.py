# -*- coding: utf-8 -*-
"""
Created on Thu May 26 22:54:24 2022

@author: T430s
"""

# projectile app
import streamlit as st
import matplotlib.pyplot as plt
#from math import *
import numpy as np
import pandas as pd
#from PIL import Image

# finding the maximum angle routine

def theta(beta):
    return (np.pi/180)*beta


def ballistic(height,angle,speed):
    a = (4.9/(speed**2*np.cos(theta(angle))**2))
    b = -np.tan(theta(angle))
    c = -height
    root = np.roots([a,b,c])
    return root.max()



def max_range(H,V): # finds the angle for maximum range using dataframe method

    x = []
    y = []
    for i in range(1,90):
         x.append(i)
         y.append(ballistic(H,i,V))
         
    x_new = np.array(x).reshape(89,1)
    y_new = np.array(y).reshape(89,1)
    data = np.append(x_new,y_new,axis = 1)
    df = pd.DataFrame(data)
    degree = df.iloc[df.iloc[:,1].idxmax(),0] # finds the position of the
    # cell of column[0] for which column[1] has the max value                                           
    return degree
    #print("The angle for the maximum range for the given H and v0 is:", degree)




# max range with simple loop method

def Find_MaxRange(H,V):  # very slightly differ especially at large height
    ang = np.linspace(1,90,200)
    distance = []
    for p in ang:
        distance.append(ballistic(H,p,V)) # it won't take an array, so had to make a for loop to make a distance array
    distance = np.array(distance)
    
    # stops the loop as soon as the range starts decreasing from the maximum
    for i in range(len(ang)):
         if distance[i+1] < distance[i]:
            break
    return round(ang[i])  




# finding the horixontal range for given, yo, vo and theta
def H_range(yo,vo,angle):
    conversion = (np.pi/180)
    a = -4.905
    b = vo*np.sin(angle*conversion)
    c = yo
    t = (-b - np.sqrt(b**2- (4*a*c)))/(2*a) # getting positive time
    x = vo*np.cos(angle*conversion)*t
    return x
# total time of flight
def time(yo,vo,angle):
    conversion = (np.pi/180)
    a = -4.905
    b = vo*np.sin(angle*conversion)
    c = yo
    t = (-b - np.sqrt(b**2- (4*a*c)))/(2*a) # getting positive time
    return t
# speed at which it hits the ground
def finalspeed(yo,vo,angle):
    vx = vo*np.cos(theta(angle))
    vy = vo*np.sin(theta(angle)) - (9.81*time(yo,vo,angle)) #angle already converted to radians in time function
    v = np.sqrt(vx**2 + vy**2)
    return round(v,1)

# angle at which it hits the ground
def finalangle(yo,vo,angle):
    vx = vo*np.cos(theta(angle))
    vy = vo*np.sin(theta(angle)) - (9.81*time(yo,vo,angle)) #angle already converted to radians in time function
    final_angle = np.arctan(vy/vx)*(180/np.pi)
    return round(final_angle)
    


# projectile path plotting, this function is needed for the projectile function which plots the path
    
def projectile_function(y0,x_distance,v0,angle):  # simulate the projectile motion
    conversion = (np.pi/180)           # for ground - ground projection
    y = y0 + x_distance*np.tan(angle*conversion) - (4.905*x_distance**2/(v0**2*np.cos(angle*conversion)**2))
    # above is the ballistic equation using projectile motion
    return y
    
    #if y >= 0:
       #return y
    
    #elif y<=0:
        #return None   # if y becomes '-', it will return null number
     




     
def projectile(yo,vo,angle):
    x_distance = H_range(yo, vo, angle)
   
   #y0 = initial height
   #x_distance = total distance
   #v0 = initial angle of projection
   
    x = np.linspace(0,x_distance,40)
    y = []
    for i in x:
        out = projectile_function(yo,i,vo,angle)
        y.append(out)

        
    st.write("* The Horizontal Range is:", round(H_range(yo,vo,angle),1),"m") 
    st.write ("* Time of flight is:", round(time(yo,vo,angle),2), "s") 
    st.write ("* Maximum height reached is:",round(max(y),1),'m')  
    st.write ("* The angle for the maximum range for the given intial height and initial speed is:",Find_MaxRange(yo,vo),'degree')   # access the function to calculat the angle for                       
    st.write("* The projectile's final speed before it hits the ground is:",finalspeed(yo,vo,angle),'m/s')
    st.write("* It will hit the ground at an angle:",finalangle(yo,vo,angle),'degree')
    plt.plot(x,y,'b')
    plt.xlabel('Distance(m)')
    plt.ylabel('Height(m)')
    st.set_option('deprecation.showPyplotGlobalUse', False) # not to print the error message
    plt.show()
    st.pyplot()
    


#image = Image.open('projectile.jpg')
#st.image(image)

st.write("""
## 2- Dimensional Projectile Motion Simulation
### --by A. Maharjan
""")


st.sidebar.header('specify the initial height:')
yo = st.sidebar.number_input('Insert an intial height in m',step = 0.1)
st.sidebar.write('---')

st.sidebar.header('specify the initial speed:')
vo = st.sidebar.number_input('Insert an initial speed in m/s',step = 0.1)
st.sidebar.write('---')

st.sidebar.header('specify the angle of projection:')
angle = st.sidebar.number_input('Insert the angle of projection in degrees',step = 0.1)
st.sidebar.write('---')

st.write("""
#### Selected Inputs
""")
parms = pd.DataFrame([[yo,vo,angle]],columns=['Initial Height(m)','Initial Speed(m/s)','Angle(degree)'])
st.write(parms)


if st.button('Press to calculate and simulate the projectile motion'):
    if ((yo==0) & (vo==0) & (angle==0)):
        st.write('Make the speed and angle non-zero')
    elif ((yo !=0) & (vo==0) & (angle ==0)):
        st.write('Make the speed non-zero')
    elif ((yo ==0) & (vo==0) & (angle !=0)):
        st.write('Make the speed non-zero')    
    elif (vo ==0):
        st.write('Make the speed non-zero')
    else:
        projectile(yo,vo,angle)
    
st.write('---')


st.sidebar.header('Quadratic Equation Solver')
st.sidebar.write(""" ### ax^2 + bx + c = 0 """)

a = st.sidebar.number_input('Coeff  a:',step = 0.01)
b = st.sidebar.number_input('Coeff  b:',step = 0.01)
c = st.sidebar.number_input('Coeff  c:',step = 0.01)
    
if st.sidebar.button('Calculate Roots'):
    root = np.roots([a,b,c]) # it retuns a list of roots
    st.write('The roots are:')
    for i in root:
        st.write(round(i,3))
        
        
























