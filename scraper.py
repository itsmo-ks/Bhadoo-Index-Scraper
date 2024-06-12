import requests
import base64 
import json
import urllib
import getpass


next_page = False
next_page_token = "" 


def decrypt(string): 
     return base64.b64decode(string[::-1][24:-20]).decode('utf-8')  


def check_protected(url):
    r = requests.get(url)
    if r.status_code == 401:
        print("The index link is password protected.")
        username = input("Enter username: ")
        password = getpass.getpass(prompt="Enter password: ")
        return (username, password)
    else:
        return None

    
def func(payload_input, url, auth=None): 
    global next_page 
    global next_page_token
    
    url = url + "/" if url[-1] != '/' else url
    
    encrypted_response = requests.post(url, data=payload_input, auth=auth)
   
    try: decrypted_response = json.loads(decrypt(encrypted_response.text))
    except: return "something went wrong. check index link again"
       
    page_token = decrypted_response["nextPageToken"] 
    if page_token == None: 
        next_page = False 
    else: 
        next_page = True 
        next_page_token = page_token 
   
     
    result = ""
   
    if list(decrypted_response.get("data").keys())[0] == "error": pass
    else :
        file_length = len(decrypted_response["data"]["files"])
        for i, _ in enumerate(range(file_length)):
            files_type   = decrypted_response["data"]["files"][i]["mimeType"] 
            files_name   = decrypted_response["data"]["files"][i]["name"] 
         
            if files_type == "application/vnd.google-apps.folder": pass
            else:
                direct_download_link = url + urllib.parse.quote(files_name)
                result += f"{direct_download_link}\n"
        return result
        

def main():
    global next_page 
    global next_page_token
    next_page = False
    next_page_token = "" 
    index_link = input("Can you please enter your index link you want to extract: ")
    auth = check_protected(index_link)
    print(f"Index Link: {index_link}\n\n")
    x = 0
    result = ""
    payload = {"page_token":next_page_token, "page_index": x}	
    result += func(payload, index_link, auth=auth) or ""
    while next_page == True:
        payload = {"page_token":next_page_token, "page_index": x}
        result += func(payload, index_link, auth=auth) or ""
        x += 1

    output_file = input("\nCan you please enter the file name of the extracted files: ") + ".txt"
    with open(output_file, "w") as f:
        f.write(result)
    print(f"\nResults saved to {output_file}")
        

if __name__ == "__main__":
    main()
