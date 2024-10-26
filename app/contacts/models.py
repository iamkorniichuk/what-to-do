from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Contact(models.Model):
    class Meta:
        abstract = True

    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, models.CASCADE)


class Email(Contact):
    class Meta:
        default_related_name = "email"

    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email
