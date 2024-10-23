#Written By Shubham Prakash on 22/10/24
#Purpose: To do the allergen test for the sequence using Algred2
#Input: A CSV file with columns like- Protein ID, Sequence, Allergen Test etc.UPDATE inputFile variable accordingly
#Output: Will modify the Allergen Test column in the input inself
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to send POST request and get the allergenicity result
def get_allergenicity_result(sequence,id):
    print("-----------------------------------------")
    print("Attempting: Allergen Test for : ", id)
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
        print("Success: Allergen Test for : ", id)
    else:
        result = "ERROR:SERVER"
        print("Failed: Allergen Test for : ", id)
    return result
start_time = time.time()
inputFile="smalloutput.csv"
# Read the CSV with the sequences
df = pd.read_csv(inputFile)

# Iterate over each row in the DataFrame and fetch the allergenicity result
for index, row in df.iterrows():
    sequence = row['Sequence']  # Get the sequence
    id=row['Protein ID']
    result = get_allergenicity_result(sequence,id)  # Fetch the result using the function
    
    # Update the 'Allergen Test' column with the fetched result
    df.at[index, 'Allergen Test'] = result

# Save the updated DataFrame back to the CSV
df.to_csv(inputFile, index=False)
print(f"#############################\nCOMPLETED:ALLERGEN TEST\n(Check {inputFile}.csv)")
end_time = time.time()
total_time = end_time - start_time
print(f"Time Taken: {total_time:.2f} sec\n#############################")

