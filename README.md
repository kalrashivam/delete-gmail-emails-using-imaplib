This is a python script to delete gmail emails randomly.
This is made to delete a percentage of emails for each day but can be easily changed otherwise.
And just make sure that the expunge command runs everytime.

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
