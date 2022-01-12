from decouple import config
from linkedinScraper import SeleniumScraper


def main(request):
  url = request['url']
  username = request['username']
  secret = request['password']
  users = request['profile_urls']
  linkedin = SeleniumScraper(url)
  linkedin.login(username, secret)
  profiles = linkedin.scrape_profiles(users)

  # Saving data
  print('Scraping complete.')
  return {'scraped_data': profiles}


if __name__ == '__main__':
  base_url = 'https://www.linkedin.com'
  username = config("USERNAME")
  secret = config("PASSWORD")
  users = ['https://www.linkedin.com/in/ben-affleck-966710207',
           'https://www.linkedin.com/in/ben-affleck-3603ab200/']
  request = {'url': base_url, 'username': username,
             'password': secret, 'profile_urls': users}
  data = main(request)
  import json
  with open('profiles.txt', 'w') as f:
    json.dump(data, f)
