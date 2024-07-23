import json
import pandas as pd
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Sample JSON data
json_data = '''
[
    {"name": "John Doe", "email": "john@example.com", "age": 30},
    {"name": "Jane Smith", "email": "jane@example.com", "age": 25}
]
'''

# Convert JSON data to DataFrame
data = json.loads(json_data)
df = pd.DataFrame(data)

# Save DataFrame to Excel file
excel_file = 'data.xlsx'
df.to_excel(excel_file, index=False)

# Email details
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "anasbenbow123@gmail.com"
smtp_password = "znya yyup ztbm lzxj"
to_email = "anasbenabbou776@gmail.com"
subject = "JSON Data Excel File"
body = "Please find attached the Excel file created from JSON data."

# Create email
msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = to_email
msg['Subject'] = subject

# Attach the body text
msg.attach(MIMEText(body, 'plain'))

# Attach the Excel file
with open(excel_file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {excel_file}",
    )
    msg.attach(part)

# Send email
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls(context=context)
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, to_email, msg.as_string())

print("Email sent successfully!")
