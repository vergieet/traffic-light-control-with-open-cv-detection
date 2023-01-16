# External module imports
import RPi.GPIO as GPIO
from gpiozero import TrafficLights
import time

# Pin Definitons:
west_lights = TrafficLights(4, 3, 2)
east_lights = TrafficLights(14, 15, 18)
north_lights = TrafficLights(17, 27, 22)
south_lights = TrafficLights(10, 9, 11)

green_waiting_time = 30
yellow_switching_time = 2

def switch_green(to_green,to_reds):
    to_green.off()
    to_green.green.on()
    for to_red in to_reds:
        to_red.off()        
        to_red.red.on()

def switch_yellow(green_to_red,red_to_green):
    green_to_red.amber.on()
    green_to_red.green.off()
    red_to_green.amber.on()
    red_to_green.red.off()

while(True):
    switch_green(west_lights, [east_lights, north_lights, south_lights])
    time.sleep(green_waiting_time)
    switch_yellow(west_lights, east_lights)
    time.sleep(yellow_switching_time)
    switch_green(east_lights, [west_lights, north_lights, south_lights])
    time.sleep(green_waiting_time)
    switch_yellow(east_lights, north_lights)
    time.sleep(yellow_switching_time)
    switch_green(north_lights, [west_lights, east_lights, south_lights])
    time.sleep(green_waiting_time)
    switch_yellow(north_lights, south_lights)
    time.sleep(yellow_switching_time)
    switch_green(south_lights, [west_lights, north_lights, east_lights])
    time.sleep(green_waiting_time)
    switch_yellow(south_lights, west_lights)
    time.sleep(yellow_switching_time)
    
