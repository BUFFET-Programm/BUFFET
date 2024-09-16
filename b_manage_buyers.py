from important_variables import BASE_DIR, TRAINER_FILE_PATH, ALGORITHM_PATH, DATABASE_PATH
import cv2
import numpy as np
from os import mkdir, listdir
from shutil import rmtree
import random
from PIL import Image
from collections import Counter
from b_buyer_log import change_log_name
import sqlite3

size_face_options = ['rotate', 'scale', 'flip', 'translate']
detector = cv2.CascadeClassifier(ALGORITHM_PATH)


def check_name_is_new(name: str) -> bool:
    '''Checks buyer name is unique.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT name FROM buyers')
    names = cursor.fetchall()
    db.close()
    names_ = []
    for n in names:
        names_.append(name[0])
    if name in names_:
        return False
    else:
        return True

def next_id_for_buyer() -> int:
    '''Returns next buyer id for register in trainer.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT id FROM buyers')
    ids = cursor.fetchall()
    ids_ = [id[0] for id in ids]
    ids_.sort()
    try:
        id = ids_[-1]+1
    except:
        id = 1
    db.close()
    return id

def read_all_ids() -> dict[int, str]:
    '''Returns a dict from buyers's name and id.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT id, name FROM buyers')
    data = cursor.fetchall()
    dict = {row[0]: row[1] for row in data}
    db.close()
    return dict

def read_all_buyers_name() -> list:
    'Reads all buyers name.'
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT name FROM buyers')
    data = cursor.fetchall()
    names = [buyer[0] for buyer in data]
    db.close()
    return names

def take_images_from_buyer_face() -> None:
    '''Takes images from buyer face and saves them.'''
    folder_path = BASE_DIR+'/tmp_images'
    try:
        mkdir(folder_path)
    except FileExistsError:
        rmtree(folder_path)
        mkdir(folder_path)
    count = 0
    cap = cv2.VideoCapture(0)
    while count < 70:
        ret, frame = cap.read()
        size = random.choice(size_face_options)
        for (x, y, w, h) in detector.detectMultiScale(frame):
            face = cv2.cvtColor(
                frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            path = folder_path+'/tmp_'+str(count)+'.jpg'
            cv2.imwrite(path, apply_changes(face, size))
            count += 1

def register_buyer_in_database(name: str, charge: int, school: str, class_: str, id: int) -> None:
    '''Inserts buyer info into database.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('INSERT INTO buyers (name, id, school, class, charge) VALUES (?,?,?,?,?)', (name, id, school, class_, charge))
    db.commit()
    db.close()

def register_buyer_in_trainer(id: int) -> None:
    '''Saves buyer's face features in trainer file.'''
    face_samples = []
    ids = []
    folder_path = BASE_DIR+'/tmp_images'
    images_path = listdir(folder_path)
    for image_path in images_path:
        full_image_path = folder_path+'/'+image_path
        image = Image.open(full_image_path)
        np_image = np.array(image)
        face_samples.append(np_image)
        ids.append(id)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if id == 1:
        recognizer.train(face_samples, np.array(ids))
    else:
        recognizer.read(TRAINER_FILE_PATH)
        recognizer.update(face_samples, np.array(ids))
    recognizer.write(TRAINER_FILE_PATH)

def register_buyer(name: str, charge: int, school: str, class_: str) -> None:
    '''A method for call others methods for register buyer.'''
    try:
        id = next_id_for_buyer()
        take_images_from_buyer_face()
        register_buyer_in_trainer(id)
        register_buyer_in_database(name, charge, school, class_, id)
        return True
    except:
        return False

def get_identity() -> str | bool:
        '''Recognizes buyer and returns his name if everything was good.'''
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(TRAINER_FILE_PATH)
        except:
            return 'unknown'
        count = 0
        repetition_list = []
        names_ids_dict = read_all_ids()
        cap = cv2.VideoCapture(0)
        while count < 15:
            ret, frame = cap.read()
            faces = detector.detectMultiScale(frame)
            face = None
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
            try:
                gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            except:
                continue
            for index, confidence in [recognizer.predict(gray)]:
                if (confidence < 80):
                    repetition_list.append(names_ids_dict[index])
                else:
                    repetition_list.append('unknown')
                count += 1
        if len(repetition_list)<10:
            return False
        else:
            repetition = Counter(repetition_list)
            identity = repetition.most_common()[0][0].rstrip()
            return identity

def submit_information() -> list | bool:
    '''Takes buyer name and returns his full information.'''
    name = get_identity()
    if not name:
        return False
    elif name == 'unknown':
        return 'unknown'
    else:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT * FROM buyers WHERE name=?',(name,))
        data = list(cursor.fetchone())
        db.close()
        return (data[0], data[4], data[2], data[3])

def change_buyer_name(previous_name: str, new_name: str) -> None:
    '''Changes buyer name.'''
    try:
        if check_name_is_new(new_name):
            db = sqlite3.connect(DATABASE_PATH)
            db.execute('UPDATE buyers SET name=? WHERE name=?', (new_name, previous_name,))
            db.commit()
            change_log_name(previous_name, new_name)
            db.close()
    except ValueError:
        pass

def change_buyer_face(buyer_name: str) -> None:
    '''Changes buyer face.'''
    try:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT id FROM buyers WHERE name=?', (buyer_name,))
        id = cursor.fetchone()[0]
        take_images_from_buyer_face()
        register_buyer_in_trainer(id)
        db.close()
    except ValueError:
        pass

def apply_changes(image, option) -> Image:
    '''Applies change on image for better image processing and recognition.'''
    if len(image.shape) == 2:
        rows, cols = image.shape
    else:
        rows, cols, _ = image.shape
    if option == 'rotate':
        angle = 45
        rotation_matrix = cv2.getRotationMatrix2D(
            (cols/2, rows/2), angle, 1)
        rotated_image = cv2.warpAffine(
            image, rotation_matrix, (cols, rows))
        return rotated_image
    if option == 'flip':
        flipped_image = cv2.flip(image, 1)
        return flipped_image
    if option == 'scale':
        scale_factor = 1.5
        scaled_image = cv2.resize(
            image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
        return scaled_image
    if option == 'translate':
        x_translation = 50
        y_translation = 30
        translation_matrix = np.float32(
            [[1, 0, x_translation], [0, 1, y_translation]])
        translated_image = cv2.warpAffine(
            image, translation_matrix, (cols, rows))
        return translated_image
