from local_files import get_all_files
from PIL import Image
import os
import cv2
import math


def split_image(image_path, n, output_folder):
    '''
    Функция делит изображения из image_path на n**2 частей и сохраняет кусочки в папку output_folder

    :param image_path: Путь к изображению, которое нужно сплитануть
    :param n: Количество кусочков, на которые делим (Итоговое количество кусочков будет равно n**2)
    :param output_folder: Путь к папке, в которую нужно сохранить кусочки изображения
    :return:
    '''
    try:
        # Открываем изображение
        image = Image.open(image_path)
        width, height = image.size

        # Проверяем, что n - это делитель ширины или высоты изображения
        if width % n != 0 and height % n != 0:
            raise ValueError("Число n должно быть делителем ширины или высоты изображения")

        # Вычисляем размеры кусочков
        piece_width = width // n
        piece_height = height // n

        # Создаем выходную папку, если она не существует
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        alphavit = 'abcdefghijklmnopqrstuvwxyz'
        # Разделяем и сохраняем части изображения
        piece_number = 0
        for i in range(0, width, piece_width):
            for j in range(0, height, piece_height):
                box = (i, j, i + piece_width, j + piece_height)
                piece = image.crop(box)
                piece_filename = os.path.join(output_folder, f"piece_{alphavit[piece_number]}.jpg")
                piece.save(piece_filename)
                piece_number += 1

        print(f"{piece_number} частей изображения сохранено в {output_folder}")

    except Exception as e:
        print(f"Ошибка: {e}")


def draw_boxes(image, predictions):
    '''
    Функция принимает изображение (cv2.imread()) и координаты, размеры предпологаемых яблок. Функция рисует
    прямоугольники, ориентируясь на predictions

    :param image:
    :param predictions:
    :return:
    '''
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


def reconstruct_image(output_file, n=16, folder_path='detected-images/'):
    '''
    Функция обратно соединяет куочки изображения и дополнительно переворачивает их (так как они были перевёрнуты раньше
    при сплите)

    :param output_file: Путь к файлу, в который сохраеняется соеденённое изображение
    :param n: Количество кусочков
    :param folder_path:
    :return:
    '''
    try:
        # Получаем список всех файлов в папке и сортируем их по имени
        files = get_all_files(folder_path)

        # Проверяем, что количество файлов совпадает с n
        if len(files) != n:
            raise ValueError(f"Количество файлов ({len(files)}) не совпадает с n ({n})")

        # Открываем первое изображение, чтобы получить его размеры
        first_image = Image.open(files[0])
        piece_width, piece_height = first_image.size

        # Определяем размеры итогового изображения
        pieces_per_row = int(math.sqrt(n))
        total_width = piece_height * pieces_per_row
        total_height = piece_width * pieces_per_row

        # Создаем новое изображение для результата
        result_image = Image.new('RGB', (total_width, total_height))

        # Разворачиваем изображения и размещаем их в правильном порядке
        piece_number = 0
        for row in range(pieces_per_row):
            for col in range(pieces_per_row):
                # Индекс для правильного порядка изображений
                correct_index = (pieces_per_row - 1 - row) * pieces_per_row + col
                # Поворачиваем изображение на 90 градусов влево (270 градусов вправо)
                piece = Image.open(files[correct_index]).rotate(90, expand=True)

                # Вычисляем положение текущего кусочка
                x = col * piece_height
                y = row * piece_width

                # Вставляем кусочек в итоговое изображение
                result_image.paste(piece, (x, y))

                piece_number += 1

        # Сохраняем итоговое изображение
        result_image.save(output_file)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    n = 4
    image_path = 'images/DSC01634.JPG'
    output_folder = 'splited-images'

    split_image(image_path, n, output_folder)
