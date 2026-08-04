const token = localStorage.getItem("token");


// get product id from URL

const params = new URLSearchParams(
    window.location.search
);

const productId = params.get("id");



async function loadProductDetails(){

    try{

        const response = await fetch(
            `${API_URL}/products/${productId}`,
            {
                method:"GET",

                headers:{
                    "Authorization":`Bearer ${token}`
                }
            }
        );


        if(!response.ok){

            throw new Error("Product not found");

        }


        const product = await response.json();


        const container =
            document.getElementById("product-details");


        container.innerHTML = `

            <img
                src="${product.image}"
                width="300"
                height="250"
            >


            <h1>
                ${product.name}
            </h1>


            <p>
                ${product.description}
            </p>


            <h2>
                Price: ₹${product.price}
            </h2>


            <p>
                Stock: ${product.stock}
            </p>


            <p>
                Category:
                ${product.category.name}
            </p>

            <button onclick="addToCart(${product.id})">
                Add To Cart
            </button>

            <button onclick="addToWishlist(${product.id})">
                ❤️ Add to Wishlist
            </button>

        `;

        loadReviews(product.id);


    }
    catch(error){

        console.log(error);

    }

}


loadProductDetails();