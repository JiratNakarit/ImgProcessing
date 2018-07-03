import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color stream
pipeline = rs.pipeline()
config = rs.config()
rs.config.enable_device_from_file(config, 'test.bag')
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
pipeline.start(config)

while True:
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()

     # Apply colormap on depth image
    depth_color_frame = rs.colorizer().colorize(depth_frame)

    # Convert images to numpy arrays
    depth_color_image = np.asanyarray(depth_color_frame.get_data())

    cv2.imshow('depth', depth_color_image)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        pipeline.stop()
        break
