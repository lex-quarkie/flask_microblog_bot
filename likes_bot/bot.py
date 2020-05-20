import logging
import requests
import random

from helpers import generate_username, pw_gen, generate_post_body
from config import (API_URL,
                    MAX_POSTS_PER_USER, MAX_LIKES_PER_USER,
                    NUMBER_OF_LIKES, NUMBER_OF_POSTS, NUMBER_OF_USERS)

logger = logging.basicConfig(level=logging.DEBUG)


class GlobalState(object):  # singleton
    def __init__(self):
        self.get_posts_ids()
        self.posts_count_on_start = self.posts_count()
        self.added_posts_count = 0
        self.likes_added = 0
        self.bots = []

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GlobalState, cls).__new__(cls)
        return cls.instance

    def get_posts_ids(self):
        url = f"{API_URL}/posts"
        r = requests.get(url=url, json={})
        if r.status_code == 200:
            result = []
            for post in r.json():
                result.append(post.pop("id"))
            self.posts_ids = list(set(result))

    def posts_count(self):
        return len(self.posts_ids)

    def added_posts_count(self):
        return len(self.posts_ids)

    def add_post_id(self, id):
        self.posts_ids.append(id)

    def bots_count(self):
        return len(self.bots)

    def likes_count(self):
        return self.likes_added

    def script_stats(self):
        return {'added_posts': self.added_posts_count,
                'created_users': self.bots_count(),
                'likes_count': self.likes_count()}

    def get_bot(self, id):
        return self.bots[id]

    def add_bot(self, bot):
        if isinstance(bot, BotUser) and bot not in self.bots:
            self.bots.append(bot)
            logging.info("Bot added to global state")
        else:
            logging.info("Got a problem while adding Bot to global state")

    def create_bot(self):
        new_bot = BotUser()
        self.add_bot(new_bot)
        new_bot.signup()

        return new_bot

    def select_bot(self, attr_name=None):
        def map_param_to_attr_name(key=attr_name):
            return {'likes_count': MAX_LIKES_PER_USER,
                    'posts_count': MAX_POSTS_PER_USER}[key]


        bots_weights = [getattr(bot, attr_name) + random.randint(100, 110)  # random weights initialization
                        for bot in self.bots
                        if getattr(bot, attr_name) < map_param_to_attr_name()]
        if bots_weights:
            bot = random.choices(self.bots, weights=bots_weights[::-1]).pop()
        else:
            bot = self.create_bot()

        return bot


class BotUser(object):
    def __init__(
        self,
        registered=False,
        headers=None,
        posts_count=0,
        likes_count=0
    ):
        if not headers:
            self.headers = {"Accept": "*/*", }
        self.registered = registered
        self.username = generate_username()
        self.password = pw_gen()
        self.access_token = ''
        self.posts_count = posts_count
        self.likes_count = likes_count

    def signup(self):
        logging.debug(f'Bot >> username: {self.username} Starting signup process')
        r = requests.post(
            url=f'{API_URL}/signup',
            json={'username': self.username, 'password': self.password},
            headers=self.headers,
        )

        if r.status_code == 201:
            self.registered = True
            self.access_token = r.json()['access_token']
            self.headers["Authorization"] = f'Bearer {self.access_token}'
            self.user_id = r.json()['id']
            logging.info(f'Signup: OK, username: {self.username}')
        else:
            logging.info(f'Problem while signing up user with username {self.username}')
            logging.debug(r.json())

    def login(self):
        logging.debug(f'Bot >> username: {self.username} starting login process')
        r = requests.post(
            url=f'{API_URL}/login',
            json={'username': self.username, 'password': self.password},
            headers=self.headers,
        )
        self.access_token = r.json().get('access_token')
        if not self.headers.get("Authorization"):
            logging.warning('Access token not found: Abort')
            return
        if r.status_code == 200:
            self.access_token = r.json()['access_token']
            logging.info(f'Login: OK, username: {self.username}')
        else:
            logging.info(f'Problem while logging up user with username {self.username}')
            logging.debug(r.json())

    def create_post(self, body=None):
        logging.debug(f'Bot >> username: {self.username} starting create post process')
        r = requests.post(
            url=f'{API_URL}/posts',
            headers=self.headers,
            json={'body': generate_post_body() if body is None else body},
        )

        if not self.headers.get("Authorization"):
            logging.warning('Access token not found: Abort')
            return
        if r.status_code == 201:
            self.posts_count += 1
            gs().added_posts_count += 1
            post_id = r.json()['id']
            gs().posts_ids.append(post_id)
            logging.info(f'Create post: OK, username: {self.username}, post_id: {post_id}')

    def like(self, post_id):
        logging.debug(f'Bot >> username: {self.username} starting like process')
        r = requests.get(url=f'{API_URL}/posts/{post_id}/like',
                         headers=self.headers)
        logging.info(r.status_code)
        if r.status_code == 200:
            self.likes_count += 1
            gs().likes_count += 1


def gs():
    import gc

    global_state = [obj for obj in gc.get_objects() if isinstance(obj, GlobalState)]
    return global_state[0]


def create_posts():
    bot = gs().select_bot('posts_count')
    bot.create_post()


def like_posts():
    post_id = random.choice(gs().posts_ids)
    bot = gs().select_bot('likes_count')
    bot.like(post_id)


def create_bots(count):
    for _ in range(count):
        gs().create_bot()


def main():
    global_state = GlobalState()
    create_bots(NUMBER_OF_USERS)
    while global_state.added_posts_count < NUMBER_OF_POSTS:
        create_posts()
    while global_state.likes_added < NUMBER_OF_LIKES:
        like_posts()

    logging.info(global_state.script_stats())


if __name__ == '__main__':
    main()
