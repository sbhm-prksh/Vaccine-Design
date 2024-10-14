import urllib.parse
import urllib.request
import csv

# The URL where the form is being submitted
url = "https://www.ddg-pharmfac.net/vaxijen/scripts/VaxiJen_scripts/VaxiJen3.pl"

def submit_form(seq, threshold):
    print(type(threshold))
    data = {
        'seq': seq,
        # "uploaded_file": "(binary)",
        "Target": "parasite",
        "SequenceOnOff": "A",
        "threshold": threshold,

    }
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    try:
        # Sending the POST request
        request = urllib.request.Request(url, data=encoded_data)
        response = urllib.request.urlopen(request)
        response_content = response.read().decode('utf-8')
        print(response_content)
        return response_content

    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
        return None

def check_for_antigen(response_content):
    if '>ANTIGEN<' in response_content:
        return 'Antigen'
    elif '>NON-ANTIGEN<' in response_content:
        return 'Non-Antigen'
    else:
        return 'Unknown'

def main():
    threshold=0.5
    results = []
    
    # Read protein sequences from toCheck.csv
    with open('toCheck.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        test_counter = 1
        for row in reader:
            if row:
                seq = row[0]  # Assuming the protein sequence is in the first column
                # finalSeq = f'>Test{test_counter}\n{seq}'
                print(f'Running Prediction for Sequence-{test_counter}')
                response_content = submit_form(seq, threshold)
                if response_content:
                    # output_filename = f'output{test_counter-1}.html'
                    # with open(output_filename, mode='w') as output_file:
                    #     output_file.write(response_content)
                    result = check_for_antigen(response_content)
                    results.append((seq, result))
                test_counter += 1

    # Write all results to a final result.csv file
    with open('resultVaxigen.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sequence', 'Prediction'])
        writer.writerows(results)
    print("Prediction Completed. Check result.csv")
if __name__ == "__main__":
    main()
