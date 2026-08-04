const token = localStorage.getItem("token");

async function checkout(){

    const response = await fetch(
        `${API_URL}/orders/checkout`,
        {
            method:"POST",

            headers:{
                "Authorization":`Bearer ${token}`,
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                coupon:document.getElementById("coupon").value

            })
        }
    );

    const data = await response.json();

    if(response.ok){

        alert("Order placed successfully!");

        window.location.href="orders.html";

    }
    else{

        alert(data.detail);

    }

}