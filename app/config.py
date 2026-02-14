import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "docker":
    load_dotenv(".env.docker", override=True)
else:
    load_dotenv(".env.local", override=True)
