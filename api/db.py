import dropbox
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


def get_avatar_default():
    dbx = dropbox.Dropbox(token)
    result = dbx.files_get_temporary_link('/avatars/user.png')
    return result.link


def handle_uploaded_file(f, username):
    with open('media/avatars/{}.png'.format(username), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

