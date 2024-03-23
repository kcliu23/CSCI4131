// E7I1F54GHGCD8SZ3
document.getElementById("fetchButton").addEventListener("click", function() {
    const tickerSymbol = document.getElementById("tickerSymbol").value;
    const apiKey = "E7I1F54GHGCD8SZ3";

    const stocks = new Stocks(apiKey);

    // Fetch stock data using stocks.js
    stocks.timeSeries({
        symbol: tickerSymbol,
        interval: "15min",
        amount: 10
    })
    .then(response => {
        if (response.length > 0) {
            // Initialize an empty string to store the values
            let displayText = "";
        

            response.forEach(dataPoint => {
                const open = dataPoint.open;
                const low = dataPoint.low;
                const high = dataPoint.high;
                const close = dataPoint.close;
                const volume = dataPoint.volume;
                const date = dataPoint.date;
        
                displayText += `Open: ${open}\nLow: ${low}\nHigh: ${high}\nClose: ${close}\nVolume: ${volume}\nDate: ${date}\n\n`;
            });
        
            const quoteDisplay = document.getElementById("quoteDisplay");
            quoteDisplay.value = displayText;
        } else {

            const quoteDisplay = document.getElementById("quoteDisplay");
            quoteDisplay.value = "Error fetching stock data: NOT AVAILABLE";
            console.log("No data available for the specified stock symbol.");
        }
    })
    .catch(error => {
        console.log("Error fetching stock data:", error);
    });
});