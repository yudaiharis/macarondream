import requests
from retry import retry

# -------------------------------
# Linenotify Class
# -------------------------------
class Linenotify:

    def __init__(self, token):
        self.api = 'https://notify-api.line.me/api/notify'
        self.header = {'Authorization': 'Bearer ' + token}

    @retry(requests.exceptions.ConnectionError, tries=100, delay=1)
    def send(self, *lines):
        message = ''
        for obj in lines:
            message += '\n' + obj
        payload = {'message': message}
        #files = {"imageFile":open('/tmp/' + self.tv_dir +  '.png','rb')}
        #files = {"imageFile":open(r'c:\tmp\sceeenshot1.png','rb')}
        #requests.post(self.api, headers=self.header, params=payload, files=files)
        requests.post(self.api, headers=self.header, params=payload)

# -------------------------------
# EOF
# -------------------------------