'use strict';
import React from 'react';
import $ from 'jquery';
import 'typehead';
import utils from './utils.js';
import EventEmitter from 'eventemitter3';

var translates = {
    'Для определения вашего местоположения необходимо дать разрешение в вашем бразузере': {
        'en': 'To determine your location you need to give permission in your browser',
        'tt': 'Билгеләү өчен Сезнең җир бирергә кирәк рөхсәт сезнең бразузере'
    },
    'Загрузка...': {
        'en': 'Loading...',
        'tt': 'Зинһар көтегез...',
    },
    'Ошибка': {
        'en': 'Error',
        'tt': 'Хата',
    },
    'Расстояние до Вас': {
        'en': 'Distance to you',
        'tt': 'Ераклык сезгә кадәр',
    },
    'Расстояние': {
        'en': 'Distance',
        'tt': 'Ераклык',
    },
    'Ничего не найдено': {
        'en': 'Nothing found',
        'tt': 'Бернәрсә дә табылмаган',
    },
    'Мое местоположение': {
        'en': 'My location',
        'tt': 'Минем җир',
    },
    'Ближайшие библиотеки': {
        'en': 'Nearest libraries',
        'tt': 'Якындагы китапханәләр',
    },
    'Введите адрес для поиска ближайшей библиотеки': {
        'en': 'Enter address to find a library nearby',
        'tt': 'Языгыз адрес эзләү өчен якындагы китапханә',
    },
    'подробнее': {
        'en': 'details',
        'tt': 'җентекле',
    },
    'Ваше местоположение': {
        'en': 'Your location',
        'tt': 'Сезнең җир'
    },
    'Искомый адрес': {
        'en': 'Search address',
        'tt': 'Телсез адрес',
    },
    'Алфавитный указатель муниципальных районов': {
        'en': 'Alphabetical index of municipalities',
        'tt': 'Муниципаль районнарның алфавит күрсәткече',
    },
    'Выберите букву района или нажмите на гео точку для поиска ближайших библиотек': {
        'en': 'Search region by the first letter or Press geotag to find a library near you',
        'tt': 'Сайлагыз хәрефе район яки басыгыз гео ноктасы эзләү өчен якындагы китапханәләр',
    }

};

function translate(message) {
    return (translates[message] || {})[window.CURRENT_LANGUAGE] || message;
}



let searchId = 0;

const POSITION_TYPES = {
    ADDRESS: 'ADDRESS',
    USER: 'USER',
};

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
        const {lat = 0, lon = 0} = params;
        const position = {};
        if (lat && lon) {
            position.latitude = lat;
            position.longitude = lon;
            position.type = POSITION_TYPES.ADDRESS;
        }
        eventEmitter.emit(EVENTS.END_FILERING, {
            error,
            response,
            position,
        });
    });
});


eventEmitter.on(EVENTS.GEO_DETECTION, () => {
    utils.detectUserGeoPosition().then(position => {
        let error = false;
        let response = {};
        utils.geoSearch({
            lat: position.latitude,
            lon: position.longitude,
        }).then(resp => {
            response = resp;
        }).catch(err => {
            error = err;
        }).then(() => {
            eventEmitter.emit(EVENTS.END_FILERING, {
                response,
                error,
                position: {
                    latitude: position.latitude,
                    longitude: position.longitude,
                },
            });
        });
    }).catch(() => {
        alert(translate('Для определения вашего местоположения необходимо дать разрешение в вашем бразузере'));
    });
});


function renderLoader(message = translate('Загрузка...')) {
    return (
        <div className="lds-roller-wrap-center">
            <div className="lds-roller">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    );
}

