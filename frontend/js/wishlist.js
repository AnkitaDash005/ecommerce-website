const wishlistToken = localStorage.getItem("token");


// ADD TO WISHLIST

async function addToWishlist(productId){

    try{

        const response = await fetch(
            `${API_URL}/wishlist/`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json",
                    "Authorization":`Bearer ${wishlistToken}`
                },

                body:JSON.stringify({
                    product_id: productId
                })
            }
        );


        const data = await response.json();


        if(response.ok){

            alert("Added to wishlist");

        }
        else{

            alert(data.detail);

        }

    }
    catch(error){

        console.log(error);

    }

}



// LOAD WISHLIST

async function loadWishlist(){

    try{

        const response = await fetch(
            `${API_URL}/wishlist/`,
            {
                headers:{
                    "Authorization":`Bearer ${wishlistToken}`
                }
            }
        );


        const wishlist = await response.json();
        console.log("Wishlist response:", wishlist);


        const container =
            document.getElementById("wishlist");


        container.innerHTML="";


        if(wishlist.length === 0){

            container.innerHTML =
            "<h3>Wishlist is empty</h3>";

            return;

        }


        wishlist.forEach(item=>{

            const div=document.createElement("div");


            div.innerHTML=`

                <h2>
                    ${item.product.name}
                </h2>

                <p>
                    ₹${item.product.price}
                </p>


                <button onclick="removeWishlist(${item.id})">
                    Remove
                </button>

                <hr>

            `;


            container.appendChild(div);

        });


    }
    catch(error){

        console.log(error);

    }

}




async function removeWishlist(id){

    await fetch(
        `${API_URL}/wishlist/${id}`,
        {
            method:"DELETE",

            headers:{
                "Authorization":`Bearer ${wishlistToken}`
            }
        }
    );


    loadWishlist();

}

// Load wishlist page automatically
if(document.getElementById("wishlist")){
    loadWishlist();
}