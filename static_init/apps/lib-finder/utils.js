'use strict';
const $ = window.$;

function getDistrictLetters() {
  return new Promise((resolve, reject) => {
    $.get('/ru/participants/get_district_letters/').done(letters => {
      resolve(letters);
    }).fail(error => {
      console.error(error);
      reject(error);
    });
  });
}

function filterByDistricts(params) {
  return new Promise((resolve, reject) => {
    $.get('/ru/participants/filter_by_districts/', params).done(data => {
      resolve(data);
    }).fail(error => {
      console.error(error);
      reject(error);
    });
  });
}

function geoSearch(params) {
  return new Promise((resolve, reject) => {
    $.get('/ru/participants/geosearch/nearest/', params).done(data => {
      resolve(data);
    }).fail(error => {
      console.error(error);
      reject(error);
    });
  });
}

function getPositionAddress(params) {
  return new Promise((res, rej) => {
    $.get('//geocode-maps.yandex.ru/1.x/', {
      format: 'json',
      geocode: params.longitude + ',' + params.latitude,
    }).done(function (data) {
      const address = ((((data.response.GeoObjectCollection.featureMember[0] || {}).GeoObject || {}).metaDataProperty || {}).GeocoderMetaData || {}).text || '';
      res(address);
    }).error(function (error) {
      rej(error);
    });
  });
}

function getTypeHeadSource(myPosition) {
  return (query, cb) => {
    $.get('//geocode-maps.yandex.ru/1.x/', {
      format: 'json',
      geocode: query,
      ll: myPosition[1] + ',' + myPosition[0],
      spn: '3.0,3.0',
    }).done(data => {
      const results = [];
      data.response.GeoObjectCollection.featureMember.forEach((item) => {
        results.push({
          value: item.GeoObject.metaDataProperty.GeocoderMetaData.text,
          position: item.GeoObject.Point.pos,
        });
      });
      cb(results);
    }).error(error => {
      console.error(error);
    });
  };
}

function detectUserGeoPosition() {
  return new Promise((res, rej) => {
    navigator.geolocation.getCurrentPosition(result => {
      res({
        latitude: result.coords.latitude,
        longitude: result.coords.longitude,
      });
    }, error => {
      rej(error);
    });
  });
}

function humanizeDistance(distance) {
  const km = Math.floor(distance);
  const meters = Math.round(distance % 1 * 1000);
  const stringParts = [];
  if (km) {
    stringParts.push(km + ' км');
  }
  if (meters) {
    stringParts.push(meters + ' м');
  }
  return stringParts.join(' ');
}

export default {
  getDistrictLetters,
  filterByDistricts,
  geoSearch,
  getPositionAddress,
  detectUserGeoPosition,
  humanizeDistance,
  getTypeHeadSource,
};

