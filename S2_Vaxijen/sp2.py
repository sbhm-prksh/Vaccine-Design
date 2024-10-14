import urllib.parse
import urllib.request

# The URL where the form is being submitted
url = "https://www.ddg-pharmfac.net/vaxijen/scripts/VaxiJen_scripts/VaxiJen3.pl"

# Define the data to be sent in the POST request
mydata = {
    'seq': 'MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRYFDSFGNLSSASAIMGNPKVKAHGKK',
    'Target': 'parasite',
    'SequenceOnOff': 'A',
    'threshold': '0.5',
    'submit': 'Submit'
}

# Encode the form data so it can be sent in the POST request
encoded_data = urllib.parse.urlencode(mydata).encode('utf-8')

# Mimic the headers from the browser request, including User-Agent and cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://www.ddg-pharmfac.net/vaxijen/VaxiJen/VaxiJen.html',
    'Cookie': 'cf_clearance=HWMCR_ZXimN5QccxHpNeInoirWnGUqb8sjJbC2ZP3EU-1728862379-1.2.1.1-4l4CkK3PF2Nx9VTqd40LsLcCHFKIP3mOhIYDhcRb.qstUK.G1STQVNiezqqAWX1uHbPwWnU4mfWITYfe7ciPN1r4gKjCujWGd1y_xKqnSJzRW0sIi7TlqR0i2UFS2d2n8PWLsUrwn0h7ggH.A.b8Az.YyWfbqkzwpv01t.tIFynUzMoOiJZYV8sFXvb7.uZ3f5URP.ErTao9ZJ_dugzD8wuU_600mByoZzZ6MYMYnlkAaOIKE8Er3SHMRpLx1LnR7Knhis_URm8zj.Pt7ESpgyxFvwHqdynfmvoYhKZKwj4.C7xGWxHBDVCg52zjzAqKr7p3hrqHimuHO4CphxEl9Hhl4O63fgLKi1dvjI909YlKLd8.I9KLr48jjfWc.xLEU4_ynIIxg8qCVBzQuIg90d9t3e8mQDgLXO8AMd_UTPE'  # Replace with your actual cf_clearance cookie value
}

# Sending the POST request
try:
    # Create a request object with the URL, encoded data, and headers
    request = urllib.request.Request(url, data=encoded_data, headers=headers)
    
    # Send the request and get the response
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
