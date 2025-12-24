import os
import datetime
import yagmail
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import re
import pandas as pd
# Load environment variables from .env
load_dotenv()

# Config from environment
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ZOHO_EMAIL = os.getenv("ZOHO_EMAIL")
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD")
HR_EMAIL = os.getenv("HR_EMAIL")

# Initialize Slack client
client = WebClient(token=SLACK_BOT_TOKEN)



def fetch_checkins():
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date(), datetime.time.min)
    oldest = midnight.timestamp()

    checkins = []

    try:
        # Get all top-level messages
        response = client.conversations_history(channel=CHANNEL_ID, oldest=oldest)
        messages = response["messages"]

        for msg in messages:
            # ✅ Check top-level message for check-in
            text = msg.get("text", "")
            user_id = msg.get("user", "")
            ts = float(msg.get("ts", "0"))
            time_str = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

            if re.search(r"check[\s\-]?in", text, re.IGNORECASE) and user_id:
                user_info = client.users_info(user=user_id)
                real_name = user_info["user"]["profile"]["real_name"]
                checkins.append({
                    "Employee": real_name,
                    "Time": time_str,
                    "Message": text
                })

            # ✅ Now check thread replies (if any)
            if "reply_count" in msg and msg["reply_count"] > 0:
                thread_ts = msg["ts"]
                replies = client.conversations_replies(channel=CHANNEL_ID, ts=thread_ts)

                for reply in replies["messages"][1:]:  # skip first (it's the parent message)
                    text = reply.get("text", "")
                    user_id = reply.get("user", "")
                    ts = float(reply.get("ts", "0"))
                    time_str = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                    if re.search(r"check[\s\-]?in", text, re.IGNORECASE) and user_id:
                        user_info = client.users_info(user=user_id)
                        real_name = user_info["user"]["profile"]["real_name"]
                        checkins.append({
                            "Employee": real_name,
                            "Time": time_str,
                            "Message": text
                        })

        print(f"📋 Found {len(checkins)} check-ins (including threads and messages).")
        return checkins

    except SlackApiError as e:
        print(f"❌ Error fetching messages: {e}")
        return []




def send_email(checkins):
    """Send email with the check-in report as Excel attachment to HR."""
    if not checkins:
        print("📭 No check-ins to email.")
        return

    try:
        # ✅ Create DataFrame directly from list of dicts
        df = pd.DataFrame(checkins, columns=["Employee", "Time", "Message"])

        # Save to Excel
        file_name = "daily_checkins.xlsx"
        df.to_excel(file_name, index=False)

        # Send email with attachment
        yag = yagmail.SMTP(
            user=ZOHO_EMAIL,
            password=ZOHO_PASSWORD,
            host='smtp.zoho.com',
            port=587,
            smtp_starttls=True,
            smtp_ssl=False
        )

        subject = "Daily Check-ins Report (Excel)"
        body = "Please find the daily check-in report."

        yag.send(to=HR_EMAIL, subject=subject, contents=body, attachments=file_name)
        print("📧 Email with Excel attachment sent to HR.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def job():
    """Main job to fetch check-ins and send the email."""
    print("🔄 Running job...")
    checkins = fetch_checkins()
    send_email(checkins)

if __name__ == "__main__":
    now = datetime.datetime.now()
    print(f"🕒 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Forcing job run for testing...")
    job()
