import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox

im = cv2.imread('media/TerusanDiengBarat.png')
plt.imshow(im)
plt.show()
bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)
plt.imshow(output_image)
plt.show()

print('Jumlah mobil terdekteksi: ' + str(label.count('car')))
print('Jumlah bus terdeteksi: ' + str(label.count('bus')))
print('Jumlah truk terdeteksi: ' + str(label.count('truck')))
print('Jumlah motor terdeteksi: ' + str(label.count('motorcycle')))