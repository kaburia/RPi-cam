from picamera import PiCamera
from time import sleep
import os
from datetime import datetime


# get the current time
def get_current_time():
    time_now = datetime.now()
    current_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


# initialize camera
def init_camera(open=True):
    if open:
        camera = PiCamera()
        camera.resolution = (1920, 1080)  # Set resolution to 1080p
        camera.framerate = 30  # Set framerate to 30fps
        # camera.rotation = 180  # Rotate the camera if needed
        # camera.start_preview()
        sleep(2)  # Allow the camera to warm up
        return camera
    else:
        # close the camera
        camera.close()

# take picture
def capture_image(todays_date):
    # set the name of the imae from the current time
    current_time = get_current_time()
    # check if folder exists then create it
    if not os.path.exists('deploy-test-data'):
        os.makedirs('deploy-test-data', exist_ok=True)
    image_name = f"deploy-test-data/{todays_date}/image_{current_time.replace(' ', '_').replace(':', '-')}.jpg"
    # Initialize the camera
    camera = init_camera(open=True)
    # Capture the image
    camera.capture(image_name)
    print(f"Image captured and saved as {image_name}")
    # Close the camera
    init_camera(open=False)
    return image_name