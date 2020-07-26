#Video sequence is just a collection of frames or collection of images that runs with respect to time.
#Make code stare at background without hand
#Bring hand in foreground with background
#Apply background-subtraction
#Thresholding is the assigment of pixel intensities to 0’s and 1’s based a particular threshold level so that our object of interest alone is captured from an image.
#Contour is the outline or boundary of an object located in an image.

'''
ToDo's:
	Background Subtraction
	Motion Detection and Thresholding
	Contour Extraction
'''

import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
import mss, os



#-----------------------------------------------------------------------------------------------------------------------------------
#global var
background = None 
_cnt = 0

#-----------------------------------------------------------------------------------------------------------------------------------
#directory operations
dir_path = os.getcwd()
print(dir_path)
full_path = dir_path + '\screenshots'
if not os.path.exists(full_path):
    os.makedirs(full_path)
print(full_path)    



#-----------------------------------------------------------------------------------------------------------------------------------
'''
dst(x,y)=(1−alpha).dst(x,y)+alpha.src(x,y)
Parameters for accumulateWeighted():	
	src – Input image as 1- or 3-channel, 8-bit or 32-bit floating point.
	dst – Accumulator image with the same number of channels as input image, 32-bit or 64-bit floating-point.
	alpha – Weight of the input image.
	mask – Optional operation mask.
The function accumulateWeighted calculates the weighted sum of the input image src and the accumulator dst so that dst becomes a running average of a frame sequence.
alpha regulates the update speed (how fast the accumulator “forgets” about earlier images). The function supports multi-channel images. Each channel is processed independently.


#img - current frame
#avgWeight - threshold to perform running average over images
#accumulateWeighted() - compute running average over background and current frame
'''

def compute_running_average(image, avgWeight):
	global background
	if background is None:
		background = image.copy().astype("float")
		return
	cv2.accumulateWeighted(image, background, avgWeight)

#-----------------------------------------------------------------------------------------------------------------------------------
'''
#Threshold Logic:

#when x(n) is pixel,
	if n >= threshold:
		x(n) = 1
	else:
		x(n) = 0

cv2.contourArea uses green's theorem to find area.
Green's Theorem:
Let 'c' be a positively oriented, piecewise smooth, simple closed curve in a plane, and let d be the region bounded by c. If P and Q are functions of (x, y) defined on an open region containing d and have continuous partial derivatives there, then,
INc(P dx + Q dy) = IN(INd( daba Q / daba x - daba P / daba y)) dx dy
where, IN - integral


#cv2.findContours() --> image, retrievalmode, approximationmethod
#cv2.RETR_EXTERNAL --> 	retrieves only the extreme outer contours. 
#cv2.CHAIN_APPROX_SIMPLE --> compresses horizontal, vertical, and diagonal segments and leaves only their end points. For example, an up-right rectangular contour is encoded with 4 points. 
'''

