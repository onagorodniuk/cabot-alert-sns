from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from django.db import models
from django.conf import settings
from django.template import Context, Template
from os import environ as env

import requests
import json
import datetime
#from subprocess import Popen, PIPE
import subprocess
#from subprocess import call, PIPE, Popen
import logging

template = """{% if service.overall_status != service.PASSING_STATUS %}{\"date\": \"{{ date }}\",\"cabot_service_name\": \"{{ service.name }}\", \"cabot_service_status\": \"{{ service.overall_status }}\", \"cabot_service_id\": \"{{ service.id }}\", {% for check in service.all_failing_checks %}  \"cabot_failed_checks\": {% if check.check_category == 'Jenkins check' %}{% if check.last_result.error %} \"{{ check.name }} ({{ check.last_result.error|safe }})\" {{jenkins_api}}job/{{ check.name }}/{{ check.last_result.job_number }}/console{% else %} \"{{ check.name }}\" {{jenkins_api}}/job/{{ check.name }}/{{check.last_result.job_number}}/console {% endif %}{% else %} \"{{ check.name }} {% if check.last_result.error %} ({{ check.last_result.error|safe }})\"{% endif %}{% endif %}{% endfor %},\"cabot_service_url\": \"{{ scheme }}://{{ host }}{% url 'service' pk=service.id %}\"}{% endif %}"""

logger = logging.getLogger(__name__)

class SnsAlert(AlertPlugin):
    name = "Sns"
    author = "Oleksandr Nagorodniuk"

    def send_alert(self, service, users, duty_officers):
        #if not self._service_alertable(service):
        #    return
        #sns_aliases= []
        #users = list(users) + list(duty_officers)

        #sns_aliases = [u.sns_arn for u in SnsAlertUserData.objects.filter(user__user__in=users)]



        if service.overall_status == service.PASSING_STATUS:
                return #alert = False
        if service.overall_status == service.ERROR_STATUS:
                if service.old_overall_status in (service.ERROR_STATUS, service.ERROR_STATUS):
                        return #alert = False  # Don't alert repeatedly for ERROR
        if service.overall_status == service.WARNING_STATUS:
                if service.old_overall_status in (service.WARNING_STATUS, service.WARNING_STATUS):
                        return
        if service.overall_status == service.CRITICAL_STATUS:
                if service.old_overall_status in (service.CRITICAL_STATUS, service.CRITICAL_STATUS):
                        return
#       else:

        now_date=datetime.datetime.now()
        c = Context({
        'service': service,
        'host': settings.WWW_HTTP_HOST,
        'scheme': settings.WWW_SCHEME,
        'date': now_date,
                    })

        message = Template(template).render(c)
        p=subprocess.Popen(['/usr/local/bin/aws', 'sns', 'publish', '--topic-arn', 'ARRRRRRRRRNNNNNNNN', '--profile', 'cabot_alert_sns', '--message', message],  stderr=subprocess.PIPE)
        err = p.communicate()[1]
        if p.returncode != 0:
                logger.exception('Error making AWS CLI call:' + '\n' + str(err))

class SnsAlertUserData(AlertPluginUserData):
    name = "Sns Plugin"
    sns_arn = models.CharField(max_length=1000, blank=True)
