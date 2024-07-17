from roboflowapi import picture_apples_detect
from image_processing import reconstruct_image
from decorators import timer

@timer
def detect_all_apples(input_file, output_file):
    '''
    Функция для распознования яблок на 1 изображении

    :param input_file:
    :param output_file:
    :return:
    '''
    cnt_apples = picture_apples_detect(input_file, n=2)
    reconstruct_image(output_file)
    print(f"Итоговое изображение сохранено в {output_file}. Найдено {cnt_apples} яблок")


if __name__ == '__main__':
    detect_all_apples('images/DSC01634.JPG', 'images/Complete_DSC01634.JPG')
