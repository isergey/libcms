'use strict';
import React from 'react';
import utils from './utils.js';
import EventEmitter from 'eventemitter3';

let searchId = 0;

const EVENTS = {
  START_FILTERING: 'START_FILTERING',
  END_FILERING: 'END_FILERING',
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
    name: React.PropTypes.string,
  },
  render() {
    return (
      <div className="map-box__list-bib__item">
        <a className="map-box__list-bib__item__link" href="#" title="">{this.props.name}</a>
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
      return (
        <MapBoxItem key={index}
          code={item.code}
          name={item.name}
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
          <AbcCrumbArrow/>
        </ul>
      </div>
    );
  },
});

const MapBox = React.createClass({
  render() {
    return (
      <div className="map-box">
        <MapBoxItems />
        <AbcCrumbs />
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
  handleStartFiltering() {

  },
  handleEndFiltering(params) {
    const { items = [] } = params;
    this.itemsMap.geoObjects(items.map(item => {
      return new window.ymaps.Placemark([item.altitude, item.longitude], {
        hintContent: item.name || '',
        balloonContent: item.name || '',
      });
    }));
  },
  render() {
    return (
      <div id="map" ref="map">
        <MapBox />
      </div>
    );
  },
});

export default function (element) {
  React.render(<LibFinder />, element);
}