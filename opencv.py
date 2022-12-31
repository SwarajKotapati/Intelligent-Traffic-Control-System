import cv2
import numpy as np

# Web camera

cap = cv2.VideoCapture('video.mp4')

count_line_position = 550
min_widht_rect = 80 
min_height_rect = 80
offset = 6
car_counter = 0


def center_handle(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)

    cx = x+x1
    cy = y+y1

    return cx,cy

detect = []

#Initialize Background Substractor

algo = cv2.createBackgroundSubtractorMOG2()

while True:
    ret,frame1 = cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    # applying on each frame 
    #find the grey scale gauussian images
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilatada = cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
    counter,h = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #draw line
    cv2.line(frame1,(23,count_line_position),(1200,count_line_position),(255,20,20),3)
    
    for(i,c) in enumerate(counter):
        (x,y,w,h)  = cv2.boundingRect(c)
        validate_counter = (w>=min_widht_rect) and (h>=min_height_rect)

        if not validate_counter:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(10,10,250),2)
        

        center = center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(250,10,10),-1)


        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                car_counter = car_counter+ 1

            cv2.line(frame1,(23,count_line_position),(1200,count_line_position),(255,200,200),3)
            detect.remove((x,y))
            print("Vehicle Counter "+str(car_counter))

            
    cv2.putText(frame1,"VEHICLE COUNTER "+str(car_counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)

    
    # cv2.imshow('Detector',dilatada)



    cv2.imshow('Video Original',frame1)

    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
cap.release()