import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime
import os

# Email credentials and settings

RECIPIENT = "ilekuraidowu@gmail.com"
SUBJECT = "Remember to log your time on Personio."
BODY = "This is a friendly reminder to log your time on Personio with this link https://fctg.personio.de/"

def send_email():
    # Check if today is Monday through Friday
    current_day = datetime.now().weekday()  # 0=Monday, 6=Sunday
    if current_day < 5:  # Monday to Friday
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = RECIPIENT
        msg["Subject"] = SUBJECT
        msg.attach(MIMEText(BODY, "plain"))

        try:
            # Connect to Gmail's SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(EMAIL, PASSWORD)
                server.send_message(msg)
                print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        print("Today is not a weekday. Email not sent.")

def delete_email():
    try:
        # Connect to Gmail's IMAP server
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(EMAIL, PASSWORD)
            mail.select("inbox")

            # Search for the specific email by subject
            status, messages = mail.search(None, f'SUBJECT "{SUBJECT}"')
            email_ids = messages[0].split()

            if email_ids:
                for email_id in email_ids:
                    # Mark email for deletion
                    mail.store(email_id, "+FLAGS", "\\Deleted")
                mail.expunge()  # Permanently delete the email
                print("Email deleted successfully.")
            else:
                print("No email found with the given subject.")
    except Exception as e:
        print(f"Error deleting email: {e}")

# Schedule the email deletion one hour after sending
# schedule.every().day.at("09:00").do(send_email)  # Send email at 9:00 AM if it's a weekday
# schedule.every(1).hour.do(delete_email)  # Schedule deletion

# Keep the script running to execute the scheduled task

send_email()
def time_sleep(hours_before_delete: int) -> int:
    seconds_to_hours = hours_before_delete * 3600
    return round(seconds_to_hours)

def main():
    print("about to send the email")
    send_email()
    print("sleeping now")
    time.sleep(time_sleep(0.01))
    delete_email()


if __name__ == "__main__":
    main()
