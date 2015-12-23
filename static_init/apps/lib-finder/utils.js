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

export default {
  getDistrictLetters,
};

