"""
Usage: python gmail_delete.py

Make sure to set the variables under "SET THESE"

Deletes the "percentage" of emails from the specified Gmail account for the
specified time period.

For example, the default parameters will delete 75% of emails in the account
that came during 2019.

Note: it might be deleting entire threads, so be careful.

If you get authentication errors even though credentials are correct:
1. Enable "less secure apps" via https://myaccount.google.com/u/0/lesssecureapp
2. Allow non-web access via https://accounts.google.com/b/0/DisplayUnlockCaptcha
"""

import imaplib
import datetime
import random


# delete mails for the given date
def get_emails(start_date, last_date):
    last_date += datetime.timedelta(days=1)
    last_date = last_date.strftime('%Y/%m/%d')
    start_date = start_date.strftime('%Y/%m/%d')
    search_key = "after:" + start_date + "before:" + last_date

    status, message_ids = con.search(None, 'X-GM-RAW', search_key)

    if status != 'OK':
        print "messages can't be fetched"

    return message_ids[0].split()


# SET THESE

user = ''
password = ''

max_emails_per_day = 2500

start_year = 2019
start_month = 1
start_day = 1

end_year = 2019
end_month = 12
end_day = 31

# END SET THESE

imap_url = "imap.googlemail.com"

try:
    con = imaplib.IMAP4_SSL(imap_url)
    print "\nConnecting to mailbox..."
    con.login(user, password)
    con.select('INBOX')
except imaplib.IMAP4.error as e:
    print "Log in failed: %s" % e
    raise SystemExit

start_date_time = datetime.datetime(start_year, start_month, start_day)
last_date_time = datetime.datetime(end_year, end_month, end_day)

uids = get_emails(start_date_time, last_date_time)
print "total emails from %d/%d/%d - %d/%d/%d: %d" % \
    (start_year, start_month, start_day, end_year, end_month, end_day, len(uids))

print "Do you wish to continue? (y/n)"
answer = raw_input()

if answer.lower() != 'y':
    print "Quitting\n\n"
    raise SystemExit

success = 0
failed = 0

while (start_date_time <= last_date_time):
    uids = get_emails(start_date_time, start_date_time)

    print("total emails for %s: %d"
          % (start_date_time.strftime('%Y/%m/%d'), len(uids)))

    random.shuffle(uids)
    uids_to_delete = uids[max_emails_per_day:]
    current_date = start_date_time.strftime('%Y/%m/%d')
    start_date_time += datetime.timedelta(days=1)
    emails_deleted = 0
    try:
        if uids_to_delete:
            typ, stored = con.store(
                ",".join(uids_to_delete), '+FLAGS', '\\Deleted'
            )
            emails_deleted = len(stored)

        print("Deleted emails for %s: %d" % (current_date, emails_deleted))
        success += emails_deleted
    except imaplib.IMAP4.error:
        print "Deletion failed %s: %d" % (current_date, len(uids_to_delete))
        failed += len(uids_to_delete)

typ, expunged = con.expunge()
print "Deleted successfully: %d" % success
print "Deletion failed: %d" % failed

con.close()
con.logout()