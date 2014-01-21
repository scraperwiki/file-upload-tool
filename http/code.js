$(function(){

  // set up special form inputs
  $('#next').val(window.location)
  $('#apikey').val(scraperwiki.readSettings().source.apikey)

  // listen for selection of new files
  $('#file').on('change', function(){
    if( $(this).val() != '' ){
      $('#upload-button').addClass('loading disabled').html("Uploading file&hellip;")
      $('#up :submit').trigger('click')
    }
  })

  // window.readSettings().filePath will be set
  // if we've just received a new file
  var filePath = scraperwiki.readSettings().filePath
  if (filePath) {
    $('#content').prepend('<p>Uploaded file: <a href="' + filePath + '">' + filePath + '</a></p>')
    $('#upload-button').html('Upload another file')
  }

})
