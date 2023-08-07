from typing import Any, Optional
from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        user = User.objects.get(pk = 4)
        group, created = Group.objects.get_or_create(
            name= 'profiel_manager',
        )
        permission_profile = Permission.objects.get(
            codename = 'view_profiel',
        )
        permission_logentry = Permission.objects.get(
            codename = 'view_logentry',
        )
        
        #Добавление разрешения в группу
        group.permissions.add(permission_profile)

        #Добавление пользователя в группу
        user.groups.add(group)

        #Связать пользователя напрямую с разрешением
        user.user_permissions.add(permission_logentry)

        group.save()
        user.save()