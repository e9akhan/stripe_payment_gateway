# Get Started

## Setup

- Login to Stripe Account
- Click on `Developer` link on top.
- In `API Keys`, get `Publishable Key` and `Secret Key`.


## Create a .env file with following variable
- STRIPE_TEST_SECRET_KEY=<YOUR_STRIPE_TEST_SECRET_KEY>
- STRIPE_TEST_PUBLISHABLE_KEY=<YOUR_STRIPE_TEST_PUBLISHABLE_KEY>
- STRIPE_WEBHOOK_KEY=<YOUR_STRIPE_WEBHOOK_KEY>


## Create a virtual environment
```
python3 -m venv venv
```


## Install requirements
```
pip3 install -r requirements.txt
```


## Install Stripe CLI
- Download the latest linux tar.gz file from https://github.com/stripe/stripe-cli/releases/tag/v1.20.0.
- Unzip the file: `tar -xvf stripe_X.X.X_linux_x86_64.tar.gz`.
- Move `./stripe` to your execution path.


## Login to CLI
```
stripe login --api-key <YOUR_STRIPE_SECRET_KEY>
stripe listen --forward-to <WEBHOOK_ENDPOINT>
```
- This will generate your webhook key and will call the webhook after every payment.
- Store the webhook key in `.env`