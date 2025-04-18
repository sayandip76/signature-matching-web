function previewImage(input, imgId) {
  const file = input.files[0];
  const reader = new FileReader();
  reader.onload = function (e) {
    document.getElementById(imgId).src = e.target.result;
  };
  if (file) {
    reader.readAsDataURL(file);
  }
}

async function compare() {
  const file1 = document.getElementById("file1").files[0];
  const file2 = document.getElementById("file2").files[0];
  const resultEl = document.getElementById("result");

  if (!file1 || !file2) {
    alert("Please select both signature images.");
    return;
  }

  const formData = new FormData();
  formData.append("file1", file1);
  formData.append("file2", file2);

  resultEl.className = "badge fs-5 p-3 bg-secondary";
  resultEl.innerText = "Comparing...";

  try {
    const response = await fetch("/compare", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.error) {
      resultEl.innerText = "Error: " + result.error;
      resultEl.className = "badge fs-5 p-3 bg-danger";
    } else {
      const isMatch = result.match;
      resultEl.innerText = isMatch
        ? "Signatures Match"
        : "Signatures Do Not Match";

      resultEl.className = `badge fs-5 p-3 ${
        isMatch ? "bg-success" : "bg-danger"
      }`;
    }
  } catch (err) {
    console.error("Fetch error:", err);
    resultEl.innerText = "An error occurred.";
    resultEl.className = "badge fs-5 p-3 bg-warning text-dark";
  }
}
