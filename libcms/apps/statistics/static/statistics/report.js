$(document).ready(function () {
  //alert("ready!");

  $(".stat-main-table").floatThead();

  $(".stat-parameters-select").change(function (evt) {
    var control = $(evt.target);
    var val = control.val();
    window.location.replace(val);
  });

  $(".stat-multilevel-parameter a").click(function (evt) {
    var control = $(evt.target);
    var val = control.attr("href");
    window.location.replace(val);
    return false;
  });

  $(".stat-data .stat-level-control").click(function (evt) {
    showLevelTable(evt.target);
    return false;
  });

  $(".stat-multilevel-parameter .stat-level-control").click(function (evt) {
    showLevelParameter(evt.target);
    return false;
  });

  $("th .stat-collapse-control").click(function (evt) {
    processCollapse(evt.target);
    return false;
  });

  $("li .stat-collapse-control").click(function (evt) {
    processCollapseParameter(evt.target);
    return false;
  });

  $(".stat-parameter-change").click(function (evt) {
    processParameterChange(evt.target);
    return false;
  });
});

function showLevelTable(src) {
  var level = parseInt($(src).val());
  $(".stat-main-table tbody tr").each(function (index, elem) {
    var tr = $(elem);
    var levelStr = tr.attr("data-level");
    if (levelStr === null) {
      return;
    }

    var level1 = parseInt(levelStr);
    var icon = $(".stat-collapse-control > span", tr);

    if (level1 <= level) {
      tr.show();
      tr.removeAttr("data-hidden");
    }
    else {
      tr.hide();
      tr.attr("data-hidden", 1);
    }

    if (level1 < level) {
      icon.removeClass("glyphicon-plus");
      icon.addClass("glyphicon-minus");

    }
    else {
      icon.addClass("glyphicon-plus");
      icon.removeClass("glyphicon-minus");
    }
  });
}


function processCollapse(src) {
  var tr = $(src).closest("tr");
  var level = parseInt(tr.attr("data-level"));

  var icon = $(".stat-collapse-control > span", tr);
  var isOpen = icon.hasClass("glyphicon-minus");

  processCollapse2(tr, level, isOpen);

  if (isOpen) {
    icon.addClass("glyphicon-plus");
    icon.removeClass("glyphicon-minus");
  }
  else {
    icon.removeClass("glyphicon-plus");
    icon.addClass("glyphicon-minus");
  }
}

function processCollapse2(tableRow, level, isOpen) {
  var i;

  var tableRowSpan = getRowSpan(tableRow);
  var nextTableRow = tableRow;

  for (i = 0; i < tableRowSpan; i++) {
    nextTableRow = nextTableRow.next();
  }

  if (nextTableRow.length < 1) {
    return;
  }

  var nextLevel = parseInt(nextTableRow.attr("data-level"));
  if (nextLevel <= level) {
    return;
  }

  var nextTableRowSpan = getRowSpan(nextTableRow);
  var nextTableRow2 = nextTableRow;
  for (i = 0; i < tableRowSpan; i++) {

    if (isOpen) {
      nextTableRow2.hide();
      if (nextLevel === level + 1) {
        nextTableRow2.attr("data-hidden", "1");
      }
    }
    else {
      if (nextLevel === level + 1) {
        nextTableRow2.show();
        nextTableRow2.removeAttr("data-hidden");
      }
      else {
        var isHidden = nextTableRow2.attr("data-hidden") === "1";
        if (!isHidden) {
          nextTableRow2.show();
        }
      }
    }

    nextTableRow2 = nextTableRow2.next();
  }

  processCollapse2(nextTableRow, level, isOpen);
}

function getRowSpan(tableRow) {
  var rowSpan = $("th:first-child", tableRow).attr('rowspan');
  if (rowSpan === "") {
    rowSpan = 1;
  }
  else {
    rowSpan = parseInt(rowSpan);
  }

  return rowSpan;
}

function showLevelParameter(src) {
  var level = parseInt($(src).val());
  var div1 = $(src).closest(".stat-multilevel-parameter");
  var ul = div1.children("ul");
  showLevelParameter2(ul, level);
}

function showLevelParameter2(ul, level) {
  if (level === 0) {
    ul.hide();
    return;
  }

  ul.show();
  ul.children("li").each(function (index, elem) {
    var li = $(elem);

    var icon = $(".stat-collapse-control > span", li);
    if (level > 1) {
      icon.removeClass("glyphicon-plus");
      icon.addClass("glyphicon-minus");
    }
    else {
      icon.addClass("glyphicon-plus");
      icon.removeClass("glyphicon-minus");
    }

    var ul2 = li.children("ul");
    showLevelParameter2(ul2, level - 1);
  });
}

function processCollapseParameter(src) {
  var li = $(src).closest("li");
  var icon = $(".stat-collapse-control > span", li);
  var isOpen = icon.hasClass("glyphicon-minus");

  if (isOpen) {
    $("ul", li).hide();
    icon.addClass("glyphicon-plus");
    icon.removeClass("glyphicon-minus");
  }
  else {
    $("ul", li).show();
    icon.removeClass("glyphicon-plus");
    icon.addClass("glyphicon-minus");
  }
}

function processParameterChange(src) {
  var button = $(src);
  var dimensionCode = button.attr("data-dimension");

  var divData = $(".stat-data");
  var divParam = $("div[data-dimension='" + dimensionCode + "']");

  if (divData.is(':visible')) {
    divData.hide();
    divParam.show();
  }
  else {
    divData.show();
    divParam.hide();
  }
}