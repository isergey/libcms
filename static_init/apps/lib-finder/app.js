'use strict';
import React from 'react';
import utils from './utils.js';

const MapBoxItem = React.createClass({
  render() {
    return (
      <div className="map-box__list-bib__item">
        <a className="map-box__list-bib__item__link" href="#" title="">Республиканская</a>
        <span>(52598)</span>
      </div>
    );
  },
});

const MapBoxItems = React.createClass({
  render() {
    return (
      <div className="map-box__list-bib">
        <MapBoxItem />
        <MapBoxItem />
        <MapBoxItem />
        <MapBoxItem />
        <MapBoxItem />
        <MapBoxItem />
        <MapBoxItem />
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
      onClick: () => {},
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
            <img src="/static/dist/images/geo_plain.svg" />
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
    console.log(letter);
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