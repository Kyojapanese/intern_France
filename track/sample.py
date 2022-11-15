import cv2 as cv
img = cv.imread('./image/dpg.jpg')
grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
custom_cascade = cv.CascadeClassifier('./cascade/dogtest2.xml')
custom_rect = custom_cascade.detectMultiScale(grayimg, scaleFactor=1.07, minNeighbors=2, minSize=(1, 1))
print(custom_rect)
if len(custom_rect) > 0:
    for rect in custom_rect:
        cv.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0, 255), thickness=3)
cv.imshow('image', img)
cv.waitKey(0)
cv.destroyAllWindows()