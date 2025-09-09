'''
Run the overhead scheme Megadetector + SAHI
- PytorchWildlife --- MDV6-yolov9-e
- SAHI (512,512) overlap 80%
'''

from sahi import AutoDetectionModel
from sahi.predict import  get_sliced_prediction
from PytorchWildlife.models import detection as pw_detection

# Load the detection model
def load_megdet(version="MDV6-yolov9-e", device='cuda'):
    detection_model = pw_detection.MegaDetectorV6(device=device, 
                                              pretrained=True, 
                                              version=version)
    return detection_model

# Configure the Autodetection model for an image
def tiling_with_sahi(image_path,
                model_type='ultralytics',
                model_path="/root/.cache/torch/hub/checkpoints/MDV6-yolov9-e-1280.pt",
                confidence_threshold=0.5,
                device="cuda:0",
                slice_height = 512,
                slice_width = 512,
                overlap_height_ratio = 0.8,
                overlap_width_ratio = 0.8
        ):
    

    # Set up the auto detection
    detection_model = AutoDetectionModel.from_pretrained(
                            model_type=model_type,
                            model_path=model_path,
                            confidence_threshold=confidence_threshold,
                            device=device
                        )
    # Get the results for a single image
    result = get_sliced_prediction(
                image_path,
                detection_model,
                slice_height=slice_height,
                slice_width=slice_width,
                overlap_height_ratio=overlap_height_ratio,
                overlap_width_ratio=overlap_width_ratio
    )

    return result

if __name__ == '__main__':
    # get the megdet to get the path 
    load_megdet()

    # run tiling for one image
    tiling_with_sahi('data/image.jpg')





