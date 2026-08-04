document
.getElementById("loginForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;


    const response = await fetch(
        `${API_URL}/auth/login`,
        {
            method: "POST",

            headers:{
                "Content-Type":"application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );


    const data = await response.json();


    if(response.ok){

        // save JWT token
        localStorage.setItem(
            "token",
            data.access_token
        );


        alert("Login successful");


        // redirect
        window.location.href="products.html";

    }
    else{

      alert(JSON.stringify(data.detail));

    }

});