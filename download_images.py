import requests
from PIL import Image
from io import BytesIO

def download_image(url, path):
    try:
        # Отправляем запрос к URL
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на наличие ошибок

        # Открываем изображение из загруженных данных
        image = Image.open(BytesIO(response.content))

        # Сохраняем изображение на локальный диск
        image.save(path)
        print(f"Изображение успешно сохранено в {path}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке изображения: {e}")
    except IOError as e:
        print(f"Ошибка при сохранении изображения: {e}")

# URL изображения и путь для сохранения
link = r'https://app.roboflow.com/zorinskij-sad-apple/appletree_apples_detection/images/PaUPCTe9mjgePeP5Hybn?jobStatus=assigned&annotationJob=lu8Qhsk3wcdkBqo25EIr'
path = r'C:\Users\Админ\Desktop\Desktop\PyCharm\ComputerVision\images'

# Скачиваем и сохраняем изображение
download_image(link, path)
