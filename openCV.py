# import time
import cv2
import mss
import numpy as np

jyp_img = cv2.imread('mom.jpeg')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
record = False

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 55, "left": 60, "width": 920, "height": 1200-55}

    while "Screen capturing":
        # last_time = time.time()

        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        # sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # screen = cv2.filter2D(screen, -1, sharpening)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # screen_median = cv2.medianBlur(screen_gray, 5)
        screen_edge = cv2.Canny(screen, 100, 300, 5)

        # img_color = cv2.imread("1.png")

        _, screen_binary = cv2.threshold(screen_edge, 127, 255, 0)
        screen_dilate = cv2.dilate(screen_binary, (3,3))
        
        _, contours_screen, hierarchy = cv2.findContours(screen_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours_screen is not 0:
            for cnt_1 in contours_screen:
                area = cv2.contourArea(cnt_1)
                if area > 20.0:
                    x, y, w, h = cv2.boundingRect(cnt_1)
                    if (50 < w < 600 and 50 < h < 600) or (300 < w < 800 and 300 < h < 800):
                        cv2.drawContours(screen, [cnt_1], 0, (0, 0, 255), 3)  # RED
                        cv2.rectangle(screen, (x,y), (x+w, y+h), (0, 0, 255), 3)
                        jyp_resize = cv2.resize(jyp_img, (w,h))
                        screen[y:y+h, x:x+w] = jyp_resize
                        # print(w, h)
                        # np.copyto(screen, result)



        # count_contours = 0
        # for cnt in contours_screen:
        #     cv2.drawContours(screen, [cnt], 0, (255, 0, 0), 3)  # blue
        #     count_contours += 1
        

        # for cnt in contours_screen:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     if w > 50 and h > 50:
        #         cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 0), -1)
        # cv2.imshow('canny', screen_edge)
        # cv2.imshow('T', screen_dilate)
        # cv2.imshow("result", screen)


        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY))

        # print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit and stop record
        cv2.imshow("result", screen)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            print("stop record")
            record = False
            video.release()
            break
        elif cv2.waitKey(25) & 0xFF == ord("r"):
            print("record start")
            record = True
            video = cv2.VideoWriter("see_yadong" + ".avi", fourcc, 20.0, (screen.shape[1], screen.shape[0]))
        
        if record == True:
            video.write(screen)