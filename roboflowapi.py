from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from image_processing import split_image, draw_boxes
from local_files import get_all_files
from global_variables import alphavit
import cv2


def get_api(url='https://detect.roboflow.com', key='JJBJxldWGHzfpkUGxBVb'):
    return InferenceHTTPClient(
        api_url=url,
        api_key=key
    )


def picture_apples_detect(image_path, n=4, threshold=0.3, iou_threshold=0.7):
    output_folder = 'splited-images'
    filename = str(image_path.split('/')[1].split('.')[0])
    split_image(image_path, n, output_folder)
    cnt_apples = 0
    for index, image in enumerate(get_all_files(output_folder)):
        cnt_apples_on_image, img_with_boxes = piece_apple_detect(image, threshold, iou_threshold)
        cnt_apples += cnt_apples_on_image
        output_path = f'detected-images/{filename}_{alphavit[index]}_{threshold}.jpg'
        cv2.imwrite(output_path, img_with_boxes)

    return cnt_apples


def piece_apple_detect(image, threshold, iou_threshold):
    CLIENT = get_api()
    custom_configuration = InferenceConfiguration(confidence_threshold=threshold, iou_threshold=iou_threshold)
    img = cv2.imread(image)
    with CLIENT.use_configuration(custom_configuration):
        # https://universe.roboflow.com/deep-learning-mqq34/apples-detection-xkhog/model/4
        result = CLIENT.infer(img, model_id="apples-detection-xkhog/4")
    return len(result['predictions']), draw_boxes(img, result['predictions'])


if __name__ == '__main__':
    picture_apples_detect('images/DSC01634.JPG')
