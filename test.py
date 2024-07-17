from PIL import Image
import os
import math
from roboflowapi import get_all_files


def reconstruct_image(folder_path, n, output_file):
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
        print(f"Итоговое изображение сохранено в {output_file}")

    except Exception as e:
        print(f"Ошибка: {e}")


# Пример использования
folder_path = 'detected-images/'
n = 16
output_file = 'images/complete.jpg'

# Соединяем изображения
reconstruct_image(folder_path, n, output_file)
