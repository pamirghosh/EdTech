const pay_btn=document.querySelector(".payment");
pay_btn.addEventListener('click',(e)=>{
  e.preventDefault();
  price=document.querySelector('.price').value;
  console.log(price)
  const data={
    price:price
  };
  fetch('create-order',{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
  }).then((response)=>{
      return response.json();
  }).then((data)=>{
    console.log(data)
    var options={
      key:data.key_id,
      amount: data.amount,
      currency: "INR",
      order_id: data.order_id,
      
      handler: function(resp) {
        console.log("Handler called!", resp);
        fetch("/verify-payment", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(resp)
        })
        .then(function(result) { return result.json(); })
        .then(function(resultData) {
            if(resultData.status === "success") {
                alert("Payment Successful!");
                window.location.href = "/our-courses";
            } else {
                alert("Payment Failed!");
            }
        });
      }
    };
    
    var rzp = new Razorpay(options);
    rzp.open();
  });
});
