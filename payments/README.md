# Payments App

A comprehensive Django payments app with Stripe and PayPal integration for handling payments, subscriptions, and invoices.

## Features

- ✅ Stripe integration (one-time payments & subscriptions)
- ✅ PayPal integration (one-time payments)
- ✅ Payment tracking and history
- ✅ Subscription management
- ✅ Invoice generation
- ✅ Webhook handling
- ✅ Refund processing
- ✅ Multiple currency support

## Installation

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... other apps
    'payments',
]
```

### 2. Configure Payment Settings

Add to your `settings.py`:

```python
# Stripe Configuration
STRIPE_PUBLIC_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'
STRIPE_WEBHOOK_SECRET = 'whsec_...'

# PayPal Configuration
PAYPAL_CLIENT_ID = 'your-paypal-client-id'
PAYPAL_CLIENT_SECRET = 'your-paypal-secret'
PAYPAL_MODE = 'sandbox'  # or 'live' for production

# Payment Settings
PAYMENT_CURRENCY = 'USD'
PAYMENT_SUCCESS_URL = '/payments/success/'
PAYMENT_CANCEL_URL = '/payments/cancel/'
```

### 3. Install Required Packages

```bash
pip install stripe
pip install paypalrestsdk
pip install python-decouple
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Include URLs

Add to your main `urls.py`:

```python
urlpatterns = [
    # ... other patterns
    path('payments/', include('payments.urls')),
]
```

### 6. Setup Webhooks

#### Stripe Webhooks
1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/payments/webhook/stripe/`
3. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`, `customer.subscription.created`, etc.
4. Copy webhook secret to `STRIPE_WEBHOOK_SECRET`

#### PayPal Webhooks
1. Go to PayPal Developer Dashboard → Webhooks
2. Add webhook: `https://yourdomain.com/payments/webhook/paypal/`
3. Select events: `PAYMENT.SALE.COMPLETED`, `PAYMENT.SALE.REFUNDED`, etc.

## Usage

### One-Time Payments

#### Stripe Payment

```python
from payments.services import StripeService

# Create payment intent
stripe_service = StripeService()
payment_intent = stripe_service.create_payment_intent(
    amount=1000,  # Amount in cents ($10.00)
    currency='usd',
    customer_email='customer@example.com',
    metadata={'order_id': '12345'}
)

# Get client secret for frontend
client_secret = payment_intent['client_secret']
```

#### PayPal Payment

```python
from payments.services import PayPalService

# Create payment
paypal_service = PayPalService()
payment = paypal_service.create_payment(
    amount=10.00,
    currency='USD',
    description='Product Purchase',
    return_url='http://yourdomain.com/payments/paypal/execute/',
    cancel_url='http://yourdomain.com/payments/cancel/'
)

# Get approval URL for redirect
approval_url = payment.get_approval_url()
```

### Subscriptions (Stripe)

```python
from payments.services import StripeService

stripe_service = StripeService()

# Create subscription
subscription = stripe_service.create_subscription(
    customer_email='customer@example.com',
    price_id='price_...',  # Stripe price ID
    trial_days=14
)
```

### Refunds

#### Stripe Refund

```python
from payments.services import StripeService

stripe_service = StripeService()
refund = stripe_service.create_refund(
    payment_intent_id='pi_...',
    amount=500  # Partial refund of $5.00
)
```

#### PayPal Refund

```python
from payments.services import PayPalService

paypal_service = PayPalService()
refund = paypal_service.refund_payment(
    sale_id='...',
    amount=5.00
)
```

## API Endpoints

### Create Stripe Payment Intent
```
POST /payments/stripe/create-intent/
{
    "amount": 1000,
    "currency": "usd",
    "description": "Product purchase"
}
Response: {
    "client_secret": "pi_..._secret_...",
    "payment_intent_id": "pi_..."
}
```

### Create PayPal Payment
```
POST /payments/paypal/create/
{
    "amount": 10.00,
    "currency": "USD",
    "description": "Product purchase"
}
Response: {
    "approval_url": "https://www.paypal.com/...",
    "payment_id": "PAYID-..."
}
```

### Execute PayPal Payment
```
POST /payments/paypal/execute/
{
    "payment_id": "PAYID-...",
    "payer_id": "..."
}
```

### Create Subscription
```
POST /payments/stripe/create-subscription/
{
    "price_id": "price_...",
    "customer_email": "customer@example.com",
    "trial_days": 14
}
```

