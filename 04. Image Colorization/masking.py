import cv2
import numpy as np

# 모델 로드하기
proto = 'models/colorization_deploy_v2.prototxt'
weights = 'models/colorization_release_v2.caffemodel'

net = cv2.dnn.readNetFromCaffe(proto, weights)

pts_in_hull = np.load('models/pts_in_hull.npy')
pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1).astype(np.float32)
net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull]

net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full((1, 313), 2.606, np.float32)]

# 이미지 전처리하기
img = cv2.imread('imgs/05.jpeg')

h, w, c = img.shape

img_input = img.copy()

img_input = img_input.astype('float32') / 255.
img_lab = cv2.cvtColor(img_input, cv2.COLOR_BGR2Lab)
img_l = img_lab[:, :, 0:1] # L채널 추출

blob = cv2.dnn.blobFromImage(img_l, size=(224, 224), mean=[50, 50, 50])

# 이미지 후처리하기
net.setInput(blob)
output = net.forward()

output = output.squeeze().transpose((1, 2, 0))

output_resized = cv2.resize(output, (w, h))

output_lab = np.concatenate([img_l, output_resized], axis=2)

output_bgr = cv2.cvtColor(output_lab, cv2.COLOR_Lab2BGR)
output_bgr = output_bgr * 255.0
output_bgr = np.clip(output_bgr, 0 , 255)
output_bgr = output_bgr.astype('uint8')

mask = np.zeros_like(img, dtype='uint8')
# mask = cv2.circle(mask, center=(260, 260), radius = 200, color = (1,1,1), thickness = -1)
mask = cv2.rectangle(mask, pt1=(224, 97), pt2=(393, 357), thickness=-1, color = (1,1,1))

color = output_bgr * mask
gray = img * (1 - mask)

output2 = color + gray

cv2.imshow('result2', output2)

cv2.imshow('img', img)
cv2.imshow('output', output_bgr)

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("X: " + str(x) + ", Y: " + str(y))
    else:
        pass
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('img', onMouse)

cv2.waitKey(0)
