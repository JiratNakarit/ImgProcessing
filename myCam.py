import numpy as np
import cv2
import pyrealsense2 as rs

class myCamera:

    def __init__(self, MODESET=None, STORAGESET=None, P=480, FRAMERATE=30):

        def set_mode(MODE, STORAGE):
            if MODE == None:
                pass
            elif MODE == 'record':
                config.enable_record_to_file(STORAGE)
            elif MODE == 'read':
                config.enable_device_from_file(STORAGE)

        # Configure depth and color stream
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Set resolution and frame rate
        if P == 360:
            config.enable_stream(rs.stream.depth, 480, 360, rs.format.z16, FRAMERATE)
            config.enable_stream(rs.stream.color, 480, 360, rs.format.bgr8, FRAMERATE)
        elif P == 480:
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, FRAMERATE)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, FRAMERATE)
        elif P == 720:
            config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, FRAMERATE)
            config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, FRAMERATE)
        else:
            pass

        # Set mode
        set_mode(MODESET, STORAGESET)
        # Start streaming
        self.pipeline.start(config)

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
