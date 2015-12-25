'use strict';
import React from 'react';
import $ from 'jquery';
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
  let response = {};
  utils.filterByDistricts(params).then(resp => {
    response = resp;
  }).catch(err => {
    error = err;
  }).then(() => {
    eventEmitter.emit(EVENTS.END_FILERING, {
      error,
      response,
    });
  });
});


eventEmitter.on(EVENTS.GEO_DETECTION, () => {
  navigator.geolocation.getCurrentPosition(result => {
    // eventEmitter.emit(EVENTS.DETECT_GEO_POSITION, {
    //  latitude: result.coords.latitude,
    //  longitude: result.coords.longitude,
    // });
    let error = false;
    let response = {};
    utils.geoSearch({
      lat: result.coords.latitude,
      lon: result.coords.longitude,
    }).then(resp => {
      response = resp;
    }).catch(err => {
      error = err;
    }).then(() => {
      eventEmitter.emit(EVENTS.END_FILERING, {
        response,
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


const ContextMenu = React.createClass({
  propTypes: {
    children: React.PropTypes.object,
    onClickAway: React.PropTypes.func,
  },
  getInitialState() {
    return {
      open: false,
      left: 0,
      top: 0,
    };
  },
  componentDidMount() {
    if (!this.manuallyBindClickAway) this._bindClickAway();
  },
  componentWillUnmount() {
    this._unbindClickAway();
  },
  componentClickAway() {
    this.setState({
      open: false,
    });
  },
  open(position = {}) {
    if (this.state.open && opened) {
      return;
    }
    const calculatePosition = this._calculatePosition(position);
    this.setState({
      open: true,
      left: calculatePosition.left,
      top: calculatePosition.top,
    });
  },
  close() {
    this.setState({
      open: false,
      left: 0,
      top: 0,
    });
  },
  _calculatePosition(position) {
    let { left = 0, top = 0 } = position;
    if (this.isMounted()) {
      const $selfNode = $(React.findDOMNode(this));
      const selfWidth = $selfNode.width();
      const selfHeght = $selfNode.height();
      if (left + selfWidth > window.innerWidth) {
        left = window.innerWidth - selfWidth;
      } else {
        left = left - selfWidth / 2;
      }

      if (top + selfHeght > window.innerHeight) {
        top = window.innerHeight - selfHeght;
      }

      if (left < 0) {
        left = 0;
      }

      if (top < 0) {
        top = 0;
      }
    }
    return {
      left,
      top,
    };
  },
  _isDescendant(parent, child) {
    let node = child.parentNode;

    while (node !== null) {
      if (node === parent) return true;
      node = node.parentNode;
    }

    return false;
  },
  _checkClickAway(event) {
    if (this.isMounted()) {
      const el = React.findDOMNode(this);
      if (event.target !== el &&
          !this._isDescendant(el, event.target) &&
          document.documentElement.contains(event.target)) {
        if (this.componentClickAway) this.componentClickAway(event);
      }
    }
  },
  _bindClickAway() {
    document.addEventListener('mouseup', this._checkClickAway);
    document.addEventListener('touchend', this._checkClickAway);
  },
  _unbindClickAway() {
    document.removeEventListener('mouseup', this._checkClickAway);
    document.removeEventListener('touchend', this._checkClickAway);
  },
  render() {
    const classes = ['abc-crumbs__list__hover-box'];
    if (this.state.open) {
      classes.push('abc-crumbs__list__hover-box_show');
    }
    const style = {}
    if (this.state.left !== 0 || this.state.top !== 0) {
      style.left = this.state.left;
      style.top = this.state.top;
    }
    return (
      <div className={classes.join(' ')} style={style}>
        {this.props.children}
      </div>
    );
  },
});

const MapBoxItem = React.createClass({
  propTypes: {
    id: React.PropTypes.number,
    code: React.PropTypes.string,
    distance: React.PropTypes.number,
    href: React.PropTypes.string,
    name: React.PropTypes.string,
  },
  renderDistance() {
    if (!this.props.distance) {
      return null;
    }
    return (
      <span title="Расстояние до Вас">
        {` (Расстояние: ${utils.humanizeDistance(this.props.distance)})`}
      </span>
    );
  },
  render() {
    return (
      <div className="map-box__list-bib__item">
        <a className="map-box__list-bib__item__link"
          target={this.props.href ? '_blank' : ''}
          href={this.props.href || '#1'}
        >{this.props.name}</a>
        { this.renderDistance() }
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
      { e: EVENTS.GEO_DETECTION, h: this.handleStartFiltering },
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
    const { response = {}, error = false } = params;
    this.setState({
      inited: true,
      loaded: true,
      items: response.object_list || [],
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
    letter: React.PropTypes.object,
    onDistrictClick: React.PropTypes.func,
  },
  getDefaultProps() {
    return {
      letter: '',
      onClick: () => {
      },
    };
  },
  handleDistrictClick(districtId) {
    const contextMenu = this.refs.contextMenu;
    if (contextMenu) {
      contextMenu.close();
    }
    if (this.props.onDistrictClick) {
      this.props.onDistrictClick(districtId);
    }
  },
  handleClick(event) {
    if (this.refs.contextMenu) {
      this.refs.contextMenu.open({
        left: event.clientX,
        top: event.clientY,
      });
    }
  },
  renderContextMenu() {
    const districts = (this.props.letter.districts || []).map((district, index) => {
      return (
        <div key={district.id || index} className="map-box__list-bib__item">
          <a onClick={this.handleDistrictClick.bind(this, district.id)}
            className="map-box__list-bib__item__link" href="#1"
          >{district.name}</a>
        </div>
      );
    });
    return (
      <ContextMenu ref="contextMenu">
        <div className="map-box__list-bib">
          {districts}
        </div>
      </ContextMenu>
    );
  },
  render() {
    return (
      <li onClick={this.handleClick}>
        <span title="" href="#" className="abc-crumbs__list_link"> {this.props.letter.name} </span>
        {this.renderContextMenu()}
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
  handleDistrictClick(districtId) {
    eventEmitter.emit(EVENTS.START_FILTERING, {
      districtId,
    });
  },
  handleArrowClick() {
    eventEmitter.emit(EVENTS.GEO_DETECTION);
  },
  renderLetters() {
    return this.state.letters.map((letter, index) => {
      return <AbcCrumbLetter onDistrictClick={this.handleDistrictClick} key={index} letter={letter}/>;
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
      center: [55.797746, 49.115573],
      zoom: 10,
      controls: [],
    });
    this.itemsMap.controls.add('zoomControl', { float: 'left' });
    this.itemsMap.controls.add('searchControl', { float: 'left' });
    this.itemsMap.controls.add('typeSelector', { float: 'left' });
    this.itemsMap.controls.add('fullscreenControl', { float: 'left' });
    this.itemsMap.controls.add('trafficControl', { float: 'left' });
    this.itemsMap.controls.add('routeEditor', { float: 'left' });
    // this.itemsMap.controls.add(new window.ymaps.control.ZoomControl());
  },
  drowItemsToMap(items) {
    const clusterer = new window.ymaps.Clusterer();
    items.forEach(item => {
      const library = item.library || {};
      if (!library.latitude || !library.longitude) {
        return;
      }
      clusterer.add(new window.ymaps.Placemark([library.latitude, library.longitude], {
        hintContent: `${library.name || ''} <a target="_blank" href="${item.href}">подробнее</a>`,
        balloonContent: `${library.name || ''} <a target="_blank" href="${item.href}">подробнее</a>`,
      }));
    });
    this.itemsMap.geoObjects.add(clusterer);
    this.itemsMap.setBounds(this.itemsMap.geoObjects.getBounds());
    this.itemsMap.setZoom(this.itemsMap.getZoom() - 1);
  },
  drowUserPosition(position = {}) {
    if (position.latitude && position.longitude) {
      this.itemsMap.geoObjects.add(new window.ymaps.Placemark([position.latitude, position.longitude], {
        hintContent: 'Ваше местоположение',
        balloonContent: 'Ваше местоположение',
      }, {
        preset: 'islands#redCircleIcon',
      }));
    }
  },
  handleStartFiltering() {

  },
  handleEndFiltering(params) {
    this.itemsMap.geoObjects.removeAll();
    const { response = {}, position = {} } = params;
    this.drowUserPosition(position)
    this.drowItemsToMap(response.object_list || []);
  },
  handleGeoDetection(params) {
    console.log('handleGeoDetection', params);
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
          <h2 className="map-box__title">Алфавитный указатель муниципальных районов РТ</h2>
          <AbcCrumbs />
          <MapBoxItems />
        </div>
      </div>
    );
  },
});

export default function (element) {
  React.render(<LibFinder />, element);
}