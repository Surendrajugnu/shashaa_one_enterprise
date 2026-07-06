# Email Configuration Setup

To enable email notifications for callback requests, follow these steps:

## 1. Get Your Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with your Gmail account (surendra.jugnu@gmail.com)
3. Select **Mail** and **Windows Computer** (or your device type)
4. Google will generate a 16-character app password
5. Copy this password (it looks like: `abcd efgh ijkl mnop`)

## 2. Create .env File

Create a file named `.env` in the project root directory with:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=surendra.jugnu@gmail.com
MAIL_PASSWORD=your-16-character-app-password-here
MAIL_DEFAULT_SENDER=surendra.jugnu@gmail.com
```

Replace `your-16-character-app-password-here` with the actual password from step 1.

## 3. Install python-dotenv

```bash
pip install python-dotenv
```

## 4. Restart the App

Kill the current Flask server and start it again:

```bash
python3 app.py
```

## 5. Test It

1. Go to http://127.0.0.1:5000/get-callback
2. Fill in the form with test data
3. Click "Request Callback"
4. Check your email at surendra.jugnu@gmail.com for the notification

## Troubleshooting

- If emails don't send, check the Flask console for error messages
- Make sure you used the **App Password**, not your regular Gmail password
- Ensure 2-factor authentication is enabled on your Gmail account
- The .env file is ignored by Git for security (see .gitignore)
