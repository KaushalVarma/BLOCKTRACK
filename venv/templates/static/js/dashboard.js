document.addEventListener("DOMContentLoaded", () => {
    fetch('/get-latest-transactions')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
            drawCharts(data);
        })
        .catch(error => console.error('Error fetching transactions:', error));
});

function populateTable(transactions) {
    const tbody = document.querySelector('#transactionTable tbody');
    tbody.innerHTML = ''; // Clear previous content

    transactions.forEach(tx => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${tx.hash}</td>
            <td>${tx.from}</td>
            <td>${tx.to}</td>
            <td>${tx.value}</td>
            <td>${tx.blockNumber}</td>
        `;
        tbody.appendChild(row);
    });
}

function drawCharts(transactions) {
    const lineChartCtx = document.getElementById('lineChart').getContext('2d');
    const pieChartCtx = document.getElementById('pieChart').getContext('2d');
    const barChartCtx = document.getElementById('barChart').getContext('2d');

    // Prepare data for the charts
    const labels = transactions.map(tx => `Block ${tx.blockNumber}`);
    const values = transactions.map(tx => tx.value);

    // Line chart: Transaction value over blocks
    new Chart(lineChartCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Transaction Value (Wei)',
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        }
    });

    // Pie chart: Distribution of transactions by address
    const fromAddresses = {};
    transactions.forEach(tx => {
        fromAddresses[tx.from] = (fromAddresses[tx.from] || 0) + 1;
    });
    const pieLabels = Object.keys(fromAddresses);
    const pieData = Object.values(fromAddresses);

    new Chart(pieChartCtx, {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieData,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        }
    });

    // Bar chart: Number of transactions per block
    const blockCounts = {};
    transactions.forEach(tx => {
        blockCounts[tx.blockNumber] = (blockCounts[tx.blockNumber] || 0) + 1;
    });
    const barLabels = Object.keys(blockCounts);
    const barData = Object.values(blockCounts);

    new Chart(barChartCtx, {
        type: 'bar',
        data: {
            labels: barLabels,
            datasets: [{
                label: 'Transactions per Block',
                data: barData,
                backgroundColor: 'rgba(153, 102, 255, 0.6)'
            }]
        }
    });
}
