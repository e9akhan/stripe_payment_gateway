const buttons = document.querySelectorAll('#buy-now-button')
// Create a Checkout Session
async function initialize() {
  const response = await fetch("/make-payment/", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  const session = await response.json();
  // console.log(response.json())
  var stripe = Stripe(session.checkout_public_key)

  const checkout = await stripe.redirectToCheckout({
    sessionId: session.checkout_session_id,
  });

  if (checkout.error){
    console.log(checkout.error)
  }
}

buttons.forEach(button=>{
  button.addEventListener("click", function(e){
    e.preventDefault();
    initialize()
  })
});