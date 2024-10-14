#PHOBIUS DATABASE FOR SIGNAL P DETECTION
#JUST A INITIAL TEST WITH SINGLE PEPTIDE
#NEEDED TO BUILDUP IT FOR READING AND WRITING FROM CSV
import urllib.parse
import urllib.request

# The URL where the form is being submitted 
url = "https://phobius.sbc.su.se/cgi-bin/predict.pl"

# Define the data to be submitted
data = {
   "protseq": ">sequence_name\nACCTGCAGATGGTGAACATCTCCCTGCGCGTCCTCACCCGCCCCAATGCTGCAGAGCTG",
   "protfile": "",  
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
