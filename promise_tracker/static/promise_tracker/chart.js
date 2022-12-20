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
            // hoverOffset: 4
        }]
    };

    const configPromiseParty = {
        type: 'doughnut',
        // plugins: [{
        //     afterDraw: chart => {
        //       var ctx = chart.chart.ctx;
        //       ctx.save();
        //       var image = new Image();      
        //       image.src = 'https://i.stack.imgur.com/S7tJH.png';      
        //       imageSize = 40;
        //       ctx.drawImage(image, chart.chart.width / 2 - imageSize / 2, chart.chart.height / 2 - imageSize / 2, imageSize, imageSize);
        //       ctx.restore();
        //     }
        //   }],  
        data: dataPromiseParty,        
    };

    new Chart(
        document.getElementById('myPieChart'),
        configPromiseParty
    );
});