function renderError(message = translate('Ошибка')) {
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
        if (this.state.open) {
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
        let {left = 0, top = 0} = position;
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
        const classes = ['map-nav-dropdown-wrap'];
        if (this.state.open) {
            classes.push('map-nav-dropdown-wrap_show');
        }
        const style = {};
        if (this.state.left !== 0 || this.state.top !== 0) {
            style.left = this.state.left;
            style.top = this.state.top;
        }
        return (
            <div className={classes.join(' ')} style={style}>
                <button className="map-nav-dropdown-btn" onClick={this.close}>
                    Закрыть
                </button>
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
            <span title={translate('Расстояние до Вас')}>
        {` (${translate('Расстояние')}: ${utils.humanizeDistance(this.props.distance)})`}
      </span>
        );
    },
    render() {
        return (
            <div className="map-nav-result__item">
                <a className="map-nav-result__link"
                   target={this.props.href ? '_blank' : ''}
                   href={this.props.href || '#1'}
                >{this.props.name}</a>
                {this.renderDistance()}
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
            {e: EVENTS.START_FILTERING, h: this.handleStartFiltering},
            {e: EVENTS.GEO_DETECTION, h: this.handleStartFiltering},
            {e: EVENTS.END_FILERING, h: this.handleEndFiltering},
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
        const {response = {}, error = false} = params;
        this.setState({
            inited: true,
            loaded: true,
            items: response.object_list || [],
            error,
        });
    },
    renderItems() {
        var items = this.state.items.map((item, index) => {
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
        return (
            <ul className="map-nav-result">
                {items}
            </ul>
        );
    },
    renderNotFound() {
        return <div>translate(Ничего не найдено)</div>;
    },
    renderNotInited() {
        // return <div className="help-text">Укажите букву района или нажмите на стрелку для поиска ближайших
        //     библиотек</div>;
        return null;
    },
    render() {
        let content = null;

        if (this.state.error) {
            content = renderError();
        } else if (!this.state.loaded) {
            content = renderLoader();
        } else if (!this.state.inited) {
            return null;
            // content = this.renderNotInited();
        } else if (!this.state.items.length) {
            content = this.renderNotFound();
        } else {
            content = this.renderItems();
        }

        return (
            <div key={searchId} className="map-nav-result-box">
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
                <li key={district.id || index} className="map-nav-dropdown-menu__item">
                    <a onClick={this.handleDistrictClick.bind(this, district.id)}
                       className="map-nav-dropdown-menu__link" href="#1"
                    >{district.name}</a>
                </li>
            );
        });
        return (
            <ContextMenu ref="contextMenu">
                <ul className="map-nav-dropdown-menu">
                    {districts}
                </ul>
            </ContextMenu>
        );
    },
    render() {
        return (
            <li className="map-nav-abc__item" onClick={this.handleClick}>
                <button className="map-nav-abc__link"><span>{this.props.letter.name}</span></button>
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
        <span title={translate('Мое местоположение')} href="#" className="abc-crumbs__list_link-img">
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
            <ul className="map-nav-abc">
                {lettersContent}
                {/*<AbcCrumbArrow onClick={this.handleArrowClick}/>*/}
            </ul>
        );
    },
});

const AddrSearch = React.createClass({
    componentDidMount() {
        const $typeahead = $(this.refs.input.getDOMNode());
        let position = {};
        utils.detectUserGeoPosition().then(result => {
            position = result;
        }).catch(error => {
            // alert('Ваше местоположение не определено');
            console.error('Error of user geo detection', error);
        }).then(() => {
            $typeahead.typeahead(
                {
                    minLength: 3,
                    highlight: true,
                },
                {
                    name: 'qaddr',
                    source: utils.getTypeHeadSource([position.latitude, position.longitude]),
                }
            );
            $typeahead.on('typeahead:selected', function (e, datum) {
                const positionParts = datum.position.split(' ');
                eventEmitter.emit(EVENTS.START_FILTERING, {
                    lat: positionParts[1],
                    lon: positionParts[0],
                });
            });
        });
    },
    handleArrowClick() {
        eventEmitter.emit(EVENTS.GEO_DETECTION);
    },
    renderSuggest() {

        return (
            <div className="adrr-search__result-box">
                <div className="map-box__list-bib__item">
                    <a className="map-box__list-bib__item__link" href="#" title="">Республиканская</a>
                </div>
                <div className="map-box__list-bib__item">
                    <a className="map-box__list-bib__item__link" href="#" title="">Республиканская</a>
                </div>
                <div className="map-box__list-bib__item">
                    <a className="map-box__list-bib__item__link" href="#" title="">Республиканская</a>
                </div>
                <div className="map-box__list-bib__item">
                    <a className="map-box__list-bib__item__link" href="#" title="">Республиканская</a>
                </div>
                <div className="map-box__list-bib__item">
                    <a className="map-box__list-bib__item__link" href="#" title="">Республиканская</a>
                </div>
            </div>
        );
    },
    render() {
        return (
            <div className="map-nav-search">
                <div className="map-nav-search__geo-col">
                    <button className="map-nav__geo-btn" onClick={this.handleArrowClick}>
                        <i className="icon-locating" title={translate('Ближайшие библиотеки')}></i>
                    </button>
                </div>
                <div className="map-nav-search__search-col">
                    <div className="map-nav-search-input">
                        <input ref="input" className="map-nav-search-input__input"
                               placeholder={translate('Введите адрес для поиска ближайшей библиотеки')}/>
                        <button className="map-nav-search-input__btn">
                            <i className="icon-search" title="Поиск"></i>
                        </button>
                    </div>
                </div>

            </div>
        );
    },
});

