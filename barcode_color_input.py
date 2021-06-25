# Python code for Multiple Color Detection 

# import numpy as np 
import cv2 
from pyzbar.pyzbar import decode 
from pyfirmata import util, Arduino
import time


# Capturing video through webcam 
# url = "http://192.168.86.60:4747/video"

myCam = input("Enter Camera Number: ")
webcam = cv2.VideoCapture(int(myCam))
board = Arduino('COM3')
it = util.Iterator(board)
it.start()

led_red = board.get_pin('d:12:o')
led_green = board.get_pin('d:8:o')
button = board.get_pin('d:10:i')

sku_barcode = input("Enter SKU Barcode Number: ")

# Start a while loop 
while(1): 
	
	# Reading the video from the 
	# webcam in image frames 
	_, imageFrame = webcam.read() 
	state = button.read()
    
	barcodes = decode(imageFrame)
	for barcode in barcodes:
	    x, y , w, h = barcode.rect
# 	    sku_barcode = "X0015QGNBL"
	    sku_qrcode = "EU0396"
        #1
	    barcode_info = barcode.data.decode('utf-8')
	    cv2.rectangle(imageFrame, (x, y),(x+w, y+h), (0, 255, 0), 2)
 	    # print(barcode_info)
        #2
	    font = cv2.FONT_HERSHEY_DUPLEX
	    cv2.putText(imageFrame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
	    if state:
 	        led_green.write(1)
 	        sku_barcode = barcode_info
 	        time.sleep(1)
	    if (barcode_info == sku_barcode or barcode_info == sku_qrcode):
 	        led_red.write(0)
 	        led_green.write(1)
 	        print("Right barcode/qrcode")
 	        time.sleep(1)
 	        led_red.write(0)
 	        led_green.write(0)
	    else:
 	        led_red.write(1)
 	        led_green.write(0)
 	        print("Wrong barcode/qrcode")
 	        time.sleep(1)
 	        led_red.write(0)
 	        led_green.write(0)
            
	
	# Program Termination 
	cv2.imshow("Barcode Detection in realtime", imageFrame) 
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		webcam.release()
		cv2.destroyAllWindows() 
		break
