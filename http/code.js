var showUserFilterChoice = function() {
  $("#filter-choice").show()
  
}

// Move this upstream.
scraperwiki.readSettings = function() {
  try {
    // Try the hash from this window
    return JSON.parse(decodeURIComponent(window.location.hash.substr(1)))
  } catch (e) {
    try {
      // Try the hash from the container, if it has one?
      return JSON.parse(decodeURIComponent(parent.location.hash.substr(1)))
    } catch (e) {}    
  }
  return null
}

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
    "if the problem persists. <br>Status: " + jqXHR.status + ", "+ textStatus + ", "+errorThrown, "error")
}

var showFormattingError = function(msg) {
  $("#formatting-error").show().find(".message").text(msg)
}

var errorFromRunlog = function(runlogEntry) {
  var exception = runlogEntry.exception_value.replace(/u(["'])/g, '$1')

  var regex = /^(MultipleCellsAssertionError|NoCellsAssertionError)\(['"](.+)['"],\)$/
  var matches = exception.match(regex)
  if (matches) {
    showFormattingError(matches[2])
    return
  } 

  var regex = /^(TableError)\(['"](.+)['"],\)$/
  var matches = exception.match(regex)
  if (matches) {
    showFormattingError(matches[2].replace('No table called', 'No worksheet called'))
    return
  }

  var regex = /^(ReadError)\(['"](.+)['"],\)$/
  var matches = exception.match(regex)
  if (matches) {
    var msg = "That file was not a spreadsheet"

    var mimeTypeRegex = /MIME type: "(.*)"/
    var mimeTypeMatches = matches[2].match(mimeTypeRegex)
    if (mimeTypeMatches) {
      msg += " (we detected file type: " + mimeTypeMatches[1] + ")."
    } else {
      msg += "."
    } 
    showFormattingError(msg)
    return
  }


  traceback = "<pre>" + runlogEntry.traceback + "</pre>"
  // TODO We should show stack trace here too
  scraperwiki.alert("An error occurred whilst processing the file.", traceback, "error")
}

var fetchFiltersAndPopulate = function() {
  return $.ajax({
    "url": "filters.json",
    "dataType": "json"
  }).done(function(data) {      
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
  }).fail(function(jqXHR, textStatus, errorThrown) {
    var m = "Available filters could not be loaded."
    errorGenericNetworkProblem(m, jqXHR, textStatus, errorThrown)
  })
}

var fetchSettings = function() {
  return $.ajax({
    "url": "allSettings.json",
    "dataType": "json"
  }).fail(function(jqXHR, textStatus, errorThrown) {
    if (jqXHR.status == 404) {
      // If allSettings.json doesn't exist yet, the user hasn't made
      // a choice...
      showUserFilterChoice()
      // ... and we need to install the Python requirements.
      runSetup()
      return
    }
    var m = "Settings couldn't be loaded."
    errorGenericNetworkProblem(m, jqXHR, textStatus, errorThrown)
  })
}

var fetchLastRunlogEntry = function() {
  var dfd = $.Deferred()
  
  var q = "SELECT * from _sw_runlog ORDER BY time DESC LIMIT 1"
  scraperwiki.dataset.sql(q).done(function(data) {
    dfd.resolve(data[0])
    
  }).fail(function(jqXHR, textStatus, errorThrown) {
    if (jqXHR.status == 400 || jqXHR.status == 404) {
      dfd.resolve(null)
      return
    }
    
    var m = "Last runlog entry couldn't be loaded."
    errorGenericNetworkProblem(m, jqXHR, textStatus, errorThrown)
    
    dfd.reject(jqXHR, textStatus, errorThrown)
  })
  
  return dfd.promise()
}

// Runs setup.sh in the box, via the exec endpoint. Generally we
// expect this to be only run once, but it is not harmful to run
// multiple times, just a bit slow.
// It would be bad to upload a file before this script finishes,
// but we don't yet check. :todo:(drj/dragon) make it work.
var runSetup = function() {
  scraperwiki.exec("/home/tool/setup.sh")
}

var onFilterSelection = function() {

  var $select = $(this)
  var filterName = $select.children("[value='"+$select.val()+"']").text()
  
  scraperwiki.dataset.name(filterName)
    
  $select.attr("disabled", true)
  $("#filter-saving").show()
  $(".filter-name").text(filterName)

  // Set allSettings via set-filter cgi-bin endpoint
  $.ajax({
    url: "../cgi-bin/set-filter",
    data: {
      filter: $(this).val(),
      filterName: filterName
    },
    dataType: "json"
    
  }).done(function(data) {
    $("#filter-choice").hide()
    showUploadButton()
    
  }).fail(function(jqXHR, textStatus, errorThrown) {
    var m = "Problem saving filter selection."
    errorGenericNetworkProblem(m, jqXHR, textStatus, errorThrown)
    
    $select.attr("disabled", false)
    $("#filter-saving").hide()
  })
}

var onFileUpload = function(){
  if ($(this).val() != '') {
    $('#upload-button,#upload-another-button')
      .addClass('loading disabled')
      .html("Uploading file&hellip;")
    setTimeout(function() { $('#up :submit').trigger('click') }, 0)
  }
}

$(function(){

  // set up special form inputs
  $('#next').val(window.location)
  $('#apikey').val(scraperwiki.readSettings().source.apikey)

  // listen for selection of new files
  $('#file').on('change', onFileUpload)  
  $("#filter-select").on("change", onFilterSelection)

  // window.readSettings().filePath will be set
  // if we've just received a new file
  var filePath = scraperwiki.readSettings().filePath

  var userJustUploadedSomething = window.location.search == "?uploaded"

  fetchFiltersAndPopulate()

  // No .fail is needed because *the callees implement their own .fail()s*
  // Take care to maintain this.
  $.when(fetchSettings(), fetchLastRunlogEntry())
    .done(function(settings, runlogEntry) {
      // Unwrap the 'when'
      settings = settings[0]
      
      if (settings == null || !("filter" in settings)) {
        // Filter hasn't been picked yet
        showUserFilterChoice()
        return
      }
      
      $(".filter-name").text(settings["filterName"])
      
      if (runlogEntry == null) {
        // We've never run before
        showUploadButton()
        return
      }
      
      showUploadAnotherButton()
      
      if (runlogEntry.success) {      
        if (userJustUploadedSomething) {
          $("#success").show()
        }
      } else {
        errorFromRunlog(runlogEntry)
      }
    })
})

