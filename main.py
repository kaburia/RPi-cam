'''
The aim of the main file is to capture images after every set interval of time and save them with a timestamp.
It uses the PiCamera library to interface with the Raspberry Pi camera module.
It also uses the time library to manage the intervals between captures.

After k time intervals, it then runs the speciesnet model then saves the output json with a timestamp
'''

# Image capturing section
from picamera import PiCamera
from time import sleep, strftime
import os
import subprocess
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.io as pio
import json
import plotly.graph_objects as go


# Function to capture images at regular intervals
def capture_images(interval, duration, save_dir):
    camera = PiCamera()
    camera.resolution = (1024, 768)  # Set resolution (you can adjust this)
    os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

    end_time = datetime.now().timestamp() + duration
    while datetime.now().timestamp() < end_time:
        timestamp = strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(save_dir, f"image_{timestamp}.jpg")
        camera.capture(image_path)
        print(f"Captured {image_path}")
        sleep(interval)

    camera.close()
    print("Image capturing completed.")


# Function to run the speciesnet model and output json with the timestamp
def run_speciesnet(input_folder, model_path):
    timestamp = strftime("%Y%m%d-%H%M%S")
    output_json = f"predictions_{timestamp}.json"
    command = [
        "python", "-m", "speciesnet.scripts.run_model",
        "--folders", input_folder,
        "--predictions_json", output_json,
        "--model", model_path
    ]
    subprocess.run(command)
    print(f"SpeciesNet model run completed. Predictions saved to {output_json}")
    return output_json


# Main function
def main():
    # Parameters
    interval = 30  # Interval in seconds between image captures
    capture_duration = 600  # Duration for each capture session (10 minutes)
    k_intervals = 50  # Number of capture sessions before running the model
    save_dir = "data"  # Directory to save captured images
    model_path = "model/speciesnet_model.h5"  # Path to the SpeciesNet model
    
    print("Starting RPi Camera monitoring system...")
    print(f"Capture interval: {interval} seconds")
    print(f"Capture duration per session: {capture_duration} seconds")
    print(f"Model will run after every {k_intervals} capture sessions")
    
    session_count = 0
    
    try:
        while True:
            session_count += 1
            print(f"\n--- Starting capture session {session_count} ---")
            
            # Capture images for the specified duration
            capture_images(interval, capture_duration, save_dir)
            
            # Check if it's time to run the model
            if session_count % k_intervals == 0:
                print(f"\n--- Running SpeciesNet model after {k_intervals} sessions ---")
                try:
                    # Run the SpeciesNet model on captured images
                    predictions_file = run_speciesnet(save_dir, model_path)
                    print(f"Model predictions saved to: {predictions_file}")
                    
                    # Optional: Clean up old images to save space
                    # You can uncomment the following lines if you want to remove old images
                    # print("Cleaning up old images...")
                    # for filename in os.listdir(save_dir):
                    #     if filename.endswith('.jpg'):
                    #         os.remove(os.path.join(save_dir, filename))
                    
                except Exception as e:
                    print(f"Error running SpeciesNet model: {e}")
            
            print(f"Session {session_count} completed. Waiting for next session...")
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("RPi Camera monitoring system stopped.")


# Entry point
if __name__ == "__main__":
    main()
