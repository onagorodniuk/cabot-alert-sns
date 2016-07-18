from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from django.db import models
from django.conf import settings
from django.template import Context, Template
from os import environ as env

import requests
import json


class SnsAlert(AlertPlugin):
    name = "Sns"
    author = "Oleksandr Nagorodniuk"

    def send_alert(self, service, users, duty_officers):

                c = Context({
                        'service': service,
                        'host': settings.WWW_HTTP_HOST,
                        'scheme': settings.WWW_SCHEME,
                        })

                message = Template(post_template).render(c)

class SnsAlertUserData(AlertPluginUserData):
    name = "Sns Plugin"
    favorite_bone = models.CharField(max_length=50, blank=True)
