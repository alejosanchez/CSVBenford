// Benford's Law analyzer
$(function () {

});

function fillColumns(){
    // Find classes not belonging to tinyMCE
    // Split the classes from original stylesheets and from eudeba.css

    var cssFrom = $('#css-from');
    for(var i in sheets) {
        var option = '<option value="' + selector + '">'
                + sheetName + ': ' + selector + '</option>\r\n'
        cssFrom.append($(option));
    }

}
