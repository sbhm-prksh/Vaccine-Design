#Written by Shubham Prakash and Sufi during 01/10/24 to 22/10/24
#Purpose: This script will do three task, first will convert fasta file to csv file.
#Purpose(cont): Then using Algpred2 server, run allergicity test for certain number(input by user) of sequence
#Purpose(cont): Finally using Phobius server, will  detect presence of signal Peptides.

#Input: fasta_file variable. I have named it input.fa. Feel free to change.
#Output: csv_file variable. I have named it output.csv. Feel free to change.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
######################################################################
# STEP-1: FASTA TO CSV
######################################################################
def parse_fasta(file):
    """Parse a FASTA file and return a dictionary with protein IDs and sequences."""
    # Initialize the dictionary to hold your data
    data = {
        'Protein ID': [],
        'Allergen Test':[],
        'Antigen Test':[],
        'Signal P':[],
        'Sequence': []
    }
    
    with open(file, 'r') as f:
        protein_id = ""
        sequence = []
        
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if protein_id:
                    data['Protein ID'].append(protein_id)
                    data['Sequence'].append(''.join(sequence))
                    data['Allergen Test'].append("Pending")
                    data['Antigen Test'].append("Pending")
                    data['Signal P'].append("Pending")
                protein_id = line[1:].split()[0]
                sequence = []
            else:
                sequence.append(line)
        if protein_id:
            data['Protein ID'].append(protein_id)
            data['Sequence'].append(''.join(sequence))
            data['Allergen Test'].append("Pending")
            data['Antigen Test'].append("Pending")
            data['Signal P'].append("Pending")
    return data
def fasta_to_csv(fasta_file, csv_file):
    """Convert FASTA to CSV using pandas."""
    data = parse_fasta(fasta_file)
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

######################################################################
# STEP-2: ALLERGIC CHECK
######################################################################
def get_allergenicity_result(sequence,id,index):
    print("------------------------------------------------------")
    print(f"|   {index + 1}. Attempting: Allergen Test for: {id}  |")

    payload = {
        "name": "Job5",
        "seq": f">Protein\n{sequence}",  # Pass the sequence here
        "terminus": 4,
        "svm_th": 0.3,
    }
    url = "https://webs.iiitd.edu.in/raghava/algpred2/batch_action.php"
    
    r = requests.post(url, data=payload)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            # Find the result in the table (you might need to adjust the index if it's different)
            # result = soup.find_all("td")[6].get_text()  # Assuming the 7th <td> contains the result
            result = soup.find_all("td")[6].get_text().strip()
        except IndexError:
            result = "ERROR:DATA EXTRACTION"
        print(f"|   {index + 1}. Success   : Allergen Test for: {id}  |")
    else:
        result = "ERROR:SERVER"
        print(f"|   {index + 1}. Failed   : Allergen Test for: {id}  |")
    return result
######################################################################
# STEP-3: Signal P Detection
######################################################################
def get_signalP_result(sequence, id, index):
    print("------------------------------------------------------")
    print(f"|      {index + 1}. Detecting: SignalP for: {id}      |")
    payload = {
        "protseq": f">{id}\n{sequence}",
        "format": 'nog',
    }
    url = "https://phobius.sbc.su.se/cgi-bin/predict.pl"
    
    r = requests.post(url, data=payload)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            text = soup.find("pre").get_text()
            if "signal" in text.lower():
                result = "Found"
            else:
                result = "Not Found"
        except IndexError:
            result = "ERROR:DATA EXTRACTION"
        print(f"|      {index + 1}. Success  : SignalP for: {id}      |")
    else:
        result = "ERROR:SERVER"
        print(f"|       {index + 1}. Failed  : SignalP for: {id}      |")
    return result
######################################################################
# DRIVER CODE STARTS
######################################################################
fasta_file = 'input.fa'  # INPUT FASTA File
csv_file = 'output.csv'  # OUTPUT CSV File
print("======================================================")
print("|                 PROCESS INITIATED                  |")
print("======================================================")
print("|                                                    |")
print("| Step1: FASTA to CSV Conversion                     |")
print("| Step2: Allergenicity Test (AlgPred2)               |")
print("| Step3: Signal Peptide Detection (Phobius)          |")
print("|                                                    |")
print("======================================================")
print("|                  STEP-1 INTIATED                   |")
print("======================================================")
wholeTimeStart=time.time()
start_time = time.time()
fasta_to_csv(fasta_file, csv_file)
end_time = time.time()
total_time = end_time - start_time
print(f"| Success: Converted {fasta_file}->{csv_file}  |")
print(f"| Time Taken: {total_time:.2f} sec                               |")
print("======================================================")
print("|                  STEP-1 COMPLETED                  |")
print("======================================================\n\n")
print("======================================================")
print("|                  STEP-2 INTIATED                   |")
print("======================================================")
df = pd.read_csv(csv_file)
num_sequences = int(input(f"|            Total sequences available: {len(df)}        |\n|     How many sequences do you want to process? "))
num_sequences = min(num_sequences, len(df))
start_time = time.time()
for index, row in df.head(num_sequences).iterrows():
    sequence = row['Sequence']
    id = row['Protein ID']
    result = get_allergenicity_result(sequence, id, index)
    df.at[index, 'Allergen Test'] = result
df.to_csv(csv_file, index=False)
end_time = time.time()
total_time = end_time - start_time
print("------------------------------------------------------")
print(f"| Success: Done with Allergen Test.                  |")
print(f"| Check {csv_file}                              |")       
print(f"| Time Taken: {total_time:.2f} sec                              |")
print("======================================================")
print("|                  STEP-2 COMPLETED                  |")
print("======================================================\n\n")
print("======================================================")
print("|                  STEP-3 INTIATED                   |")
print("======================================================")
start_time = time.time()
df = pd.read_csv(csv_file)
for index, row in df.head(num_sequences).iterrows():
    sequence = row['Sequence']
    id = row['Protein ID']
    result = get_signalP_result(sequence, id, index)
    df.at[index, 'Signal P'] = result
df.to_csv(csv_file, index=False)
end_time = time.time()
total_time = end_time - start_time
print("------------------------------------------------------")
print(f"| Success: Done with SignalP Detection.              |")
print(f"| Check {csv_file}                              |")       
print(f"| Time Taken: {total_time:.2f} sec                               |")
print("======================================================")
print("|                  STEP-3 COMPLETED                  |")
print("======================================================")
wholeTimeEnd=time.time()
wholeTotalTime=wholeTimeEnd-wholeTimeStart
print(f"| All three steps successfully completed.            |")
print(f"| Check {csv_file}. Thank You!                  |")       
print(f"| Total Time Taken: {wholeTotalTime:.2f} sec                        |")
print("======================================================")
print("|                PROCESS TERMINATED                  |")
print("======================================================\n\n")




