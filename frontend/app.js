const API_URL = "http://127.0.0.1:8000";

async function encode() {
  const image = document.getElementById("encodeImage").files[0];
  const message = document.getElementById("message").value;

  const formData = new FormData();
  formData.append("image", image);
  formData.append("message", message);

  const response = await fetch(`${API_URL}/encode`, {
    method: "POST",
    body: formData
  });

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "encoded_image.png";
  a.click();
}

async function decode() {
  const image = document.getElementById("decodeImage").files[0];

  const formData = new FormData();
  formData.append("image", image);

  const response = await fetch(`${API_URL}/decode`, {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById("output").innerText =
    "Decoded Message: " + data.message;
}
