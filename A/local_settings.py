SECRET_KEY = 'django-insecure-)uedg@fx@6#zw&$9#4_%vh^2nyyz1m6t1uug#vh-le15bv$um*'

DEBUG = True

# EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

# KAVE_NEGAR
KAVE_API_KEY = ''
KAVE_SENDER = ''


# OAUTH2
SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''

SOCIAL_AUTH_LOGIN_REDIRECT_URL = ''
SOCIAL_AUTH_LOGIN_ERROR_URL = ''

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

# Use this configuration if you have set up to receive email from the GOOGLE API
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
]
