import time

class TrafficLightController:
    def __init__(self, east_red_time, south_red_time, west_red_time, north_red_time, east_max_red_time, south_max_red_time, west_max_red_time, north_max_red_time, east_min_green_time, south_min_green_time, west_min_green_time, north_min_green_time):
        self.east_red_time = east_red_time
        self.south_red_time = south_red_time
        self.west_red_time = west_red_time
        self.north_red_time = north_red_time
        self.east_max_red_time = east_max_red_time
        self.south_max_red_time = south_max_red_time
        self.west_max_red_time = west_max_red_time
        self.north_max_red_time = north_max_red_time
        self.east_min_green_time = east_min_green_time
        self.south_min_green_time = south_min_green_time
        self.west_min_green_time = west_min_green_time
        self.north_min_green_time = north_min_green_time
        self.east_green_time = 0
        self.south_green_time = 0
        self.west_green_time = 0
        self.north_green_time = 0
        self.east_state = 'red'
        self.south_state = 'red'
        self.west_state = 'red'
        self.north_state = 'red'
        self.previous_east_state = 'red'
        self.previous_south_state = 'red'
        self.previous_west_state = 'red'
        self.previous_north_state = 'red'

    def run(self):
        while True:
            # Prioritize traffic lamp with highest red time
            highest_red_time = max(self.east_red_time, self.south_red_time, self.west_red_time, self.north_red_time)
            if highest_red_time == self.east_red_time and self.east_red_time >= self.east_max_red_time and self.east_green_time >= self.east_min_green_time:
                self.east_red_time = 0
                self.east_green_time = 0
                self.previous_east_state = self.east_state
                self.east_state = 'green'
                self.green("East")
            elif highest_red_time == self.south_red_time and self.south_red_time >= self.south_max_red_time and self.south_green_time >= self.south_min_green_time:
                self.south_red_time = 0
                self.south_green_time = 0
                self.previous_south_state = self.south_state
                self.south_state = 'green'
                self.green("South")
            elif highest_red_time == self.west_red_time and self.west_red_time >= self.west_max_red_time and self.west_green_time >= self.west_min_green_time:
                self.west_red_time = 0
                self.west_green_time = 0
                self.previous_west_state = self.west_state
                self.west_state = 'green'
                self.green("West")
            elif highest_red_time == self.north_red_time and self.north_red_time >= self.north_max_red_time and self.north_green_time >= self.north_min_green_time:
                self.north_red_time = 0
                self.north_green_time = 0
                self.previous_north_state = self.north_state
                self.north_state = 'red'
                self.green("North")
            else:
                self.east_red_time += 1
                self.south_red_time += 1
                self.west_red_time += 1
                self.north_red_time += 1
                self.east_green_time += 1
                self.south_green_time += 1
                self.west_green_time += 1
                self.north_green_time += 1
                self.red()
            print(f'East: {self.east_red_time} secs, State: {self.east_state} , South: {self.south_red_time} secs, State: {self.south_state}, West: {self.west_red_time} secs, State: {self.west_state}, North: {self.north_red_time} secs, State: {self.north_state}')
            time.sleep(1)
            
    def green(self, direction):
        if self.previous_east_state != self.east_state or self.previous_south_state != self.south_state or self.previous_west_state != self.west_state or self.previous_north_state != self.north_state:
            self.yellow()
        print(f"{direction} traffic lamp is green")
        time.sleep(2)
        self.yellow()
        if direction == 'East':
            self.east_state = 'red'
        elif direction == 'South':
            self.south_state = 'red'
        elif direction == 'West':
            self.west_state = 'red'
        elif direction == 'North':
            self.north_state = 'red'

    def red(self):
        self.yellow()
        print("All traffic lamps are red")
        
    def yellow(self):
        print("All traffic lamps are yellow")
        time.sleep(2)

controller = TrafficLightController(10, 5, 15, 3, 20, 15, 10, 5, 5, 8, 10, 15)
controller.run()


