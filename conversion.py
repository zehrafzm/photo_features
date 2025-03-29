# conversion.py
import cv2
import os

def process_file(input_path, output_path, lower_threshold, upper_threshold, is_black_background):
    """
    Processes an image or video file using Canny edge detection.
    Parameters:
        - input_path: Path to the input file.
        - output_path: Path to save the processed file.
        - lower_threshold: Lower threshold for Canny edge detection.
        - upper_threshold: Upper threshold for Canny edge detection.
        - is_black_background: Background color (True for black, False for white).
    """
    # Check the file type
    ext = os.path.splitext(input_path)[-1].lower()

    if ext in [".jpg", ".jpeg", ".png"]:
        # Process image
        process_image(input_path, output_path, lower_threshold, upper_threshold, is_black_background)
    elif ext in [".mp4", ".avi", ".mov"]:
        # Process video
        process_video(input_path, output_path, lower_threshold, upper_threshold, is_black_background)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def process_image(input_path, output_path, lower_threshold, upper_threshold, is_black_background):
    # Read the image
    image = cv2.imread(input_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, lower_threshold, upper_threshold)

    # Create the output image
    if is_black_background:
        output = cv2.bitwise_not(edges)  # Invert edges for black background
    else:
        output = edges  # White background

    # Save the output image
    cv2.imwrite(output_path, output)

def process_video(input_path, output_path, lower_threshold, upper_threshold, is_black_background):
    import cv2

    # Settings
    scale_percent = 50      # Resize to 50% of original size
    frame_skip = 2          # Process every 2nd frame (reduce FPS by half)

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) / frame_skip  # Adjust output FPS
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate new dimensions
    new_width = int(orig_width * scale_percent / 100)
    new_height = int(orig_height * scale_percent / 100)

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height), isColor=False)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames to reduce workload
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        # Resize frame
        frame = cv2.resize(frame, (new_width, new_height))

        # Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Canny edge detection
        edges = cv2.Canny(gray, lower_threshold, upper_threshold)

        # Invert edges if needed
        if is_black_background:
            output_frame = cv2.bitwise_not(edges)
        else:
            output_frame = edges

        # Write processed frame
        out.write(output_frame)

        frame_count += 1

    cap.release()
    out.release()

"""
def process_video(input_path, output_path, lower_threshold, upper_threshold, is_black_background):
    # Open the video
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4 files
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the output video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, lower_threshold, upper_threshold)

        # Create the output frame
        if is_black_background:
            output_frame = cv2.bitwise_not(edges)  # Invert edges for black background
        else:
            output_frame = edges  # White background

        # Write the frame to the output video
        out.write(output_frame)

    # Release resources
    cap.release()
    out.release()
"""
