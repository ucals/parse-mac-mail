import os
import re
import pandas as pd
from datetime import datetime

targetdir = '/Users/carlos/Dropbox'
rootdir = '/Users/carlos/Library/Mail/V4'

email_lines = []
emails = []
df1 = pd.DataFrame(columns=['Name', 'Email', 'String'])
df2 = pd.DataFrame(columns=['Email'])

for subdir, dirs, files in os.walk(rootdir):
    gen = (f for f in files if f.endswith('.emlx'))
    for index, file in enumerate(gen):
        file_path = os.path.join(subdir, file)
        with open(file_path, encoding='utf-8', errors='replace') as f:
            for line in f:
                if line.startswith('From:') or line.startswith('To:'):
                    processed_line = line.strip().lower().split(':')[1]
                    for emails_names in processed_line.split(','):
                        if len(emails_names) > 0 and '@' in emails_names:
                            email_lines.append(emails_names.strip().replace('"', ''))

x = set(email_lines)
x = sorted(x)
for index, email_line in enumerate(x):
    m = re.search('(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)', email_line)
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
