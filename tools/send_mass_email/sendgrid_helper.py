#!/usr/bin/env python
import json
from time import sleep

import argparse
import datetime
import requests
import sys

import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError
from smtpapi import SMTPAPIHeader


sendgrid_api_user = 'hackillinois'
sendgrid_api_key = 'RXeN7Ju2y'

sendgrid_api_url = 'https://api.sendgrid.com/api'
sendgrid_identity = 'contact@hackillinois.org'

# CHANGE THESE
sendgrid_template_name = 'Second Survey Email'
category = "test_team"
subject = "test"

def main():
    parser = argparse.ArgumentParser(description='Send Mass Emails')
    parser.add_argument('filename', help='A comma separated list of emails to send to')
    args = parser.parse_args()

    emails = parse_emails(args.filename)

    print '%d emails read from file: %s' % (len(emails), emails)

    # SendGrid's email API adding only adds 1000 people at a time.
    # If we have a need for it, it's just a few lines to support more than 1000 people by making multiple requests
    if len(emails) > 1000:
        print 'Error: cannot email more than 1000 people. See code for details. This could be easily hacked around.'
        exit()

    if raw_input('> Would you would like to email these addresses? [y/n]: ').lower() != 'y':
        exit()

    # Locate the email containing our template and get the data from it
    template_html, template_subject, template_text = locate_template_email()

    # Create a new email with the data from the template
    message = create_email(template_html, template_subject, template_text, emails, category)

    # Confirm that we should actually send it now
    if raw_input('> Email ready to send. Would you like to send now? [y/n]: ').lower() != 'y':
        exit()

    # Send the email

    print 'Sending email...'
    sg = sendgrid.SendGridClient(sendgrid_api_user, sendgrid_api_key, raise_errors=True)

    try:
        sg.send(message)
    except SendGridError:
        print SendGridError
        exit()
    print "Email Sent!"


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

def create_email(template_html, template_subject, template_text, emails, category):
    print 'Creating Email...'
    message = sendgrid.Mail()

    message.set_subject(subject)
    message.set_text(template_text)
    message.set_html(template_html)
    message.set_from(sendgrid_identity)
    message.add_category(category)
    message.add_to(emails)
    #message.add_bcc(['example1@email.com', 'example2@gmail.com]')

    print 'Email created successfully!'
    return message

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

def exit():
    sys.exit(0)


if __name__ == '__main__':
    main()