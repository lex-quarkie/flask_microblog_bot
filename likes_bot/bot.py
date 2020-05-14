import logging
import random
import requests
import string

from helpers import generate_post_body, generate_user_creds
from config import (API_URL, NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER)

logger=logging.basicConfig(level=logging.INFO)

user_list = [{'id': '9',
              'username': 'quarkie_1337',
              'password': '1ee7f00d',
              'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk0NDk2MjMsIm5iZiI6MTU4OTQ0OTYyMywian'
              'RpIjoiNTU5Y2ZmYzAtZjZiYS00MjdhLWIwYWMtM2FmN2FhYzY0NzEzIiwiZXhwIjoxNTg5NDUwNTIzLCJpZGVudGl0eSI6eyJ1c2Vyb'
              'mFtZSI6InF1YXJraWVfMTMzNyJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.xdIpdvG2Y3azhXsInfK_71CEMgyBftKFv'
              'O0N1PXgr7M}]'
               }]

users_likes_posts = {}
headers = {'Accept': '*/*',}

def pw_gen(size=8, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def signup(creds={}, headers=headers):
    url = f'{API_URL}/signup'
    r = requests.post(url=url,
                      headers=headers,
                      json=creds)
    logging.info((r.status_code,r.json()))
    if r.status_code == 200:
        creds['access_token'] = r.json()['access_token']
        creds['user_id'] = r.json()['id']
    return creds


def login(creds={}, headers=headers):
    url = f'{API_URL}/login'
    r = requests.post(url=url,
                      headers=headers,
                      json=creds)
    logging.info((r.status_code,r.json()))
    creds['access_token'] = r.json()['access_token']
    return r.status_code


def create_post(headers, access_token):
    headers['Authorization'] = f'Bearer {access_token}'
    url = f'{API_URL}/posts'
    post_json= {"body": generate_post_body()}

    r = requests.post(url=url,
                      headers=headers,
                      json=post_json)
    logging.info((r.status_code,r.json()))


def like_post(user_id, post_id, access_token):
    headers['Authorization'] = f'Bearer {access_token}'
    url = f'{API_URL}/posts/{post_id}/like'
    r = requests.get(url=url,
                      headers=headers)
    logging.info(r.status_code)
    if r.status_code == 200:
        if users_likes_posts.get('user_id'):
            users_likes_posts[user_id] = users_likes_posts.get('user_id', {'post_id': post_id, 'likes_count': 1})
        else

def admin(headers=headers):
    url = f'{API_URL}/admin'
    r = requests.get(url=url,
                     headers=headers)


def main():

    # print(generate_post_body())
    # # creds = (generate_user_creds(1))
    # signup(user_creds[0])

    # add_token_to_creds(user_creds[0], login(user_creds[0]))
    # create_post(headers, access_token=user_creds[0]['access_token'])
    like_post(1, access_token=user_creds[0]['access_token'])



main()


# pool = Pool(processes=10)
# async_result = pool.imap_unordered(parse_id, id_lst)
