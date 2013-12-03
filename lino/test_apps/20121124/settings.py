INSTALLED_APPS = ['lino.test_apps.20121124']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}


SECRET_KEY = "123"
