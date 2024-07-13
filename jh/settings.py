from os import environ


SESSION_CONFIGS = [
    dict(
        name='Pay_with_BDM',
        display_name="Pay_with_BDM",
        app_sequence=['Pay_with_BDM'],
        num_demo_participants=1,
    ),
]


MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]



SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.025, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []


LANGUAGE_CODE = 'en'


REAL_WORLD_CURRENCY_CODE = '£'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/Experiment.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '1314'

INSTALLED_APPS = ['otree']
