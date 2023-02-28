import re
import json
import csv


def get_department_info(patients):
    setOfDepartments = {}
    for patient in patients:
        if patient["doctor_faculty"] not in setOfDepartments:
            setOfDepartments[patient["doctor_faculty"]] = 1
        else:
            setOfDepartments[patient["doctor_faculty"]] += 1

    return dict(sorted(setOfDepartments.items(), key=lambda item: item[1], reverse=True))


filepath = "Dataset/2020.txt"
# Open the file

# Open the patient.txt file
with open(filepath, "r", encoding="utf-8") as file:
    # Read the file contents
    file_contents = file.read()

# Split the file contents into a list of patient strings
patients = re.split(r"id=", file_contents)[1:]

# Create an empty list to store the patient data dictionaries
patient_data_list = []
index = 0
# Iterate over the list of patient strings
for patient_string in patients:
    index += 1

    # Split the patient string into a list of lines
    patient_lines = patient_string.strip().split("\n")
    # Get the patient ID from the first line
    patient_id = int(patient_lines[0])
    # Create empty variables for storing data
    doctor_faculty = ""
    descriptions = []
    dialogues = []
    # print("PATIENTLINES", patient_lines)

    # Iterate over the lines and extract the data
    # buffer = ""
    # diagnosesPresent = False
    # for lineIndex, line in enumerate(patient_lines[1:]):
    #     if line.startswith("Description"):
    #         doctor_faculty = buffer
    #         buffer = ""
    #     elif line.startswith("Dialogue"):
    #         descriptions = buffer
    #         buffer = ""
    #     elif line.startswith("Diagnosis"):
    #         dialogues = buffer
    #         buffer = ""
    #         diagnosesPresent = True
    #         break  # After seeing the diagnosis, we can stop

    # Order: doctorfaculty -> Description -> Dialogue -> Diagnosis
    diagnosisPresent = False
    if "Diagnosis" in patient_lines:
        indexOfDiagnosis = patient_lines.index("Diagnosis")
        diagnoses = patient_lines[indexOfDiagnosis + 1:]
        diagnosisPresent = True
    elif "Diagnosis and suggestions" in patient_lines:
        indexOfDiagnosis = patient_lines.index("Diagnosis and suggestions")
        diagnoses = patient_lines[indexOfDiagnosis + 1:]
        diagnosisPresent = True
    else:
        indexOfDiagnosis = len(patient_lines)
        diagnoses = "None"
    dialoguePresent = False
    if "Dialogue" in patient_lines:
        indexOfDialogue = patient_lines.index("Dialogue")
        dialogues = patient_lines[indexOfDialogue + 1:indexOfDiagnosis]
        dialoguePresent = True
    else:
        dialogues = "None"
    if "Doctor faculty" not in patient_lines:
        continue
    indexOfDoctorFaculty = patient_lines.index("Doctor faculty")
    indexOfDescription = patient_lines.index("Description")

    doctor_faculty = patient_lines[indexOfDoctorFaculty + 1].split(" ")[2]
    if dialoguePresent:
        descriptions = patient_lines[indexOfDescription + 1:indexOfDialogue]
    else:
        # This cuts it either to before Diagnosis, or till end of file
        descriptions = patient_lines[indexOfDescription + 1:indexOfDiagnosis]

    # Create a dictionary for the patient data
    patient_data = {
        "id": patient_id,
        "doctor_faculty": doctor_faculty,
        "description": "".join(descriptions),
        "dialogue": "".join(dialogues),
        "diagnosis": "".join(diagnoses)
    }
    # print(patient_data)

    # Append the patient data dictionary to the list
    topDepartments = ["皮肤科", "妇科", "骨科", "儿科",
                      "泌尿外科", "妇产科", "眼科", "消化内科", "神经内科", "内科"]
    if patient_data["doctor_faculty"] in topDepartments:
        patient_data_list.append(patient_data)


patient_data_list_count = get_department_info(patient_data_list)
print(patient_data_list_count)
json_data = json.dumps(patient_data_list, ensure_ascii=False, indent=4)
# print(json_data)
# Write the JSON object to a file
with open("patient_data.json", "w", encoding="utf-8") as file:
    file.write(json_data)

# Get the keys from the first JSON object
keys = patient_data_list[0].keys()

# Open the CSV file for writing
with open('patient_data.csv', 'w', newline='') as output_file:
    # Create a CSV writer object
    writer = csv.DictWriter(output_file, fieldnames=keys)

    # Write the header row to the CSV file
    writer.writeheader()

    # Write each JSON object as a row to the CSV file
    for json_obj in patient_data_list:
        writer.writerow(json_obj)
