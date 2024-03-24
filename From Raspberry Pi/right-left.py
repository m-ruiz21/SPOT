import pyrealsense2 as rs
from time import sleep
from servo_send import servo_send

def detect_objects(depth_array):
    height, width = len(depth_array), len(depth_array[0])
    left, middle, right = width // 3, 2 * width // 3, width
    threshold = 0.3  # Threshold for detecting significant difference in depth

    # Calculate average depth in each region
    avg_depth_left = sum(depth_array[y][x] for y in range(height) for x in range(left)) / (height * left)
    avg_depth_middle = sum(depth_array[y][x] for y in range(height) for x in range(left, middle)) / (height * (middle - left))
    avg_depth_right = sum(depth_array[y][x] for y in range(height) for x in range(middle, right)) / (height * (right - middle))

    # Check if the average depth in any region is significantly different
    objects_detected = {
        "left": avg_depth_left < avg_depth_middle - threshold or avg_depth_left < avg_depth_right - threshold,
        "middle": avg_depth_middle < avg_depth_left - threshold or avg_depth_middle < avg_depth_right - threshold,
        "right": avg_depth_right < avg_depth_left - threshold or avg_depth_right < avg_depth_middle - threshold
    }

    return objects_detected

try:
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    pipeline.start(config)

    while True:
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth:
            continue

        depth_array = [[depth.get_distance(x, y) for x in range(640)] for y in range(480)]

        # Perform object detection
        objects_detected = detect_objects(depth_array)
        print("Objects detected:")
        for region, detected in objects_detected.items():
            if detected:
                print(f" - {region}")
        
        objects_detected = detect_objects(depth_array)
                
        # Servo steering logic
        if objects_detected["left"]:
            servo_send(600)  # Steer right
        elif objects_detected["right"]:
            servo_send(100)  # Steer left
        elif objects_detected["middle"]:
            # If the middle is blocked, choose to steer left or right
            # You might want to add more sophisticated logic here
            servo_send(600 if not objects_detected["right"] else 100)
        else:
            servo_send(300)  # Move straight if no object detected                

    exit(0)
except Exception as e:
    print(e)
    pass
