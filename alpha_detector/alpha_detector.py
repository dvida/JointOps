import cv2
import cv2.cv as cv
import numpy as np

img_name = "CR39.jpg"

img = cv2.imread(img_name,0) #Reading image
img = cv2.GaussianBlur(img,(15,15),0) #Kernel size is equal to the noise size
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR) #Converting image to B/W for saving
#cimg = cv2.Canny(cimg, 5, 100, 5)


#cv2.imshow('prep', cimg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

print 'trazim'
circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,40, param1=50,param2=14,minRadius=5,maxRadius=14) #Performing Hough circle transform
# ARGUMENTS:
# CV_HOUGH_GRADIENT: Define the detection method. Currently this is the only one available in OpenCV
# dp = 1: The inverse ratio of resolution
# min_dist = 40: Minimum distance between detected centers
# param_1 = 50: Upper threshold for the internal Canny edge detector
# param_2 = 14*: Threshold for center detection.
# min_radius = 5: Minimum radio to be detected. If unknown, put zero as default.
# max_radius = 20: Maximum radius to be detected. If unknown, put zero as default
print 'gotovo'

try:
	#Draw circles on image
	circles = np.uint16(np.around(circles)) 
	for i in circles[0,:]:
	    # draw the outer circle
	    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
	    # draw the center of the circle
	    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
except:
	img_name += '_NONE_'

#cv2.imshow('detected circles',cimg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

cv2.imwrite(''.join(img_name.split('.')[:-1])+'_count-'+str(len(circles[0]))+'.jpg', cimg)

#gatorz