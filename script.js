let fileInput = document.getElementById("filepicker");
let innerImage = document.querySelector(".inner-upload-image");
let image = null;
let url = null;
let InputImg = document.getElementById("input-image");
let icon = document.querySelector("#icon");
let span = document.querySelector("span");
let OriginalImg = document.querySelector(".resultImg1 img");
let GeneratedImg = document.querySelector(".resultImg2 img");

let uploadBtn = document.querySelector("#upload-btn");
let style2 = document.querySelector(".style2");
let resultPage = document.querySelector(".result");
let loading = document.querySelector("#loading");
let downloadBtn = document.querySelector("#download");
let resetBtn = document.querySelector("#reset");

// Flask Backend API URL (Update with your Vercel URL after deployment)
const API_URL = "https://your-vercel-app.vercel.app/remove-bg"; // Change this after deploying

// Handle Image Selection
innerImage.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    image = fileInput.files[0];
    if (!image) return;

    let reader = new FileReader();
    reader.onload = (e) => {
        InputImg.src = e.target.result;
        InputImg.style.display = "block";
        icon.style.display = "none";
        span.style.display = "none";
        OriginalImg.src = e.target.result;
    };
    reader.readAsDataURL(image);
});

// Upload Image & Remove Background
uploadBtn.addEventListener("click", async () => {
    if (!image) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("image", image);

    loading.style.display = "block";

    try {
        let response = await fetch(API_URL, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) throw new Error("Failed to process image");

        let blob = await response.blob();
        url = URL.createObjectURL(blob);
        GeneratedImg.src = url;

        // Show result section
        loading.style.display = "none";
        style2.style.display = "none";
        resultPage.style.display = "flex";
    } catch (error) {
        console.error(error);
        alert("Error processing image");
        loading.style.display = "none";
    }
});

// Download Processed Image
downloadBtn.addEventListener("click", () => {
    if (!url) return;
    let a = document.createElement("a");
    a.href = url;
    a.download = "processed-image.png";
    a.click();
});

// Reset Everything
resetBtn.addEventListener("click", () => {
    window.location.reload();
});
fetch("https://your-flask-app.vercel.app/remove-bg", {  
    method: "POST",
    body: formData
})
