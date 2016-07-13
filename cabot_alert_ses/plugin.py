from cabot.plugins.models import AlertPlugin
from django import forms
from os import environ as env

from logging import getLogger
logger = getLogger(__name__)

class SesAlertUserSettingsForm(forms.Form):
    favorite_bone = forms.CharField(max_length=100)

class SesletonAlertPlugin(AlertPlugin):
    name = "ses"
    slug = "cabot_alert_ses"
    author = "Oleksandr Nagorodniuk"
    version = "0.0.1"
    font_icon = "fa fa-code"

    user_config_form = SesAlertUserSettingsForm

    def send_alert(self, service, users, duty_officers):
        calcium_level = env.get('CALCIUM_LEVEL') 
        message = service.get_status_message()
        for u in users:
            logger.info('{} - This is bad for your {}.'.format(
                message,
                u.cabot_alert_ses_settings.favorite_bone))

        return True

