from traffic_light_controller import TrafficLightController
from traffic_resource_manager import TrafficLightResource
from traffic_cctv_streamer import TrafficCCTVStreamer
import multiprocessing
multiprocessing.set_start_method("fork")

q = multiprocessing.Queue()
resource = TrafficLightResource(q)
# Instantiate controller for traffic light
controller = TrafficLightController(resource)
# Instantiate streamer to watch traffic light
streamer = TrafficCCTVStreamer(resource)

if __name__ == "__main__":
    jobs = []
    # jobs.append(multiprocessing.Process(
    #     target=controller.run, args=()
    # ))
    jobs.append(multiprocessing.Process(
        target=streamer.stream_traffic, args=()
    ))
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()