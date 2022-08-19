from utility_functions import *

record_objs = create_initial_patient_records(2800)
simulate_patient_monitoring(record_objs, runtime=300, interval=1)
    
# if __name__ == '__main__':
#     records = create_patient_records(5)
#     send_records(records)