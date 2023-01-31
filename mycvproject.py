# number plate recognition
import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

image = cv2.imread('number_plate.jpg')

# using live image on webcam
# while True:
#         cam = cv2.VideoCapture(0)
#
#         result,image = cam.read()
#         if result:
#                 cv2.imshow("number plate", image)
#                 cv2.waitKey(0)
#                 cv2.destroyAllWindows()
#                 cv2.imwrite("lena_dip.jpg",image)
#                 break
#         else:
#                 print("Recapturing")
image = imutils.resize(image, width=300 )

smt_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray", image)
# cv2.waitKey(0)

smt_gray = cv2.bilateralFilter(smt_gray,11,17,17)

#detecting the edges of smoothened image
edged = cv2.Canny(smt_gray,30,200)
# cv2.imshow("edged gray", image)
# cv2.waitKey(0)

# Contours are defined as the line joining all the points along the boundary of an image that are having the same intensity
cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
# print(cnts)
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
# cv2.imshow("contours",image1)
# cv2.waitKey(0)

# sorting identified counters
cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
# cv2.imshow("Top 30 contours",image2)
# cv2.waitKey(0)

# finding number plate , here counter with 4 sides
i=7 # wats this 7?
for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
                screenCnt = approx
                x, y, w, h = cv2.boundingRect(c)
                new_img = image[y:y + h, x:x + w]
                cv2.imwrite('./' + str(i) + '.png', new_img)
                i += 1
                break
# here        cv2.approxPolyDP is used to get number of sides of polygon
#             cv2.boundingRect(c) : This finds the coordinates of the part identified as the license plate.
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("image with detected license plate", image)
cv2.waitKey(0)

Cropped_loc = './7.png'
cv2.imshow("cropped", cv2.imread(Cropped_loc))
plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
print("Number plate is:", plate,type(plate))

# cv2.destroyAllWindows()