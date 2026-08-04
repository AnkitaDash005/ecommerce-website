const API_URL = "http://127.0.0.1:8000";


document
.getElementById("signupBtn")
.addEventListener("click", signup);



async function signup(){

    const name =
    document.getElementById("name").value;


    const email =
    document.getElementById("email").value;


    const password =
    document.getElementById("password").value;



    const response = await fetch(
        `${API_URL}/auth/signup`,
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

           body: JSON.stringify({
                username: name,
                email: email,
                password: password
            })
        }
    );


    const data = await response.json();


    if(response.ok){

        alert("Signup successful");

        window.location.href="login.html";

    }
    else{

        alert(data.detail);

    }

}