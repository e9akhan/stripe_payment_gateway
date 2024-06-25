const buttons = document.querySelectorAll('#buy-now-button')
// Create a Checkout Session
function initialize() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/make-payment/", false);
  xhr.send()
;
  if (xhr.status !== 200) {
    throw new Error("Network response was not ok");
  }

  const session = JSON.parse(xhr.responseText);
  var stripe = Stripe(session.checkout_public_key);

  const checkout = stripe.redirectToCheckout({
    sessionId: session.checkout_session_id,
  });

  if (checkout.error){
    console.log(checkout.error);
  }
}

buttons.forEach(button=>{
  button.addEventListener("click", function(e){
    e.preventDefault();
    initialize();
  })
});