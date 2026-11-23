import csv, json

import numpy as np

policy = json.loads('{"INSTANCE": "serving-lab", "ZONE": "lab-zone-a", "authorized_identity": "lab.operator", "prediction_contract": {"request": {"distance_category": "long_distance", "numeric_values": 5}, "response": {"predicted_class": "late"}}, "credentials": "runtime-injected only"}')

incident_evidence_rows = list(csv.DictReader(open('incident_evidence.csv')))

incident_evidence = {}

incident_evidence['phase'] = np.array([r['phase'] for r in incident_evidence_rows])

incident_evidence['INSTANCE'] = np.array([r['INSTANCE'] for r in incident_evidence_rows])

incident_evidence['ZONE'] = np.array([r['ZONE'] for r in incident_evidence_rows])

incident_evidence['authorized_identity'] = np.array([r['authorized_identity'] for r in incident_evidence_rows])

incident_evidence['instance_state'] = np.array([r['instance_state'] for r in incident_evidence_rows])

incident_evidence['process_state'] = np.array([r['process_state'] for r in incident_evidence_rows])

incident_evidence['readiness'] = np.array([r['readiness'] == 'True' for r in incident_evidence_rows])

incident_evidence['prediction_contract_pass'] = np.array([r['prediction_contract_pass'] == 'True' for r in incident_evidence_rows])

incident_evidence['fault_evidence'] = np.array([r['fault_evidence'] for r in incident_evidence_rows])

incident_evidence['hypothesis_result'] = np.array([r['hypothesis_result'] for r in incident_evidence_rows])

incident_evidence['credential_review_pass'] = np.array([r['credential_review_pass'] == 'True' for r in incident_evidence_rows])

hypothesis_command = 'test_hypothesis'

inspect_command = 'inspect'

prediction_command = 'bounded_prediction'

readiness_command = 'readiness'

reconnect_command = 'reconnect'

reproduce_command = 'reproduce_fault'

start_command = 'start'

stop_command = 'stop'

wait_running_command = 'wait_running'

wait_stopped_command = 'wait_stopped'

SUCCESSFUL_HYPOTHESIS = 'runbook-approved service fault reproduced'

import base64, zlib
exec(zlib.decompress(base64.b64decode('eJytVktv3DYQvudX0CfuAirQXGXoEDibxkC7NrzrQ7MQBEbixkxlUqUou5vA/z0zJPWiuC4adC9aDsnhN988K34kmpfqiesVK41Qss22SvKE8CdRcVnyQqvnXtYa1RSlemxqbni21x1fp28I/Pg/DS8Nr4qW/93hLZKRAxWyRTFNCNW80arqQN2RdbUVGd6a4uHUKPPAW9GiCPXj95kJU+Ci4ZWTM22GDd1JKeQXp7ZUUg5vsEpI3lpVn1UnKwDUaF4JaxjNLVRxJN5QIlqCdqWDIFsaYu9YCoQskRFTzJhBfYHAaSW8bvl8y+r6zI9K8wzXh1/zS8KOhmu3fOsQgrXA7nekzzC8awU0dTcPoTxPKHBbgt3hwbk4f3HauxKFx66ekJ99YID2knjO++VA71TEqlO/GMktGtZ6LfaVCuLqyES9Kh94+dc6hXum05J8R1+arqUpxe1Oc5rYf0C5PUpT+0motwX1r+z/9cug2ejOPKyeWI0B2Ku2S2Qf45Io7QVZRihKqL0NxKA3iZDk4GhKrANyF8c+QODEgV5vd/t326sNzS+yRtWiPE1lxCk60E8329kRtx62GSBVWnwD+2z0CHOano5uj1hs8DnzLJvT8y175AUkxhdu6HqKXirjGbIISnASamZ1oSEc+bP1Fc1H5pzqxTmvdZIwF5EEiblWSOBejGfAx14FTf2fl8EdToAe8VszVzhZlg3FZE4OnLDBscyKi4ze3W+319vfaGCokMJa6Q6O1PF6+l5YsRbvIs19ptkjQ2Fw7ve4giQEWC7cQ1RORf+qLVjnoIWVcw4tmuBQ2nqsoxBea9G0HJNkd391tdntPtz/Xnz88/Zm/3Gzu97FbI7qD4yZgDtnhK31UVJ/+oGheC6jIaO7/c3tLUbDGTyznhPHNe1+AZ7p3tx1r4Lab+7+uN6+22/e07H4YrU6Sxo2wrPo4PYk8iIZMXnv/zEAyuHd/t9Y7Rv2Arctvf8ldb2molGtCdP3VZy9vrPJ3s8RP1FekHJvyTLZB9sDQyCFIRtxPrE34nYE6rL4K/M+/Ur0jANS2GGwp0+UECYr30L8k+PVfB2LPqtiYWN/51wNiAxpc2ThgGGfWaKbHAMbjIYH+iYXAxtoDWBHQA2NEG+v+kxDGCFpI8DgkbDbwjTpK0nh5++Tf2Zop763p8vhI6HfYMIcd9zMkdBhhEhfnS8S6npBPykmYf9Kz/W1ZNo9sA2NRyNtZdn1QYIegzV+Etp7awQccSUqGocTnC8gqYx45L8I+dVRr2R9uiQla4A6WPaAiRtkoKC/vPkBlCJSXQ==')), globals())

action0 = inspect_command

action1 = reproduce_command

action2 = hypothesis_command

action3 = stop_command

action4 = wait_stopped_command

action5 = start_command

action6 = wait_running_command

action7 = reconnect_command

action8 = readiness_command

action9 = prediction_command

result = recover([action0,action1,action2,action3,action4,action5,action6,action7,action8,action9])

failed_hypothesis_rows=[dict(incident_evidence_rows[0],hypothesis_result='failed'),dict(incident_evidence_rows[1])]

failed_service_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],prediction_contract_pass=False)]

failed_readiness_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],readiness=False)]

failure_records=[recover(None,failed_hypothesis_rows),recover(None,stop_complete=False),recover(None,failed_service_rows),recover(None,failed_readiness_rows)]