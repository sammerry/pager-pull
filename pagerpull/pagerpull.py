import click
import time
import pypd
import sys
import json
import subprocess
import os
import logging



log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)



def sendmessage(title, description, service='notify-send', icon=None, urgency='critical'):
    command = [service]

    if icon:
        command.append('-i')
        command.append(icon)

    command.append(title)
    command.append(description)

    try:
        log.debug('command: %s' % ' '.join(command))
        subprocess.Popen(command)
    except Exception as e:
        log.error('Failure writing to notify-send', e)

@click.command()
@click.option('-t', '--api-token',
        help="Pagerduty token required")
@click.option('-i', '--interval',
        help="Pull interval, 15s default")
@click.option('--icon',
        help='Change the notification icon')
@click.option('-n', '--notifier',
        help="Notification application, default: notify-send")
@click.option('-u', '--urgency',
        help="The urgency for notify send: low, normal, critical")
@click.option('-v', '--verbose',
        is_flag=True,
        help="verbose logging")
@click.option('--test',
        is_flag=True,
        help="Skip pagerduty and trigger a single notification with test data")
def cli(*args, **kwargs):
    """
    Pager Pull: pull from pagerduty api and trigger a system notifier like notify-send when a triggered event exists.
    """
    if kwargs['verbose']:
        print('setting debug')
        log.setLevel(logging.DEBUG)

    pypd.api_key = os.getenv('PAGERDUTY_TOKEN', kwargs['api_token'])

    if not pypd.api_key:
        log.critical('Missing api token use --api-token or PAGERDUTY_TOKEN')
        return

    notifier = kwargs['notifier'] or 'notify-send'
    interval = int(kwargs['interval'] or '15')
    urgency = kwargs['urgency'] or 'critical'
    icon = kwargs['icon'] or 'error'

    log.debug('api-token: %s' % (pypd.api_key is not None))
    log.debug('notifier: %s' % notifier)
    log.debug('interval: %s' % interval)
    log.debug('urgency: %s' % urgency)
    log.debug('icon: %s' % icon)

    while True:

        if kwargs['test']:
            title = 'Test Event'
            description = 'This is a test notification.'
            sendmessage(title, description, icon=icon, service=notifier, urgency=urgency)
            return

        try:
            incidents = pypd.Incident.find(statuses=['triggered'])
        except Exception as e:
            log.error('Error Connecting To Pagerduty', e)
            incidents = []

        for i in incidents:
            log.debug(i.json)
            j = i.json
            title = j['title']
            description = j['description']
            sendmessage(title, description, icon=icon, service=notifier, urgency=urgency)

        time.sleep(interval)

