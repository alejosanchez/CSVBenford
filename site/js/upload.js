// Eudeba epub uploader
$(function() {

    uploadForm = $("form[name=csv-file-upload]");

    // From http://stackoverflow.com/a/16086380
    //    uploadForm.submit( function() {
    uploadForm.bind("submit", function (event) {

alert('submitting...');
        var formData = new FormData($(this)[0]);

        $.ajax({

            url:         $(this).attr("action"),
            type:        'POST',
            data:        formData,
            async:       false,
            success:     function (data) {
alert('done! result:\r\n\r\n' + data);
                        // location.reload();
            },
            cache:       false,
            contentType: false,
            processData: false
        });

        return false;
    });

});
