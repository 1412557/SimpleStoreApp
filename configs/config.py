import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432  # 1 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "123456")
    user, db_name = "postgres", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"