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
    scrapeSimilarCourses(text, count);
  });

  var scrapeSimilarCourses = function(text, count) {
    var $sentDiv = $("#termDiv");
    $sentBtn = $("#findTerm");
    text = text.trim();  // trim whitespace from both ends
    count = count.trim();

    if ($sentDiv.is(":visible")) {
      $sentDiv.hide();
      $sentBtn.removeClass("active");
    } else {
      $sentDiv.show();
      var $sentTable = $("#termDiv table");
      var $tbody = $sentTable.children("tbody");
      updateValue("/findSimilarCoursestoTerm", text, count, $tbody, function(res) {
        $sentBtn.addClass("active");
        $tbody.empty();
        var sentences = res.result;
        if (sentences.length <= 0 || !text.trim()) {
          $tbody.append("<tr>" +
            "<td>No such course</td>" +
            "<td>0</td>" +
            "</tr>");
        } else {   
          sentences.forEach(function(elem, index) {         
            $tbody.append("<tr>" + 
              "<td>" + elem.course + "</td>" +
              "<td>" + elem.score +"</td>" + 
              "</tr>");
          });
        }
      });
    }
  };
}).call(this);