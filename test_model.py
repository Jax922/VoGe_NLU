import requests
import csv
import json

# def test_rasa_nlu(file_path, rasa_server_url):
#     total = 0
#     errors = 0

#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             payload = {"text": line.strip()}
#             response = requests.post(rasa_server_url + "/model/parse", json=payload)
#             result = response.json()

#             expected_intent = "highlight" 
#             predicted_intent = result.get("intent", {}).get("name")

#             if predicted_intent != expected_intent:
#                 errors += 1
#             total += 1

#     error_rate = errors / total
#     return error_rate

def test_rasa_nlu(file_path, rasa_server_url, output_csv):
    total = 0
    acc = 0
    expected_intent = "highlight"
    with open(file_path, 'r', encoding='utf-8') as file, \
         open(output_csv, 'w', newline='', encoding='utf-8') as out_file:
        
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(["Test Sentence", "Predicted Intent"])

        for line in file:
            payload = {"text": line.strip()}
            response = requests.post(rasa_server_url + "/model/parse", json=payload)
            result = response.json()
            if(result.get("intent", {}).get("confidence") > 0.8):
                if result.get("intent", {}).get("name") == expected_intent:
                    acc += 1
                predicted_intent = result.get("intent", {}).get("name", "No intent detected")
            else:
                predicted_intent = "No intent detected"
            csv_writer.writerow([line.strip(), predicted_intent])
            total += 1

    acc_rate = acc / total
    print(f"Accuracy: {acc_rate}")

test_file_path = './test_data/highlight_real.txt'  
rasa_url = 'http://localhost:5005' 
output_csv_path = './test_data/test_highlight_result.csv'

test_rasa_nlu(test_file_path, rasa_url, output_csv_path)
