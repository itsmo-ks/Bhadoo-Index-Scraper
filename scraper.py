import requests
import base64 
import json
import urllib


next_page = False
next_page_token = "" 
 

def decrypt(string): 
     return base64.b64decode(string[::-1][24:-20]).decode('utf-8')  

  
def func(payload_input, url): 
    global next_page 
    global next_page_token
    
    url = url + "/" if  url[-1] != '/' else url
         
    encrypted_response = requests.post(url, data=payload_input)
   
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
    index_link = input("Enter the index link: ")
    print(f"Index Link: {index_link}\n\n")
    x = 0
    payload = {"page_token":next_page_token, "page_index": x}	
    print(func(payload, index_link))
    while next_page == True:
        payload = {"page_token":next_page_token, "page_index": x}
        print(func(payload, index_link))
        x += 1

main()
