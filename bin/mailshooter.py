import os
import yaml
import argparse
import csv
from mako.template import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def parse_args():
    parser = argparse.ArgumentParser(description='Shooting mails. yeah')

    parser.add_argument(
        '--config',
        default='./config.yaml',
        type=argparse.FileType('r'),
        help='configuration file')
    
    parser.add_argument(
        'template', metavar='TEMPLATE',
        type=argparse.FileType('r'),
        help='Template file for mail. Mako template engine format')
    
    parser.add_argument(
        'csv', metavar='CSV',
        type=argparse.FileType('r'),
        help='Data for templates. First row is template argument')

    return parser.parse_args()

def csv_to_dict(csvfile):
    csvreader = csv.reader(csvfile)

    header_row = next(csvreader)

    if 'email' not in header_row:
        raise Exception("CSV must contain 'email' column")
    
    for row in csvreader:
        yield dict(zip(header_row, row))

def inflate(config, template, datas):
    sender = config['sender']
    subject = template['subject']
    body_template = Template(template['body'])

    attachments = []
    for cid in template['attachment'].keys():
        info = template['attachment'][cid]
        with open(info['path'], 'rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', '<{0}>'.format(cid))
            attachments.append(image)
    
    for data in datas:
        receiver = data['email']
        root = MIMEMultipart('related')
        root['Subject'] = subject
        root['From'] = sender
        root['To'] = receiver

        try:
            body = body_template.render(**data)
        except:
            raise Exception("Check template's variables and csv header")
        
        text = MIMEText(body, 'html', 'utf-8')

        root.attach(text)
        for attach in attachments:
            root.attach(attach)

        yield dict(
            sender = sender,
            receiver = receiver,
            message = root)
        
def send(config, mails):
    smtp = smtplib.SMTP(config['smtp'], config['port'])
    smtp.starttls()
    smtp.login(config['id'], config['password'])

    count=1
    for mail in mails:
        print('sending {0} th mail to {1}'.format(count, mail['receiver']))
        smtp.sendmail(
            mail['sender'], mail['receiver'],
            mail['message'].as_string())
        count = count + 1
        
    smtp.quit()

def main():
    args = parse_args();

    config = yaml.load(args.config)

    template = yaml.load(args.template)
    datas = csv_to_dict(args.csv)

    mails = inflate(config, template, datas)
    
    send(config, mails)

if __name__ == '__main__':
    main()
