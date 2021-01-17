import requests, time, os

TOKEN = "349JaTCo6MGo4snnxrygsW"
DBAUTH = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhYmFzZUlkIjoiVUxBcDlvRFI4dUU1cE5aRjdSbW8yVSIsImFjY2Vzc1Blcm0iOiJmdWxsIiwidG9rZW5JZCI6ImVuQ2YwMTBZZ0J6bVdoVWJGWkJZMXFkY0JWbFhscEg1VHVOQ0xUQlRNTmdRcFc1dDZKelZ2QTBxampIQ0FRUjMiLCJpYXQiOjE2MTA4OTE0MzIsImV4cCI6MTYxMTMyMzQzMiwiaXNzIjoiZHJvcGJhc2UuaW8iLCJzdWIiOiJoM3F3dFgzYVZaVmVSOEd2NTViYlR6In0.nL2lg0DlWSo-UGCvfXMUC-Y1saCc8lkT9nR6xZE7hfw"

def upload_file_via_presigned_url(contents):
    # First, we need to get pre-signed url 
    r = requests.post("https://api2.dropbase.io/v1/pipeline/generate_presigned_url", data={'token': TOKEN})
    if(r.status_code != 200): # Something failed
        print(r.status_code)
        print(r.json()) # Detailed error message
    presigned_url = r.json()["upload_url"] # Link to upload a file
    job_id = r.json()["job_id"] # Job_id to see the status of the pipeline once the file is uploaded
    
    #create file
    if os.path.exists('temp.json'):
        os.remove('temp.json')
    with open('temp.json', 'w+') as f:
        f.write(contents)

    # Now we upload the file
    r = requests.put(presigned_url, data=open("temp.json", 'rb')) # replace NHkJR6qjRu8kkRSk8zHiGt.csv with your file
    if(r.status_code != 200): # Failed to upload and run pipeline
        print(r.status_code)
        print(r.json())

    # The pipeline will now run
    return job_id

def query_db(query):
    r = requests.get('https://query.dropbase.io/ULAp9oDR8uE5pNZF7Rmo2U/' + query, headers={'Authorization': DBAUTH})
    return r

def get_status(job_id):
    # Call the server to get the status
    r = requests.get("https://api2.dropbase.io/v1/pipeline/run_pipeline", data={ "job_id":job_id })
    
    # Keep pinging the server until the job is finished
    while(r.status_code != 200):
        print(r.json()) # Prints the message of what is happening
        time.sleep(1)
        r = requests.get("https://api2.dropbase.io/v1/pipeline/run_pipeline", data={ "job_id":job_id})

    # id statys code is not 200 nor 202, then error occured
    if(r.status_code != 200):
        print("There is an error")
        print(r.status_code)
        print(r.json())
    
    else:
        print("Successful!")