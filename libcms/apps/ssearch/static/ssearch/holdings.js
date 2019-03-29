(function () {

    const LOAD_HOLDERS = 'LOAD_HOLDERS';
    const COMPLETE_LOAD_HOLDERS = 'COMPLETE_LOAD_HOLDERS';
    const LOAD_HOLDERS_ERROR = 'LOAD_HOLDERS_ERROR';
    const SWITCH_TAB = 'SWITCH_TAB';

    const initialState = {
        holders: [],
        loaded: true,
        error: '',
        activeTab: 'list',
    };


    function loadHolders() {
        return {
            type: LOAD_HOLDERS,
        }
    }

    function completeLoadHolders(holders) {
        return {
            type: COMPLETE_LOAD_HOLDERS,
            holders,
        }
    }

    function loadHoldersError(holders) {
        return {
            type: COMPLETE_LOAD_HOLDERS,
            holders,
        }
    }

    function switchTab(activeTab) {
        return {
            type: SWITCH_TAB,
            activeTab,
        }
    }

    function reducer(state = initialState, action) {
        switch (action.type) {
            case LOAD_HOLDERS:
                return Object.assign({}, state, {
                    loaded: false,
                    error: '',
                });
            case  COMPLETE_LOAD_HOLDERS:
                return Object.assign({}, state, {
                    loaded: true,
                    holders: action.holders,
                    error: '',
                });
            case  LOAD_HOLDERS_ERROR:
                return Object.assign({}, state, {
                    loaded: true,
                    error: action.error,
                });
            case SWITCH_TAB:
                return Object.assign({}, state, {
                    activeTab: action.activeTab,
                });
            default:
                return state;
        }
    }

    function loadHoldings(dispatch, recordId) {
        dispatch(loadHolders());
        return new Promise((res, rej) => {
            setTimeout(() => {
                const holders = [
                    {
                        id: '1',
                        name: 'НБ',
                        coords: [],
                    },
                    {
                        id: '2',
                        name: 'РЮБ',
                        coords: [],
                    },
                ];
                dispatch(completeLoadHolders(holders))
            }, 1000)
        });
    }

    const store = Redux.createStore(reducer);


    function Holder({name}) {
        return (
            <li className="card-booking__item">
                <p className="card-booking__name">{name}</p>
                <a className="card-booking__geo" href="/ru/participants/detail/42017092/" target="_blank">
                    <i className="icon-locating" title="Контакты"></i>
                </a>
                <a className="card-booking__btn" href="/ru/orders/zorder/2/?id=ru%5Cnlrt%5C1405619">
                    Забронировать
                </a>

            </li>
        );
    }

    function HolderList({holders}) {
        return (
            <ul className="card-booking">
                {holders.map(holder => <Holder key={holder.id} name={holder.name}/>)}
            </ul>
        );
    }

    function HoldersMap() {
        return (
            <div>Map</div>
        );
    }

    const Holders = ReactRedux.connect((state) => ({...state}))(function ({loaded, error, holders, activeTab}) {
        return (
            <div className="record_holders card card_bs-2 card_booking">
                <div className="card__header">
                    <h2 className="card__title card__title_sm">
                        Бронирование
                        <div className="record_holders__tabs">
                            <span className="record_holders__tab"
                                  onClick={() => store.dispatch(switchTab('list'))}>Список</span>
                            <span className="record_holders__tab"
                                  onClick={() => store.dispatch(switchTab('map'))}>Карта</span>
                        </div>
                    </h2>
                </div>
                <div className="card__body">
                    {!loaded ? <div key="loader">Загрузка</div> : null}
                    {error && <div key="error">Ошибка</div>}
                    <div style={{display: activeTab !== 'list' ? 'none': ''}}>
                        <HolderList holders={holders}/>
                    </div>
                    <div style={{display: activeTab !== 'map' ? 'none': ''}}>
                        <HoldersMap holders={holders}/>
                    </div>
                </div>
            </div>
        );
    });

    loadHoldings(store.dispatch);

    ReactDOM.render(
        <ReactRedux.Provider store={store}>
            <Holders recordId="zsawbjdruo"/>
        </ReactRedux.Provider>,
        document.getElementById('record_holdings')
    );
})();