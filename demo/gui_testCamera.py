import cv2
import numpy as np

from variables import coord_yx
from variables import dict_faceColor

# Outputs frames of different colors, including raw (scaled) & combined images
def colorFrames(frame):
	# Gaussian filter is applied to captured image - remove noises
	image_gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
	frame_hsv = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV)	# Converts color-space from BGR to HSV

	maskCount = 6
	# In OpenCV, range is [179, 255, 255]
	# Defines boundaries in HSV for different colors (in order WROYGB)
	# IE hsv_colorRange[2][0] = (np.array([13, 77, 208]) - such is lower-bound of red HSV values
	hsv_colorRange = (	(np.array([0, 0, 176]),		np.array([34, 115, 255])), 	# Bound of white
						(np.array([0, 132, 35]),	np.array([12, 255, 255])),	# Bound of red_low
						(np.array([0, 173, 200]), 	np.array([31, 237, 255])),	# Bound of orange
						(np.array([16, 132, 194]), 	np.array([100, 160, 255])),	# Bound of yellow
						(np.array([45, 53, 88]), 	np.array([91, 255, 255])),	# Bound of green
						(np.array([101, 128, 128]), np.array([150, 255, 255])))	# Bound of blue
	hsv_redHigh = (np.array([170, 50, 50]),	np.array([180, 255, 255]))	# Bound of red_high

	# Sets threshold to the HSV image - iterates over all six colors
	mask_color = []
	[mask_color.append(cv2.inRange(frame_hsv, hsv_colorRange[i][0],	hsv_colorRange[i][1])) for i in range(maskCount)]
	# Sets threshold for high-bound red, given high-bound HSV value
	mask_color[1] = mask_color[1] + cv2.inRange(frame_hsv, hsv_redHigh[0],	hsv_redHigh[1])

	# Combines previous HSV masks together
	kernel = np.ones((5, 5), np.uint8)	# Sets erosion filter factor
	mask_combined = cv2.erode((mask_color[0] + mask_color[1] + mask_color[2] + mask_color[3] + mask_color[4] + mask_color[5]), kernel)
	# Eroding reduces noise in image

	# Resizes raw image from gaussian image
	result_raw = cv2.resize(image_gaussian, (300, 300))
	# Resizes previous individual masks to allow color checking
	result_color = []
	# Applies a bitwise-AND operation on the combined mask and original (blurred) image
	# This allows for a normalised coordinate system afterwards
	[result_color.append(cv2.resize(cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_color[i]), (300, 300))) for i in range(maskCount)]
	result_combined = result_color[0] + result_color[1] + result_color[2] + result_color[3] + result_color[4] + result_color[5]
	# Such will be used during detecting each facelets, per each point in image
	return result_raw, result_combined, result_color # Passes raw, combined, and colored images back to parent function

def readFrame(cap, camera):
	ret, frame = cap.read()
	#frame = cv2.resize(frame, (300, 300))
	result_raw, result_combined, result_color = colorFrames(frame)

	dot_radius = 3
	cubeDir = ("URF", "DLB") # Defines cube direction with tuple of strings
	#color_pixel = ((255 * camera), 0, (255 * abs(camera - 1)))
	dict_colorRGB = {
			'W': (255, 255, 255),
			'R': (255, 0, 0),
			'O': (255, 128, 0),
			'Y': (255, 255, 0),
			'G': (0, 255, 0),
			'B': (0, 0, 255)	}
	for face in range(len(coord_yx[camera])):
		for row in range(len(coord_yx[camera][face])):
			for column in range(len(coord_yx[camera][face][row])):
				coord_xy = (coord_yx[camera][face][row][column][1], coord_yx[camera][face][row][column][0])
				color_pixel_temp = dict_colorRGB.get(dict_faceColor.get(cubeDir[camera][face]))
				# Converts BGR to RGB
				color_pixel = (color_pixel_temp[2], color_pixel_temp[1], color_pixel_temp[0])
				img = cv2.circle(result_raw, coord_xy, dot_radius, (color_pixel), -1)
	return result_raw, result_combined, result_color

def runCam_vidCap():
	return cv2.VideoCapture(0), cv2.VideoCapture(1)

def runCamera():
	# Considers two cameras - runs both simultaneously
	# NB: Change parameters of VideoCapture to change between webcams
	cap_0, cap_1 = runCam_vidCap
	 # Camera 2
	while(True):
		# Capture frame-by-frame by iterating single function readFrame
		# Returns necessary arrays containing color information passed back to parent
		result_raw_0, result_combined_0, result_color_0 = readFrame(cap_0, 0)
		result_raw_1, result_combined_1, result_color_1 = readFrame(cap_1, 1)

		cv2.imshow("Raw 0", result_raw_0)	# Displays image/video in frame
		cv2.imshow("Raw 1", result_raw_1)	# Displays image/video in frame
		cv2.imshow("Combined 0", result_combined_0)
		cv2.imshow("White 1", result_combined_1)

		keystroke = cv2.waitKey(1) & 0xFF	# Recognises keystroke
		if keystroke == 32: # wait for spacebar to run recognition
			cap_0.release()
			cap_1.release()
			break
	cv2.destroyAllWindows()	# With everything done, release capture
	return (result_combined_0, result_combined_1), (result_color_0, result_color_1)