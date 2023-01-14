# author: Arun Ponnusamy
# website: https://www.arunponnusamy.com

# object detection video example using tiny yolo model.
# usage: python object_detection_video_yolov3_tiny.py /path/to/video

# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import matplotlib.pyplot as plt
import cv2

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
pr = True
i = 1
trafficLightBarat = {"minimumGreenLightCount": 10, "maximumRedTimeTreshold": 30, "current_light": "green", "green_start_time": 0, "red_start_time": 0}
trafficLightTimur = {"minimumGreenLightCount": 10, "maximumRedTimeTreshold": 30, "current_light": "green", "green_start_time": 0, "red_start_time": 0}
trafficLightUtara = {"minimumGreenLightCount": 10, "maximumRedTimeTreshold": 30, "current_light": "green", "green_start_time": 0, "red_start_time": 0}
trafficLightSelatan = {"minimumGreenLightCount": 10, "maximumRedTimeTreshold": 30, "current_light": "green", "green_start_time": 0, "red_start_time": 0}
trafficstate = "BARAT"
trafficStateCount = [0 , 0 , 0 ,0] # state count from barat timur selatan utara

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
    # cv2.imshow("Real-time object detection 1", outPaskalBarat)
    # cv2.imshow("Real-time object detection 2", outPaskalKaliki)
    # cv2.imshow("Real-time object detection 3", outPaskalKalikiAng)
    # cv2.imshow("Real-time object detection 4", outPaskalTimur)
    trafficLoadPaskalBarat = calculate_traffic_load(labelPaskalBarat)
    trafficLoadPaskalTimur = calculate_traffic_load(labelPaskalTimur)
    trafficLoadPaskalUtara = calculate_traffic_load(labelPaskalKaliki)
    trafficLoadPaskalSelatan = calculate_traffic_load(labelPaskalKalikiAng)

    print('Iteration-' + str(i))
    i = i + 1
    print('Traffic Load Paskal Barat: ' + str(trafficLoadPaskalBarat))
    print('Traffic Load Paskal Timur: ' + str(trafficLoadPaskalTimur))
    print('Traffic Load Paskal Selatan: ' + str(trafficLoadPaskalUtara))
    print('Traffic Load Paskal Utara: ' + str(trafficLoadPaskalSelatan))

    highestTraffic = None
    if (
        trafficLoadPaskalBarat > trafficLoadPaskalTimur and
        trafficLoadPaskalBarat > trafficLoadPaskalSelatan and
        trafficLoadPaskalBarat > trafficLoadPaskalUtara
       ):
        highestTraffic = "BARAT"
    elif (
        trafficLoadPaskalTimur > trafficLoadPaskalSelatan and
        trafficLoadPaskalTimur > trafficLoadPaskalUtara 
        ):
        highestTraffic = "TIMUR"
    elif (
        trafficLoadPaskalSelatan > trafficLoadPaskalUtara
    ):
        highestTraffic = "SELATAN"
    else:
        highestTraffic = "UTARA"

    def resetTrafficLight():
        trafficLightBarat["red_start_time"] = 0
        trafficLightTimur["red_start_time"] = 0
        trafficLightUtara["red_start_time"] = 0
        trafficLightSelatan["red_start_time"] = 0
        trafficLightBarat["green_start_time"] = 0
        trafficLightTimur["green_start_time"] = 0
        trafficLightUtara["green_start_time"] = 0
        trafficLightSelatan["green_start_time"] = 0

    if (
        trafficLightBarat["green_start_time"] <= trafficLightBarat["minimumGreenLightCount"] and
        trafficLightTimur["red_start_time"] <= trafficLightTimur["maximumRedTimeTreshold"] and
        (trafficStateCount[0] <= trafficStateCount[1] and trafficStateCount[0] <= trafficStateCount[2] and trafficStateCount[0] <= trafficStateCount[3])
       ):
        print("barat" + str(trafficStateCount))
        if trafficstate != "BARAT":
            print("tes")
            trafficStateCount[3] = trafficStateCount[3] + 1
            resetTrafficLight()
        trafficstate = "BARAT"
        trafficLightBarat["green_start_time"] = trafficLightBarat["green_start_time"] + 1
        trafficLightTimur["red_start_time"] = trafficLightTimur["red_start_time"] + 1
        trafficLightUtara["red_start_time"] = trafficLightUtara["red_start_time"] + 1
        trafficLightSelatan["red_start_time"] = trafficLightSelatan["red_start_time"] + 1
    elif (
        trafficLightTimur["green_start_time"] <= trafficLightTimur["minimumGreenLightCount"] and
        trafficLightSelatan["red_start_time"] <= trafficLightSelatan["maximumRedTimeTreshold"] and
        (trafficStateCount[1] <= trafficStateCount[0] and trafficStateCount[1] <= trafficStateCount[2] and trafficStateCount[1] <= trafficStateCount[3])
        ):
        print("timur" + str(trafficStateCount))
        if trafficstate != "TIMUR":
            trafficStateCount[0] = trafficStateCount[0] + 1
            resetTrafficLight()
        trafficstate = "TIMUR"
        trafficLightBarat["red_start_time"] = trafficLightBarat["red_start_time"] + 1
        trafficLightTimur["green_start_time"] = trafficLightTimur["green_start_time"] + 1
        trafficLightUtara["red_start_time"] = trafficLightUtara["red_start_time"] + 1
        trafficLightSelatan["red_start_time"] = trafficLightSelatan["red_start_time"] + 1
    elif (
        trafficLightSelatan["green_start_time"] <= trafficLightSelatan["minimumGreenLightCount"] and
        trafficLightUtara["red_start_time"] <= trafficLightUtara["maximumRedTimeTreshold"] and
        (trafficStateCount[2] <= trafficStateCount[0] and trafficStateCount[2] <= trafficStateCount[1] and trafficStateCount[2] <= trafficStateCount[3])
    ):
        print("selatan")
        if trafficstate != "SELATAN":
            trafficStateCount[1] = trafficStateCount[1] + 1
            resetTrafficLight()
        trafficstate = "SELATAN"
        trafficLightBarat["red_start_time"] = trafficLightBarat["red_start_time"] + 1
        trafficLightTimur["red_start_time"] = trafficLightTimur["red_start_time"] + 1
        trafficLightUtara["red_start_time"] = trafficLightUtara["red_start_time"] + 1
        trafficLightSelatan["green_start_time"] = trafficLightSelatan["green_start_time"] + 1
    else:
        print("utara")
        if trafficstate != "UTARA":
            trafficStateCount[2] = trafficStateCount[2] + 1
            resetTrafficLight()
        trafficstate = "UTARA"
        trafficLightBarat["red_start_time"] = trafficLightBarat["red_start_time"] + 1
        trafficLightTimur["red_start_time"] = trafficLightTimur["red_start_time"] + 1
        trafficLightUtara["green_start_time"] = trafficLightUtara["green_start_time"] + 1
        trafficLightSelatan["red_start_time"] = trafficLightSelatan["red_start_time"] + 1
    

    print('Traffic Light Paskal Barat Status: ' + str(trafficLightBarat))
    print('Traffic Light Paskal Timur: ' + str(trafficLightTimur))
    print('Traffic Light Paskal Selatan: ' + str(trafficLightUtara))
    print('Traffic Light Paskal Utara: ' + str(trafficLightSelatan))

    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# release resources
videoPaskalBarat.release()
videoPaskalKaliki.release()
videoPaskalKalikiAng.release()
videoPaskalTimur.release()

cv2.destroyAllWindows()        