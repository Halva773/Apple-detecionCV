from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from split_images import save_images
import cv2
import os


def draw_boxes(image, predictions):
    for prediction in predictions:
        # Центр прямоугольника
        center_x = int(prediction['x'])
        center_y = int(prediction['y'])
        width = int(prediction['width'])
        height = int(prediction['height'])
        confidence = prediction['confidence']

        # Вычисление начальной и конечной точки прямоугольника
        start_point = (center_x - width // 2, center_y - height // 2)
        end_point = (center_x + width // 2, center_y + height // 2)
        color = (0, 255, 0)  # Зеленый цвет для яблок
        thickness = 2

        # Рисуем прямоугольник
        image = cv2.rectangle(image, start_point, end_point, color, thickness)

        # Добавляем текст с уровнем уверенности
        text = f"{confidence:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (0, 0, 255)  # Красный цвет для текста
        font_thickness = 1
        image = cv2.putText(image, text, (start_point[0], start_point[1] - 10), font, font_scale, font_color,
                            font_thickness, cv2.LINE_AA)

    return image


def get_all_files(folder_path):
    try:
        # Получаем список всех файлов и папок в указанной директории
        entries = os.listdir(folder_path)

        # Формируем список полных путей файлов
        return [os.path.join(folder_path, entry) for entry in entries if
                os.path.isfile(os.path.join(folder_path, entry))]

    except Exception as e:
        print(f"Ошибка: {e}")
        return []


if __name__ == '__main__':
    n = 4  # Квадратный корень количества кусков, на которые изображение будет разделено (при n=4 будет 16 кусочков)
    image_path = 'images/DSC01634.JPG'  # Путь к изображению
    output_folder = 'splited-images'  # Путь к папке, куда будут сохраняться кусочки изображения
    threshold = 0.3  # Пороговый уровень уверенности в яблоке на кратинке
    alphavit = 'abcdefghijklmnopqrstuvwxyz'

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="JJBJxldWGHzfpkUGxBVb"
    )

    filename = str(image_path.split('/')[1].split('.')[0])
    save_images(image_path, output_folder, n)

    custom_configuration = InferenceConfiguration(confidence_threshold=threshold, iou_threshold=0.7)

    cnt_apples = 0

    for index, image in enumerate(get_all_files(output_folder)):
        img = cv2.imread(image)
        with CLIENT.use_configuration(custom_configuration):
            # result = CLIENT.infer(img, model_id=r"apple-sdwin/1")

            # https://universe.roboflow.com/deep-learning-mqq34/apples-detection-xkhog/model/4
            # Эта модель сильно лучше той, что выше
            result = CLIENT.infer(img, model_id="apples-detection-xkhog/4")

        cnt_apples += len(result['predictions'])

        img_with_boxes = draw_boxes(img, result['predictions'])

        output_path = f'detected-images/{filename}_{alphavit[index]}_{threshold}.jpg'
        cv2.imwrite(output_path, img_with_boxes)
    print(cnt_apples)