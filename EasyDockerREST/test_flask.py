# importing the requests library
import requests

# api-endpoint
URL = "http://localhost:5001/build"

# location given here
dockerfile = "FROM hello-world\n"

# defining a params dict for the parameters to be sent to the API
PARAMS = {"dockerfile": "FROM hello-world\n"}

# sending get request and saving the response as response object
r = requests.post(url=URL, json=PARAMS)

# printing the output
print(r.text)
