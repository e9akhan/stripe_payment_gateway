# from django.shortcuts import render

# # Create your views here.
import stripe
import os
import requests
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render


load_dotenv()


stripe.api_key = os.getenv("STRIPE_TEST_SECRET_KEY")


def returnpage(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    if session['payment_status'] == 'unpaid':
        return HttpResponse("payment not successful")

    invoice_id = session['invoice']
    if invoice_id:
        stripe.Invoice.send_invoice(invoice_id)

    return JsonResponse(
        {"session": session}, status=200
    )


def checkoutpage(request):
    return render(request, "checkout.html")


@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        params = request.POST
        payment_methods = params.getlist("payment_method_types")
        product_name = params["product_name"]
        product_amount = params["product_amount"]
        quantity = params["quantity"]
        mode = params["mode"]
        invoice_creation_status = params["invoice_creation_status"]
        success_url = params["success_url"]
        cancel_url = params["cancel_url"]
        customer_email = params["customer_email"]

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=payment_methods,
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data":{
                            "name": product_name,
                        },
                        "unit_amount": product_amount
                    },
                    "quantity": quantity,
                }],
                mode=mode,
                invoice_creation={
                    "enabled": invoice_creation_status
                },
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
                customer_email=customer_email,
            )
            
        except stripe.CardError as ce:
            return JsonResponse(error=ce)
        except stripe.InvalidRequestError as invalid_request:
            print(invalid_request)
            return HttpResponse(status=400)

        return JsonResponse({"data": session})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

    
@csrf_exempt
def makepayment(request):
    url = request.build_absolute_uri(reverse("create-checkout-session"))
    data = {
        "payment_method_types": ["card", "amazon_pay"],
        "product_name": "T-Shirt",
        "product_amount": 2000,
        "quantity": 1,
        "invoice_creation_status": True,
        "success_url": "http://127.0.0.1:4242/return/",
        "cancel_url": "http://127.0.0.1:4242/",
        "customer_email": "akhan@enine.dev",
        "mode": "payment"
    }
    response = requests.post(url, data=data)
    session = response.json()["data"]

    return JsonResponse(
            {
                "checkout_public_key": os.getenv('STRIPE_TEST_PUBLISHABLE_KEY'),
                "checkout_session_id": session["id"]
            }
        )

# @csrf_exempt
# def stripe_webhook(request):
#     if request.method == "POST":
#         payload = request.body.decode('utf-8')
#         sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#         event = None

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, os.getenv('STRIPE_WEBHOOK_KEY')
#             )
#         except ValueError as e:
#             # Invalid payload
#             print('⚠️  Webhook error while parsing request payload.' + str(e))
#             return JsonResponse({'success': False}, status=400)
#         except stripe.SignatureVerificationError as e:
#             # Invalid signature
#             print('⚠️  Webhook signature verification failed.' + str(e))
#             return JsonResponse({'success': False}, status=400)

#         # Handle the event
#         if event['type'] == 'checkout.session.completed':
#             session = event['data']['object']
#             invoice_id = session['invoice']
#             # Handle completed checkout session event
#             if invoice_id:
#                 invoice = stripe.Invoice.send_invoice(invoice_id)
#                 print(f"Sent invoice {invoice.id}")

#         # Return a response to acknowledge receipt of the event
#         return JsonResponse({'status': 'success'})

#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# def handle_checkout_session_completed(session):
#     # Retrieve relevant information from the session object
#     payment_intent = session['payment_intent']
#     customer_email = session['customer_details']['email']
#     amount_total = session['amount_total']
#     payment_status = session['payment_status']

#     # Implement your business logic based on the completed session
#     print(f"Checkout session completed for customer {customer_email} with payment intent {payment_intent} and amount {amount_total} cents. Status: {payment_status}")

