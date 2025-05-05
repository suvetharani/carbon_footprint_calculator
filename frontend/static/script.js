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
          let chart;
          const chartElement = document.getElementById("carbonChart");

          if (chart) chart.destroy();

          const labels = Object.keys(data.contributions);
          const values = Object.values(data.contributions);

          if (window.carbonChartInstance) {
            window.carbonChartInstance.destroy();
          }

          window.carbonChartInstance = new Chart(chartElement, {
            type: "pie",
            data: {
              labels: labels,
              datasets: [{
                label: "Carbon Contribution (kg CO₂)",
                data: values,
                backgroundColor: [
                  "#f94144", "#f3722c", "#f8961e", "#f9844a",
                  "#f9c74f", "#90be6d", "#43aa8b", "#577590", "#277da1"
                ],
              }]
            },
            options: {
              responsive: false,
              maintainAspectRatio: false,
              plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                  callbacks: {
                    label: (context) => {
                      const label = context.label || '';
                      const value = context.raw || 0;
                      return `${label}: ${value.toFixed(2)} kg CO₂`;
                    }
                  }
                }
              }
            }
            
          });
        })
        .catch((err) => {
          console.error(err);
          document.getElementById("result").innerText = "⚠️ Failed to get prediction. Check console.";
        });
      
  });
  