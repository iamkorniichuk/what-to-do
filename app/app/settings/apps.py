DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.gis",
]
THIRD_PARTY_APPS = [
    "corsheaders",
    "drf_spectacular",
    "rest_framework",
    "django_filters",
    "rest_framework_gis",
    "rest_framework_simplejwt.token_blacklist",
]
PROJECT_APPS = [
    "activities",
    "authentication",
    "bookings",
    "commons",
    "contacts",
    "interactions",
    "recommendations",
    "schedules",
    "users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS
