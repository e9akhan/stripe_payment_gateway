from django.urls import path
from payment_app.views import makepayment, create_checkout_session, returnpage, checkoutpage, stripe_webhook

urlpatterns = [
    # path("charge/", charge),
    path("make-payment/", makepayment, name="make-payment"),
    path("create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("", checkoutpage, name="checkout"),
    path("return/", returnpage, name="return"),
    path("webhook/", stripe_webhook)
]