### Cancel Subscription
```
POST /payments/stripe/cancel-subscription/
{
    "subscription_id": "sub_..."
}
```

### Get Payment History
```
GET /payments/history/
Response: [
    {
        "id": 1,
        "amount": "10.00",
        "currency": "USD",
        "status": "succeeded",
        "provider": "stripe",
        "created_at": "2026-01-09T10:56:29Z"
    }
]
```

### Create Refund
```
POST /payments/refund/
{
    "payment_id": 1,
    "amount": 5.00,
    "reason": "Customer request"
}
```

## Models

### Payment
Tracks all payments made through the system.

Fields:
- `user` - ForeignKey to User
- `amount` - Decimal amount
- `currency` - Currency code
- `status` - Payment status (pending, succeeded, failed, refunded)
- `provider` - Payment provider (stripe, paypal)
- `provider_payment_id` - External payment ID
- `description` - Payment description
- `metadata` - JSON metadata

### Subscription
Tracks user subscriptions.

Fields:
- `user` - ForeignKey to User
- `plan_name` - Subscription plan name
- `status` - Subscription status (active, canceled, past_due)
- `provider` - Payment provider
- `provider_subscription_id` - External subscription ID
- `current_period_start` - Period start date
- `current_period_end` - Period end date
- `cancel_at_period_end` - Boolean

### Invoice
Tracks invoices for payments.

Fields:
- `payment` - ForeignKey to Payment
- `invoice_number` - Unique invoice number
- `amount` - Invoice amount
- `status` - Invoice status (draft, sent, paid, void)
- `due_date` - Payment due date
- `pdf_file` - PDF invoice file

### Refund
Tracks refund transactions.

Fields:
- `payment` - ForeignKey to Payment
- `amount` - Refund amount
- `reason` - Refund reason
- `status` - Refund status
- `provider_refund_id` - External refund ID

## Frontend Integration

### Stripe Elements (JavaScript)

```html
<script src="https://js.stripe.com/v3/"></script>
<script>
    const stripe = Stripe('{{ STRIPE_PUBLIC_KEY }}');
    
    // Create payment intent on backend first
    fetch('/payments/stripe/create-intent/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({amount: 1000, currency: 'usd'})
    })
    .then(res => res.json())
    .then(data => {
        return stripe.confirmCardPayment(data.client_secret, {
            payment_method: {
                card: cardElement,
                billing_details: {email: 'customer@example.com'}
            }
        });
    })
    .then(result => {
        if (result.error) {
            console.error(result.error.message);
        } else {
            console.log('Payment succeeded!');
        }
    });
</script>
```

### PayPal Buttons (JavaScript)

```html
<script src="https://www.paypal.com/sdk/js?client-id={{ PAYPAL_CLIENT_ID }}"></script>
<div id="paypal-button-container"></div>
<script>
    paypal.Buttons({
        createOrder: function(data, actions) {
            return fetch('/payments/paypal/create/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({amount: 10.00, currency: 'USD'})
            })
            .then(res => res.json())
            .then(data => data.payment_id);
        },
        onApprove: function(data, actions) {
            return fetch('/payments/paypal/execute/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    payment_id: data.orderID,
                    payer_id: data.payerID
                })
            })
            .then(res => res.json())
            .then(data => alert('Payment successful!'));
        }
    }).render('#paypal-button-container');
</script>
```

## Testing

### Test Cards (Stripe)

- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `4000 0027 6000 3184`

### Test PayPal

Use PayPal Sandbox accounts from Developer Dashboard.

## Security Best Practices

1. **Never expose secret keys** in frontend code
2. **Validate webhook signatures** to prevent fraud
3. **Use HTTPS** for all payment endpoints
4. **Store minimal payment data** (use provider IDs)
5. **Implement idempotency** for payment operations
6. **Log all transactions** for audit trail
7. **Handle errors gracefully** with user-friendly messages
8. **Comply with PCI DSS** if storing card data

## Troubleshooting

### Issue: Webhook not receiving events
- Check webhook URL is publicly accessible
- Verify webhook secret is correct
- Check firewall/security settings
- Review webhook logs in provider dashboard

### Issue: Payment fails silently
- Check API keys are correct
- Verify amount is in correct format (cents for Stripe)
- Check currency is supported
- Review error logs

### Issue: Subscription not created
- Verify price ID exists in Stripe
- Check customer email is valid
- Ensure payment method is attached
- Review subscription settings

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
