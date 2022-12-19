async function getData(url) {
    const res = await axios.get(url);
    return await res.data;
}

let promiseParty = [];
let promisePolitician = [];

promiseParty = getData('/api/promise/party');
console.log(promiseParty);
promisePolitician = getData('/api/promise/politician');