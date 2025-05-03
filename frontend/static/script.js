document.getElementById("carbonForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
  
    fetch("/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then(async (res) => {
          if (!res.ok) {
            const errorText = await res.text(); // get HTML error
            throw new Error(`Server error: ${errorText}`);
          }
          return res.json();
        })
        .then((data) => {
          document.getElementById("result").innerText =
            `Predicted Carbon Emissions: ${data.total_emissions} kg CO₂`;
        })
        .catch((err) => {
          console.error(err);
          document.getElementById("result").innerText = "⚠️ Failed to get prediction. Check console.";
        });
      
  });
  