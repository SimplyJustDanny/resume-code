import os

env_is_prod = os.getenv("ENV_IS_PROD")
print(env_is_prod)

pg_config = {}

if env_is_prod == "FALSE":
    pg_config = {
        'host' : os.getenv("DB_HOSTNAME"),
        'user' : os.getenv("DB_USERNAME"),
        'password' : os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_DATABASENAME"),
        'port' : os.getenv("DB_PORT")
    }
else:
    pg_config = {
        # REDACTED
    }

pg_config = {
    'host' : os.getenv("DB_HOSTNAME"),
    'user' : os.getenv("DB_USERNAME"),
    'password' : os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASENAME"),
    'port' : os.getenv("DB_PORT")
}

print(pg_config)
