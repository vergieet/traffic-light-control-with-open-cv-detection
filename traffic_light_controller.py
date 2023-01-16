import time
import math
from traffic_resource_manager import TrafficLightResource
import RPi.GPIO as GPIO
from gpiozero import TrafficLights

# Pin Definitons:

class TrafficLightController:
    def __init__(self, traffic_resource):
        self.west_lights = TrafficLights(4, 3, 2)
        self.east_lights = TrafficLights(14, 15, 18)
        self.north_lights = TrafficLights(17, 27, 22)
        self.south_lights = TrafficLights(10, 9, 11)
        self.traffic_resource = traffic_resource
        self.traffic_lights = {
            "BARAT":{
                "minimumGreenLightCount": 5,
                "maximumRedTimeTreshold": 5,
                "minimum_traffic_point_to_recalculate": 5,
                "traffic_point_recalculation_multiplier": 0.75,
                "current_light": "green",
                "green_start_time": 0,
                "red_start_time": 0
            },
            "TIMUR":{
                "minimumGreenLightCount": 5,
                "maximumRedTimeTreshold": 5,
                "minimum_traffic_point_to_recalculate": 5,
                "traffic_point_recalculation_multiplier": 0.75,
                "current_light": "green",
                "green_start_time": 0,
                "red_start_time": 0
            },
            "UTARA":{
                "minimumGreenLightCount": 5,
                "maximumRedTimeTreshold": 5,
                "minimum_traffic_point_to_recalculate": 5,
                "traffic_point_recalculation_multiplier": 0.75,
                "current_light": "green",
                "green_start_time": 0,
                "red_start_time": 0
            },
            "SELATAN":{
                "minimumGreenLightCount": 5,
                "maximumRedTimeTreshold": 5,
                "minimum_traffic_point_to_recalculate": 5,
                "traffic_point_recalculation_multiplier": 0.75,
                "current_light": "green",
                "green_start_time": 0,
                "red_start_time": 0
            },
        }
        self.trafficstate = "BARAT"
        self.prev_trafficstate = "UTARA"
        self.alreadyGreenLights = []
        self.prioritized_lamp = None
        self.lock_prioritized_lamp = False
  
    def yellow_delay_switch(self, from_light_key, to_light):
        if from_light_key == "BARAT":
            self.switch_lamp_yellow(to_light, self.west_lights)
        elif from_light_key == "TIMUR":
            self.switch_lamp_yellow(to_light, self.east_lights)
        elif from_light_key == "SELATAN":
            self.switch_lamp_yellow(to_light, self.south_lights)
        elif from_light_key == "UTARA":
            self.switch_lamp_yellow(to_light, self.north_lights)
        time.sleep(2)

    def traffic_switch(self, from_light_key, to_light_key):
        if to_light_key == "BARAT":
            self.yellow_delay_switch(from_light_key, self.west_lights)
            self.switch_lamp_green(self.west_lights, [self.east_lights, self.north_lights, self.south_lights])
        elif to_light_key == "TIMUR":
            self.yellow_delay_switch(from_light_key, self.east_lights)
            self.switch_lamp_green(self.east_lights, [self.west_lights, self.north_lights, self.south_lights])
        elif to_light_key == "SELATAN":
            self.yellow_delay_switch(from_light_key, self.south_lights)
            self.switch_lamp_green(self.south_lights, [self.east_lights, self.north_lights, self.west_lights])
        elif to_light_key == "UTARA":
            self.yellow_delay_switch(from_light_key, self.north_lights)
            self.switch_lamp_green(self.north_lights, [self.east_lights, self.west_lights, self.south_lights])
    
    def switch_lamp_green(self, to_green, to_reds):
        to_green.off()
        to_green.green.on()
        for to_red in to_reds:
            to_red.off()        
            to_red.red.on()

    def switch_lamp_yellow(self, green_to_red,red_to_green):
        green_to_red.off()
        green_to_red.amber.on()
        red_to_green.off()
        red_to_green.amber.on()

    def green(self, trafficLight):
        trafficLight["current_light"] = "green";
        trafficLight["green_start_time"] = trafficLight["green_start_time"] + 1;

    def red(self, trafficLight):
        trafficLight["current_light"] = "red";
        trafficLight["red_start_time"] = trafficLight["red_start_time"] + 1;

    def yellow(self, trafficLight):
        trafficLight["current_light"] = "yellow";
        trafficLight["yellow_start_time"] = trafficLight["yellow_start_time"] + 2;
        time(2)

    def do_prioritize(self, trafficToBePrioritized):
        if not self.lock_prioritized_lamp:
            self.prioritized_lamp = trafficToBePrioritized
            self.lock_prioritized_lamp = True

    def force_prioritize(self, trafficToBePrioritized):
        self.prioritized_lamp = trafficToBePrioritized
        self.lock_prioritized_lamp = True

    def adjust_min_green_light(self, trafficToBeAdjusted, trafficPoint):
        if trafficPoint > self.traffic_lights[trafficToBeAdjusted]["minimum_traffic_point_to_recalculate"]:
            recalculationValue = math.ceil(trafficPoint * self.traffic_lights[trafficToBeAdjusted]["traffic_point_recalculation_multiplier"]);
            print("recalculation on-" + trafficToBeAdjusted +": " + str(recalculationValue))
            self.traffic_lights[trafficToBeAdjusted]["minimumGreenLightCount"] = recalculationValue
            print(trafficToBeAdjusted + str(self.traffic_lights[trafficToBeAdjusted]))

    
    def already_fulfill_green_time(self, trafficLight):
        if(trafficLight["green_start_time"] > trafficLight["minimumGreenLightCount"]):
            return True
        return False

    def reset_count(self, trafficLight , light):
        trafficLight[(str(light) + "_start_time")] = 0;

    def tickTrafficLight(self):
        # Do adjust green light based on traffic resource
        for key, _ in self.traffic_lights.items():
            if not key == self.trafficstate:
                self.adjust_min_green_light(key, self.traffic_resource.read_traffic_load(key))
                
        #Traffic ticking systems
        for key, _ in self.traffic_lights.items():
            if key == self.trafficstate:
                self.green(self.traffic_lights[key])
                # Do prioritization if there is a lamp that need to be prioritized
                if(not self.prioritized_lamp == None and self.already_fulfill_green_time(self.traffic_lights[key])):
                    self.traffic_switch(self.prev_trafficstate, self.trafficstate)
                    self.prev_trafficstate = self.trafficstate
                    self.reset_count(self.traffic_lights[self.trafficstate], "green")
                    self.reset_count(self.traffic_lights[self.prioritized_lamp], "red")
                    self.trafficstate = self.prioritized_lamp
                    self.lock_prioritized_lamp = False
            else:
                self.red(self.traffic_lights[key])
            

    def run(self):
        while True:
            # Prioritize traffic lamp with highest red time
            redLightStartTimeAggregated = {
                'BARAT' : (0 if self.traffic_lights['BARAT']['maximumRedTimeTreshold'] >= self.traffic_lights['BARAT']['red_start_time'] else self.traffic_lights["BARAT"]["red_start_time"]),
                'TIMUR': (0 if self.traffic_lights['TIMUR']['maximumRedTimeTreshold'] >= self.traffic_lights['TIMUR']['red_start_time'] else self.traffic_lights["TIMUR"]["red_start_time"]),
                'SELATAN': (0 if self.traffic_lights['SELATAN']['maximumRedTimeTreshold'] >= self.traffic_lights['SELATAN']['red_start_time'] else self.traffic_lights["SELATAN"]["red_start_time"]),
                'UTARA': (0 if self.traffic_lights['UTARA']['maximumRedTimeTreshold'] >= self.traffic_lights['UTARA']['red_start_time'] else self.traffic_lights["UTARA"]["red_start_time"]) 
            }
            highest_red_time = max(redLightStartTimeAggregated, key=redLightStartTimeAggregated.get)
            highest_red_time = None if redLightStartTimeAggregated[highest_red_time] == 0 else highest_red_time
            
            if not highest_red_time == None:
                self.do_prioritize(highest_red_time)
                # print(str(highest_red_time) + ":" +  str(self.traffic_lights[highest_red_time]["red_start_time"]))
            
            # print(self.prev_trafficstate + ":" + str(self.traffic_lights[self.prev_trafficstate]))
            # print(self.trafficstate + ":" + str(self.traffic_lights[self.trafficstate]))
            time.sleep(1)
            self.tickTrafficLight()
