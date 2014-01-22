var showUserFilterChoice = function() {
  $("#filter-choice").show()
  
}

var onFilterSelection = function() {
  $("#filter-choice").hide()
  showUploadButton()
}
$("#filter-select").on("change", onFilterSelection)

var showUploadButton = function() {
  $("#file-upload").show()
}

var showUploadAnotherButton = function() {
  $("#file-uploaded").show()
}
  
var errorGenericNetworkProblem = function(msg, jqXHR, textStatus, errorThrown) {
  // Otherwise, it's an unknown error and we don't (can't) know what to do.
  // Show the user an error and ask them to try again later or report it
  // if it is persistent.
  scraperwiki.alert("Oops, something went wrong.",
    msg+" Try again later and please report it "+
    "if the problem persists. Status: " + jqXHR.status, "error")
}

$(function(){

  // set up special form inputs
  $('#next').val(window.location)
  $('#apikey').val(scraperwiki.readSettings().source.apikey)

  // listen for selection of new files
  $('#file').on('change', function(){
    if ($(this).val() != '') {
      $('#upload-button').addClass('loading disabled').html("Uploading file&hellip;")
      $('#up :submit').trigger('click')
    }
  })

  // window.readSettings().filePath will be set
  // if we've just received a new file
  var filePath = scraperwiki.readSettings().filePath
  if (filePath) {
    showUploadAnotherButton()
  }
  
  $.ajax({"url": "settin1gs.json", "dataType": "json"})
    .done(function(data) {
      if ("filter" in data) {
        showUploadButton()
        return
      }
      showUserFilterChoice()
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      if (jqXHR.status == 404) {
        // if settings.json doesn't exist yet, the user hasn't made a choice.
        showUserFilterChoice()
        return
      }
      var m = "Settings couldn't be loaded."
      errorGenericNetworkProblem(m, jqXHR, textStatus, errorThrown)
    })
    
  $.ajax({"url": "filters.json", "dataType": "json"})
    .done(function(data) {      
      var $select = $("#filter-select")
      $select.find("option")
      
      // Remove placeholder "Loading...", from the HTML.
      $select
        .empty()
        .html("<option></option>")
      
      $.each(data, function(key, value) {
        $select.append($('<option>').val(key).text(value))
      })
      
      $select.attr("disabled", false)
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      var m = "Available filters could not be loaded."
      errorGenericNetworkProblem(m, jqXHR, textStatus, errorThrown)
    })
    
})

