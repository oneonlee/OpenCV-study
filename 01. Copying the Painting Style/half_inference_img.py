import cv2
import numpy as np

net = cv2.dnn.readNetFromTorch('models/instance_norm/the_scream.t7')
net2 = cv2.dnn.readNetFromTorch('models/eccv16/the_wave.t7')
net3 = cv2.dnn.readNetFromTorch('models/instance_norm/feathers.t7')


img = cv2.imread('imgs/hw.jpeg')
cropped_img = img[147:369, 481:811]

h, w, c = cropped_img.shape

cropped_img = cv2.resize(cropped_img, dsize=(500, int(h / w * 500)))

MEAN_VALUE = [103.939, 116.779, 123.680]
blob = cv2.dnn.blobFromImage(cropped_img, mean=MEAN_VALUE)

net.setInput(blob)
output = net.forward()

output = output.squeeze().transpose((1, 2, 0))

output += MEAN_VALUE
output = np.clip(output, 0, 255)
output = output.astype('uint8')

output = cv2.resize(output, (w, h))

net2.setInput(blob)
output2 = net2.forward()

output2 = output2.squeeze().transpose((1, 2, 0))

output2 += MEAN_VALUE
output2 = np.clip(output2, 0, 255)
output2 = output2.astype('uint8')

output2 = cv2.resize(output2, (w, h))


net3.setInput(blob)
output3 = net3.forward()

output3 = output3.squeeze().transpose((1, 2, 0))

output3 += MEAN_VALUE
output3 = np.clip(output3, 0, 255)
output3 = output3.astype('uint8')

output3 = cv2.resize(output3, (w, h))

output = output[0:70 , :]
output2 = output2[70:140 , :]
output3 = output3[140: , :]


output4 = np.concatenate([output, output2, output3], axis = 0)

img[147:369, 481:811] = output4



cv2.imshow('img', img)
# cv2.imshow('img', cropped_img)
cv2.imshow('output', output)


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("X: " + str(x) + ", Y: " + str(y))
    else:
        pass
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('img', onMouse)

cv2.waitKey(0)


