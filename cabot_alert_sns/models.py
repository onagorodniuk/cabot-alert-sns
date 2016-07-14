from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

class SnsAlert(AlertPlugin):
    name = "Sns"
    author = "Oleksandr Nagorodniuk"

    def send_alert(self, service, users, duty_officers):
        """Implement your send_alert functionality here."""
        return

class SesAlertUserData(AlertPluginUserData):
    name = "Ses Plugin"
    favorite_bone = models.CharField(max_length=50, blank=True)
