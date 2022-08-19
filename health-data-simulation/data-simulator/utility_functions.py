from PatientRecord import PatientRecord
import csv
from copy import deepcopy
import datetime
import time
import json
import boto3
import uuid
import os

###General Methods###
def validate_updates(record):
    entry1 = deepcopy(record.get_entry())
    record.update_entry()
    entry2 = record.get_entry()
    for k, v in entry1.items():
        if v == entry2[k]:
            print("Both {} are the same:{}".format(k,v))
        else:
            print("\n{} are not the same:\nR1:{}\nR2:{}".format(k, v, entry2[k]))
    
    return

def create_initial_patient_records(n=10):
    records = []
    for i in range(n):
        records.append(PatientRecord())
    return records
    
def combine_records(records, object_name):
    record_entries = []
    
    for record in records:
        record_entries.append(record.entry)
    
    col_names = record_entries[0].keys()
    time_stamp_no_spaces = "-".join(str(datetime.datetime.now()).split(" "))
    time_stamp_no_colon = "-".join(time_stamp_no_spaces.split(":"))
    filepath = object_name + time_stamp_no_colon + ".json"
    
    with open(filepath, 'w') as f:
        json.dump(record_entries, f, default=str)
    
    return filepath
    
def send_records(records, object_name, bucket_name):
    s3 = boto3.client("s3")
    records_filepath = combine_records(records, object_name)
    
    with open(records_filepath, "rb") as f:
        s3.upload_fileobj(f, bucket_name, records_filepath)
        
    os.remove(records_filepath)
    
    return

def simulate_patient_monitoring(patient_records, object_name="OBJECT_NAME", 
bucket_name='BUCKET_NAME', runtime=600, interval=30):
    
    start_time = time.time()
    interval_time = time.time()
    elapsed_time = 0
    
    while(elapsed_time < runtime):
        for record in patient_records:
            record.update_entry()
        
        if time.time() - interval_time > interval:
            send_records(patient_records, object_name, bucket_name)
            interval_time = time.time()
        
        # time.sleep(0.5)
        elapsed_time = time.time() - start_time
    
    return patient_records