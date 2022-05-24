from dotenv import load_dotenv
import os

load_dotenv()

pg_login = os.getenv('PG_LOGIN')
pg_password = os.getenv('PG_PASSWORD')
