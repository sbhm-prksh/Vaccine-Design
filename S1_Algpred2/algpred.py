import urllib.parse
import urllib.request
import csv

# The URL where the form is being submitted
url = "https://webs.iiitd.edu.in/raghava/algpred2/batch_action.php"

def submit_form(name, seq, terminus, svm_th):
    data = {
        'name': name,
        'seq': seq,
        'terminus': terminus,
        'svm_th': svm_th,
    }
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    try:
        # Sending the POST request
        request = urllib.request.Request(url, data=encoded_data)
        response = urllib.request.urlopen(request)
        response_content = response.read().decode('utf-8')

        return response_content

    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
        return None

def check_for_allergen(response_content):
    if '<td>Allergen' in response_content:
        return 'Allergen'
    elif '<td>Non-Allergen' in response_content:
        return 'Non-Allergen'
    else:
        return 'Unknown'

def main():
    terminus = 4
    svm_th = 0.5
    results = []
    
    # Read protein sequences from sample.csv
    with open('sample.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        test_counter = 1
        for row in reader:
            if row:
                seq = row[0]  # Assuming the protein sequence is in the first column
                name = 'Job1'
                finalSeq = f'>Test{test_counter}\n{seq}'
                print(f'Running Prediction for Sequence-{test_counter}')
                response_content = submit_form(name, finalSeq, terminus, svm_th)
                
                if response_content:
                    # output_filename = f'output{test_counter-1}.html'
                    # with open(output_filename, mode='w') as output_file:
                    #     output_file.write(response_content)
                    result = check_for_allergen(response_content)
                    results.append((seq, result))
                test_counter += 1

    # Write all results to a final result.csv file
    with open('resultAlgpred.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sequence', 'Prediction'])
        writer.writerows(results)
    print("Prediction Completed. Check result.csv")
if __name__ == "__main__":
    main()
