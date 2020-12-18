import os


class Config(object):
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")
    database_url = f"postgresql://{postgres_user}:{postgres_password}@postgres_db:5432/{postgres_db}"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", database_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 's3cr3tk3y')
    SECRET_KEY = os.getenv("SECRET_KEY", 's3cr3tk3y')
