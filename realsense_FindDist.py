import numpy as np
import cv2
import pyrealsense2 as pyrs

class camera:

    def __init__(self):
        # Configure depth and color stream
        self.pipeline = pyrs.pipeline()
        self.config = pyrs.config()
        self.config.enable_stream(pyrs.stream.depth, 640, 480, pyrs.format.z16, 30)
        self.config.enable_stream(pyrs.stream.color, 640, 480 ,pyrs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(self.config)

    def initial(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        self.depth_frame = frames.get_depth_frame()
        self.color_frame = frames.get_color_frame()

        # Convert images to numpy arrays
        self.depth_img = np.asanyarray(self.depth_frame.get_data())
        self.color_img = np.asanyarray(self.color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        self.depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_img, alpha=0.03), cv2.COLORMAP_JET)

    def final(self):
        cv2.destroyAllWindows()
        self.pipeline.stop()

    def find_contours(self):
        img_gray = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img_gray,100,200)
        thresh = cv2.adaptiveThreshold(edges, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 6)
        img_cont, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def find_4angle(self,contours,condition_area=1000):
        selected_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt) >= condition_area:
                epsilon = 0.1*cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,epsilon,True)
                if len(approx) == 4:
                    selected_contours.append(cnt)
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    depth = self.depth_frame.get_distance(cx,cy)
                    if depth != 0.0:
                        cv2.putText(self.color_img, str(depth),(500,100), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,0),2,cv2.LINE_AA)
        cv2.drawContours(self.color_img, selected_contours, -1, (0,0,255), 3)

    def show_result(self):
        # Stack both images horizontally
        images = np.hstack((self.color_img, self.depth_colormap))

        cv2.imshow('color_image', images)
        if cv2.waitKey(1) == 27:
            return True
        else:
            return False

if __name__ == '__main__':
    cam = camera()
    while True:
        cam.initial()
        cnt = cam.find_contours()
        cam.find_4angle(cnt,1000)
        if cam.show_result():
            break
    cam.final()
