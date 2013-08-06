// Benford's Law analyzer
$(function() {
    getCSVList();
    pickCSV();
    uploader();
    columnPicked();
});

function pickCSV() {

    $('#csv-list').change( function() {

        var fileName = $(this).find(":selected").text();
        getColumns(fileName); // Add columns of selected CSV file
    });
}

function getCSVList() {
    $.getJSON('/cgi-bin/csv-list.py',
            function (result) {
                  fillCSVList(result['csvFiles']);
              });
}

function fillCSVList(csvFiles) {

    var files = $('#csv-list');     // CSV files available

    for(var i in csvFiles) {
        var fileName = csvFiles[i];
        var option = '<option value="' + i + '">' + fileName + '</option>\r\n';
        files.append($(option)); // Add to grouping column select
    }
}

function csvAddOne(fileName) {

    var files    = $('#csv-list');     // CSV files available
    var filesLen = document.getElementById("csv-list").length;
    var option   = '<option value="' + filesLen + '" selected="selected">'
                   + fileName + '</option>\r\n';
    files.append($(option)); // Add to grouping column select
}

// Bind to an upload form,
function uploader() {
    uploadForm = $("form[name=csv-file-upload]");

    // From http://stackoverflow.com/a/16086380
    uploadForm.bind("submit", function (event) {

        var fileName = getFilenameInput('filename');
        if ( ! /\.csv/.test(fileName) ) {
            alert('El archivo debe tener extensión ".csv"');
            return;
        }

        var formData = new FormData($(this)[0]);

        $.ajax({

            url:         $(this).attr("action"),
            type:        'POST',
            data:        formData,
            async:       false,
            success:     function (data) {
                        csvAddOne(fileName);  // Update file list, select
                        getColumns(fileName); // Get columns of new file
            },
            cache:       false,
            contentType: false,
            processData: false
        });

        return false;
    });

}

function fillColumns(columnNames) {

    var group = $('#column-group'); // Column to group by
    var check = $('#column-check'); // Column to analyze

    for(var i in columnNames) {
        var colName = columnNames[i];
        var option = '<option value="' + i + '">' + colName + '</option>\r\n';
        group.append($(option)); // Add to grouping column select
        check.append($(option)); // Add to check column select
    }
}

function getColumns(fileName) {

    clearColumns();       // Remove all columns
    $.getJSON('/cgi-bin/csv-columns.py',
              { 'dataset' : fileName },
              function (result) {
                  fillColumns(result['columns']);
              });
}

function clearColumns() {
    // Remove all but first
    $("#column-group").find('option:gt(0)').remove().end();
    $("#column-check").find('option:gt(0)').remove().end();
}

// Hack to get filename from form input file element
//   from http://stackoverflow.com/a/857662
function getFilenameInput(inputName) {

    var fullPath = document.getElementById(inputName).value;

    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var fileName = fullPath.substring(startIndex);
        if (fileName.indexOf('\\') === 0 || fileName.indexOf('/') === 0) {
            fileName = fileName.substring(1);
        }
    }
    return fileName;
}

function pickGroup() {
    $('#column-group').change( function() {
        var fileName = $(this).find(":selected").text();
        getColumns(fileName); // Add columns of selected CSV file
    });
}

// Checks if column picked are both valid
function checkPick() {

    var selGroup = $("#column-group").find(":selected").val();
    var selCheck = $("#column-check").find(":selected").val();

    if (selGroup == "invalid" || selCheck == "invalid") {
        $("#analyze-button").attr("disabled", "disabled");
    } else {
        $("#analyze-button").removeAttr("disabled");
    }
}

function columnPicked() {
    $('#column-group').change(checkPick);
    $('#column-check').change(checkPick);
}

$(function () {
        $('#container').highcharts({
            title: {
                text: 'Porcentage de dígitos en datasets por columna de grupo',
                x: -20 //center
            },
            subtitle: {
                text: 'Comparados con la Ley de Benford',
                x: -20
            },
            xAxis: {
                categories: ['1', '2', '3', '4', '5', '6', '7', '8', '9' ]
            },
            yAxis: {
                title: {
                    text: 'Porcentaje de digitos'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: '%'
            },
            legend: {
                layout:        'vertical',
                align:         'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [
                {
                    name:    'Porcentajes esperados (Ley de Benford)',
                    data:    [ 30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6 ]

                }, {
                    name:    'Alumnos matriculados - Mendoza',
                    data:    [24.7, 20.1, 13.0, 8.2, 8.5, 6.9, 6.6, 6.9, 5.0],
                    visible: false

                }, {
                    name:    'Alumnos matriculados - Ciudad de Bs. As.',
                    data:    [29.4, 6.1, 6.6, 8.3, 11.1, 7.9, 9.2, 11.7, 9.8],
                    visible: false

                }, {
                    name:    'Pacientes camas - Salta',
                    data:    [31.9, 17.6, 12.1, 13.2, 7.7, 7.7, 2.2, 3.3, 4.4],
                    visible: false
                        
                }, {
                    name:    'Pacientes camas - La Rioja',
                    data:    [19.2, 21.2, 9.6, 21.2, 9.6, 1.9, 5.8, 9.6, 1.9],
                    visible: false
                        
            }]
        });
    });
