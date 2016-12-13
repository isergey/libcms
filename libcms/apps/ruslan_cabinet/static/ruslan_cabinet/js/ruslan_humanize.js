(function ($) {
  'use strict';
  window.Ruslan = window.Ruslan || {};
  var SRU = {}, Order = {};

  var ORDER_NOT_POSSIBLE_MSG = 'Электронный заказ на книговыдачу невозможен';
  var DISABLE_ORDER_RESTRICTIONS = ['Электронный заказ на книговыдачу невозможен'];

  var prepareLocalLocationsForOrder = function(canOrderBranches) {
    var localLocationsForOrder = [];
      if (canOrderBranches && Array.isArray(canOrderBranches)) {
        canOrderBranches.forEach(function(branch) {
          localLocationsForOrder.push(branch.toLowerCase())
        });
      }
    return localLocationsForOrder;
  };

  /**
   * Get diagnostics form sru response
   * @param sruResponse
   * @returns {*|{}}
   */
  SRU.getDiagnostics = function (sruResponse) {
    return sruResponse.diagnostics || {};
  };

  /**
   * Extract records from sru result
   * @param result
   * @returns {Array}
   */
  SRU.getRecords = function (sruResponse) {
    return (sruResponse.records || {}).record || [];
  };

  /**
   * Extract record from result set by identifier
   * @param recordList from result set
   * @param identifier
   * @returns null or record
   */
  SRU.extractRecordWithIdentifier = function (recordList, identifier) {
    var i = 0, record = null, currentRecord = 0;
    for (i = 0; i < recordList.length; ++i) {
      currentRecord = recordList[i];
      if (currentRecord.recordIdentifier === identifier) {
        record = currentRecord;
        break;
      }
    }
    return record;
  };

  SRU.getBibRecordContent = function (recordFromResult) {
    var content = ((((recordFromResult.recordData || {}).content || [{}])[0].record || {}).bibliographicRecord || {}).record || {};
    return content;
  };

  SRU.getRecordHoldings = function (recordFromResult) {
    var content = (((recordFromResult.recordData || {}).content || [{}])[0].holdingsData || {}).holdingsAndCirc || [];
    return content;
  };



  Order.buildHoldingsGroups = function (holdings, canOrderBranches) {
    //console.log('holdings', holdings);
    var LOCAL_LOCATION_FOR_ORDER = prepareLocalLocationsForOrder(canOrderBranches);

    var groups = {};
    holdings.forEach(function (holding) {
      var nucCode = holding.nucCode;
      if (!nucCode) {
        return;
      }

      var nucCodeData = groups[nucCode] || {};

      var localLocation = holding.localLocation;

      if (!localLocation) {
        return;
      }

      var localLocationData = nucCodeData[localLocation] || {};
      nucCodeData[localLocation] = localLocationData;

      var stats = localLocationData.stats ||
        {
          total: 0,
          restricted: 0,
          availableNow: 0,
          onHold: 0,
          forOrder: 0,
          restrictionList: [],
          shelvingData: [],
          callNumber: []
        };

      localLocationData.stats = stats;

      var circulationData = holding.circulationData || [];

      circulationData.forEach(function (circulationItem) {
        var availableNow = circulationItem.availableNow,
          onHold = circulationItem.onHold,
          restrictions = circulationItem.restrictions;

        stats.total += 1;

        if (availableNow === true) {
          stats.availableNow += 1;

          if (restrictions) {
            stats.restricted += 1;
            if (stats.restrictionList.indexOf(restrictions) < 0) {
              stats.restrictionList.push(restrictions);
            }
          }
        }

        if (availableNow === true) {
          if ((!restrictions || DISABLE_ORDER_RESTRICTIONS.indexOf(restrictions) === -1)
            && LOCAL_LOCATION_FOR_ORDER.indexOf(localLocation.toLocaleLowerCase()) !== -1) {
            stats.forOrder += 1;
          } else {
            if (stats.restrictionList.indexOf(ORDER_NOT_POSSIBLE_MSG) == -1) {
              stats.restrictionList.push(ORDER_NOT_POSSIBLE_MSG);
            }
          }
        } else {
          if (LOCAL_LOCATION_FOR_ORDER.indexOf(localLocation.toLocaleLowerCase()) === -1) {
            if (stats.restrictionList.indexOf(ORDER_NOT_POSSIBLE_MSG) == -1) {
              stats.restrictionList.push(ORDER_NOT_POSSIBLE_MSG);
            }
          }
        }


        if (onHold === true) {
          stats.onHold += 1;
        }

        if (availableNow === true) {
          if (holding.callNumber && stats.callNumber.indexOf(holding.callNumber) === -1) {
            stats.callNumber.push(holding.callNumber);
          }
          if (holding.shelvingData && stats.shelvingData.indexOf(holding.shelvingData) === -1) {
            stats.shelvingData.push(holding.shelvingData);
          }
        }
      });

      groups[nucCode] = nucCodeData;
    });
    return groups;
  };


  window.Ruslan.Humanize = {
    SRU: SRU,
    Order: Order
  };
})($);

