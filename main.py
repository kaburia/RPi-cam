'''
The aim of the main file is to capture images after every set interval of time and save them with a timestamp.
It uses the PiCamera library to interface with the Raspberry Pi camera module.
It also uses the time library to manage the intervals between captures.

After k time intervals, it then runs the speciesnet model then saves the output json with a timestamp
'''

# Image capturing section
from time import sleep
import os
from utils.camera_img import capture_image
from datetime import datetime
from utils.run_model import run_speciesnet

# Set the time to sleep between captures (in seconds)
def sleep_interval(seconds):
    # Set time to sleep
    sleep(seconds)
    print(f"Slept for {seconds} seconds")


k_interval = 10

# Main Loop
def main():
    count = 0

    while True:
        # Get today's date to create a folder for today's images
        todays_date = datetime.now().strftime("%Y-%m-%d")

        # Check if today's folder exists, if not create it
        if not os.path.exists(f'deploy-test-data/{todays_date}'):
            os.makedirs(f'deploy-test-data/{todays_date}', exist_ok=True)

        # Start to capture the image
        image_file = capture_image(todays_date)
        count += 1


        # Sleep for 30 seconds
        sleep_interval(30)

        # Run the species net in divisions of 10
        if count % k_interval == 0:
            input_folder = f'deploy-test-data/{todays_date}'
            model_dir_path = 'model'

            # run speciesnet
            run_speciesnet(input_folder, model_dir_path)
            print(f"Ran SpeciesNet on images in {input_folder}")
            count = 0

if __name__ == "__main__":
    main()


