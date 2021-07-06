queue()
	.defer(d3.json, piechartDataUrl)
    .defer(d3.json, barchartDataUrl)
    .await(ready);

function ready(error, dataset, datasetBarChart) {
    d3map();
    d3PieChart(dataset, datasetBarChart);
    d3BarChart(datasetBarChart);
}