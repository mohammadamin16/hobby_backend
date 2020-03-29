from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, name, password=""):
        username = username
        password = password
        name = name
        user = self.model(
            username=username,
            password=password,
            name=name
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, name, password):

        user = self.create_user(
            username=username,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    # avatar = models.ImageField(upload_to='avatars/', default='')
    # bio = models.CharField(max_length=1000)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'name']

    objects = UserManager()

    # Hobby Fields:
    # watched_films = models.ManyToManyField('films.Film', blank=True, related_name='watched')
    # fav_list      = models.ManyToManyField('films.Film', blank=True, related_name='fav')
    # last_watched_film = models.ForeignKey('films.Film', on_delete=models.CASCADE, blank=True, related_name='lastWatched', null=True)
    # requested_users = models.ManyToManyField('accounts.User', related_name='request_users', blank=True, null=True)
    # friends = models.ManyToManyField('accounts.User', related_name='friends_users', blank=True, null=True)
    # suggests = models.ManyToManyField('films.Suggest', related_name='suggests', null=True, blank=True)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


