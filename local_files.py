import os


def get_all_files(folder_path):
    '''
    Функция принимает путь к папке и возвращает все файлы, которые находятся в этой папке

    :param folder_path:
    :return:
    '''
    try:
        # Получаем список всех файлов и папок в указанной директории
        entries = os.listdir(folder_path)

        # Формируем список полных путей файлов
        return [os.path.join(folder_path, entry) for entry in entries if
                os.path.isfile(os.path.join(folder_path, entry))]

    except Exception as e:
        print(f"Ошибка: {e}")
        return []