import cv2
import numpy as np
import sys
from freenect import sync_get_video as get_video
from freenect import sync_get_depth as get_depth

drawing = list()
drawPoints6 = 0
drawPoints5 = 0
drawPoints4 = 0
drawPoints3 = 0
drawPoints2 = 0
drawPoints1 = 0
drawPoints = 0

def get_our_input(ourDecision):
	vision,depth = get_video(),get_depth()
	lines = 0

	if ourDecision == 1:
		array,_ = vision
		array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
		array2,_ = depth
		_,array2 = cv2.threshold(array2, 600, 255, cv2.THRESH_BINARY_INV)

		try:
			ourTest = np.where(array2 == np.min(array2[np.nonzero(array2)]))

			cv2.circle(array, (ourTest[1][0],ourTest[0][0]), 5, (0,0,255), -1)
			lines = (ourTest[1][0],ourTest[0][0])
		except:
			pass

	return array, lines

ourValue = 1
if __name__ == "__main__":
	while 1:
		try:
			drawPoints6 = drawPoints5
			drawPoints5 = drawPoints4
			drawPoints4 = drawPoints3
			drawPoints3 = drawPoints2
			drawPoints2 = drawPoints1
			
			frame, drawPoints1 = get_our_input(ourValue)
			
			prev_drawPoints = drawPoints
			drawPoints = (int(round(np.average([drawPoints5[0], drawPoints4[0], drawPoints3[0], drawPoints2[0], drawPoints1[0]]))), int(round(np.average([drawPoints5[1], drawPoints4[1], drawPoints3[1], drawPoints2[1], drawPoints1[1]]))))

			drawing.append(drawPoints)
		except:
			frame,_ = get_our_input(ourValue)
			pass

		try:
			prevPointX = drawing[0][0]
			prevPointY = drawing[0][1]
			
		except:
			pass

		for point in drawing:
			ourDistance =((((int(point[1])- int(prevPointY)) **2) + ((int(prevPointX) - int(point[0])) **2)) ** .5)
			if ourDistance <=50:
				cv2.line(frame, (prevPointX,prevPointY), (point[0],point[1]), (0,0,255), 5)

			prevPointX = point[0]
			prevPointY = point[1]	

		frame = cv2.flip(frame,1)
		cv2.putText(frame, "Press Q to Quit, and C to Clear",(40,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,200), 1, cv2.LINE_AA, False)
		cv2.imshow("Camera Feed", frame)

		if cv2.waitKey(5) & 0xFF ==ord('q'):
			break

		elif cv2.waitKey(5) & 0xFF ==ord('1'):
			ourValue = 1
		elif cv2.waitKey(5) & 0xFF ==ord('c'):
			drawing = list()
