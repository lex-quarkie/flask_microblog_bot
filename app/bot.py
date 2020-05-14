import logging
import random
import requests
import string

logger=logging.basicConfig(level=logging.INFO)

config = {}

API_URL = 'http://0.0.0.0:5000'
NUMBER_OF_USERS = 10
MAX_POSTS_PER_USER = 40
MAX_LIKES_PER_USER = 20

user_creds = []

usernames = ["Daredevil", "Dazzler",
             "Decepticon", "Devastator",
             "Diablo", "Domino", "Doppelganger",
             "Dreadnought", "Electro", "Elektra",
             "Enchantress", "Eradicator", "Excalibur"]

headers = {'Accept': '*/*',}

def pw_gen(size=8, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def generate_user_creds(count=NUMBER_OF_USERS, user_creds=[]):
    for _ in range(count+1):
        username = random.choice(usernames)
        password = pw_gen()
        user_creds.append({'username': username,
                           'password': password})
    return user_creds

def signup(creds={}, headers=headers):
    url = f'{API_URL}/signup'
    r = requests.post(url=url,
                      headers=headers,
                      json=creds)
    logging.info(r.status_code)

def admin(headers=headers):
    url = f'{API_URL}/admin'
    r = requests.get(url=url,
                     headers=headers)


def main():
    creds = (generate_user_creds(1))
    signup(creds[0])

if __name__=='__main__':
    main()


# pool = Pool(processes=10)
# async_result = pool.imap_unordered(parse_id, id_lst)
