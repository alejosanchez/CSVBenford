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
    if (selGroup == 'invalid' || selCheck == 'invalid') {
        $("analyze-button").attr("disabled", "disabled");
    } else {
        $("analyze-button").removeAttr("disabled");                             
    }
}

function columnPicked() {
    $('#column-group').change(checkPick);
    $('#column-check').change(checkPick);
}
