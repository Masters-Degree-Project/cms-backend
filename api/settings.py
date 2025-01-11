DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'django_password',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# OpenAI API Key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') 