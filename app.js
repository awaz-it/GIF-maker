// Elements
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const dropArea = document.getElementById("dropArea");
const previewBtn = document.getElementById("previewBtn");
const createBtn = document.getElementById("createBtn");
const delayInput = document.getElementById("delay");
const gifText = document.getElementById("gifText");
const downloadLink = document.getElementById("downloadLink");

let animationInterval;
let imageFiles = [];

// --- Helper Functions ---

// Show thumbnails
function showThumbnails(files) {
  preview.innerHTML = "";
  imageFiles = Array.from(files);

  imageFiles.forEach((file, index) => {
    if (!file.type.startsWith("image/")) return;

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.setAttribute("draggable", true);
    img.dataset.index = index;

    // Drag & drop reorder
    img.addEventListener("dragstart", dragStart);
    img.addEventListener("dragover", dragOver);
    img.addEventListener("drop", dropImage);

    preview.appendChild(img);
  });
}

// --- Drag & Drop functions ---
let dragSrcIndex = null;

function dragStart(e) {
  dragSrcIndex = e.target.dataset.index;
}

function dragOver(e) {
  e.preventDefault();
}

function dropImage(e) {
  e.preventDefault();
  const destIndex = e.target.dataset.index;
  if (dragSrcIndex === null || destIndex === null) return;

  // Swap positions
  [imageFiles[dragSrcIndex], imageFiles[destIndex]] = [
    imageFiles[destIndex],
    imageFiles[dragSrcIndex]
  ];
  showThumbnails(imageFiles);
}

// --- File input & drag-drop ---
fileInput.addEventListener("change", () => showThumbnails(fileInput.files));

dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.background = "#eef";
});
dropArea.addEventListener("dragleave", () => {
  dropArea.style.background = "#fafafa";
});
dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.style.background = "#fafafa";
  const files = e.dataTransfer.files;
  fileInput.files = files;
  showThumbnails(files);
});

// Add click handler for the drop area to trigger file input
dropArea.addEventListener("click", () => {
  fileInput.click();
});

// --- Preview slideshow ---
previewBtn.addEventListener("click", () => {
  if (imageFiles.length === 0) {
    alert("Upload images first!");
    return;
  }
  clearInterval(animationInterval);

  const previewContainer = document.getElementById("preview-container");
  let i = 0;
  const img = document.createElement("img");
  img.style.maxWidth = "100%";
  img.style.maxHeight = "400px";
  img.style.objectFit = "contain";
  img.style.border = "2px solid var(--border-light)";
  img.style.borderRadius = "0.5rem";
  img.style.boxShadow = "var(--shadow-sm)";
  previewContainer.innerHTML = "";
  previewContainer.appendChild(img);

  const delay = parseInt(delayInput.value) || 200;

  animationInterval = setInterval(() => {
    img.src = URL.createObjectURL(imageFiles[i]);
    i = (i + 1) % imageFiles.length;
  }, delay);
});

// --- Create GIF ---
createBtn.addEventListener("click", () => {
  if (imageFiles.length === 0) {
    alert("Upload images first!");
    return;
  }

  const images = imageFiles.map((file) => URL.createObjectURL(file));

  // --- Calculate max width & height ---
  let maxWidth = 0;
  let maxHeight = 0;

  const promises = imageFiles.map((file) => {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        if (img.width > maxWidth) maxWidth = img.width;
        if (img.height > maxHeight) maxHeight = img.height;
        resolve();
      };
      img.src = URL.createObjectURL(file);
    });
  });

  Promise.all(promises).then(() => {
    const delay = parseInt(delayInput.value) || 200;

    const text = gifText.value || "";
    const color = document.getElementById("textColor").value;
    const size = document.getElementById("fontSize").value;
    const position = document.getElementById("textPosition").value;

    // Position text
    let x = maxWidth / 2;  // center horizontally
let y = 30;            // default "top"

if (position === "top") {
  y = 30; // ~30px from top
} else if (position === "center") {
  y = maxHeight / 2; // vertical middle
} else if (position === "bottom") {
  y = maxHeight - 30; // ~30px from bottom
}
    // --- Create GIF ---
    gifshot.createGIF(
      {
        images: images,
        interval: delay / 1000,
        gifWidth: maxWidth,
        gifHeight: maxHeight,
        text: text,
        fontSize: size + "px",
        fontWeight: "bold",
        fontFamily: "Arial",
        fontColor: color,
        textAlign: "center",
textBaseline: "top",
       textXCoordinate: x,   
  textYCoordinate: y
      },
      function (obj) {
        if (!obj.error) {
          downloadLink.style.display = "inline-block";
          downloadLink.href = obj.image;
          downloadLink.download = "mygif.gif";
          downloadLink.textContent = "Download GIF";
          alert("GIF created! Click the download link.");
        } else {
          alert("Error creating GIF. Try fewer images or smaller size.");
        }
      }
    );
  });
});

// --- Dark mode ---
document.addEventListener("DOMContentLoaded", () => {
  const darkModeToggle = document.getElementById("darkModeToggle");

  darkModeToggle.addEventListener("change", () => {
    document.body.classList.toggle("dark-mode", darkModeToggle.checked);
  });
});
