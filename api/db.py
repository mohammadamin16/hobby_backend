import dropbox
# from accounts.models import User
from django.conf import settings

token = settings.DROPBOX_TOKEN


def upload_avatar(file, username):
    try:
        print('FILE:', file)
        dbx = dropbox.Dropbox(token)
        dbx.files_upload(file, '/avatars/{}/{}.png'.format(username, username))
    except TypeError:
        dbx = dropbox.Dropbox(token)
        dbx.files_upload(get_file(file), '/avatars/{}/{}.png'.format(username, username),
                         mode=dropbox.files.WriteMode.overwrite)


def get_file(_filepath):
    f = open(_filepath, 'rb')
    return f.read()


def get_avatar_link(username):
    dbx = dropbox.Dropbox(token)
    result = dbx.files_get_temporary_link('/avatars/{}/{}.png'.format(username, username))
    return result.link


if __name__ == "__main__":
    link = get_avatar_link('amin')
    print(link)


def get_avatar_default():
    dbx = dropbox.Dropbox(token)
    result = dbx.files_get_temporary_link('/avatars/user.png')
    return result.link
