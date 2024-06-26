const buttons = document.querySelectorAll('#buy-now-button')
// Create a Checkout Session
async function initialize() {
  const response = await fetch(
    "/make-payment/",
    {method: "GET"}
  )
;
  if (!response.ok) {
    console.log(response.error)
    throw new Error("Network response was not ok");
  }

  const session = await response.json();
  var stripe = Stripe(session.checkout_public_key);

// Redirect to checkout page
  const checkout = stripe.redirectToCheckout({
    sessionId: session.checkout_session_id,
  });

// If any error print
  if (checkout.error){
    console.log(checkout.error);
  }
}

buttons.forEach(button=>{
  button.addEventListener("click", function(e){
    e.preventDefault();
    // paymenturl = button.getAttribute('data-target-url')
    initialize();
  })
});