import json
import boto3
import random
import datetime
import uuid
import numpy as np
from faker import Faker

fake = Faker()

avg_systolic = 110
systolic_sd = 10

avg_diastolic = 75
diastolic_sd = 5

avg_heart_rate = 90
heart_rate_sd = 10

avg_body_temp = 98.7
body_temp_sd = 0.7

avg_blood_oxygen = 92
blood_oxygen_sd = 5

avg_blood_sugar = 125
blood_sugar_sd = 10

class PatientRecord():
    def __init__(self):
        self.systolic = round(np.random.normal(loc=avg_systolic, scale=systolic_sd))
        self.diastolic = round(np.random.normal(loc=avg_diastolic, scale=diastolic_sd))
        self.heart_rate = round(np.random.normal(loc=avg_heart_rate, scale=heart_rate_sd))
        self.body_temperature = round(np.random.normal(loc=avg_body_temp, scale=body_temp_sd),1)
        self.blood_oxygen = round(np.random.normal(loc=avg_blood_oxygen))
        self.blood_sugar = round(np.random.normal(loc=avg_blood_sugar, scale=blood_sugar_sd))
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.DOB = fake.date_between()
        # self.address = fake.address()
        self.check_in_date = datetime.date.today()
        self.timestamp = datetime.datetime.now()
        self.record_id = str(uuid.uuid4())
        self.patient_id = str(uuid.uuid4())
        
        self.entry = {
            "Record_ID" : self.record_id,
            "Patient_ID" : self.patient_id,
            "First_Name" : self.first_name,
            "Last_Name" : self.last_name,
            "DOB" : self.DOB,
            # "Address" : self.address,
            "Check_In_Date" : self.check_in_date,
            "Record_Timestamp" : self.timestamp,
            "Systolic_BP" : self.systolic,
            "Diastolic_BP" : self.diastolic,
            "Heart_Rate" : self.heart_rate,
            "Body_Temperature" : self.body_temperature,
            "Blood_Oxygen" : self.blood_oxygen,
            "Blood_Sugar" : self.blood_sugar
        }
        
        return
    
    def __eq__(self, other):
        entry1 = self.get_entry()
        entry2 = other.get_entry()
        are_equal = True
        
        for k, v in entry1.items():
            if v == entry2[k]:
                print("Both {} are the same:{}".format(k,v))
            else:
                print("\n{} are not the same:\nR1:{}\nR2:{}".format(k, v, entry2[k]))
                are_equal = False
        
        return are_equal
    
    def print_contents(self):
        print(json.dumps(self.entry, indent=4, default=str))
        
        return
    
    def update_time_stamp(self):
        self.timestamp = datetime.datetime.now()
        self.entry["Record_Timestamp"] = self.timestamp
        
        return
    
    def update_record_id(self):
        self.record_id = str(uuid.uuid4())
        self.entry["Record_ID"] = self.record_id
        
        return
    
    # Use this as a reference for healthy and unhealthy blood pressure ranges
    # https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings 
    def update_systolic(self):
        self.systolic = round(np.random.normal(loc=avg_systolic, scale=systolic_sd))
        self.entry["Systolic_BP"] = self.systolic
        
        return
    
    def update_diastolic(self):
        self.diastolic = round(np.random.normal(loc=avg_diastolic, scale=diastolic_sd))
        self.entry["Diastolic_BP"] = self.diastolic
        
        return
    
    def update_heart_rate(self):
        self.heart_rate = round(np.random.normal(loc=avg_heart_rate, scale=heart_rate_sd))
        self.entry["Heart_Rate"] = self.heart_rate
        
        return
    
    def update_body_temp(self):
        self.body_temperature = round(np.random.normal(loc=avg_body_temp, scale=body_temp_sd), 1)
        self.entry["Body_Temperature"] = self.body_temperature
        
        return
    
    def update_blood_oxygen(self):
        self.blood_oxygen = round(np.random.normal(loc=avg_blood_oxygen, scale=blood_oxygen_sd))
        
        if self.blood_oxygen > 100:
            self.blood_oxygen = 100
        
        self.entry["Blood_Oxygen"] = self.blood_oxygen
        
        return
    
    def update_blood_sugar(self):
        self.blood_sugar = round(np.random.normal(loc=avg_blood_sugar, scale=blood_sugar_sd))
        self.entry["Blood_Sugar"] = self.blood_sugar
        
        return
    
    def update_entry(self):
        self.update_time_stamp()
        self.update_record_id()
        self.update_systolic()
        self.update_diastolic()
        self.update_heart_rate()
        self.update_body_temp()
        self.update_blood_oxygen()
        self.update_blood_sugar()
        
        return
    
    def get_entry(self):
        
        return self.entry