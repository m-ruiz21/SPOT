import pyrealsense2 as rs

try:
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start streaming
    pipeline.start(config)

    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Initialize histogram bins for depth values
        histogram = [0] * N

        # Calculate bin size
        bin_size = M / N  # Range is from 0 to M meters

        # Count occurrences of each depth value
        depth_array = [[depth_frame.get_distance(x, y) for x in range(640)] for y in range(480)]

        # Perform object detection
        objects_detected = detect_objects(depth_array)
        print("Objects detected:")
        for region, detected in objects_detected.items():
            if detected:
                print(f" - {region}")

        # Print ASCII histogram
        for y in range(480):
            for x in range(640):
                dist = depth_array[y][x]
                if 0 < dist < M:
                    # Determine the bin index for this depth value
                    bin_index = int(dist / bin_size)
                    histogram[bin_index] += 1

        # print("Depth Histogram:")
        # for i, count in enumerate(histogram):
        #     print(f"{i * bin_size:.2f}-{(i + 1) * bin_size:.2f}: {count}")

    exit(0)
except Exception as e:
    print(e)
    pass
