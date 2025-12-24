# Slack Daily Check-in Automation

A Python-based automation script that collects daily employee check-in messages from a Slack channel (including thread replies), generates an Excel report, and emails it to HR automatically.

---

## 📌 Overview

This project is designed to automate daily attendance/check-in tracking from Slack.  
It scans messages posted after midnight, identifies check-in messages using keyword matching, extracts employee details, and sends a consolidated Excel report via email.

The application runs as a standalone Python script and does **not store data permanently**.

---

## ⚙️ How It Works

1. Loads configuration securely using environment variables
2. Connects to Slack using the Slack Web API
3. Fetches all messages posted after midnight from a specified channel
4. Scans both channel messages and thread replies for check-in keywords
5. Extracts employee name, time, and message content
6. Generates an Excel report using pandas
7. Emails the report to HR using Zoho SMTP
8. Runs fully in memory (no database or persistent storage)

---

## 🛠️ Tech Stack

- **Language:** Python
- **Slack API:** `slack_sdk`
- **Email:** Zoho SMTP via `yagmail`
- **Environment Management:** `python-dotenv`
- **Data Processing:** `pandas`
- **Excel Export:** `openpyxl`

---

## 🔐 Security Practices

- No hardcoded API keys or passwords
- Uses environment variables for all sensitive data
- `.env` file is excluded from version control
- `.env.example` provided for reference

---

## 📂 Project Structure

```text
project/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
