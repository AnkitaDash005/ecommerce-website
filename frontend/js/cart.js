const cartToken = localStorage.getItem("token");


async function addToCart(product_id){

    try{

        const response = await fetch(
            `${API_URL}/cart/`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json",
                    "Authorization":`Bearer ${cartToken}`
                },

                body: JSON.stringify({
                    product_id: product_id,
                    quantity: 1
                })
            }
        );

        const data = await response.json();

        if(response.ok){
            alert("Product added to cart");
        }
        else{
            alert(data.detail || "Failed to add product");
        }

    }
    catch(error){
        console.log(error);
    }
}


// ---------- LOAD CART ----------

async function loadCart(){

    try{

        const response = await fetch(
            `${API_URL}/cart/`,
            {
                method:"GET",

                headers:{
                    "Authorization":`Bearer ${cartToken}`
                }
            }
        );

        if(!response.ok){
            throw new Error("Failed to load cart");
        }

        const cart = await response.json();

        const container = document.getElementById("cart-items");

        if(!container) return;

        container.innerHTML = "";

        if(cart.items.length === 0){

            container.innerHTML = "<h3>Your cart is empty</h3>";

            document.getElementById("total").innerHTML = "Total: ₹0";

            document.getElementById("checkout-link").style.display = "inline";

            return;
        }

        cart.items.forEach(item => {

            const div = document.createElement("div");

            div.innerHTML = `
                <h3>${item.product}</h3>

                <p>Price: ₹${item.price}</p>

                <p>
                    Quantity:
                    <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>

                    ${item.quantity}

                    <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </p>

                <p>Subtotal: ₹${item.subtotal}</p>

                <button onclick="removeFromCart(${item.id})">
                    Remove
                </button>
                <hr>
            `;

            container.appendChild(div);

        });

        document.getElementById("total").innerHTML =
            `Total: ₹${cart.total}`;

    }
    catch(error){

        console.log(error);

    }

}
async function removeFromCart(cartId){

    try{

        const response = await fetch(
            `${API_URL}/cart/${cartId}`,
            {
                method:"DELETE",

                headers:{
                    "Authorization":`Bearer ${cartToken}`
                }
            }
        );

        const data = await response.json();

        if(response.ok){

            alert(data.message);

            loadCart();

        }
        else{

            alert(data.detail);

        }

    }
    catch(error){

        console.log(error);

    }

}

async function updateQuantity(cartId, quantity){

    if(quantity <= 0){

        removeFromCart(cartId);
        return;

    }

    try{

        const response = await fetch(
            `${API_URL}/cart/${cartId}`,
            {
                method:"PUT",

                headers:{
                    "Content-Type":"application/json",
                    "Authorization":`Bearer ${cartToken}`
                },

                body: JSON.stringify({
                    quantity: quantity
                })
            }
        );

        const data = await response.json();

        if(response.ok){

            loadCart();

        }
        else{

            alert(data.detail);

        }

    }
    catch(error){

        console.log(error);

    }

}


// Automatically load the cart only on cart.html
if(document.getElementById("cart-items")){
    loadCart();
}