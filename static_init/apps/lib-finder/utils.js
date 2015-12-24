'use strict';
import $ from 'jquery';

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
      console.log('data', data);
      resolve(data.object_list);
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

export default {
  getDistrictLetters,
  filterByDistricts,
  geoSearch,
  getPositionAddress,
};

