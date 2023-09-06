import sys
import pathlib
import shutil
from re import sub


def normalize(filename):
    pattern = r'[^\w.]+'
    return sub(pattern, '_', filename)

def sorted_folder(file_path):

    dict_extension = {

    "images" : ('JPEG', 'PNG', 'JPG', 'SVG'),
    "video" : ('AVI', 'MP4', 'MOV', 'MKV'),
    "documents" : ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    "audio" : ('MP3', 'OGG', 'WAV', 'AMR'),
    "archives" : ('ZIP', 'GZ', 'TAR')

                    }

    known_extension = set()
    unknown_extension = set()

    my_object_folder = pathlib.Path(file_path)

    if my_object_folder.is_file():
        print(f"i'm sorting files in folder")

    if my_object_folder.is_dir():
        if not my_object_folder.iterdir():
            shutil.rmtree(my_object_folder)
        else:
            for files in my_object_folder.iterdir():
                if files.exists() and files.is_file() and not files.name.startswith('.DS_Store'):
                    normalized_filename = normalize(files.name)
                    file_extension = files.suffix[1:].upper()
                    for key, val in dict_extension.items():
                        if file_extension in dict_extension["archives"]:
                            known_extension.add(file_extension)
                            new_folder_path = my_object_folder / key
                            new_folder_path.mkdir(exist_ok=True)
                            shutil.unpack_archive(files, new_folder_path)
                            break
                        elif file_extension in val:
                            known_extension.add(file_extension)
                            new_folder_path = my_object_folder / key
                            new_folder_path.mkdir(exist_ok=True)
                            new_file_path = new_folder_path / normalized_filename
                            files.rename(new_file_path)
                            break
                    else:
                        unknown_extension.add(file_extension)
                        new_folder_path = my_object_folder / 'unknown'
                        new_folder_path.mkdir(exist_ok=True)
                        new_file_path = new_folder_path / normalized_filename
                        files.rename(new_file_path)
                elif files.is_dir():
                    sorted_folder(files)

    print("Known Extensions:", known_extension)
    print("Unknown Extensions:", unknown_extension)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Приклад запуску: script.py "/home/user/папка яку треба розібрати"')
    else:
        file_path = sys.argv[1]
        sorted_folder(file_path)