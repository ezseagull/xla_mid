import cv2
import numpy as np
import matplotlib.image as mpimage
import matplotlib.pyplot as plt

img1 = cv2.imread('data/chinh.jpg')
# def randomDraw(img1):
cp = img1.copy()

img = cv2.resize(img1, (400, 400))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(img, 100, 200)

# define a (3, 3) structuring element
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# apply the dilation operation to the edged image
dilate = cv2.dilate(edged, kernel, iterations=1)

# find the contours in the dilated image
contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image_copy = img.copy()
image_copy2 = img.copy()

print(len(contours), "objects were found in this image.")

#Vẽ hình lên các vật thể ngẫu nhiên
color = list(np.random.random(size=3) * 256)
ind = np.random.randint(10, 15)
for i in range(ind):
    x1 = np.random.randint(10, len(contours))
    y1 = np.random.randint(0, len(contours))
    x,y,w,h = cv2.boundingRect(contours[x1])
    ((cX, cY), radius) = cv2.minEnclosingCircle(contours[y1])
    color = list(np.random.random(size=3) * 256)
    cv2.circle(cp, (int(cX), int(cY)), int(radius), color, 3)
    cv2.rectangle(cp, (x, y), (x + w, y + h), color, 4)


# cv2.imshow('image', cp)
# cv2.imwrite('image.png', cp)
# cv2.imwrite("l1v.jpg", cp)

# cv2.waitKey()
# x = np.zeros((400,30,3), np.uint8)
# result = np.hstack((img1, x, cp))
# cv2.imshow("Differences", result)  
# cv2.imwrite("l1.jpg", result)

#Xoay hình ngẫu nhiên
numbers = np.random.randint(10, 15)
h, w = img1.shape[0], img1.shape[1]
k = np.random.randint(1, 3)
cpy = img1.copy()
for i in range(k):
    w1 = 30
    h1 = 50
    y = np.random.randint(0, h - h1)
    x = np.random.randint(0, w - w1)
    area = cpy[y:y+h, x:x+w]
    fl = (1, -1)
    cpy[y:y+h, x:x+w] = cv2.flip(area, np.random.choice(fl))
    
#Xóa vật thể
def is_contour_bad(c):
    area= cv2.contourArea(c)
    print(area)
    if  area >100: return False
    return True

mask = np.ones(img1.shape[:2], dtype="uint8") *255
# loop over the contours
for c in contours:
	# if the contour is bad, draw it on the mask
	if is_contour_bad(c):
		cv2.drawContours(mask, [c], -1, (0, 0, 0), -1)

# remove the contours from the image and show the resulting images
image = cv2.bitwise_and(img1, img1, mask=mask)
cv2.imshow("Mask", mask)
cv2.imshow("After", image)
cv2.waitKey(0)
x = np.zeros((400,30,3), np.uint8)
result = np.hstack((img1, x, image))
cv2.imshow("Differences", result)  
cv2.imwrite("l3.jpg", result)
# cv2.imshow('image', cpy)
# cv2.imwrite('image.png', cpy)
# cv2.waitKey()
# x = np.zeros((400,30,3), np.uint8)
# result = np.hstack((img1, x, cpy))
# cv2.imshow("Differences", result)  
# cv2.imwrite("l2.jpg", result)

def get_contour_areas(contours):

    all_areas= []

    for cntIdx, cnt in enumerate(contours):
        area= cv2.contourArea(cnt)
        if area < 20 or area > 100: continue
        all_areas.append(area)

    return all_areas

sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
# largest_item= sorted_contours[25]


#EASY LEVEL
result = np.zeros_like(image_copy)

for i in range(119, 120):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result, [sorted_contours[i]], 0, (0,255,255), cv2.FILLED)
    cv2.imwrite('knife_edge_result6.jpg', result)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)  
for i in range(15, 16):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result, [sorted_contours[i]], 0, (139,255,255), cv2.FILLED)
    cv2.imwrite('knife_edge_result6.jpg', result)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)   
for i in range(16, 17):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result, [sorted_contours[i]], 0, (139,25,255), cv2.FILLED)
    cv2.imwrite('knife_edge_result6.jpg', result)
for i in range(23, 24):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result, [sorted_contours[i]], 0, (139,25,255), cv2.FILLED)
    cv2.imwrite('knife_edge_result6.jpg', result)
dst = cv2.addWeighted(image_copy, 1, result, 0.7,3)
cv2.imwrite('data/easy.jpg', dst)
cv2.imshow("edged",result)
cv2.imshow("edged",dst)


#NORMAL LEVEL
result2 = np.zeros_like(image_copy2)

for i in range(6, 7):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result2, [sorted_contours[i]], 0, (131,139,134), cv2.FILLED)
    cv2.imwrite('knife_edge_result7.jpg', result2)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)
for i in range(7, 8):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result2, [sorted_contours[i]], 0, (0,255,205), cv2.FILLED)
    cv2.imwrite('knife_edge_result7.jpg', result2)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)
for i in range(9, 10):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result2, [sorted_contours[i]], 0, (139,139,131), cv2.FILLED)
    cv2.imwrite('knife_edge_result7.jpg', result2)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)
for i in range(21, 22):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result2, [sorted_contours[i]], 0, (0, 100, 0), cv2.FILLED)
    cv2.imwrite('knife_edge_result7.jpg', result2)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)
for i in range(33, 34):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result2, [sorted_contours[i]], 0, (0,255,205), cv2.FILLED)
    cv2.imwrite('knife_edge_result7.jpg', result2)
   # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)
for i in range(37, 38):
    epsilon = 0.1*cv2.arcLength(sorted_contours[i], True)
    approx = cv2.approxPolyDP(sorted_contours[i], epsilon, False)

    cv2.drawContours(result2, [sorted_contours[i]], 0, (105,105,105), cv2.FILLED)
    cv2.imwrite('knife_edge_result7.jpg', result2)
    # cv2.drawContours(image_copy, sorted_contours[i], -1, (255,255,255),thickness=cv2.FILLED)
dst2 = cv2.addWeighted(image_copy2, 1, result2, 1,3)
cv2.imwrite('data/normal.jpg', dst2)
# cv2.imshow("edged",result2)
# cv2.imshow("edged",dst2)

cv2.waitKey(0)
cv2.destroyAllWindows()