from django.urls import path
from payment_app.views import makepayment, returnpage, checkoutpage, stripe_webhook, create_checkout_session

urlpatterns = [
    # path("charge/", charge),
    path("make-payment/", makepayment),
    path("create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("checkout/", checkoutpage, name="checkout"),
    path("return/", returnpage, name="return"),
    path("webhook/", stripe_webhook)
]