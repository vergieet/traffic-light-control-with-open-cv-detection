import cvlib as cv
from cvlib.object_detection import draw_bbox
from traffic_resource_manager import TrafficLightResource
import cv2

class TrafficCCTVStreamer:
    def __init__(self, traffic_resource):
        self.traffic_resource = traffic_resource
        self.west_video_source = "media/paskalbarat.mp4"
        self.east_video_source = "media/paskalbarat.mp4"
        self.north_video_source = "media/paskalbarat.mp4"
        self.south_video_source = "media/paskalbarat.mp4"

    def calculate_traffic_load(self, label):
            return label.count('car') + (label.count('bus') * 1.25) + (label.count('truck') * 1.25) + (label.count('motorcycle') * 0.5)

    def stream_traffic(self):
        print("Stream traffic from CCTV turned on")
        # open webcam
        west_video_stream = cv2.VideoCapture(self.west_video_source)
        east_video_stream = cv2.VideoCapture(self.east_video_source)
        north_video_stream = cv2.VideoCapture(self.north_video_source)
        south_video_stream = cv2.VideoCapture(self.south_video_source)

        if not west_video_stream.isOpened() or not east_video_stream.isOpened() or not north_video_stream.isOpened() or not south_video_stream.isOpened():
            print("Could not open video")
            exit()
        

        # loop through frames
        while west_video_stream.isOpened() or east_video_stream.isOpened() or north_video_stream.isOpened() or south_video_stream.isOpened():
            # read frame from webcam 
            status_west_video, frame_west_video = west_video_stream.read()
            status_east_video, frame_east_video = east_video_stream.read()
            status_north_video, frame_north_video = north_video_stream.read()
            status_south_video, frame_south_video = south_video_stream.read()
            # apply object detection
            
            # point = [41, 145, 325,472]
            # roi = frame_west_video[point[1]:point[3], point[0]:point[2]]
            bbox_west, label_west, config_west = cv.detect_common_objects(frame_west_video)
            bbox_east, label_east, config_east = cv.detect_common_objects(frame_east_video)
            bbox_north, label_north, config_north = cv.detect_common_objects(frame_north_video)
            bbox_south, label_south, config_south = cv.detect_common_objects(frame_south_video)
            # draw bounding box over detected objects
            # out_west = draw_bbox(frame_west_video, bbox_west, label_west, config_west, write_conf=True)
            # out_east = draw_bbox(frame_east_video, bbox_east, label_east, config_east, write_conf=True)
            # out_north = draw_bbox(frame_north_video, bbox_north, label_north, config_north, write_conf=True)
            # out_south = draw_bbox(frame_south_video, bbox_south, label_south, config_south, write_conf=True)
            
            # display output
            # cv2.imshow("Traffic Overview For WEST", out_west)
            # cv2.imshow("Traffic Overview For EAST", out_east)
            # cv2.imshow("Traffic Overview For NORTH", out_north)
            # cv2.imshow("Traffic Overview For SOUTH", out_south)
            traffic_load_west = self.calculate_traffic_load(label_west)
            traffic_load_east = self.calculate_traffic_load(label_east)
            traffic_load_north = self.calculate_traffic_load(label_north)
            traffic_load_south = self.calculate_traffic_load(label_south)
            # print(
            #     "WEST:" + str(traffic_load_west) + "\n" +
            #     "EAST:" + str(traffic_load_east) + "\n" + 
            #     "SOUTH:" + str(traffic_load_north) + "\n" +
            #     "NORTH:" + str(traffic_load_south) + "\n"
            # )

            self.traffic_resource.save_traffic_load("BARAT", traffic_load_west)
            self.traffic_resource.save_traffic_load("TIMUR", traffic_load_east)
            self.traffic_resource.save_traffic_load("SELATAN", traffic_load_south)
            self.traffic_resource.save_traffic_load("UTARA", traffic_load_north)
            # self.traffic_resource.save_traffic_load(
            #     "WEST:" + str(traffic_load_west) + "\n" +
            #     "EAST:" + str(traffic_load_east) + "\n" + 
            #     "SOUTH:" + str(traffic_load_north) + "\n" +
            #     "NORTH:" + str(traffic_load_south) + "\n"
            # )
            
            # press "Q" to stop
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        # release resources
        west_video_stream.release()
        east_video_stream.release()
        north_video_stream.release()
        south_video_stream.release()

        cv2.destroyAllWindows()        
