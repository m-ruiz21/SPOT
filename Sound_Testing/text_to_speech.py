# Basic Imports and Intialize
import pyttsx3
engine = pyttsx3.init()

engine.setProperty('rate', 150)     # setting up new voice rate

# Get User to type in Object Location and best route to go
c = True
while(c):
    obstacle_loc = input("Enter Obstacles Current Location: ")
    compass_dir = input("Enter Location User should go (Compass Direction): ")

    engine.say("Pause. Object detected in " + obstacle_loc +" area, " + "Face" + compass_dir + "and proceed")
    
    engine.runAndWait()
    c = bool( input("Enter 'False' to end and 'True' to continue: "))
    