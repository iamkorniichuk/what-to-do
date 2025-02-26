from .base import env


with env.prefixed("POSTGRES_"):
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": env.str("DB"),
            "USER": "postgres",
            "PASSWORD": env.str("PASSWORD"),
            "HOST": "db",
            "PORT": "5432",
        }
    }
