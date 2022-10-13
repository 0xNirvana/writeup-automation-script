import requests
import json

host = "https://api.medium.com/v1"

def check_token():
    if not os.path.exists("token"):
        print("Token file not found!")
        print("Generate a token from Medium's setting page.")
        print("Copy the token and paste in the a file named 'token' in the same directory as this script.")
        exit(1)
    token = open("token", "r").read()
    path = '/me'
    headers = {'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json',
            'Accept': 'application/json'}

    response_raw = requests.get(host+path, headers=headers)
    response = json.loads(response_raw.content)

    if not response_raw.status_code == 200:
        print("Issue with authorization.")
        print("Check the provied token.")
        exit(1)

    id = response["data"]["id"]
    print("ID Found: " + id)
    return token, id


if __name__ == '__main__':
    token, id = check_token()
    if (token != None and id != None):
        published = process_publish(token, id)
        if (published):
            git_push()
    else:
        print("No/Invalid Token Found!")