const apiKey = '';
const apiUrl = 'https://dataapi.callgear.com/2.0';


const requestData = {
    jsonrpc: "2.0",
    id: 1,
    method: "get.account",
    params: {
        access_token: apiKey,
    }
};

fetch(apiUrl, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
})
    .then(response => response.json())
    .then(data => {
        console.log("Account Info:", data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
