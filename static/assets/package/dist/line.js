$(document).ready(function(){
    var ctx = $("#line-chartcanvas"); 

    var data = {
        labels: ["match1", "match2", "match3", "match4", "match5"],
        datasets: [
            {
                label: "Hugo",
                data: [10, 50, 25, 90, 40],
                backgroundColor: "blue",
                borderColor: "lightblue",
                fill: false,
                lineTension: 0.3,
                pointRadius: 5
            },
            {
                label: "ZMan",
                data: [20, 35, 40, 60, 50],
                backgroundColor: "red",
                borderColor: "pink",
                fill: false,
                lineTension: 0.3,
                pointRadius: 5
            }
        ]
    };

    var chart = new Chart(ctx, {
        type: "line",
        data: data,
        options: {}
    });
});