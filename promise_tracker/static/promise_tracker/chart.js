promiseParty.then((response) => {
    const dataPromiseParty = {
        labels: response.map((data) => data.party),
        datasets: [{
            label: 'Parties',
            data: response.map((data) => data.count),            
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

promisePolitician.then((response) => {
    const dataPromisePolitician = {
        labels: response.map((data) => data.name),
        datasets: [{
            label: 'Promises by Politician',
            data: response.map((data) => data.count),            
            hoverOffset: 4
        }]
    };

    const configPromisePolitician = {
        type: 'bar',        
        data: dataPromisePolitician,        
    };

    new Chart(
        document.getElementById('dashboardBarChart'),
        configPromisePolitician
    );
});

ratingPolitician.then((response) => {
    ratings =  response.ratings;
    // document.querySelector('#profile_pic').src = response.photo;
    document.querySelector('#politician_name').innerHTML = response.fname + ' ' +response.lname;
    const dataRatingPolitician = {
        labels: ratings.map((x) => x.title ),
        datasets: [{
            label: response.fname + ' ' +response.lname,
            data: ratings.map((x) => x.count ),
        }]
    };

    const configRatingPolitician = {
        type: 'pie',
        data: dataRatingPolitician,        
    };

    let myPiePolitician = new Chart(
        document.getElementById('dashboardPiePolitician'),
        configRatingPolitician
    );
});

ratingParty.then((response) => {
    ratings =  response.ratings;
    // document.querySelector('#profile_pic').src = response.photo;
    document.querySelector('#party_name').innerHTML = response.name;
    const dataRatingParty = {
        labels: ratings.map((x) => x.title ),
        datasets: [{
            label: response.acronym,
            data: ratings.map((x) => x.count ),
        }]
    };

    const configRatingParty = {
        type: 'pie',
        data: dataRatingParty,        
    };

    let myPieParty = new Chart(
        document.getElementById('dashboardPieParty'),
        configRatingParty
    );
});

