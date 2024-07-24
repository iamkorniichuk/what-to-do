from .base import env


with env.prefixed("POSTGRES_"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("NAME"),
            "USER": env.str("USER"),
            "PASSWORD": env.str("PASSWORD"),
            "HOST": env.str("HOST"),
            "PORT": env.str("PORT"),
        }
    }
