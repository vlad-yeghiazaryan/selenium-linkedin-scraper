## Use an already built docker image
```bash
ibmcloud fn action create linkedinScraper __main__.py --docker vladimiryeghiazaryan/selenium-linkedin-scraper:v0.0.1 --web true
```
or create your own image.

## Execution order:
```bash
docker build . -t <dockerhub_username>/<repo_name>:<tag_name>
```
```bash
docker push <dockerhub_username>/<repo_name>:<tag_name>
```
```bash
zip linkedinScraper.zip __main__.py linkedinScraper.py drivers/chromedriverLinux64
```
```bash
ibmcloud fn action create linkedinScraper linkedinScraper.zip --docker <dockerhub_username>/<repo_name>:<tag_name> --web true
```
```bash
ibmcloud fn action invoke linkedinScraper -r --param-file invoke.txt
```
Testing internally 
```bash
docker run --rm -it --entrypoint bash <dockerhub_username>/<repo_name>:<tag_name>
```
```bash
python3 __main__.py
```

This is the equivalent python dictionary representation of the payload. Make sure to convert it into a valid json before sending the request.
```python
from decouple import config
base_url = 'https://www.linkedin.com'
username = config("USERNAME")
secret = config("PASSWORD")
users = ['https://www.linkedin.com/in/ben-affleck-966710207', 'https://www.linkedin.com/in/ben-affleck-3603ab200/']
payload = {'url': base_url, 'username': username, 'password':secret, 'profile_urls':users}
print(payload)
```
```javascript
{"url": "https://www.linkedin.com", "username": "fakefan665@gmail.com", "password": "ben affleck", "profile_urls": ["https://www.linkedin.com/in/ben-affleck-966710207", "https://www.linkedin.com/in/ben-affleck-3603ab200/"]}
```
