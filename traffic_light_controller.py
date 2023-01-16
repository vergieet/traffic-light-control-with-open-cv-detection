import time
import math
from traffic_resource_manager import TrafficLightResource

class TrafficLightController:
    def __init__(self, traffic_resource):
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
            # self.traffic_lights[trafficToBeAdjusted]["minimumGreenLightCount"] = recalculationValue
            print(trafficToBeAdjusted + str(self.traffic_lights[trafficToBeAdjusted]))

    
    def already_fulfill_green_time(self, trafficLight):
        if(trafficLight["green_start_time"] > trafficLight["minimumGreenLightCount"]):
            return True
        return False

    def reset_count(self, trafficLight , light):
        trafficLight[(str(light) + "_start_time")] = 0;

    def tickTrafficLight(self):
        print(self.traffic_resource.read_traffic_load());
        for key, _ in self.traffic_lights.items():
            if key == self.trafficstate:
                self.green(self.traffic_lights[key])
                if(not self.prioritized_lamp == None and self.already_fulfill_green_time(self.traffic_lights[key])):
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
            print(self.trafficstate + ":" + str(self.traffic_lights[self.trafficstate]))
            time.sleep(1)
            self.tickTrafficLight()
