from lxml import html
from more_itertools import peekable

import re
import json
import sys


def delete_xpath(dom, xpath):
    for el in dom.xpath(xpath):
        el.getparent().remove(el)
    return dom


def split_emails_html(email_string):
    for email in email_string.xpath("a"):
        yield email.text, email.attrib['href']


def split_emails_text(email_string):
    return [e.strip() for e in email_string.split(":", 1)[-1].split(';')]


def extract_all_emails(elements, el):
    emails = [split_emails_text(el.text)]
    try:
        if ';' in el.text:
            while ';' in elements.peek().text and ':' not in elements.peek().text:
                el = next(elements)
                emails += split_emails_text(el.text)
    except TypeError:
        # Not sure what is catching this error
        pass
    try:
        while elements.peek().xpath('a') or ';' in elements.peek().text:
            el = next(elements)
            emails += list(split_emails_html(el))
    except TypeError:
        # Not sure what is catching this error
        pass
    return list(filter(None, emails))


def get_email(elements):
    elements = peekable(elements)
    email = {'body': []}
    while True:
        el = next(elements)
        indicator = (el.text or '').strip().lower()
        if indicator.startswith('from:'):
            if email:
                yield email
            email = {'body': []}
            email['from'] = extract_all_emails(elements, el)
        elif indicator.startswith('reply to:'):
            email['replyto'] = extract_all_emails(elements, el)
        elif indicator.startswith('to:'):
            email['to'] = extract_all_emails(elements, el)
        elif indicator.startswith('cc:'):
            email['cc'] = extract_all_emails(elements, el)
        elif indicator.startswith('subject:'):
            email['subject'] = el.text.split(':', 1)[-1].strip()
            if not email['subject']:
                el = next(elements)
                email['subject'] = el.text
        elif indicator.startswith('date:') or indicator.startswith('sent:'):
            email['date'] = el.text.split(':', 1)[-1].strip()
            if not email['date']:
                el = next(elements)
                email['date'] = el.text
        elif indicator.startswith('attachments:'):
            email['attachments'] = []
            try:
                while elements.peek().text[-4] == '.':
                    el = next(elements)
                    email['attachments'].append(el.text)
            except (IndexError, TypeError):
                pass
        else:
            try:
                email['body'].append((el.attrib['left'], el.text_content()))
            except TypeError:
                pass


if __name__ == "__main__":
    filename = sys.argv[1]
    outfile = sys.argv[2]
    with open(filename, 'rb') as fd:
        html_raw = fd.read().decode('ascii', 'ignore')
        html_raw, _ = re.subn(r"&[^;]+;", "", html_raw)  # h4x
    dom = html.fromstring(bytes(html_raw, 'ascii'))

    # cleanup the dom a bit
    for b in dom.xpath('.//b'):
        b.drop_tag()
    delete_xpath(dom, ".//fontspec")
    delete_xpath(dom, ".//*[not(node())]")  # delete empty nodes
    elements = dom.xpath('.//text')

    # extract
    emails = list(get_email(elements))
    print("Extracted {} emails".format(len(emails)))
    with open(outfile, 'w+') as fd:
        json.dump(emails, fd)
