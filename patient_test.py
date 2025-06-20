import datetime

import sqlite3

from PIL import Image


DB_PATH = 'testing_database.db'


# generates a list of all patients in the database
def get_all_patients():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("Select * FROM Patient")
    patients = c.fetchall()
    conn.close()
    patient_list = []
    for patient in patients:
        patient_list.append(Patient(*patient[0:10]))
    del patients
    return patient_list


class Patient(object):
    def __init__(self, patient_id=1, user_id=0, name='Billy', people_counter=0, photo=None, emoji=None,
                 last_timestamp=None, last_emotion=None, supervisor='Micheal', admin='Micheal'):

        self.patient_id = patient_id
        self.name = name
        self.people_counter = people_counter
        self.supervisor = supervisor
        self.emotion = last_emotion
        self.admin = admin
        self.timestamp = last_timestamp
        self.user_id = user_id
        self.photo = photo
        self.emoji = emoji
        # if _patient_id is in the database, load the people_counter from the database
        self.load()

        # We could define other metrics here, like the average emotion, etc.

    def __str__(self):
        return "Patient: " + str(self.patient_id) + " Name: " + str(self.name)

    def __repr__(self):
        return self.__str__()

    def load(self):
        con = sqlite3.connect(DB_PATH)
        c = con.cursor()
        # if the table patients does not exist, create it
        c.execute(
            "CREATE TABLE IF NOT EXISTS Patient (id integer PRIMARY KEY, user_id integer, name text, timestamp text,"
            "people_counter integer, photo blob, emotion text, emoji blob, supervisor text, admin text, evaluation text, face_id text, FOREIGN KEY(user_id) REFERENCES user(id))")
        c.execute("SELECT * FROM Patient WHERE user_id = ?", (str(self.user_id),))
        row = c.fetchone()
        if row:
            self.user_id, self.name, self.timestamp, self.people_counter, self.photo, self.emotion, self.emoji, self.supervisor, self.admin = row[
                                                                                                                                              1:10]
            return
        else:
            # if _patient_id is not in the database, create a new patient with the _patient_id and age
            con = sqlite3.connect(DB_PATH)
            c = con.cursor()
            c.execute("Insert into Patient (name, people_counter, supervisor, emotion, admin, timestamp) "
                      "values (?, ?, ?, ?, ?, ?)",
                      (self.name, self.people_counter, self.supervisor, self.emotion, self.admin, self.timestamp))
            con.commit()
            con.close()

    '''def update(self, emotion, timestamp):
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute("UPDATE patients SET (people_counter, last_emotion, last_timestamp) = (?, ?, ?) WHERE id = ?",
                       (self.people_counter, emotion, timestamp, self.patient_id))
        con.commit()
        con.close()'''

    def mapper(self, emotion):
        self.people_counter += 1
        timestamp = datetime.datetime.now()
        emoji = ''
        if emotion == "happiness":
            emoji = '😃'
            img = Image.open("website/static/emojis/happiness.png")
        elif emotion == "sadness":
            emoji = '😔'
            img = Image.open("website/static/emojis/sadness.png")
        elif emotion == "anger":
            emoji = '😠'
            img = Image.open("website/static/emojis/anger.png")
        elif emotion == "surprise":
            emoji = '😮'
            img = Image.open("website/static/emojis/surprise.png")
        elif emotion == "disgust":
            emoji = '🤮'
            img = Image.open("website/static/emojis/disgust.png")
        elif emotion == "fear":
            emoji = '😨'
            img = Image.open("website/static/emojis/fear.png")
        elif emotion == "neutral":
            emoji = '😑'
            img = Image.open("website/static/emojis/neutral.png")

        return timestamp, emoji
