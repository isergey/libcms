(function (React, $) {
    'use strict';
    var Ruslan = window.Ruslan = window.Ruslan || {};
    var disabledBranches = ['спбгпу/ооп'];
    var getBranchTitle = (function () {
        var titles = {
            'спбгпу': {
                '31013': 'Учебно-научный сектор \"Строительство объектов возобновляемой энергетики\"',
                '31021': 'Кафедра «Гражданское строительство и прикладная экология» (КГСиПЭ)',
                '31024': 'Кафедра «Гражданское строительство и прикладная экология» (КГСиПЭ)',
                '31031': 'Кафедра «Строительство уникальных зданий и сооружений» (КСУЗИС)',
                '31032': 'Кафедра «Строительство уникальных зданий и сооружений» (КСУЗИС)',
                '31041': 'Кафедра «Строительная механика и строительные конструкции» (КСМиСК)',
                '31051': 'Кафедра «Сопротивление материалов» (КСМ)',
                '32111': 'Кафедра «Электрические станции и автоматизация энергетических систем» (ЭС и АЭС)',
                '32121': 'Кафедра «Электрические системы и сети» (ЭСиС)',
                '32132': 'Кафедра «Техника высоких напряжений, электроизоляционная и кабельная техника» (КТВНЭиКТ)',
                '32141': 'Лаборатория «Электрических машин» Кафедры «Электрических машин» (ЭМ)',
                '32151': 'Кафедра «Электротехника и электроэнергетика» (КЭиЭЭ)',
                '32152': 'Кафедра «Электротехника и электроэнергетика» (КЭиЭЭ)',
                '32154': 'Научно-исследовательская лаборатория Кафедры «Электротехника и электроэнергетика» (КЭиЭЭ)',
                '32161': 'Кафедра «Теоретические основы  электротехники» (ТОЭ)',
                '32212': 'Кафедра «Атомная и тепловая энергетика» (КАиТЭ)',
                '32221': 'Кафедра «Турбины, гидромашины и авиационные двигатели» (ТДиАД)',
                '32231': 'Кафедра «Реакторы, парогенераторы и котельные установки» (КРПиКУ)',
                '32241': 'Кафедра «Компрессорная, вакуумная и холодильная техника» (ККВиХТ)',
                '32252': 'Учебная лаборатория «Автомобили и гусеничные машины» Кафедры «Двигатели, автомобили и гусеничные машины» (ДАиГМ)',
                '32271': 'Дирекция Электромеханического отделения Института энергетики и транспортных систем (ИЭиТС ЭлМО)',
                '32283': 'Кабинет курсового и дипломного проектирования № 1 Института энергетики и транспортных систем (ИЭиТС)',
                '33013': 'Кафедра «Машиноведение и основы конструирования» (КМиК)',
                '33052': 'Кафедра «Инженерная графика и дизайн» (КИГиД)',
                '33111': 'Лаборатория «Стали и сплавы»',
                '33112': 'Лаборатория «Электрометаллургия цветных металлов» Отделения технологий материалов Кафедры «Металлургические технологии» (МТ)',
                '33121': 'Кафедра «Материалы, технологии и оборудование литейного производства» (МТиОЛП)',
                '33134': 'Лаборатория полупроводниковых материалов',
                '33141': 'Кафедра «Технология и исследование материалов»',
                '33143': 'Кафедра «Технология и исследование материалов» (КМПиТОМ)',
                '33144': 'Центр новых материалов',
                '33152': 'Кафедра «Сварка и лазерные технологии» (КСЛТ)',
                '33211': 'Кафедра «Технология машиностроения» (КТМ)',
                '33221': 'Кафедра «Автоматы» (КАвТ)',
                '33253': 'Библиотека кафедры «Транспортные и технологические системы» (КТТС)',
                '34111': 'Кафедра «Физика плазмы» (КФП)',
                '34151': 'Демонстрационный кабинет кафедры «Экспериментальная физика» (КЭФ)',
                '34152': 'Кафедра «Экспериментальная физика» (КЭФ)',
                '34171': 'Кафедра «Биофизика» (КБФ)',
                '34211': 'Кафедра «Радиофизика» (КРФ)',
                '34221': 'Кафедра «Радиотехника и телекоммуникации» (КРТиКТ)',
                '34231': 'Кафедра «Квантовая электроника» (ККЭ)',
                '34241': 'Кафедра «Физическая электроника» (КФЭ)',
                '34251': 'Кафедра «Интегральная электроника» (КИЭ)',
                '34261': 'Кафедра «Физика полупроводников и наноэлектроника» (КФПиНЭ)',
                '34271': 'Кафедра «Радиоэлектронные средства защиты информации» (РЭСЗИ)',
                '34312': 'Кафедра «Физико-химические основы медицины, биотехнология и реабилитационные биотехнические системы» (ФХОМБ и РБС)',
                '34313': 'Кафедра «Физико-химические основы медицины, биотехнология и реабилитационные биотехнические системы» (ФХОМБ и РБС (ИФС)',
                '34331': 'Дирекция отделения медицинской физики и биоинженерии',
                '34332': 'Дирекция отделения физики и нанотехнологии',
                '35011': 'Кафедра «Компьютерные системы и программные технологии» (КСПТ)',
                '35021': 'Кафедра «Системный анализ и управление» (КСАиУ)',
                '35033': 'Кафедра «Системы и технологии управления» (СиТУ)',
                '35042': 'Кафедра «Информационные и управляющие системы» (КИУС)',
                '35071': 'Кафедра «Распределенные вычисления и компьютерные сети» (КРВКС)',
                '35081': 'Кафедра «Информационная безопасность компьютерных систем» (КИБКС)',
                '35121': 'Дирекция Института информационных технологий и управления (ИИТиУ)',
                '35122': 'Высшая инженерная школа (ВИШ)',
                '36011': 'Кафедра «Прикладная математика» (КПрМат)',
                '36012': 'Кафедра «Прикладная математика» (КПрМат)',
                '36021': 'Кафедра «Механика и процессы управления» (КМиПУ)',
                '36022': 'Кафедра «Механика и процессы управления» (КМиПУ)',
                '36031': 'Кафедра «Гидроаэродинамика» (КГАД)',
                '36052': 'Кафедра «Высшая математика» (КВМ)',
                '37011': 'Кафедра «Экономика и менеджмент в машиностроении» (КЭиМвМ)',
                '37021': 'Кафедра «Экономика и менеджмент недвижимости и технологий» (КЭиМНиТ)',
                '37022': 'Кафедра «Экономика и менеджмент недвижимости и технологий» (КЭиМНиТ)',
                '37031': 'Кафедра «Экономика и менеджмент в энергетике и природопользовании» (КЭиМЭиП)',
                '37041': 'Кафедра «Информационные системы в экономике и менеджменте» (КисвЭиМ)',
                '37051': 'Кафедра «Стратегический менеджмент» (КСМ)',
                '37061': 'Кафедра «Финансы и денежное обращение» (КФиДО)',
                '37071': 'Кафедра «Предпринимательство и коммерция» (КПиК)',
                '37081': 'Кафедра «Мировая и региональная экономика» (КМиРЭ)',
                '37082': 'Кафедра «Мировая и региональная экономика» (КМиРЭ)',
                '37111': 'Дирекция Отделения «Международной высшей школы управления» (МВШУ)',
                '37211': 'Кафедра «Управление в социально-экономических системах» (КУвСЭС)',
                '37221': 'Кафедра «Национальная безопасность» (КНБ)',
                '37232': 'Центр менеджмента, инвестиций и производственного контроля (ММИиПК)',
                '38111': 'Кафедра «Инженерная педагогика и психология» (КИПиП)',
                '38121': 'Кафедра «Социально-политические технологии» (КСПТ)',
                '38131': 'Кафедра «Политическая экономия» (КПЭ)',
                '38141': 'Кафедра «Философия» (Кфил)',
                '38143': 'Кафедра отечественной и зарубежной культуры',
                '38144': 'Кафедра социологии и права',
                '38151': 'Кафедра «История» (Кист)',
                '38161': 'Учебно-спортивный комплекс',
                '38191': 'Библиотека кафедр иностранных языков',
                '38211': 'Кафедра «Теория и история государства и права» (КТиИГП)',
                '39021': 'Кафедра «Безопасность жизнедеятельности» (КБЖ)',
                '39031': 'Кафедра «Экстремальные процессы в материалах и взрывоопасность» (КЭПвМиВ)',
                '39051': 'Кафедра «Военно-воздушные силы» (Каф.ВВС)',
                '39061': 'Кафедра Связи (Каф.Св.)',
                '39071': 'Факультет военного обучения (ФВО)',
                '40011': 'Кафедра «Русского языка» (КРЯ)',
                '83502': 'Библиотека Дома ученых в Лесном (ДУ Лесной)',
                '83601': 'Отделение «Центр перспективных исследований»',
                '86201': 'Департамент капитального строительства (ДКС)',
                '88410': 'Департамент материально-технического обеспечения (ДМТО)',
                '91103': 'ОНТИ НИЛ «Политехтест КСМ»',
                '91105': 'УНПЦ «Техническая диагностика и надежность АЭС и ТЭС»',
                '93302': 'Департамент корпоративных общественных связей (ДКОС)',
                'онл': 'Отдел научной литературы',
                'онл_рк': 'Отдел научной литературы: редкая книга',
                'онл_бч': 'Отдел научной литературы: библиотека Чупрова',
                'онл_бв': 'Отдел научной литературы: библиотека Витте',
                'онл_бд': 'Отдел научной литературы: библиотека Дена',
                'онл_бс': 'Отдел научной литературы: библиотека Струве',
                'онл_кит': 'Отдел научной литературы: кабинет истории техники',
                'оул': 'Отдел учебной литературы',
                'оул_1с': 'Отдел учебной литературы 1 сектор',
                'оул_2с': 'Отдел учебной литературы 2 сектор',
                'оул_3с': 'Отдел учебной литературы 3 сектор',
                'обф': 'Обменный фонд',
                'охл': 'Отдел художественной литературы',
                'очз': 'Общий читальный зал',
                'нчз': 'Научный читальный зал',
                'нчз_ди': 'Научный читальный зал Деловая информация',
                'оэрб': 'Отдел электронных ресурсов и библиографии',
                'нчз_нтд': 'Научный читальный зал Нормативно-технической документации',
                'кат': 'Отдел комплектования и каталогизации сектор каталогизации',
                'ком': 'Отдел комплектования и каталогизации сектор комплектования',
                'кб': 'Краеведческая библиография',
                'директор': 'Кабинет директора ФБ',
                'ооп': 'Отдел обслуживания на Полюстровском пр. 14',
                'имоп': 'Институт международных образовательных программ',
                'имоп_зд': 'Зал доступа к электронным ресурсам в ИМОП',
                'кгн': 'Кабинет гуманитарных наук',
                'пс': 'Попечительский совет',
                'упкр': 'Университетский политехнический колледж «Радиополитехникум»',
                'эб': 'Электронная библиотека',
                'киу': 'Колледж информатизации и управления',
                'исф': 'Учебно-методический кабинет курсового и дипломного проектирования инженерно-строительного факультета',
                'п/р': 'Под расписку',
                'сон': 'Сектор обслуживания на Новороссийской ул. 50',
                'упк': 'Университетский политехнический колледж',
                'т.031': 'Кафедра распределенных интеллектуальных систем ИМОП',
                'т.120': 'Кабинет курсового и дипломного проектирования кафедры теории машин и механизмов',
                'т.289': 'Кафедра космических исследований',
                'т.331': 'Кафедра физики твердого тела'
            }
        };

        var alterOrgSiglas = {
            'спбгпу': ['19013582']
        };

        function getOrg(sigla) {
            var cleanedSigla = sigla.toLowerCase();
            var existOrg = titles[cleanedSigla];
            if (existOrg !== undefined) {
                return cleanedSigla;
            }

            for (var org in alterOrgSiglas) {
                var siglas = alterOrgSiglas[org] || [];
                for (var index in siglas) {
                    var alterOrgSigla = siglas[index];
                    if (alterOrgSigla === sigla) {
                        return org;
                    }
                }
            }
        }

        return function (org, branch) {
            var existOrg = getOrg(org);
            return (titles[existOrg] || {})[branch.toLowerCase()] || branch;
        };
    })();


    var API = function (settings) {
        this.getHoldingsInfo = function (params) {
            var defer = $.Deferred();
            $.get(settings.urls.holdings, params).done(function (data) {
                defer.resolve(data);
            }).error(function (error) {
                //console.error('Error while loading holdings info', error);
                defer.reject(error);
            });
            return defer;
        };
        this.makeReservation = function (params) {
            var defer = $.Deferred();
            $.post(settings.urls.makeReservation, params).done(function (data) {
                defer.resolve(data);
            }).error(function (error) {
                //console.error('Error while make reservation', error);
                defer.reject(error);
            });
            return defer;
        };
    };

    var api = null;

    var Modal = React.createClass({
        getDefaultProps: function () {
            return {
                onClose: function () {
                },
                closeButton: true,
                canClose: true
            };
        },
        componentDidMount: function () {
            var $body = $(document.body);
            this.modalBackdrop = $('<div class="modal-backdrop fade in"></div>');
            $body.append(this.modalBackdrop);
            $body.addClass('modal-open');
        },
        componentWillUnmount: function () {
            var $body = $(document.body);
            $body.removeClass('modal-open');
            this.modalBackdrop.remove();
        },
        render: function () {
            return (
                <div style={{display: 'block'}}
                     className="modal fade in"
                     aria-labelledby="myModalLabel"
                     aria-hidden="true">
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                {
                                    this.props.closeButton ?
                                        <button onClick={this.props.onClose} type="button" className="close"
                                                data-dismiss="modal"
                                                aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button> : null
                                }
                                <h4 className="modal-title" id="myModalLabel">{this.props.title || '.'}</h4>
                            </div>
                            <div className="modal-body">{this.props.children}</div>
                            <div className="modal-footer">
                                <button disabled={!this.props.canClose}
                                        onClick={this.props.onClose}
                                        type="button"
                                        className="btn btn-default">
                                    Закрыть
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    });

    var orderProcessStatuses = {
        notInited: 'notInited',
        inited: 'inited',
        complete: 'complete',
        error: 'error'
    };

    var HoldingsTable = React.createClass({
        getDefaultProps: function () {
            return {
                holdings: [],
                holdingGroups: {},
                isAuthUser: false
            };
        },
        getInitialState: function () {
            return {
                showOrder: false,
                orderProcessStatus: orderProcessStatuses.notInited,
                orderProcessError: ''
            };
        },
        orderClickHandle: function (params) {
            if (!this.props.isAuthUser) {
                alert('Для бронирования необходимо войти в систему под учетной записью читателя');
                return;
            }

            if (!confirm('Вы уверены, что хотите забронировать экземляр?')) {
                return;
            }
            var self = this;
            this.setState({
                showOrder: true,
                orderProcessStatus: orderProcessStatuses.inited
            });
            //console.log('make order', {
            //  recordId: this.props.recordId,
            //  org: params.org,
            //  branch: params.branch
            //});

            api.makeReservation({
                'record_id': this.props.recordId,
                'org': params.org,
                'branch': params.branch
            }).done(function (data) {
                self.setState({
                    orderProcessStatus: orderProcessStatuses.complete
                });
            }).fail(function (error) {
                var errorMessage = 'В процессе заказа возникла ошибка. Попробуйте позднее.';
                if (error.status === 500) {
                    errorMessage = 'При осуществлении бронирования возникла ошибка. Пожалуйста, попробуйте позже.';
                } else if (error.status === 403) {
                    errorMessage = 'У Вас нет прав сделать бронирование.';
                } else if (error.status === 401) {
                    errorMessage = 'Для бронирования необходимо войти в систему';
                } else if (error.status === 400) {
                    errorMessage = (error.responseJSON || {}).message || 'При осуществлении бронирования возникла ошибка. Пожалуйста, попробуйте позже.';
                }
                self.setState({
                    orderProcessStatus: orderProcessStatuses.error,
                    orderProcessError: errorMessage
                });
            });
        },
        canCloseOrderWindow: function () {
            var canCloseStatuses = [
                orderProcessStatuses.error,
                orderProcessStatuses.complete
            ];
            if (canCloseStatuses.indexOf(this.state.orderProcessStatus) < 0) {
                return false;
            }
            return true;
        },
        closeOrderHandle: function () {
            if (!this.canCloseOrderWindow()) {
                return;
            }
            this.setState({
                showOrder: false
            });
        },
        getOrderModal: function () {
            if (!this.state.showOrder) {
                return null;
            }
            var modalBody = null;
            if (this.state.orderProcessStatus === orderProcessStatuses.inited) {
                modalBody = (
                    <p><i className="fa fa-cog fa-spin"></i> Осуществление заказа. Пожалуйста, подождите...</p>
                );
            } else if (this.state.orderProcessStatus === orderProcessStatuses.error) {
                modalBody = (
                    <p className='alert alert-danger'><i className="fa fa-exclamation-triangle"></i>
                        { ' ' + this.state.orderProcessError}
                    </p>
                );
            } else if (this.state.orderProcessStatus === orderProcessStatuses.complete) {
                modalBody = (
                    <p className='alert alert-success'><i className="fa fa-check"></i> Заказ успешно принят. <br/> За
                        ходом
                        исполнения следите в личном кабинете в разделе "Мои заказы".</p>
                );
            }
            return (
                <Modal onClose={this.closeOrderHandle}
                       title='Бронирование экземпляра'
                       canClose={this.canCloseOrderWindow()}>
                    {modalBody}
                </Modal>
            );
        },
        render: function () {
            var rows = [], forOrderRows = [], withoutOrderRows = [], groupKey, group, branch, stats;
            for (groupKey in this.props.holdingGroups) {
                rows.push(
                    <tr>
                        <td className="holdings__org" colSpan="6">{groupKey}</td>
                    </tr>
                );
                group = this.props.holdingGroups[groupKey];
                for (branch in group) {
                    if (disabledBranches.indexOf((groupKey + '/' + branch).toLowerCase()) > -1) {
                        continue;
                    }
                    stats = group[branch].stats;

                    var orderText = '';

                    if (stats.restrictionList.length) {
                        orderText = <span>{stats.restrictionList.join('; ')}</span>;
                    } else if (stats.total && !stats.availableNow) {
                        orderText = 'Нет свободных экземпляров'
                    }

                    var shelvingData = stats.shelvingData.join('; ');
                    var callNumber = stats.callNumber.join('; ');
                    var branchTitle = getBranchTitle(groupKey, branch);
                    var candidateRows = stats.forOrder ? forOrderRows : withoutOrderRows;
                    var orderButtonTitle = this.props.isAuthUser ? 'Забронировать в: ' + branchTitle :
                        'Для бронирования необходимо войти под учетной записью читателя';

                    var orderButton = stats.forOrder ?
                        <div title={orderButtonTitle}>
                            <button className="btn btn-success"
                                    onClick={this.orderClickHandle.bind(this, {org: groupKey, branch: branch})}
                                    title={orderButtonTitle}>
                                Забронировать
                            </button>
                        </div>
                        : orderText;

                    candidateRows.push(
                        <tr>
                            <td>{branchTitle}</td>
                            <td className="holdings__total"> {stats.total}</td>
                            <td className="holdings__free">{stats.availableNow}</td>
                            <td title={shelvingData}>{shelvingData}</td>
                            <td title={callNumber}>{callNumber}</td>
                            <td>{orderButton}</td>
                        </tr>
                    );
                }
            }
            if (!forOrderRows.length && !withoutOrderRows.length) {
                return null;
            }
            return (
                <div>
                    <table className="table table-bordered table-hover holdings-table">
                        <tr className="holdings__headers">
                            <th className="holdings-header__place">Местонахождение</th>
                            <th className="holdings-header__total">Всего</th>
                            <th className="holdings-header__free">Свободно</th>
                            <th className="holdings-header__shivlet">Полочный индекс</th>
                            <th className="holdings-header__shivlet">Инвентарный номер</th>
                            <th className="holdings-header__actions"></th>
                        </tr>
                        {rows}
                        {forOrderRows}
                        {withoutOrderRows}
                    </table>
                    {this.getOrderModal()}
                </div>
            );
        }
    });

    var HoldingsApp = React.createClass({
        getDefaultProps: function () {
            return {
                canOrderBranches: [],
                isAuthUser: false,
                recordId: ''
            };
        },
        componentDidMount: function () {
            var self = this;
            if (this.props.recordId) {

            }
            api.getHoldingsInfo({
                recordId: this.props.recordId
            }).done(function (data) {
                var holdings = [], holdingGroups = {};

                var record = Ruslan.Humanize.SRU.extractRecordWithIdentifier(
                    Ruslan.Humanize.SRU.getRecords(data), self.props.recordId
                );

                if (record) {
                    holdings = Ruslan.Humanize.SRU.getRecordHoldings(record);
                    holdingGroups = Ruslan.Humanize.Order.buildHoldingsGroups(holdings, self.props.canOrderBranches);
                }

                self.setState({
                    loaded: true,
                    holdings: holdings,
                    holdingGroups: holdingGroups
                });
            }).fail(function (error) {
                //console.error('Error while holdings load', error);
                self.setState({
                    error: 'При загрузке сведений об экземплярах возникла ошибка'
                });
            });
        },
        getInitialState: function () {
            return {
                loaded: false,
                error: '',
                canBeOrdered: false,
                holdings: [],
                holdingGroups: {}
            };
        },
        renderError: function () {
            return <div className="holdings__error">{ this.state.error }</div>;
        },
        renderLoader: function () {
            return (
                <div className="holdings__loader">
                    <i className="fa fa-cog fa-spin"></i> <span>Загрузка информации об экземплярах...</span>
                </div>
            );
        },
        renderNoHoldings: function () {
            return (
                <div className="holdings__no-holdings">
                    Информация об экземплярах отсутствует.
                </div>
            )
        },
        renderHoldingsTable: function () {
            return (
                <HoldingsTable isAuthUser={this.props.isAuthUser}
                               recordId={this.props.recordId}
                               holdings={this.state.holdings}
                               holdingGroups={this.state.holdingGroups}/>
            );
        },
        render: function () {
            var rendered = null;
            if (!this.props.recordId) {
                rendered = this.renderNoHoldings();
            } else if (this.state.error) {
                rendered = this.renderError();
            } else if (!this.state.loaded) {
                rendered = this.renderLoader();
            } else if (this.state.holdings.length > 0) {
                rendered = this.renderHoldingsTable();
            } else {
                rendered = this.renderNoHoldings();
            }

            return (
                <div className="holdings">{rendered}</div>
            );
        }
    });

    /**
     * @param settings
     *  element - app element
     *  recordId - record identifier
     *  urls:
     *    holdings - must return holdings data
     * @constructor
     */
    Ruslan.HoldingsInfo = function (settings) {

        api = new API({
            urls: settings.urls
        });

        React.render(
            <HoldingsApp canOrderBranches={settings.canOrderBranches}
                         isAuthUser={settings.isAuthUser}
                         recordId={settings.recordId}/>,
            settings.element
        );
    };

})(window.React, window.$);