const LibFinder = React.createClass({
    componentDidMount() {
        this.itemsMap = null;
        window.ymaps.ready(this.initMap);
        this.subscribingEvents = [
            {e: EVENTS.START_FILTERING, h: this.handleStartFiltering},
            {e: EVENTS.END_FILERING, h: this.handleEndFiltering},
            {e: EVENTS.GEO_DETECTION, h: this.handleGeoDetection},
            {e: EVENTS.DETECT_GEO_POSITION, h: this.handleDetectGeoPosition},
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
        var self = this;
        this.itemsMap = new window.ymaps.Map(this.refs.map.getDOMNode(), {
            center: [55.797746, 49.115573],
            zoom: 10,
            controls: [],
        });
        this.itemsMap.behaviors.disable('scrollZoom');

        function initClick() {
            self.itemsMap.behaviors.enable('scrollZoom');
            self.itemsMap.events.remove('click', initClick);
        }

        this.itemsMap.events.add('click', initClick);
        this.itemsMap.controls.add('zoomControl', {float: 'left'});
        this.itemsMap.controls.add('searchControl', {float: 'left'});
        this.itemsMap.controls.add('typeSelector', {float: 'left'});
        this.itemsMap.controls.add('fullscreenControl', {float: 'left'});
        this.itemsMap.controls.add('trafficControl', {float: 'left'});
        this.itemsMap.controls.add('routeEditor', {float: 'left'});
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
                hintContent: `${library.name || ''} <a target="_blank" href="${item.href}">${translate('подробнее')}</a>`,
                balloonContent: `${library.name || ''} <a target="_blank" href="${item.href}">${translate('подробнее')}</a>`,
            }));
        });
        this.itemsMap.geoObjects.add(clusterer);
        this.itemsMap.setBounds(this.itemsMap.geoObjects.getBounds());
        this.itemsMap.setZoom(this.itemsMap.getZoom() - 1);
    },
    drowUserPosition(position = {}) {
        let content = translate('Ваше местоположение');
        if (position.type === POSITION_TYPES.ADDRESS) {
            content = translate('Искомый адрес');
        }
        if (position.latitude && position.longitude) {
            this.itemsMap.geoObjects.add(new window.ymaps.Placemark([position.latitude, position.longitude], {
                hintContent: content,
                balloonContent: content,
            }, {
                preset: 'islands#redCircleIcon',
            }));
        }
    },
    handleStartFiltering() {

    },
    handleEndFiltering(params) {
        this.itemsMap.geoObjects.removeAll();
        const {response = {}, position = {}} = params;
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
                hintContent: `${translate('Ваше местоположение')}: <b>${address}</b>`,
                balloonContent: `${translate('Ваше местоположение')}: <b>${address}</b>`,
            }, {
                preset: 'islands#redCircleIcon',
            }));
            this.itemsMap.setCenter(positionCoords);
            this.itemsMap.setZoom(11);
        });
    },
    render() {
        return (
            <div className="map">
                <div className="map__col-l">
                    <div className="map-nav">
                        <h3 className="map-nav__title">{translate('Алфавитный указатель муниципальных районов')}</h3>
                        <p className="map-nav__help-text">
                            {translate('Выберите букву района или нажмите на гео точку для поиска ближайших библиотек')}
                        </p>
                        <AddrSearch/>
                        <AbcCrumbs/>
                        <MapBoxItems/>
                    </div>
                </div>
                <div className="map__col-r" id="map" ref="map">

                </div>
            </div>
        );
    },
});

export default function (element) {
    React.render(<LibFinder/>, element);
}