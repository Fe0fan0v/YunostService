from dotenv import load_dotenv
import os

load_dotenv()

pg_login = os.getenv('PG_LOGIN')
pg_password = os.getenv('PG_PASSWORD')
db_name = os.getenv('PG_NAME')
db_host = os.getenv('PG_HOST')
db_port = os.getenv('PG_PORT')
conn_params = os.getenv('PG_PARAMS', '')
path_to_xldata = os.getenv('XL_PATH')
email_login = os.getenv('EMAIL_LOGIN')
email_password = os.getenv('EMAIL_PASSWORD')
