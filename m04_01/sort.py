import os
import re
import logging
import threading

log = logging.getLogger(__name__)

from optparse import OptionParser
import time
import shutil
import zipfile
from threading import Thread, Semaphore, RLock, current_thread

parser = OptionParser()
parser.add_option("-p", "--path", dest="directory_path",
                  default='/Users/nataliia.kovalchuk/Downloads/thresh/',
                  help="write path to directory, where files are going to be sorted")
(options, args) = parser.parse_args()


def sort_all_files(subdirectory):
    path, name = os.path.split(subdirectory)
    sorting_directories = ["images", "documents", "audio", "video", "archives"]
    new_name = normalize(directory=subdirectory, is_directory=True)
    print("DIR path")
    print(subdirectory)

    if name not in sorting_directories:

        # rename all directories
        if os.path.join(path, name) != os.path.join(path, new_name):
            try:
                os.rename(os.path.join(path, name), os.path.join(path, new_name))
            except:
                print("Directory is already renamed")

        # remove empty directory
        if len(os.listdir(subdirectory)) == 0:
            shutil.rmtree(subdirectory)

        # sorting information
        print(f"FYI: In the directory {subdirectory}:")
        print(add_new_directory(subdirectory))

        files = [f.name for f in os.scandir(subdirectory) if f.is_file()]

        # rename files
        for f in files:
            new_name = normalize(file=f)
            if os.path.join(subdirectory, f) != os.path.join(subdirectory, new_name):
                os.rename(os.path.join(subdirectory, f), os.path.join(subdirectory, new_name))

        for sorting_directory in sorting_directories:
            print("IN the loop")
            print(files)
            # sort files according to their extensions and move them to the corresponding sorting_directories
            move_files_to_sorting_directory(subdirectory, os.path.join(subdirectory, sorting_directory),
                                            define_all_files(files))
            # unzippe the archive file
            re_archives(os.path.join(subdirectory, sorting_directory))


