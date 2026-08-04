const token = localStorage.getItem("token");

async function loadOrders() {

    try {

        const response = await fetch(
            `${API_URL}/orders/`,
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to load orders");
        }

        const orders = await response.json();

        const container = document.getElementById("orders");

        container.innerHTML = "";

        if (orders.length === 0) {
            container.innerHTML = "<h3>No orders found.</h3>";
            return;
        }

        orders.forEach(order => {

            const div = document.createElement("div");

            let itemsHTML = "";

            order.items.forEach(item => {

                itemsHTML += `
                    <p>
                        ${item.product} × ${item.quantity}
                        - ₹${item.price}
                    </p>
                `;

            });

                    div.innerHTML = `

            <h2>Order #${order.id}</h2>

            <p>Status: ${order.status}</p>

            <p>Total: ₹${order.total_price}</p>

            <p>Date: ${new Date(order.created_at).toLocaleString()}</p>

            <h4>Items</h4>

            ${itemsHTML}

            ${
                order.status === "Pending"
                ? `<button onclick="cancelOrder(${order.id})">
                        Cancel Order
                </button>`
                : ""
            }

            <hr>

        `;

            container.appendChild(div);

        });

    }
    catch (error) {

        console.log(error);

    }

}
async function cancelOrder(orderId){

    try{

        const response = await fetch(
            `${API_URL}/orders/${orderId}/cancel`,
            {
                method:"PUT",

                headers:{
                    "Authorization":`Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if(response.ok){

            alert(data.message);

            // Reload orders after cancellation
            loadOrders();

        }
        else{

            alert(data.detail);

        }

    }
    catch(error){

        console.log(error);

    }

}

loadOrders();