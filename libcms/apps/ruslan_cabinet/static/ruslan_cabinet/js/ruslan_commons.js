(function (React, $) {
  'use strict';
  window.Ruslan = window.Ruslan || {};

  var Api = function (settings) {
    this.getRecords = function (params) {
      var defer = $.Deferred();
      $.get(settings.urls.getRecordsUrl, {
        'id_list': params.id_list,
        opac: params.opac
      }).done(function (data) {
        defer.resolve(data);
      }).error(function (error) {
        defer.reject(error);
        //console.error('Error while getRecord ', error);
      });
      return defer;
    };

    /**
     * Бронирование
     * @param params
     *  orderType - Hold | Non-returnable Copy
     *  recordId - идентификатор записи
     *  pickupLocation - место получения
     *  onBusyBehavior - политика обслуживания, если нет свободных экземпляров
     *  comments - комментарии
     * @returns {*}
     */
    this.makeOrder = function (params) {
      (function(params, keys) {
        for (var i in keys) {
          if (!params[keys[i]]) {
            throw new Error(keys[i] + ' param required');
          }
        }
      })(params, ['recordId', 'pickupLocation', 'orderType']);

      var orderType = params.orderType;
      var recordId = params.recordId;
      var pickupLocation = params.pickupLocation;

      var defer = $.Deffered();

      $.post({
        orderType: orderType,
        recordId: recordId,
        pickupLocation: pickupLocation
      }).done(function (data) {
        defer.resolve(data);
      }).error(function (error) {
        //console.error(error);
        defer.reject(error);
      });

      return defer;
    };
  };

  var Loader = React.createClass({
    render: function () {
      return (
        <div>{ this.props.message || 'Пожалуйста, подождите...' }</div>
      );
    }
  });

  var ErrorMessage = React.createClass({
    render: function () {
      return (
        <div>{ this.props.message || 'Неизвестная ошибка' }</div>
      );
    }
  });

  window.Ruslan.Commons = {
    Api: Api,
    ui: {
      Loader: Loader,
      ErrorMessage: ErrorMessage
    }
  };
})(React, $);

