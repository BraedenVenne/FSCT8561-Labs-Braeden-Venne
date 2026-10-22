import requests, csv
from textwrap import dedent


BASE_URL = "http://localhost:3000"

# Test base connections
try:
    response = requests.get(BASE_URL, timeout=5)
    print(f"Connected. Status: {response.status_code}")
    print(f"Response length: {len(response.content)} bytes")
except requests.RequestException as error:
    print(f"Could not connect: {error}")

# Store HTTP observations into global list
def store_observation(r, http_type):
    observations.append({
    "HTTP Method": http_type,
    "Endpoint": r.url.replace(BASE_URL, ''),
    "Status": r.status_code,
    "Response Length": len(r.content),
    "Content Type": r.headers.get("Content-Type"),
    "Server Header": r.headers.get("Server")
    })

# Request endpoints using GET or POST methods
def grab_endpoints(http_type, test_case, url):
    r = None
    if test_case != '':
        test_case = {"q": test_case}
    if http_type == "GET":
        try:
            r = requests.get(
                BASE_URL + url,
                data=test_case,
                timeout=5
            )
        except requests.RequestException as error:
            print(f"Could not connect: {error}")
    else:
        try:
            r = requests.post(
                BASE_URL + url,
                data=test_case,
                timeout=5
            )
        except requests.RequestException as error:
            print(f"Could not connect: {error}")
    return r

# Format observation for console output
def format_observation(observation_num, r, http_type):
    observation_output = dedent(
        f"""
        Observation {observation_num}:
        HTTP Method: {http_type}"
        Endpoint: {r.url.replace(BASE_URL, '')}
        Status: {r.status_code}"
        Response Length: {len(r.content)}"
        Content Type: {r.headers.get("Content-Type")}
        Server Header: {r.headers.get("Server")}

        """
    )
    return observation_output

http_methods = ["GET","POST"]
test_urls =["/", "/rest/products/search"]
test_cases = ["apple", "orange", "banana"]
observations = []
observation_num = 1

# Loop through methods and endpoints to collect scan data
for method in http_methods:
    for url in test_urls:
        if url != "/rest/products/search" and method == "GET":
            r = grab_endpoints(method, '', url)
            store_observation(r, method)
            print(format_observation(observation_num, r, method))
            observation_num += 1
        elif url == "/rest/products/search":
            for test in test_cases:
                r = grab_endpoints(method, test, url)
                store_observation(r, method)
                print(format_observation(observation_num, r, method))
                observation_num += 1

# Export findings to a CSV file
csv_filename = "http_scan_results.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "Endpoint",
        "HTTP Method",
        "Status",
        "Response Length",
        "Content Type",
        "Server Header"
    ])
    writer.writeheader()  # Write headers
    writer.writerows(observations)  # Write rows

print(f"Saved {csv_filename}")
