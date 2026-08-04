const reviewToken = localStorage.getItem("token");


let currentProductId;


// LOAD REVIEWS

async function loadReviews(productId){

    currentProductId = productId;


    const response = await fetch(
        `${API_URL}/products/${productId}/reviews`
    );


    const reviews = await response.json();


    const container =
        document.getElementById("reviews");


    container.innerHTML="";


    if(reviews.length === 0){

        container.innerHTML =
        "<p>No reviews yet</p>";

        return;
    }


    reviews.forEach(review=>{


        const div=document.createElement("div");


        div.innerHTML=`

            <p>
                Rating:
                ${"⭐".repeat(review.rating)}
            </p>

            <p>
                ${review.comment || ""}
            </p>

            <hr>

        `;


        container.appendChild(div);


    });

}



// ADD REVIEW

async function submitReview(){


    const rating =
        document.getElementById("rating").value;


    const comment =
        document.getElementById("comment").value;



    const response = await fetch(

        `${API_URL}/products/${currentProductId}/reviews`,

        {
            method:"POST",

            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${reviewToken}`
            },

            body:JSON.stringify({

                rating:Number(rating),
                comment:comment

            })
        }

    );


    const data = await response.json();


    if(response.ok){

        alert("Review added");

        loadReviews(currentProductId);

    }
    else{

        alert(data.detail);

    }

}