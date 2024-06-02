import io
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from urllib.request import urlopen
from ultralytics import YOLO

def open_file_explorer():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_label.config(text=f"File selected: {file_path}")  # Update the label with the file path
        print(f"File selected: {file_path}")
        return file_path

def infer_model(file_path):
    # Load your YOLOv8n model
    model = YOLO('yolov8_best.pt')

    # Run inference on the image
    results = model([file_path])

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        result.show()  # display to screen
        result.save(filename='result.jpg')


def submit_action():
    file_path = None  # Initialize file_path variable
    label_text = file_path_label.cget("text")
    if ": " in label_text:  # If a file is selected
        file_path = label_text.split(": ")[1]
    else:  # If no file is selected, check for URL
        url = url_entry.get()
        if url:  # If URL is provided
            try:
                with urlopen(url) as response:
                    image_data = response.read()
                    image = Image.open(io.BytesIO(image_data))
                    file_path = "temp_image.jpg"
                    image.save(file_path)
                    file_path_label.config(text=f"URL Image selected: {file_path}")
                    print(f"URL Image selected: {file_path}")
            except Exception as e:
                print(f"Error: {e}")

    if file_path:  # If file_path is not None
        infer_model(file_path)
    else:
        print("Error: No file or URL selected")

    
def open_url():
    url = url_entry.get()
    if url:
        try:
            with urlopen(url) as response:
                image_data = response.read()
                image = Image.open(io.BytesIO(image_data))
                file_path = "insect_image.jpg"
                image.save(file_path)
                file_path_label.config(text=f"URL Image selected: {file_path}")
                print(f"URL Image selected: {file_path}")
        except Exception as e:
            print(f"Error: {e}")

root = tk.Tk()
root.title("Insect Detection Web App")

# Load and set the background image (same as before)
def load_resized_image(path, size):
    image = Image.open(path)
    # Use Image.Resampling.LANCZOS as the resampling filter
    resized_image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)



# Function to resize and load images
# ...

# Create a frame for the images to keep them on the left side
image_frame = tk.Frame(root)
image_frame.pack(side=tk.LEFT)

# Load and display images in a 2x2 grid
photo1 = load_resized_image("C:/Users/shruthi prem/Desktop/tk project/ins1.png", (300, 400))
label1 = tk.Label(image_frame, image=photo1)
label1.grid(row=0, column=0)

photo2 = load_resized_image("C:/Users/shruthi prem/Desktop/tk project/ins2.png", (300, 400))
label2 = tk.Label(image_frame, image=photo2)
label2.grid(row=0, column=1)

photo3 = load_resized_image("C:/Users/shruthi prem/Desktop/tk project/ins3.png", (300, 400))
label3 = tk.Label(image_frame, image=photo3)
label3.grid(row=1, column=0)

photo4 = load_resized_image("C:/Users/shruthi prem/Desktop/tk project/ins4.png", (300, 400))
label4 = tk.Label(image_frame, image=photo4)
label4.grid(row=1, column=1)


# Create a frame for the images to keep them on the left side
# ...

# Load and display images in a 2x2 grid
# ...

banner = tk.Label(root, text="Insect Detection Web App", bg="green", fg="white", font=("Arial", 40, "bold"))
banner.pack(fill=tk.X, anchor=tk.N)

banner_bottom = tk.Label(root, text="Insect Sleuths: Unraveling the Mystery of Pests in Agricultural Crops.\nEmpowering Farmers with Precision Detection for Healthy Harvests!", bg="green", fg="white", font=("Arial", 20, "bold"))
banner_bottom.pack(side=tk.BOTTOM, fill=tk.X)

upload_frame = tk.Frame(root)
upload_frame.pack(pady=70, expand=True, fill=tk.BOTH)

file_frame = tk.Frame(upload_frame)
file_frame.pack(side=tk.TOP, fill=tk.X)

file_path_label = tk.Label(file_frame, text="No file selected", font=("Arial", 14), relief="solid", padx=30, pady=10)
file_path_label.pack(side=tk.BOTTOM)

choose_file_btn = tk.Button(file_frame, text="Choose File", command=open_file_explorer, font=("Arial", 14))
choose_file_btn.pack(side=tk.TOP, padx=30, pady=10)

url_frame = tk.Frame(upload_frame)
url_frame.pack(side=tk.TOP, fill=tk.X)

url_label = tk.Label(url_frame, text="Enter URL:", font=("Arial", 14))
url_label.pack(side=tk.LEFT, padx=30, pady=10)

url_entry = tk.Entry(url_frame, width=50, font=("Arial", 14))
url_entry.pack(side=tk.LEFT, padx=10, pady=10)


submit_frame = tk.Frame(upload_frame)
submit_frame.pack(side=tk.TOP, fill=tk.X)

submit_btn = tk.Button(submit_frame, text="Submit", command=submit_action, font=("Arial", 14))
submit_btn.pack(pady=20,padx=10)

def refresh_action():
    file_path_label.config(text="No file selected")
    url_entry.delete(0, tk.END)

refresh_frame = tk.Frame(upload_frame)
refresh_frame.pack(side=tk.TOP, fill=tk.X)

refresh_btn = tk.Button(refresh_frame, text="Refresh", command=refresh_action, font=("Arial", 14))
refresh_btn.pack(pady=20, padx=10)

root.mainloop()
