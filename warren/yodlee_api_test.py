import requests

test_api_urls = [
    "https://sandbox.api.yodlee.com:443/ysl/institutions",
    
    "https://sandbox.api.yodlee.com:443/ysl/user"
]

def send_req_get_resp(req_type, url, token, data=None):
    resp = None
    headers = {"Authorization": "Bearer "+ token, "Api-Version": "1.1"}
    if req_type.lower() == "get":
        try:
            resp = requests.get(url, headers=headers).text
        except Exception as e:
            print("Error Retriving Data ...", e)
    return resp

token = "Zqht52uc1ICARVZwjwCLTnA9Gylx" # change token
for api in test_api_urls:
    resp = send_req_get_resp('get', api, token)
    print("Response for '{}' is \n\n {} \n\n".format(api, resp))
