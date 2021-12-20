import './description.js';
import '../../../hunting/src/script/Comp/Content-list.js';
import TourismAPI from '../../../hunting/src/script/data/TourismData.js';

const main = () => {
  const tourElement = document.querySelector('content-list');
  const descElement = document.querySelector('desc-box');
  let place = JSON.parse(localStorage.getItem('place'));
  console.log(place);
  if (place) {
    descElement.place = place;
  }
  const rendering = () => {
    fetch(TourismAPI.baseUrl + '/showtwelve')
      .then((res) => res.json())
      .then((responseJson) => {
        console.log(responseJson);
        tourElement.tour = responseJson.data;
      })
      .catch((message) => {
        tourElement.renderError(message);
      });
  };
  const success_render = (results) => {
    tourElement.tour = results;
  };
  rendering();
};
document.addEventListener('DOMContentLoaded', main);
