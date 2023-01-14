# author: Arun Ponnusamy
# website: https://www.arunponnusamy.com

# object detection video example using tiny yolo model.
# usage: python object_detection_video_yolov3_tiny.py /path/to/video

# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import matplotlib.pyplot as plt
import cv2
import multiprocessing
from trafficcontrolmyself import TrafficLightController

NUM_PROC = 2

controller = TrafficLightController()

def stream_traffic():
    print("run")
    # open webcam
    videoPaskalBarat = cv2.VideoCapture("paskalbarat.mp4")
    videoPaskalKaliki = cv2.VideoCapture("paskalutara.mp4")
    videoPaskalKalikiAng = cv2.VideoCapture("paskalkalikiang.mp4")
    videoPaskalTimur = cv2.VideoCapture("paskaltim.mp4")

    def calculate_traffic_load(label):
        return label.count('car') + (label.count('bus') * 1.25) + (label.count('truck') * 1.25) + (label.count('motorcycle') * 0.5)


    if not videoPaskalBarat.isOpened() or not videoPaskalKaliki.isOpened() or not videoPaskalKalikiAng.isOpened() or not videoPaskalTimur.isOpened():
        print("Could not open video")
        exit()

    # loop through frames
    while videoPaskalBarat.isOpened() or videoPaskalKaliki.isOpened() or videoPaskalKalikiAng.isOpened() or videoPaskalTimur.isOpened():

        # read frame from webcam 
        statusPaskalBarat, framePaskalBarat = videoPaskalBarat.read()
        statusPaskalKaliki, framePaskalKaliki = videoPaskalKaliki.read()
        statusPaskalKalikiAng, framePaskalKalikiAng = videoPaskalKalikiAng.read()
        statuPaskalTimur, framePaskalTimur = videoPaskalTimur.read()
        # apply object detection

        # point = [41, 145, 325,472]
        # roi = framePaskalBarat[point[1]:point[3], point[0]:point[2]]
        bboxPaskalBarat, labelPaskalBarat, confPaskalBarat = cv.detect_common_objects(framePaskalBarat)
        bboxPaskalKaliki, labelPaskalKaliki, confPaskalKaliki = cv.detect_common_objects(framePaskalKaliki)
        bboxPaskalKalikiAng, labelPaskalKalikiAng, confPaskalKalikiAng = cv.detect_common_objects(framePaskalKalikiAng)
        bboxPaskalTimur, labelPaskalTimur, confPaskalTimur = cv.detect_common_objects(framePaskalTimur)
        
        # if pr:
        # point = [41, 145, 325,472]
        # roi = frame[point[1]:point[3], point[0]:point[2]]
            # plt.imshow(roi)
            # plt.show()
            # break
            # pr = False

        # draw bounding box over detected objects
        outPaskalBarat = draw_bbox(framePaskalBarat, bboxPaskalBarat, labelPaskalBarat, confPaskalBarat, write_conf=True)
        outPaskalKaliki = draw_bbox(framePaskalKaliki, bboxPaskalKaliki, labelPaskalKaliki, confPaskalKaliki, write_conf=True)
        outPaskalKalikiAng = draw_bbox(framePaskalKalikiAng, bboxPaskalKalikiAng, labelPaskalKalikiAng, confPaskalKalikiAng, write_conf=True)
        outPaskalTimur = draw_bbox(framePaskalTimur, bboxPaskalTimur, labelPaskalTimur, confPaskalTimur, write_conf=True)

        # display output
        
        cv2.imshow("Real-time object detection 1", outPaskalBarat)
        cv2.imshow("Real-time object detection 2", outPaskalKaliki)
        cv2.imshow("Real-time object detection 3", outPaskalKalikiAng)
        cv2.imshow("Real-time object detection 4", outPaskalTimur)
        trafficLoadPaskalBarat = calculate_traffic_load(labelPaskalBarat)
        trafficLoadPaskalTimur = calculate_traffic_load(labelPaskalTimur)
        trafficLoadPaskalUtara = calculate_traffic_load(labelPaskalKaliki)
        trafficLoadPaskalSelatan = calculate_traffic_load(labelPaskalKalikiAng)
        # highestTraffic = None
        # if (
        #     trafficLoadPaskalBarat > trafficLoadPaskalTimur and
        #     trafficLoadPaskalBarat > trafficLoadPaskalSelatan and
        #     trafficLoadPaskalBarat > trafficLoadPaskalUtara
        # ):
        #     highestTraffic = "BARAT"
        # elif (
        #     trafficLoadPaskalTimur > trafficLoadPaskalSelatan and
        #     trafficLoadPaskalTimur > trafficLoadPaskalUtara 
        #     ):
        #     highestTraffic = "TIMUR"
        # elif (
        #     trafficLoadPaskalSelatan > trafficLoadPaskalUtara
        # ):
        #     highestTraffic = "SELATAN"
        # else:
        #     highestTraffic = "UTARA"
        global controller
        controller.adjust_min_green_light("BARAT", trafficLoadPaskalBarat);
        controller.adjust_min_green_light("TIMUR", trafficLoadPaskalTimur);
        controller.adjust_min_green_light("UTARA", trafficLoadPaskalUtara);
        controller.adjust_min_green_light("SELATAN", trafficLoadPaskalSelatan);
        # press "Q" to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # release resources
    videoPaskalBarat.release()
    videoPaskalKaliki.release()
    videoPaskalKalikiAng.release()
    videoPaskalTimur.release()

    cv2.destroyAllWindows()        

def run_traffic_controller():
    global controller
    controller.run()


if __name__ == "__main__":
    jobs = []
    jobs.append(multiprocessing.Process(
        target=stream_traffic, 
        args=()
    ))
    jobs.append(multiprocessing.Process(
        target=run_traffic_controller, 
        args=()
    ))
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()