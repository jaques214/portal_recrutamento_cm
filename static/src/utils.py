import json

import requests

host = "148.69.67.24:8001"


def creatio_authenticate():
    # Login Request
    json_login = json.dumps({'Username': 'Supervisor', 'UserPassword': 'Supervisor'})
    url_login = "https://" + host + "/ServiceModel/AuthService.svc/Login"
    login_headers = {"Content-Type": 'application/json', "ForceUseSession": 'true'}
    login_response = requests.post(url_login, data=json_login, headers=login_headers, verify=False)

    # Cookies
    login_cookies = login_response.cookies.get_dict()

    # Login Request Data
    print("***** LOGIN REQUEST DATA *****")
    print("Login Body:", json_login)
    print("Login Request Cookies:")
    print(".ASPXAUTH:\n", login_cookies.get('.ASPXAUTH'))
    print("BPMCSRF:\n", login_cookies.get('BPMCSRF'))
    print("CsrfToken:\n", login_cookies.get('CsrfToken'))
    print("Login Status Code:", login_response.status_code)

    return login_cookies, login_response
