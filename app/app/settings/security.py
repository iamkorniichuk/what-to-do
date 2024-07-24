from .base import env


SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("IS_DEVELOPMENT")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", subcast=str)
CORS_ALLOWED_ORIGINS = env.list("ALLOWED_ORIGINS", subcast=str)
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

SITE_ID = 1
