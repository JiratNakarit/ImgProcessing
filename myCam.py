import numpy as np
import cv2
import pyrealsense2 as rs

class myCamera:

    def __init__(self, X=424, Y=270, FRAMERATE=30):

        # Configure depth and color stream
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, X, Y, rs.format.z16, FRAMERATE)
        self.config.enable_stream(rs.stream.color, X, Y ,rs.format.bgr8, FRAMERATE)

    def start(self):
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

    def show_result(self):
        # Stack both images horizontally
        images = np.hstack((self.color_img, self.depth_colormap))

        cv2.imshow('IMAGE', images)
        if cv2.waitKey(1) == 27:
            return True
        else:
            return False




