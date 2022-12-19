console.log("hi")
promiseParty.then((response) => {
    const dataPromiseParty = {
        labels: response.map((data) => data.party),
        datasets: [{
            label: 'Parties',
            data: response.map((data) => data.count),
            // backgroundColor: [
            //     'rgb(255, 99, 132)',
            //     'rgb(54, 162, 235)',
            //     'rgb(255, 205, 86)'
            // ],
            hoverOffset: 4
        }]
    };

    const configPromiseParty = {
        type: 'pie',
        data: dataPromiseParty,
    };

    new Chart(
        document.getElementById('promise-party'),
        configPromiseParty
    );
});