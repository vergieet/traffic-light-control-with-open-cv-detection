import multiprocessing
TRAFFIC_LOAD_SOURCE = "runtime_data/traffic_load"

class TrafficLightResource:
    def __init__(self, queue):
        manager = multiprocessing.Manager()
        self.west_traffic_load_mgr_value = manager.Value('BARAT', 0)
        self.east_traffic_load_mgr_value = manager.Value('TIMUR', 0)
        self.north_traffic_load_mgr_value = manager.Value('UTARA', 0)
        self.south_traffic_load_mgr_value = manager.Value('SELATAN', 0)
        
    
    def save_traffic_load(self, key, traffic_load):
        if key == "BARAT":
            self.west_traffic_load_mgr_value.value = traffic_load
        elif key == "TIMUR":
            self.east_traffic_load_mgr_value.value = traffic_load
        elif key == "UTARA":
            self.north_traffic_load_mgr_value.value = traffic_load
        elif key == "SELATAN":
            self.south_traffic_load_mgr_value.value = traffic_load
        

    def read_traffic_load(self, key):
        if key == "BARAT":
            return self.west_traffic_load_mgr_value.value
        elif key == "TIMUR":
            return self.east_traffic_load_mgr_value.value
        elif key == "UTARA":
            return self.north_traffic_load_mgr_value.value
        elif key == "SELATAN":
            return self.south_traffic_load_mgr_value.value
        return 0
        