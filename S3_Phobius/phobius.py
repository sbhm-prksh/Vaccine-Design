import urllib.parse
import urllib.request

# The URL where the form is being submitted (replace with your form's URL)
url = "https://phobius.sbc.su.se/cgi-bin/predict.pl"  # Replace with your form action URL

# Define the data to be submitted
data = {
   "protseq": ">sequence_name\nACCTGCAGATGGTGAACATCTCCCTGCGCGTCCTCACCCGCCCCAATGCTGCAGAGCTG",
   "protfile": "",  # Leave blank if not uploading a file
   "format": "nog"
}

# Encode the form data
encoded_data = urllib.parse.urlencode(data).encode('utf-8')

try:
    # Send the POST request
    request = urllib.request.Request(url, data=encoded_data)
    response = urllib.request.urlopen(request)
    response_content = response.read()

    # Write the response to an HTML file
    with open("response.html", "w", encoding="utf-8") as file:
        file.write(response_content.decode('utf-8'))

    print("Form submitted successfully! Check 'response.html' for the server's response.")

except urllib.error.HTTPError as e:
    print(f"HTTP error occurred: {e.code} - {e.reason}")
except urllib.error.URLError as e:
    print(f"URL error occurred: {e.reason}")
