function loadNavbar(){

    fetch("navbar.html")
    .then(response => response.text())
    .then(data => {

        document.getElementById("navbar")
            .innerHTML = data;

    });
function loadNavbar(){

    fetch("navbar.html")
    .then(response => {

        if(!response.ok){
            throw new Error("Navbar file not found");
        }

        return response.text();

    })
    .then(data => {

        document.getElementById("navbar")
            .innerHTML = data;

    })
    .catch(error => {

        console.log("Navbar Error:", error);

    });

}


loadNavbar();
}

loadNavbar();