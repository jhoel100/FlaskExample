queue()
    .defer(d3.json, datasetUrl)
    .await(ready);

function ready(error, dataset) {
    console.log(dataset)
    console.log(error)
    function arrayToTable(tableData) {
        var table = $('<table></table>');
        $(tableData).each(function (i, rowData) {
            var row = $('<tr></tr>');
            $(rowData).each(function (j, cellData) {
                row.append($('<td>'+cellData+'</td>'));
            });
            table.append(row);
        });
        return table;
    }
    /* arrayToTable(dataset) */
}