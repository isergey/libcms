'use strict';
import React from 'react';
import utils from './utils.js';
import EventEmitter from 'eventemitter3';

let searchId = 0;

const EVENTS = {
  START_FILTERING: 'START_FILTERING',
  END_FILERING: 'END_FILERING',
  GEO_DETECTION: 'GEO_DETECTION',
  END_GEO_DETECTION: 'END_GEO_DETECTION',
  DETECT_GEO_POSITION: 'DETECT_GEO_POSITION',

};

const eventEmitter = new EventEmitter();


eventEmitter.on(EVENTS.START_FILTERING, params => {
  searchId += 1;
  let error = false;
  let items = [];
  utils.filterByDistricts(params).then(orgs => {
    items = orgs;
  }).catch(err => {
    error = err;
  }).then(() => {
    eventEmitter.emit(EVENTS.END_FILERING, {
      error,
      items,
    });
  });
});


eventEmitter.on(EVENTS.GEO_DETECTION, () => {
  navigator.geolocation.getCurrentPosition(result => {
    console.log('result', result);
    eventEmitter.emit(EVENTS.DETECT_GEO_POSITION, {
      latitude: result.coords.latitude,
      longitude: result.coords.longitude,
    });
    let error = false;
    let items = [];
    utils.geoSearch({
      lat: result.coords.latitude,
      lon: result.coords.longitude,
    }).then(response => {
      items = response;
    }).catch(err => {
      error = err;
    }).then(() => {
      eventEmitter.emit(EVENTS.END_GEO_DETECTION, {
        items,
        error,
        position: {
          latitude: result.coords.latitude,
          longitude: result.coords.longitude,
        },
      });
    });
  }, () => {
    alert('Для определения вашего местоположения необходимо дать разрешение в вашем бразузере');
  });
});


function renderLoader(message = 'Загрузка...') {
  return <span>{message}</span>;
}

function renderError(message = 'Ошибка') {
  return <span>{message}</span>;
}


const MapBoxItem = React.createClass({
  propTypes: {
    id: React.PropTypes.number,
    code: React.PropTypes.string,
    distance: React.PropTypes.number,
    href: React.PropTypes.string,
    name: React.PropTypes.string,
  },
  render() {
    return (
      <div className="map-box__list-bib__item">
        <a className="map-box__list-bib__item__link" target={this.props.href ? '_blank' : ''} href={this.props.href || '#1'} title="">{this.props.name}</a>
        { this.props.distance ? <span>{this.props.distance}</span> : null }
      </div>
    );
  },
});

const MapBoxItems = React.createClass({
  getInitialState() {
    return {
      items: [],
      loaded: true,
      error: false,
      inited: false,
    };
  },
  componentDidMount() {
    this.subscribingEvents = [
      { e: EVENTS.START_FILTERING, h: this.handleStartFiltering },
      { e: EVENTS.END_FILERING, h: this.handleEndFiltering },
    ];
    this.subscribingEvents.forEach(event => {
      eventEmitter.on(event.e, event.h);
    });
  },
  componentWillUnmount() {
    this.subscribingEvents.forEach(event => {
      eventEmitter.off(event.e, event.h);
    });
  },
  handleStartFiltering() {
    this.setState({
      inited: true,
      loaded: false,
    });
  },
  handleEndFiltering(params) {
    const { items = [], error = false } = params;
    this.setState({
      loaded: true,
      items,
      error,
    });
  },
  renderItems() {
    return this.state.items.map((item, index) => {
      const library = item.library || {};
      return (
        <MapBoxItem key={index}
          code={library.code}
          name={library.name}
          href={item.href}
          distance={item.distance}
        />
      );
    });
  },
  renderNotFound() {
    return <div>Ничего не найдено</div>;
  },
  renderNotInited() {
    return <div>Укажите букву района или нажмите на стрелку для поиска ближайших библиотек</div>;
  },
  render() {
    let content = null;

    if (this.state.error) {
      content = renderError();
    } else if (!this.state.loaded) {
      content = renderLoader();
    } else if (!this.state.inited) {
      content = this.renderNotInited();
    } else if (!this.state.items.length) {
      content = this.renderNotFound();
    } else {
      content = this.renderItems();
    }
    return (
      <div key={searchId} className="map-box__list-bib">
        {content}
      </div>
    );
  },
});

const AbcCrumbLetter = React.createClass({
  propTypes: {
    letter: React.PropTypes.string,
    onClick: React.PropTypes.func,
  },
  getDefaultProps() {
    return {
      letter: '',
      onClick: () => {
      },
    };
  },
  handleClick() {
    this.props.onClick(this.props.letter);
  },
  render() {
    return (
      <li onClick={this.handleClick}>
        <span title="" href="#" className="abc-crumbs__list_link"> {this.props.letter} </span>
      </li>
    );
  },
});

