from PIL import Image
import os


def split_image(image_path, n, output_folder):
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

        # Разделяем и сохраняем части изображения
        piece_number = 0
        for i in range(0, width, piece_width):
            for j in range(0, height, piece_height):
                box = (i, j, i + piece_width, j + piece_height)
                piece = image.crop(box)
                piece_filename = os.path.join(output_folder, f"piece_{piece_number}.jpg")
                piece.save(piece_filename)
                piece_number += 1

        print(f"{piece_number} частей изображения сохранено в {output_folder}")

    except Exception as e:
        print(f"Ошибка: {e}")


def save_images(image_path, output_folder, n):
    # Разделяем изображение и сохраняем части
    split_image(image_path, n, output_folder)


if __name__ == '__main__':
    n = 4
    image_path = 'images/DSC01634.JPG'
    output_folder = 'splited-images'

    save_images(image_path, output_folder, n)
