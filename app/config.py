from decouple import config
DATABASE_URL = config("DATABASE_URL", default="postgresql://postgres:postgres@localhost:5432/emergencias")

SECRET_KEY = config("SECRET_KEY", default="dev-secret-key")

DEBUG = config("DEBUG", default=True, cast=bool)