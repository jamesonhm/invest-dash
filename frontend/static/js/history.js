
// var chartsScript = document.createElement('script');
// chartsScript.setAttribute('src', "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js");
// document.head.appendChild(chartsScript);


var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
        datasets: [{
            data: [86, 114, 106, 106, 107, 111, 133],
            label: "total",
            borderColor: "#3e95cd",
            backgroundColor: "#7bb6dd"
        }]
    },
});
