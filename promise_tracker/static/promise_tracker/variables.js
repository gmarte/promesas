async function getData(url) {
    const res = await axios.get(url);
    return await res.data;
}

let promiseParty = [];
let ratingParty = [];
let promisePolitician = [];
let ratingPolitician = [];
let newRatingParty = []

promiseParty = getData('/api/promise/party');
promisePolitician = getData('/api/promise/politician');
ratingParty = getData('/api/promise/party?id=1');
ratingPolitician  = getData('/api/promise/politician?id=1');

function change_rating(id){        
    let chartStatus = Chart.getChart("dashboardPieParty");
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }     
    axios.get('/api/promise/party?id='+id).then(response => {
        ratings =  response.data.ratings;
        // document.querySelector('#profile_pic').src = response.photo;
        document.querySelector('#party_name').innerHTML = response.data.name;
        const dataRatingParty = {
            labels: ratings.map((x) => x.title ),
            datasets: [{
                label: response.data.acronym,
                data: ratings.map((x) => x.count ),
            }]
        };
    
        const configRatingParty = {
            type: 'pie',
            data: dataRatingParty,        
        };
    
        new Chart(
            document.getElementById('dashboardPieParty'),
            configRatingParty
        );
    })
}
function change_ratingp(id){        
    let chartStatus = Chart.getChart("dashboardPiePolitician");
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }     
    axios.get('/api/promise/politician?id='+id).then(response => {
        ratings =  response.data.ratings;        
        document.querySelector('#politician_name').innerHTML = response.data.fname + ' ' +response.data.lname;
        document.querySelector('#politician_id').href = '/politicians/'+response.data.id+'/detail';
        const dataRatingPolitician = {
            labels: ratings.map((x) => x.title ),
            datasets: [{
                label: response.data.fname + ' ' +response.data.lname,
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
    })
}