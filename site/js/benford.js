// Benford's Law analyzer
$(function() {
    uploader();
});

// Bind to an upload form, 
function uploader() {
    uploadForm = $("form[name=csv-file-upload]");

    // From http://stackoverflow.com/a/16086380
    //    uploadForm.submit( function() {
    uploadForm.bind("submit", function (event) {

        var formData = new FormData($(this)[0]);

        $.ajax({

            url:         $(this).attr("action"),
            type:        'POST',
            data:        formData,
            async:       false,
            success:     function (data) {
                        // location.reload();
                        fillColumns();
            },
            cache:       false,
            contentType: false,
            processData: false
        });

        return false;
    });

}

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
