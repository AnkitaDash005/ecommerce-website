const token = localStorage.getItem("token");

let allProducts = [];

// ---------------- LOAD PRODUCTS ----------------

async function loadProducts() {

    try {

        const response = await fetch(
            `${API_URL}/products/`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to fetch products");
        }

        const data = await response.json();

        allProducts = Array.isArray(data)
            ? data
            : data.products;

        displayProducts(allProducts);

    }
    catch (error) {

        console.log(error);

    }

}

// ---------------- DISPLAY PRODUCTS ----------------

function displayProducts(products){

    const container = document.getElementById("products");

    container.innerHTML = "";

    if(!products || products.length === 0){

        container.innerHTML = "<h3>No products found.</h3>";
        return;

    }

    products.forEach(product => {

        const div = document.createElement("div");

        div.className = "product-card";

        div.innerHTML = `

            <img
                src="${product.image}"
                alt="${product.name}"
                width="220"
                height="180"
            >

            <h2 onclick="openProduct(${product.id})">
                ${product.name}
            </h2>

            <p>
                ${product.description || ""}
            </p>

            <p>
                <strong>Price:</strong> ₹${product.price}
            </p>

            <p>
                <strong>Stock:</strong> ${product.stock}
            </p>

            <button onclick="addToCart(${product.id})">
                Add To Cart
            </button>

            <hr>

        `;

        container.appendChild(div);

    });

}

// ---------------- SEARCH ----------------

function searchProducts(){

    const keyword = document
        .getElementById("search")
        .value
        .toLowerCase();

    const filtered = allProducts.filter(product =>

        product.name.toLowerCase().includes(keyword) ||

        (product.description || "")
            .toLowerCase()
            .includes(keyword)

    );

    displayProducts(filtered);

}
// ---------------- CATEGORY FILTER ----------------

function filterCategory(categoryId){

    if(categoryId === 0){

        displayProducts(allProducts);
        return;

    }

    const filtered = allProducts.filter(product =>

        product.category &&
        product.category.id === categoryId

    );

    displayProducts(filtered);

}

function openProduct(id){

    window.location.href =
        `product-details.html?id=${id}`;

}
loadProducts();