def define_all_files(files):
    image_extensions = [element.lower() for element in ['.JPEG', '.PNG', '.JPG', '.SVG']]
    video_extensions = [element.lower() for element in ['.AVI', '.MP4', '.MOV', '.MKV']]
    doc_extensions = [element.lower() for element in ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']]
    music_extensions = [element.lower() for element in ['.MP3', '.OGG', '.WAV', '.AMR']]
    archive_extensions = [element.lower() for element in ['.ZIP', '.GZ', '.TAR']]

    all_images = []
    all_videos = []
    all_docs = []
    all_musics = []
    all_archives = []
    all_others = []
    found_known_extensions = []
    found_unknown_extensions = []
    for f in files:

        if f.lower().endswith(tuple(image_extensions)):
            found_known_extensions.append(re.findall(r'[.]\w+$', f.lower())[0])
            all_images.append(f)
        elif f.lower().endswith(tuple(video_extensions)):
            found_known_extensions.append(re.findall(r'[.]\w+$', f.lower())[0])
            all_videos.append(f)
        elif f.lower().endswith(tuple(doc_extensions)):
            found_known_extensions.append(re.findall(r'[.]\w+$', f.lower())[0])
            all_docs.append(f)
        elif f.lower().endswith(tuple(music_extensions)):
            found_known_extensions.append(re.findall(r'[.]\w+$', f.lower())[0])
            all_musics.append(f)
        elif f.lower().endswith(tuple(archive_extensions)):
            found_known_extensions.append(re.findall(r'[.]\w+$', f.lower())[0])
            all_archives.append(f)
        else:
            try:
                found_unknown_extensions.append(re.findall(r'[.]\w+$', f.lower())[0])
                all_others.append(f)
            except:
                print("OH NOOOOO:  This is a strange extension: ")
                print(f)

    found_known_extensions = list(set(found_known_extensions))
    found_unknown_extensions = list(set(found_unknown_extensions))
    print(f"these known extensions {found_known_extensions} "
          f"and these unknown extensions {found_unknown_extensions} were found.")

    dict_for_all_files = {}
    file_types = ["images", "video", "documents", "audio", "archives", "others"]
    all_files = [all_images, all_videos, all_docs, all_musics, all_archives, all_others]

    for i in range(len(file_types)):
        dict_for_all_files[file_types[i]] = all_files[i]

    # pprint(dict_for_all_files)
    return dict_for_all_files


def normalize(file='', directory='', is_directory=False):
    # translate CYRILLIC_SYMBOLS into LATIN_SYMBOLS
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    TRANS = {}
    CYRILLIC = tuple([char for char in CYRILLIC_SYMBOLS])

    for cyrillic, latin in zip(CYRILLIC, TRANSLATION):
        TRANS[ord(cyrillic)] = latin
        TRANS[ord(cyrillic.upper())] = latin.upper()

    if is_directory == False:
        # get file name and extension info
        file_name_and_extension = os.path.splitext(file)
        file_name = file_name_and_extension[0]
        # file_name = re.findall(r'^(.*)(?=[.])', file)[0]

        # replace special chars and translate
        file_name_modified = file_name.translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+·"})
        file_name_translated = file_name_modified.translate(TRANS)

        new_file = os.path.join(file_name_translated + file_name_and_extension[1])
        return new_file
    else:
        path, directory_name = os.path.split(directory)
        # replace special chars and translate
        directory_name_modified = directory_name.translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+· "})
        directory_name_translated = directory_name_modified.translate(TRANS)

        new_directory = os.path.join(path, directory_name_translated)
        return new_directory


def add_new_directory(subdirectory):
    all_subdirectory_files = os.listdir(subdirectory)
    new_directory_names = ["images", "documents", "audio", "video", "archives"]
    for new_directory_name in new_directory_names:
        if new_directory_name not in all_subdirectory_files:
            # Path
            path = os.path.join(subdirectory, new_directory_name)
            # Create the directory
            os.mkdir(path)
            return ("Directory '% s' created" % new_directory_name)
        else:
            return ("Directory '% s' was already created before" % new_directory_name)


def move_files_to_sorting_directory(src_directory, dst_directory, dict_with_files):
    path, name = os.path.split(dst_directory)

    if len(dict_with_files[name]) != 0:
        print(f"Move all {name} from {src_directory} to {dst_directory}")
        for file_name in dict_with_files[name]:
            shutil.move(src_directory + "/" + file_name, dst_directory + "/" + file_name)
    return ("Files were moved")


def re_archives(directory):
    path, name = os.path.split(directory)
    archive_extensions = [element.lower() for element in ['.ZIP', '.GZ', '.TAR']]

    if name == "archives":
        for path, currentDirectory, files in os.walk(directory):
            for file in files:
                if re.findall(r'[.]\w+$', file.lower())[0] in archive_extensions:
                    print(os.path.join(path, file))
                    with zipfile.ZipFile(os.path.join(path, file), "r") as zip_ref:
                        zip_ref.extractall(path)
                # print("The unzipped file is going to be remove")
                # file.close()
                # remove(os.path.join(path, file))

class Pool:
    def __init__(self):
        self.active = []
        self.lock = RLock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            log.debug(f'The thread {name} started to work. Active threads in the pool: {self.active}')

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            log.debug(f'The thread {name} finished his work. Active threads in the pool: {self.active}')


def worker(semaphore: Semaphore, pool: Pool, subdirectory):
    log.debug('Wait')
    with semaphore:
        name = current_thread().name
        pool.make_active(name)
        start = time.time()
        sort_all_files(subdirectory)  # sorting files in the given folder
        pool.make_inactive(name)
        # check timing
        elapsed_time = time.time() - start
        print(f"An elapsed time used in each thread: {elapsed_time}")

if __name__ == "__main__":

    """ The default path = /Users/nataliia.kovalchuk/Downloads/thresh/ """
    main_path = options.directory_path
    subdirectories = [x[0] for x in os.walk(main_path)]
    print("subdirectories")
    print(subdirectories)

    # for subdirectory in subdirectories:
        # sort directly
        # sort_all_files(subdirectory)

        # sort using threads
        # start = time.time()
        # thread = Thread(target=sort_all_files, args=(subdirectory,))
        # thread.start()
        # thread.join()
        # elapsed_time = time.time() - start
        # print(f"An elapsed time used in each thread: {elapsed_time}")

    # sort using Semaphore pool
    semaphore = threading.Semaphore(3)
    pool = Pool()
    for subdirectory in subdirectories:
        thread = Thread(name=f'{subdirectory}', target=worker, args=(semaphore, pool, subdirectory))
        thread.start()
