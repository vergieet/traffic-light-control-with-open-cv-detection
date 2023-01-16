
TRAFFIC_LOAD_SOURCE = "runtime_data/traffic_load"

class TrafficLightResource:
    def __init__(self, queue):
        self.queue = queue
        
    
    def save_traffic_load(self, traffic_load):
        print("traffic_load")
        print(traffic_load)
        self.queue.put(traffic_load)

    def read_traffic_load(self):
        try:
            return self.queue.get_nowait(False)
        except:
            return ""
        