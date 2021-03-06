import numpy as np
import pyrealsense2 as rs
import cv2

# Configure depth and color stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_record_to_file('test.bag')

# Start streaming
pipeline.start(config)

while True:
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # Convert images to numpy arrays
    depth_img = np.asanyarray(depth_frame.get_data())
    color_img = np.asanyarray(color_frame.get_data())

     # Apply colormap on depth image
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha=0.03), cv2.COLORMAP_JET)

    images = np.hstack((color_img, depth_colormap))
    cv2.imshow('color_image', images)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        pipeline.stop()
        break
