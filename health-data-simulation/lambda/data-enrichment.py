import json
import logging
import boto3
import csv
import datetime
import pymysql
logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger()

rds_endpoint = "INSERT_RDS_ENDPOINT"
rds_user = "INSERT_USERNAME"
rds_password = "INSERT_PASSWORD"
rds_db = "INSERT_DB_NAME"

connection = pymysql.connect(rds_endpoint, rds_user, rds_password, rds_db)


def evaluate_BP(event):
    # https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings
    # Used above site for healthy BP ranges
    
    # logger.info("Evaluating patient BP:")
    
    systolic = event['Systolic_BP']
    diastolic = event['Diastolic_BP']
    
    if systolic < 120 and diastolic < 80:
        event['BP_evaluation'] = "normal"
        
    elif (systolic >= 120 and systolic <= 129) and diastolic < 80:
        event['BP_evaluation'] = "elevated"
        
    elif (systolic >= 130 and systolic <= 139) or (diastolic >= 80 and diastolic <= 89):
        event['BP_evaluation'] = "Hypertension_Stage_I"
        
    elif systolic >= 140 or diastolic >= 90:
        event['BP_evaluation'] = "Hypertension_Stage_II"
        
    elif systolic >= 180 or diastolic >= 120:
        event['BP_evaluation'] = "Hypertensive_Crisis"
        
    return event

def evaluate_HR(event):
    # https://www.heart.org/en/healthy-living/fitness/fitness-basics/target-heart-rates
    # Used above site for healthy HR ranges
    
    # logger.info("Evaluating patient heart rate:")
    
    heart_rate = event['Heart_Rate']
    
    if heart_rate >= 60 and heart_rate <= 100:
        event['Heart_Rate_Eval'] = "normal"
        
    elif heart_rate < 60:
        event["Heart_Rate_Eval"] = "low"
        
    else:
        event["Heart_Rate_Eval"] = "high"
    
    return event

def evaluate_blood_sugar(event):
    # https://www.webmd.com/diabetes/how-sugar-affects-diabetes
    # Used the above site to get rough numbers for this.
    # There didn't seem to be a general consensus on this, so I took some
    # liberties here based on family experience.
    
    # logger.info("Evaluating patient blood sugar:")
    
    blood_sugar = event['Blood_Sugar']
    
    if blood_sugar < 70:
        event["Blood_Sugar_Eval"] = "low"
    
    elif blood_sugar >= 180:
        event["Blood_Sugar_Eval"] = "high"
        
    else:
        event["Blood_Sugar_Eval"] = "normal"
    
    return event

def evaluate_blood_oxygen(event):
    # https://www.health.state.mn.us/diseases/coronavirus/pulseoximeter.html
    # Used the above site for healthy blood oxygen ranges
    
    # logger.info("Evaluating patient blood oxygen levels:")
    
    blood_oxygen = event["Blood_Oxygen"]
    
    if blood_oxygen < 95:
        event["Blood_Oxygen_Eval"] = "low"
        
    else:
        event["Blood_Oxygen_Eval"] = "normal"
        
    return event

def evaluate_body_temp(event):
    # https://www.mayoclinic.org/first-aid/first-aid-fever/basics/art-20056685
    # Used the above site for healthy body temperature ranges
    
    # logger.info("Evaluating patient body temperature:")
    
    body_temp = event["Body_Temperature"]
    
    if body_temp < 97:
        event["Body_Temp_Eval"] = "low"
    
    elif body_temp > 99:
        event["Body_Temp_Eval"] = "high"
        
    else:
        event["Body_Temp_Eval"] = "normal"
    
    return event

def evaluate_patient(event_body):
    logger.info("Evaluating patient metrics:")
    
    for event in event_body:
        event = evaluate_BP(event)
        event = evaluate_HR(event)
        event = evaluate_blood_sugar(event)
        event = evaluate_blood_oxygen(event)
        event = evaluate_body_temp(event)
    
    return event_body
    
def convert_to_csv(record_entries, object_name):
    ##This method doesn't require pandas, so there is no need to create lambda layers
    ##reference: https://www.datasciencelearner.com/convert-python-dict-to-csv-implementation/
    
    col_names = record_entries[0].keys()
    logger.info(col_names)
    object_name_no_ext = object_name.strip(".json")
    filepath = '/tmp/' + object_name_no_ext + ".csv"
    
    with open(filepath, 'w') as csvFile:
        wr = csv.DictWriter(csvFile, fieldnames=col_names)
        wr.writeheader()
        for entry in record_entries:
            wr.writerow(entry)
    
    return filepath
    
def send_to_processed_bucket(csv_filepath, processed_bucket):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(processed_bucket)
    key = csv_filepath.split("/")[2]
    bucket.upload_file(csv_filepath, key)
    
    return

def write_to_rds(processed_events):

    col_names = processed_events[0].keys()
    vals = []
    
    for event in processed_events:
        temp_val = []
        
        for col in col_names:
            temp_val.append(event[col])
        
        vals.append(temp_val)
        
    col_names_str = ",".join(col_names)
    sql = "INSERT INTO PatientMonitoring({}) VALUES ".format(col_names_str)

    with connection.cursor() as cursor:
        cursor.executemany(sql+"(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", vals)
        connection.commit()
        
    connection.close()
        
    return

def lambda_handler(event, context):
    # TODO implement
    
    logger.info(json.dumps(event, indent=4))
    
    # User these lines if you use SQS as the trigger#
    body_dict = json.loads(event['Records'][0]['body'])
    logger.info(json.dumps(body_dict, indent=4))
    filepath = body_dict['Records'][0]['s3']['object']['key']
    bucket_name = body_dict['Records'][0]['s3']['bucket']['name']
    #################################################
    
    # Use these lines if you use Lambda as the trigger#
    # filepath = event['Records'][0]['s3']['object']['key']
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    ###################################################
    
    logger.info(filepath)
    logger.info(bucket_name)
    
    # bucket_name = 'daniel-ab2-patient-monitor-raw'
    
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, filepath)
    event_body = json.loads(obj.get()['Body'].read())
    
    logger.info("event_body before processing:")
    logger.info(event_body[0])
    
    processed_events = evaluate_patient(event_body)
    logger.info("Patient Evaluation finished.  Results:")
    logger.info(processed_events[0])
    
    csv_filepath = convert_to_csv(processed_events, filepath)
    send_to_processed_bucket(csv_filepath)
    write_to_rds(processed_events)
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

