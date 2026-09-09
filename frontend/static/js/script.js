function copyText(elementId) {

    const text = document.getElementById(elementId).innerText;

    navigator.clipboard.writeText(text);

    alert("Complaint copied successfully!");
}
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    const submitButton = document.getElementById("submitButton");

    const loadingMessage = document.getElementById("loadingMessage");


    form.addEventListener("submit", function () {

        submitButton.disabled = true;

        submitButton.innerText = "Processing...";

        loadingMessage.style.display = "block";

    });

});