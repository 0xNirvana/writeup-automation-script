import requests
import json
import os
import re

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

def process_publish(token, id):
    publish_url = host + "/users/{}/posts".format(id)
    headers = {'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json',
            'Accept': 'application/json'}

    md_files = {}
    index = 1
    platform = input("Enter the platform (HTB/THM/...):\n")
    tags = input("Enter comma separated tags:\n")
    tags = tags.split(",")
    full_path = input("Enter the full path of the writeup directory:\n")
    
    for root, dirs, files in os.walk(os.path.abspath(full_path)):
        for file in files:
            if file.endswith('.md'):
                md_files[index] = os.path.join(root, file)
                index += 1
    print("Markdown files detected in the directory:")
    
    for key,values in md_files.items():
        print("[{}]\t\t{}".format(key, values))
    file_number = input("Enter the index value of the file that contains your writeup:\n")
    file_number = int(file_number)

    content = open(md_files[file_number], "r").read()
    content = add_display_image(content)
    # print(content)
    title = platform + ": " + re.findall('^\#\s(.+?)\n', content)[0]

    content = replace_internal_image_links(content, md_files[file_number])
    cont = input("Press enter if you want to continue to publish the file.")

    if cont != "":
        print("Exiting without publishing the article")
        exit()

    data = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "tags": tags,
        "publishStatus": "public"
    }

    post_response_raw = requests.post(publish_url, headers=headers, json=data)
    post_response = json.loads(post_response_raw.content)
    print (json.dumps(post_response, indent=4))

    return 1

if __name__ == '__main__':
    token, id = check_token()
    if (token != None and id != None):
        published = process_publish(token, id)
        if (published):
            git_push()
    else:
        print("No/Invalid Token Found!")