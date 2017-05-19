import mailbox, re, os
import pandas as pd
from datetime import datetime


targetdir = '/Users/carlos/Dropbox'
mbox_file = '/Volumes/Backup/EmailVeducaFinal/VeducaBackup.mbox/mbox'
# '/Volumes/Backup/EmailVeduca/VeducaBackup.partial.mbox/mbox'

email_lines = []
emails = []
df1 = pd.DataFrame(columns=['Name', 'Email', 'String'])
df2 = pd.DataFrame(columns=['Email'])

print('Reading mbox file...')
messages = mailbox.mbox(mbox_file)
n = len(messages)

for (i, msg) in enumerate(messages):
    if type(msg['from']) is str:
        from_str = msg['from'].strip()
        email_lines.append(from_str)
        print(from_str)

    if msg['to'] is not None:
        for emails_names in msg['to'].split(','):
            if len(emails_names) > 0 and '@' in emails_names:
                to_str = emails_names.strip().replace('"', '')
                email_lines.append(to_str)
                print(to_str)


x = set(email_lines)
x = sorted(x)
for index, email_line in enumerate(x):
    m = re.search('(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)', email_line)
    if m is not None:
        name = m.group(1)
        em = m.group(2)
        st = m.group(0)
        emails.append(em)
        df1.loc[len(df1)] = [name, em, email_line]


y = set(emails)
y = sorted(y)
for index, email in enumerate(y):
    print(email)
    df2.loc[index] = [email]

print("\nUnique entries: %d" % len(y))

tdy = datetime.now().strftime('%Y-%m-%d_%H%M%S')
df1.to_csv(os.path.join(targetdir, 'names_emails_' + tdy + '.csv'))
df2.to_csv(os.path.join(targetdir, 'emails_' + tdy + '.csv'))