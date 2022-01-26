fetch("/config/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        const stripe = Stripe(data.publicKey);

        document.querySelector("#submitBtn").addEventListener("click", () => {
            fetch("/create-checkout-session/")
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
        });
    });