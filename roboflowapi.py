from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import cv2


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

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="JJBJxldWGHzfpkUGxBVb"
)

img = cv2.imread('images/DSC01634.JPG')

threshold = 0.1
custom_configuration = InferenceConfiguration(confidence_threshold=threshold)

with CLIENT.use_configuration(custom_configuration):
    result = CLIENT.infer(img, model_id=r"apple-sdwin/1")


print(len(result['predictions']))

img_with_boxes = draw_boxes(img, result['predictions'])

# Сохраняем результат
output_path = f'images/output_with_boxes_{threshold}.jpg'
cv2.imwrite(output_path, img_with_boxes)
