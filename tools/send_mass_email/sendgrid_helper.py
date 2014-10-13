#!/usr/bin/env python
import json
from time import sleep

import argparse
import datetime
import requests
import sys

sendgrid_api_user = 'hackillinois'
sendgrid_api_key = 'RXeN7Ju2y'
sendgrid_api_url = 'https://api.sendgrid.com/api'
sendgrid_template_name = 'NEED NEW TEMPLATE'

# This must be created already in the SendGrid account
sendgrid_identity = 'contact@hackillinois.org'
sendgrid_marketing_name = 'CHANGE NAME [DATETIME]'
sendgrid_list_name = 'CHANGE NAME [DATETIME]'


def locate_template_email():
    print 'Locating Template on SendGrid system...'
    mail_list = sendgrid_req('/newsletter/list.json')
    found_template = False
    for mail in mail_list:
        if mail['name'] == sendgrid_template_name:
            found_template = True
            break
    if not found_template:
        print 'Error: Cannot find template on SendGrid system'
        exit()
    template_content_req = sendgrid_req('/newsletter/get.json', data={
        'name': sendgrid_template_name
    })
    template_subject = template_content_req['subject']
    template_html = template_content_req['html']
    template_text = template_content_req['text']
    print 'Template Loaded! Subject: %s' % template_subject

    if len(template_html) < 5 or len(template_text) < 5:
        print 'Error: The HTML or text for the template is less than 5 bytes. Aborting...'
        exit()

    return template_html, template_subject, template_text


def create_marketing_email(datetime_str, template_html, template_subject, template_text):
    print 'Creating Marketing Email...'
    marketing_email_name = sendgrid_marketing_name.replace('DATETIME', datetime_str)
    marketing_email_req = sendgrid_req('/newsletter/add.json', data={
        'identity': sendgrid_identity,
        'name': marketing_email_name,
        'subject': template_subject,
        'html': template_html,
        'text': template_text
    })

    quit_if_error(marketing_email_req)

    print 'Marketing email created successfully!'
    return marketing_email_name


def create_email_list(datetime_str):
    print 'Creating email list....'
    email_list_name = sendgrid_list_name.replace('DATETIME', datetime_str)
    email_list_req = sendgrid_req('/newsletter/lists/add.json', data={
        'list': email_list_name
    })

    quit_if_error(email_list_req)

    print 'Email list created!'
    return email_list_name


def quit_if_error(req):
    if 'message' not in req or req['message'] != 'success':
        print 'Error: %s' % req
        exit()


def add_emails_to_list(email_list_name, emails):
    print 'Adding emails to list...'
    data = []
    for email in emails:
        #TODO: Send multiple emails in one request
        #Currently I'm getting an error
        obj = {
            'email': email,
            'name': 'HackIllinois Attendee'
        }
        add_emails_req = sendgrid_req('/newsletter/lists/email/add.json', data={
            'list': email_list_name,
            'data': json.dumps(obj)
        })
        print "adding " + email + " " + str(add_emails_req["inserted"])
        #will quit if we get an error
        if add_emails_req["inserted"] != 1:
            quit_if_error(add_emails_req)

    sendgrid_req('/newsletter/lists/email/get.json', data={
            'list': email_list_name
        })
    print 'Emails added!'


def add_list_to_email(email_list_name, marketing_email_name):
    print 'Adding list to email...'
    req = sendgrid_req('/newsletter/recipients/add.json', data={
        'list': email_list_name,
        'name': marketing_email_name
    })

    quit_if_error(req)

    print 'List added successfully!'


def send_email(marketing_email_name):
    print 'Sending email...'
    req = sendgrid_req('/newsletter/schedule/add.json', data={
        'name': marketing_email_name
    })

    quit_if_error(req)

    print 'Email sent!'

def parse_emails(filename):
    with open(filename) as email_list:
        email_str = email_list.read()
        emails = email_str.strip().split(',')

        ret = []
        for i in xrange(len(emails)):
            email = emails[i].strip()
            if email != '':
                ret.append(email)

        return ret

def sendgrid_req(api_path, data={}):
    data['api_user'] = sendgrid_api_user
    data['api_key'] = sendgrid_api_key

    req = requests.post(sendgrid_api_url + api_path, data=data)
    return req.json()

def main():
    parser = argparse.ArgumentParser(description='Send HackIllinois Acceptance Emails')
    parser.add_argument('filename', help='A comma separated list of emails to send to')
    args = parser.parse_args()

    emails = parse_emails(args.filename)

    print '%d emails read from file: %s' % (len(emails), emails)

    # SendGrid's email API adding only adds 1000 people at a time.
    # If we have a need for it, it's just a few lines to support more than 1000 people by making multiple requests
    if len(emails) > 1000:
        print 'Error: cannot email more than 1000 people. See code for details. This could be easily hacked around.'
        exit()

    if raw_input('> Would you would like to email these addresses? [Y/n]: ').lower() != 'y':
        exit()

    datetime_str = datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')

    # Locate the email containing our template and get the data from it
    template_html, template_subject, template_text = locate_template_email()

    # Create a new marketing email with the data from the template
    marketing_email_name = create_marketing_email(datetime_str, template_html, template_subject, template_text)

    # Create a new email list to store our recipients
    email_list_name = create_email_list(datetime_str)

    print 'sleeping for a minute'
    sleep(60)

    # Add recipients to the list
    add_emails_to_list(email_list_name, emails)

    print 'sleeping for a minute'
    sleep(60)

    # Add the list to the email
    add_list_to_email(email_list_name, marketing_email_name)

    print 'sleeping for a minute'
    sleep(60)

    # Confirm that we should actually send it now
    if raw_input('> Email ready to send. Would you like to send now? [Y/n]: ').lower() != 'y':
        exit()

    # Send the email
    send_email(marketing_email_name)

def exit():
    sys.exit(0)


if __name__ == '__main__':
    main()