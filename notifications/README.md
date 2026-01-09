# Notifications App

A comprehensive Django notifications app supporting email, SMS, push notifications, and in-app notifications.

## Features

- ✅ Email notifications (SMTP, SendGrid, Mailgun)
- ✅ SMS notifications (Twilio, AWS SNS)
- ✅ Push notifications (Firebase, OneSignal)
- ✅ In-app notifications
- ✅ Slack notifications
- ✅ Webhook notifications
- ✅ Notification templates
- ✅ Notification preferences
- ✅ Batch notifications
- ✅ Scheduled notifications
- ✅ Notification history

## Installation

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... other apps
    'notifications',
]
```

### 2. Configure Notification Settings

Add to your `settings.py`:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yourapp.com'

# Twilio Configuration (SMS)
TWILIO_ACCOUNT_SID = 'your-account-sid'
TWILIO_AUTH_TOKEN = 'your-auth-token'
TWILIO_PHONE_NUMBER = '+1234567890'

# Firebase Configuration (Push)
FIREBASE_SERVER_KEY = 'your-firebase-server-key'
FIREBASE_SENDER_ID = 'your-sender-id'

# OneSignal Configuration (Push)
ONESIGNAL_APP_ID = 'your-app-id'
ONESIGNAL_REST_API_KEY = 'your-api-key'

# Slack Configuration
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/...'
SLACK_BOT_TOKEN = 'xoxb-...'

# Notification Settings
NOTIFICATION_RETENTION_DAYS = 90
NOTIFICATION_BATCH_SIZE = 100
```

### 3. Install Required Packages

```bash
pip install twilio
pip install firebase-admin
pip install onesignal-sdk
pip install slack-sdk
pip install sendgrid
pip install mailgun
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Include URLs

```python
urlpatterns = [
    # ... other patterns
    path('notifications/', include('notifications.urls')),
]
```

## Usage

### Email Notifications

```python
from notifications.services import EmailNotificationService

service = EmailNotificationService()

# Send single email
service.send_email(
    to='user@example.com',
    subject='Welcome!',
    template='welcome_email.html',
    context={'name': 'John Doe'}
)

# Send bulk email
service.send_bulk_email(
    recipients=['user1@example.com', 'user2@example.com'],
    subject='Newsletter',
    template='newsletter.html',
    context={'month': 'January'}
)
```

### SMS Notifications

```python
from notifications.services import SMSNotificationService

service = SMSNotificationService()

# Send SMS
service.send_sms(
    to='+1234567890',
    message='Your verification code is: 123456'
)

# Send bulk SMS
service.send_bulk_sms(
    recipients=['+1234567890', '+0987654321'],
    message='Important announcement'
)
```

### Push Notifications

```python
from notifications.services import PushNotificationService

service = PushNotificationService()

# Send to single device
service.send_push(
    device_token='device-token-here',
    title='New Message',
    body='You have a new message',
    data={'message_id': '123'}
)

# Send to multiple devices
service.send_push_to_devices(
    device_tokens=['token1', 'token2'],
    title='Update Available',
    body='A new version is available'
)

# Send to topic
service.send_push_to_topic(
    topic='news',
    title='Breaking News',
    body='Important update'
)
```

### In-App Notifications

```python
from notifications.services import InAppNotificationService

service = InAppNotificationService()

# Create notification
service.create_notification(
    user=user,
    title='New Comment',
    message='Someone commented on your post',
    notification_type='comment',
    link='/posts/123/'
)

# Get user notifications
notifications = service.get_user_notifications(user, unread_only=True)

# Mark as read
service.mark_as_read(notification_id)
```

### Slack Notifications

```python
from notifications.services import SlackNotificationService

service = SlackNotificationService()

# Send to channel
service.send_to_channel(
    channel='#general',
    message='Deployment completed successfully',
    username='Deploy Bot'
)

# Send direct message
service.send_direct_message(
    user_id='U123456',
    message='Your report is ready'
)
```

## API Endpoints

### Get User Notifications
```
GET /notifications/
Response: [
    {
        "id": 1,
        "title": "New Message",
        "message": "You have a new message",
        "type": "message",
        "is_read": false,
        "created_at": "2026-01-09T10:56:29Z"
    }
]
```

### Mark as Read
```
POST /notifications/{id}/read/
```

### Mark All as Read
```
POST /notifications/read-all/
```

### Delete Notification
```
DELETE /notifications/{id}/
```

### Get Notification Preferences
```
GET /notifications/preferences/
```

### Update Notification Preferences
```
PUT /notifications/preferences/
{
    "email_enabled": true,
    "sms_enabled": false,
    "push_enabled": true,
    "notification_types": {
        "comments": true,
        "messages": true,
        "updates": false
    }
}
```

## Models

### Notification
In-app notification model.

### NotificationPreference
User notification preferences.

### NotificationTemplate
Reusable notification templates.

### NotificationLog
History of sent notifications.

### DeviceToken
User device tokens for push notifications.

## Notification Types

- `info` - Informational
- `success` - Success messages
- `warning` - Warnings
- `error` - Error messages
- `message` - User messages
- `comment` - Comments
- `like` - Likes
- `follow` - New followers
- `system` - System notifications

## Templates

Create email templates in `notifications/templates/notifications/emails/`:

```html
<!-- welcome_email.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome, {{ name }}!</h1>
    <p>Thank you for joining our platform.</p>
</body>
</html>
```

## Celery Tasks

Schedule notifications using Celery:

```python
from notifications.tasks import send_notification_task

# Send async
send_notification_task.delay(
    user_id=user.id,
    notification_type='email',
    subject='Hello',
    message='World'
)

# Schedule for later
send_notification_task.apply_async(
    args=[user.id, 'email', 'Reminder', 'Don\'t forget!'],
    eta=datetime.now() + timedelta(hours=24)
)
```

## Best Practices

1. **Use templates** for consistent messaging
2. **Respect user preferences** - check before sending
3. **Batch notifications** for better performance
4. **Rate limit** to avoid spam
5. **Track delivery** status
6. **Handle failures** gracefully
7. **Clean old notifications** regularly
8. **Test thoroughly** before production

## Testing

```bash
python manage.py test notifications
```

## Troubleshooting

### Issue: Emails not sending
- Check SMTP credentials
- Verify firewall settings
- Check spam folder
- Review email logs

### Issue: SMS not delivered
- Verify Twilio credentials
- Check phone number format
- Ensure sufficient credits
- Review Twilio logs

### Issue: Push notifications not working
- Verify Firebase/OneSignal setup
- Check device token validity
- Ensure proper permissions
- Review service logs

## License

MIT License