def segmentation(image, threshold=25):
	global background

	diff = cv2.absdiff(background.astype("uint8"), image) #absolute difference between background and image(current frame)
    #print(diff)

	thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1] #cv2.threshold() returns two o/p. First is retval and second is threshold image. Hence, we choose second val [1]
    #print(thresholded)

	(_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Finds contours in a binary image. 
    #print(cnt)

	if len(cnts) == 0:
		return
	else:
		segmented = max(cnts, key = cv2.contourArea)
		return (thresholded, segmented)

#-----------------------------------------------------------------------------------------------------------------------------------
'''
Four Intermediate Steps

    1. Find the convex hull of the segmented hand region (which is a contour) and compute the most extreme points in the convex hull (Extreme Top, Extreme Bottom, Extreme Left, Extreme Right).
    2. Find the center of palm using these extremes points in the convex hull.
    3. Using the palm’s center, construct a circle with the maximum Euclidean distance (between the palm’s center and the extreme points) as radius.
    4. Perform bitwise AND operation between the thresholded hand image (frame) and the circular ROI (mask). This reveals the finger slices, which could further be used to calcualate the number of fingers shown.

convex_hull of 2d points using Sklansky's Algorithm (OpenCV Doc)
'''

def count_fingers(thresholded, segmented):

    #convex hull of segmented region
    conver_hull = cv2.convexHull(segmented)
    
    #extremePoints in the convex hull
    extreme_top = tuple(convex_hull[convex_hull[:, :, 1].argmin()][0]) 
    extreme_bottom = tuple(convex_hull[convex_hull[:, :, 1].argmax()][0])
    extreme_left = tuple(convex_hull[convex_hull[:, :, 0].argmin()][0])
    extreme_right = tuple(convex_hull[convex_hull[:, :, 0].argmax()][0])
    #print(extreme_top + " " + extreme_bottom + " " + extreme_left + " " + extreme_right)

    #palm center
    cX = (extreme_left[0] + extreme_right[0]) / 2
    cY = (extreme_top[1] + extreme_bottom[1]) / 2
    cX = np.round(cX).astype("int") #convert to int
    cY = np.round(cY).astype("int")

    #maximum euclidean distance between palm center and extremePoints
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]
    #print(maximum_distance)
    
    #Radius of the circle
    radius = int(0.8 * maximum_distance)
    
    #Circumference of the circle
    circumference = (2 * np.pi * radius)

    #extract circulat roi which has palm and fingers
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    print(circular_roi)
    circulat_roi = np.round(circular_roi).astype("int")
    
    #draw roi
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)
    
    #bit-wise AND between thresholded hand using roi as the mask which gives cuts obtained using mask on the thresholded hand
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    #computing contours in the circular ROI
    (_, cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #finger_cnt
    count = 0

    for c in cnts:

        #compute the box of contour
        (x, y, w, h) = cv2.boundingRect(c)

        #increment the count of fingers only if -
        #1. The contour region is not the wrist (bottom area)
        #2. The number of points along the contour does not exceed 25% of the circumference of the circular ROI
        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1
    return count

#-----------------------------------------------------------------------------------------------------------------------------------
def captureScreen(fingers):
    global _cnt
    with mss.mss() as sct:
        filename = sct.shot(mon = -1, output = full_path + '\screenshot_{}.png'.format(str(_cnt)))
        print(filename)
        _cnt = _cnt + 1
        
#-----------------------------------------------------------------------------------------------------------------------------------
def compute():

    #initialize weight for running average
    alphaWeight = 0.5 #if we set lower value, running average will be performed over larger amt of previous frames and vice-a-versa
    stream = 'http://192.168.0.4:8080/video'

    #get the reference to the webcam
    camera = cv2.VideoCapture(stream)

    top, right, bottom, left = 10, 350, 225, 590 #ROI Co-ords
    
    num_frames = 0 #initial number of frames

    while True:
        (_, frame) = camera.read()

        frame = imutils.resize(frame, width=700) #resize frame
        frame = cv2.flip(frame, 1) #flip around x-axis  -- dest(i,j) = src(i,cols-j-1) 
        clone = frame.copy()    

        (height, width) = frame.shape[:2] #get height and width of frame

        #print(str(height) +" "+ str(width))

        roi = frame[top:bottom, right:left] #get roi

        #convert to grayscale and blur
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7,7), 0) #(src ,kernel_size(height and width), sigmaX and sigmaY both set to 0)
        #https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html?highlight=gaussianblur#gaussianblur

        #to get background, keep computing running average till threshold is reached to caliberate our running average model
        if num_frames < 30:
            compute_running_average(gray, alphaWeight)
        else:
            #segment hand region
            hand = segmentation(gray)

            if hand is not None:
                #unpack thresholded image and segmented region
                (thresholded, segmented) = hand
                #print(thresholded)
                #print(segmented)

                #draw segmented region and display the frames
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255)) #(destination_img, contours to draw, contourIdx(-1 denotes all contours are drawn), color)
                

                #count no of count_fingers
                fingers = count_fingers(thresholded, segmented)
                    
                cv2.putText(clone, "Detected Value: "+str(fingers), (70,45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0 , 255), 2)

                #display thresholded image
                cv2.imshow("Thresholded", thresholded)
                captureScreen(fingers)
                
                
        #draw segmented hand
        cv2.rectangle(clone, (left, top), (right,bottom), (0, 255, 0), 2)

        #increment frame counter
        num_frames +=1

        #display frame with segmented hand
        cv2.imshow("Output", clone)

        #terminate condition
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    compute()