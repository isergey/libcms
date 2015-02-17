(function () {
  $(document).ready(function () {
    //alert("ready!");

    $(".stat-parameters-select").change(function (evt) {
      var control = $(evt.target);
      var val = control.val();
      $('body').append('<div class="report-loading-modal">Пожалуйста подождите... <img src="/static/statistics/loading-bubbles.svg" width="64" height="64"><div>');
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
    $(".stat-main-table tr").each(function (index, elem) {
      var tr = $(elem);
      var levelStr = tr.attr("data-level");
      if (levelStr == null) {
        return;
      }

      var level1 = parseInt(levelStr);
      var icon = $(".stat-collapse-control > .toggler", tr);

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
        icon.removeClass("icon-plus");
        icon.addClass("glyphicon-minus");
        icon.addClass("icon-minus");

      }
      else {
        icon.addClass("glyphicon-plus");
        icon.addClass("icon-plus");
        icon.removeClass("glyphicon-minus");
        icon.removeClass("icon-minus");
      }
    });
  }


  function processCollapse(src) {
    var tr = $(src).closest("tr");
    var level = parseInt(tr.attr("data-level"));

    var icon = $(".stat-collapse-control > .toggler", tr);
    var isOpen = icon.hasClass("glyphicon-minus");

    processCollapse2(tr, level, isOpen);

    if (isOpen) {
      icon.addClass("glyphicon-plus");
      icon.addClass("icon-plus");
      icon.removeClass("glyphicon-minus");
      icon.removeClass("icon-minus");
    }
    else {
      icon.removeClass("glyphicon-plus");
      icon.removeClass("icon-plus");
      icon.addClass("glyphicon-minus");
      icon.addClass("icon-minus");
    }
  }

  function processCollapse2(tableRow, level, isOpen) {
    var nextTableRow = tableRow.next();
    if (nextTableRow.length < 1) {
      return;
    }

    var nextLevel = parseInt(nextTableRow.attr("data-level"));
    if (nextLevel <= level) {
      return;
    }

    if (isOpen) {
      nextTableRow.hide();
      if (nextLevel == level + 1) {
        nextTableRow.attr("data-hidden", "1");
      }
    }
    else {
      if (nextLevel == level + 1) {
        nextTableRow.show();
        nextTableRow.removeAttr("data-hidden");
      }
      else {
        var isHidden = (nextTableRow.attr("data-hidden") == "1");
        if (!isHidden) {
          nextTableRow.show();
        }
      }
    }

    processCollapse2(nextTableRow, level, isOpen);
  }

  function showLevelParameter(src) {
    var level = parseInt($(src).val());
    var div1 = $(src).closest(".stat-multilevel-parameter");
    var ul = div1.children("ul");
    showLevelParameter2(ul, level);
  }

  function showLevelParameter2(ul, level) {
    if (level == 0) {
      ul.hide();
      return;
    }

    ul.show();
    ul.children("li").each(function (index, elem) {
      var li = $(elem);

      var icon = $(".stat-collapse-control > .toggler", li);
      if (level > 1) {
        icon.removeClass("glyphicon-plus");
        icon.removeClass("icon-plus");
        icon.addClass("glyphicon-minus");
        icon.addClass("icon-minus");
      }
      else {
        icon.addClass("glyphicon-plus");
        icon.addClass("icon-plus");
        icon.removeClass("glyphicon-minus");
        icon.removeClass("icon-minus");
      }

      var ul2 = li.children("ul");
      showLevelParameter2(ul2, level - 1);
    });
  }

  function processCollapseParameter(src) {
    var li = $(src).closest("li");
    var icon = $(".stat-collapse-control > .toggler", li);
    var isOpen = (icon.hasClass("glyphicon-minus") | icon.hasClass("icon-minus"));

    if (isOpen) {
      $("ul", li).hide();
      icon.addClass("glyphicon-plus");
      icon.addClass("icon-plus");
      icon.removeClass("glyphicon-minus");
      icon.removeClass("icon-minus");
    }
    else {
      $("ul", li).show();
      icon.removeClass("glyphicon-plus");
      icon.removeClass("icon-plus");
      icon.addClass("glyphicon-minus");
      icon.addClass("icon-minus");
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
})();
