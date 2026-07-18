import requests
import json

def json_lesson():
    print("--- 1. JSON Examples ---\n")
    # JSON is a lightweight data interchange format.
    # In Python, JSON data structures map to dictionaries and lists.


    python_data = {
        "name": "Alice",
        "age": 28,
        "is_student": True,
        "courses": ["Math", "Computer Science"]
    }

    # Convert Python dictionary to a JSON string (Serialization)
    # json.dumps() takes a Python object and returns a JSON formatted string.
    json_string = json.dumps(python_data)
    print("Serialized JSON String:")
    print(json_string)
    print("\n")

    # Convert JSON string back to a Python dictionary (Deserialization)
    # json.loads() takes a JSON string and parses it into a Python dictionary.
    parsed_data = json.loads(json_string)
    print(f"Deserialized Data Type: {type(parsed_data)}")
    print(f"Accessing data: Name = {parsed_data['name']}")
    print("-" * 30 + "\n")


def requests_get_lesson():
    print("--- 2. REST API GET Request (Fetching Data) ---\n")
    # REST APIs allow programs to talk to each other over the internet using HTTP.
    # We will use JSONPlaceholder, a free fake API for testing.
    
    # The URL we want to send a GET request to
    url = "https://jsonplaceholder.typicode.com/users/1"
    
    print(f"Sending GET request to {url}...")
    response = requests.get(url)

    # Check the status code to see if the request was successful
    # 200 OK means the request was successful
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("GET request successful!\n")
        
        # We can extract the JSON data from the response directly into a dictionary
        user_data = response.json()
        print(user_data)
        
        print("Data received from API:")
        print(f"Name: {user_data.get('name')}")
        print(f"Email: {user_data.get('email')}")
        print(f"Company: {user_data.get('company', {}).get('name')}")
    else:
        print("GET request failed.")
    
    print("-" * 30 + "\n")


def requests_post_lesson():
    print("--- 3. REST API POST Request (Sending Data) ---\n")
    # POST requests are used to send data to a server to create or update a resource.
    
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # Data we want to send to the server
    new_post_data = {
        "title": "Learning REST APIs",
        "body": "This is a great lesson on requests and JSON in Python.",
        "userId": 1,
        "
    }
    
    print(f"Sending POST request to {url}...")
    # The `json` parameter automatically serializes our dictionary into a JSON string
    # and sets the correct HTTP headers (Content-Type: application/json)
    response = requests.post(url, json=new_post_data)
    
    # 201 Created usually means a resource was successfully created on the server
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        print("POST request successful! Resource created.\n")
        
        # The server usually responds with the created resource and its new ID
        created_post = response.json()
        print("Response from server:")
        print(json.dumps(created_post, indent=4))
    else:
        print("POST request failed.")
        
    print("-" * 30 + "\n")

def main():
    
    print("--- 4. Understanding the main() Function ---\n")
    print("Starting Lesson from main()...\n")
    json_lesson()
    requests_get_lesson()
    requests_post_lesson()
    # print("Lesson Complete!")


if __name__ == "__main__":
    main()



#requests - 

#api - application programming interface


# get - fetch 
# post - 
# update - put
# delete

# json format