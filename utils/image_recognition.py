from ultralytics import YOLO
import cv2
import os
import re
from pathlib import Path



def detect_objects(model_path, image_path, output_dir="output_image", show_image=False,base_name="output", extension="png",img_size=640):
    # Load the YOLOv11 model
    model = YOLO(model_path)

    # Read the input image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not load image at {image_path}")
    image = cv2.resize(image, (img_size, img_size))
    # Perform detection
    results = model(image)[0]

    # Process results

    for box in results.boxes:
        # Get bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0].item()
        class_id = int(box.cls[0].item())
        class_name = model.names[class_id]

        # Draw bounding box with thinner line (thickness 1)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

        # Prepare label with class name and confidence
        label = f"{class_name}: {confidence:.2f}"

        # Draw label background, adjusted for smaller font
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        cv2.rectangle(image, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)

        # Draw label text with smaller font (0.4)
        cv2.putText(image, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # Get the next available filename
    from .util import get_next_filename
    output_path = get_next_filename(output_dir, base_name, extension)


    # Save the output image
    cv2.imwrite(output_path, image)
    print(f"Output image saved to {output_path}")

    # Optionally display the image
    if show_image:
        cv2.imshow("YOLOv11 Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_image_or_folder(model_path, image_path, output_dir,show_image=False, base_name="out", extension='png',img_size=640):
    """
    Process a single image or all images in a folder using the provided image_processor function.

    Args:
        input_path (str): Path to an image file or a folder containing images.
        image_processor (callable): Function to process each image, takes image path as argument.
    """
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

    if not output_dir.exists():
        os.makedirs(output_dir)
    if image_path.is_file():
        # Check if the file is an image
        if image_path.suffix.lower() in image_extensions:
            print(f"Processing single image: {image_path}")
            detect_objects(model_path, image_path, output_dir,show_image, base_name, extension,img_size=img_size)
        else:
            print(f"Error: '{image_path}' is not a supported image format.")

    elif image_path.is_dir():
        # Process all images in the folder
        print(f"Processing images in folder: {image_path}")
        for file_path in image_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                print(f"Processing image: {file_path}")
                detect_objects(model_path, file_path, output_dir,show_image, base_name, extension,img_size=img_size)
        print("Folder processing completed.")

    else:
        print(f"Error: '{image_path}' is neither a file nor a folder.")



def img_recognition(config):
    # Specify paths
    model_path = Path(config["model_path"])  # Replace with your .pt file path
    image_path = Path(config["input_image_path"])  # Replace with your image path
    output_dir = Path(config["output_image_path"])  # Output directory
    base_name = "output"  # Base name for output files
    extension = "png"  # File extension

    # Check if files exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    # Run detection
    process_image_or_folder(model_path, image_path, output_dir,show_image=False, base_name=base_name, extension=extension,img_size=config["image_size"])