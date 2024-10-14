import urllib.parse
import urllib.request

# The URL where the form is being submitted (replace with your form's URL)
url = "https://sbhmprksh.in/contact"

# Define the data to be submitted
data = {
    "myName": "John Doe",
    "myContact": 123456,
    "myEmail": "johndoe@example.com",
    "myAbout": "This is a test message."
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
