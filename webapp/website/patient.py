import datetime
import os
import random
import sqlite3

DB_PATH = '../patients.db'


# generates a list of all patients in the database
def get_all_patients():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS patients (id integer PRIMARY KEY, name text, age integer, "
              "people_counter integer, last_emotion text, last_timestamp text)")
    c.execute("Select * FROM patients")
    patients = c.fetchall()
    conn.close()
    patient_list = []
    for patient in patients:
        patient_list.append(Patient(*patient))
    del patients
    return patient_list


class Patient(object):
    def __init__(self, patient_id=1, name='Billy', age=10, people_counter=0, last_emotion=None, last_timestamp=None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.people_counter = people_counter
        # if _patient_id is in the database, load the people_counter from the database
        self.load()
        self.last_emotion = last_emotion
        self.last_timestamp = last_timestamp
        # We could define other metrics here, like the average emotion, etc.

    def __str__(self):
        return "Patient: " + str(self.patient_id) + " Age: " + str(self.age)

    def __repr__(self):
        return self.__str__()

    def load(self):
        con = sqlite3.connect(DB_PATH)
        c = con.cursor()
        # if the table patients does not exist, create it
        c.execute("CREATE TABLE IF NOT EXISTS patients (id integer PRIMARY KEY, name text, age integer, "
                  "people_counter integer, last_emotion text, last_timestamp text)")
        c.execute("SELECT people_counter FROM patients WHERE id = ?", (self.patient_id,))

        if row := c.fetchone():
            self.people_counter = int(row[0])
            return
        else:
            # if _patient_id is not in the database, create a new patient with the _patient_id and age
            con = sqlite3.connect(DB_PATH)
            c = con.cursor()
            c.execute("Insert into patients (name, age, people_counter) "
                      "values (?, ?, ?)", (self.name, self.age, self.people_counter))
            con.commit()
            con.close()

    def update(self, emotion, timestamp):
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute("UPDATE patients SET (people_counter, last_emotion, last_timestamp) = (?, ?, ?) WHERE id = ?",
                       (self.people_counter, emotion, timestamp, self.patient_id))
        con.commit()
        con.close()

    def mapper(self, emotion):
        self.people_counter += 1
        timestamp = datetime.datetime.now()

        emoji = ''

        if emotion == "happiness":
            emoji = '😃'
        elif emotion == "sadness":
            emoji = '😔'
        elif emotion == "anger":
            emoji = '😠'
        elif emotion == "surprise":
            emoji = '😮'
        elif emotion == "disgust":
            emoji = '🤮'
        elif emotion == "fear":
            emoji = '😨'
        elif emotion == "neutral":
            emoji = '😑'
        self.update(emotion, timestamp)
        return timestamp, emoji