const AbcCrumbArrow = React.createClass({
  propTypes: {
    onClick: React.PropTypes.func,
  },
  render() {
    return (
      <li onClick={this.props.onClick}>
        <span title="Мое местоположение" href="#" className="abc-crumbs__list_link-img">
            <img src="/static/dist/images/geo_plain.svg"/>
        </span>
      </li>
    );
  },
});

const AbcCrumbs = React.createClass({
  getInitialState() {
    return {
      letters: [],
      loaded: false,
      error: false,
    };
  },
  componentDidMount() {
    this.loadLetters();
  },
  loadLetters() {
    let loaded = false;
    let letters = [];
    let error = false;
    utils.getDistrictLetters().then(data => {
      letters = data;
    }).catch(() => {
      error = true;
    }).then(() => {
      loaded = true;
      this.setState({
        letters,
        loaded,
        error,
      });
    });
  },
  handleLetterClick(letter) {
    eventEmitter.emit(EVENTS.START_FILTERING, {
      letter,
    });
  },
  handleArrowClick() {
    eventEmitter.emit(EVENTS.GEO_DETECTION);
  },
  renderLetters() {
    return this.state.letters.map((letter, index) => {
      return <AbcCrumbLetter onClick={this.handleLetterClick} key={index} letter={letter}/>;
    });
  },
  renderLoader() {
    return <span>Загрузка...</span>;
  },
  renderError() {
    return <span>Ошибка при загрузке районов</span>;
  },
  render() {
    let lettersContent = null;
    if (!this.state.loaded) {
      lettersContent = this.renderLoader();
    } else if (this.state.error) {
      lettersContent = this.renderError();
    } else {
      lettersContent = this.renderLetters();
    }
    return (
      <div className="abc-crumbs">
        <ul className="abc-crumbs__list">
          {lettersContent}
          <AbcCrumbArrow onClick={this.handleArrowClick}/>
        </ul>
      </div>
    );
  },
});


const LibFinder = React.createClass({
  componentDidMount() {
    this.itemsMap = null;
    window.ymaps.ready(this.initMap);
    this.subscribingEvents = [
      { e: EVENTS.START_FILTERING, h: this.handleStartFiltering },
      { e: EVENTS.END_FILERING, h: this.handleEndFiltering },
      { e: EVENTS.GEO_DETECTION, h: this.handleGeoDetection },
      { e: EVENTS.END_GEO_DETECTION, h: this.handleEndGeoDetection },
      { e: EVENTS.DETECT_GEO_POSITION, h: this.handleDetectGeoPosition },
    ];
    this.subscribingEvents.forEach(event => {
      eventEmitter.on(event.e, event.h);
    });
  },
  componentWillUnmount() {
    this.subscribingEvents.forEach(event => {
      eventEmitter.off(event.e, event.h);
    });
  },
  initMap() {
    this.itemsMap = new window.ymaps.Map(this.refs.map.getDOMNode(), {
      center: [55.76, 37.64],
      zoom: 7,
    });
  },
  drowItemsToMap(items) {
    this.itemsMap.geoObjects.removeAll();
    const clusterer = new window.ymaps.Clusterer();
    items.forEach(item => {
      const library = item.library || {};
      if (!library.latitude || !library.longitude) {
        return;
      }
      clusterer.add(new window.ymaps.Placemark([library.latitude, library.longitude], {
        hintContent: library.name || '',
        balloonContent: library.name || '',
      }));
    });
    this.itemsMap.geoObjects.add(clusterer);
    this.itemsMap.setBounds(this.itemsMap.geoObjects.getBounds());
  },
  handleStartFiltering() {

  },
  handleEndFiltering(params) {
    this.itemsMap.geoObjects.removeAll();
    const { items = [] } = params;
    this.drowItemsToMap(items);
  },
  handleGeoDetection(params) {
    console.log('handleGeoDetection', params);
  },
  handleEndGeoDetection(params) {
    console.log('handleEndGeoDetection', params);
    const { items = [] } = params;
    this.drowItemsToMap(items.object_list);
  },
  handleDetectGeoPosition(params) {
    const positionCoords = [params.latitude, params.longitude];
    let address = '';
    utils.getPositionAddress(params).then(respose => {
      address = respose;
    }).catch(() => {

    }).then(() => {
      this.itemsMap.geoObjects.add(new window.ymaps.Placemark(positionCoords, {
        hintContent: `Ваше местоположение: <b>${address}</b>`,
        balloonContent: `Ваше местоположение: <b>${address}</b>`,
      }, {
        preset: 'islands#redCircleIcon',
      }));
      this.itemsMap.setCenter(positionCoords);
      this.itemsMap.setZoom(11);
    });
  },
  render() {
    return (
      <div id="map" ref="map">
        <div className="map-box">
          <MapBoxItems />
          <h2 className="map-box__title">Алфавитный указатель муниципальных районов РТ</h2>
          <AbcCrumbs />
        </div>
      </div>
    );
  },
});

export default function (element) {
  React.render(<LibFinder />, element);
}