(function() {
  var TIMEOUT = 20000;
  var loadingImg = '<img id="loadingImage" src="/static/img/ajax-loader.gif" />';

  var errored = function(xml, status, message, $elem) {
    if (status === "timeout") {
      $elem.html("Timed out. Try again.");
    } else {
      $elem.html("Something went wrong. Try again.");
    }
    return null;
  };

  function isInt(value) {
   return !isNaN(value) && parseInt(Number(value)) == value;
  }

  var updateValue = function(url, text, count, $elem, success) {
    $elem.append(loadingImg);
    $.ajax({
      url: url,
      type: "POST",
      timeout: TIMEOUT,
      data: {"text": text, "count": count},
      dataType: "json",
      success: success,
      error: function(xml, status, message) {
        errored(xml, status, message, $elem);
      }
    });
  };

  $("#findTerm").on('click', function(e) {
    e.preventDefault();
    var text = $("#searchTermBox").val();
    var count = $("#countResult").val();
    if (!count || !isInt(count)) count="10";
    scrapeSimilarCourses(text, count);
  });

  $("#highlightIt").on('click', function(e) {
    e.preventDefault();
    $("#table1").removeHighlight();
    $("#table1").highlight($("#searchTermBox").val());
  });

  var scrapeSimilarCourses = function(text, count) {
    var $sentDiv = $("#termDiv");
    $sentBtn = $("#findTerm");
    text = text.trim();  // trim whitespace from both ends
    count = count.trim();

    $sentDiv.show();
    var $sentTable = $("#termDiv table");
    var $tbody = $sentTable.children("tbody");
    updateValue("/findSimilarCoursestoTerm", text, count, $tbody, function(res) {
      $sentBtn.addClass("active");
      $tbody.empty();
      var sentences = res.result;
      if (sentences.length <= 0 || !text.trim()) {
        $tbody.append("<tr>" +
          "<td rowspan='7'>No result</td>" +
          "</tr>");
      } else {   
        sentences.forEach(function(elem, index) {         
          $tbody.append("<tr>" + 
            "<td>" + elem.course + "</td>" +
            "<td>" + elem.title + "</td>" +
            "<td>" + elem.location + "</td>" +
            "<td>" + elem.time + "</td>" +
            "<td>" + elem.instructor + "</td>" +
            "<td>" + elem.description + "</td>" +
            "<td>" + elem.score +"</td>" + 
            "</tr>");
        });
      }
    });
  };
}).call(this);