from django.contrib.auth.models import User
from django.db import models

def profiel_image_directory_path(instance: 'Profiel', filename: str) -> str:
    return 'user/user_{pk}/avatar/{filename}'.format(
        pk = instance.user.pk,
        filename = filename
    )


class Profiel(models.Model):
    class Meta:
        pass

    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio = models.TextField(max_length='500', blank= True)
    agreement_accepted = models.BooleanField(default= False)
    profile_image = models.ImageField(null= True, blank= True, upload_to=profiel_image_directory_path)