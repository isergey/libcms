$(document).ready(function () {

    // Remove style attr content manager
    $(".content *").removeAttr("style border cellspacing cellpadding bgcolor width align colspan");

    $(".search-input__select, .search-input__input").focus(function () {
        $(this).parent().addClass("search-input_focus");
    }).blur(function () {
        $(this).parent().removeClass("search-input_focus");
    })

    let newArrivalSwiper = new Swiper('.swiper-container-news-arrival', {
        slidesPerView: 4,
        spaceBetween: 25,
        loop: true,
        mousewheel: false,
        autoplay: true,
        delay: 5000,
        pagination: {
            el: '.swiper-pagination-news-arrival',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next-news-arrival',
            prevEl: '.swiper-button-prev-news-arrival',
        },
        breakpoints: {
            1300: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 1,
            },
        }
    });

    let eventSwiper = new Swiper('.swiper-container-event', {
        spaceBetween: 0,
        slidesPerView: 1,
        mousewheel: false,
        loop: true,
        autoplay: true,
        delay: 10000,
        pagination: {
            el: '.swiper-pagination-event',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next-event',
            prevEl: '.swiper-button-prev-event',
        },
    });

    let galleryThumbs = new Swiper('.gallery-thumbs', {
        spaceBetween: 10,
        slidesPerView: 4,
        freeMode: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true,
    });
    let galleryTop = new Swiper('.gallery-top', {
        spaceBetween: 10,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        thumbs: {
            swiper: galleryThumbs
        }
    });

    // Nav btn click
    $('.header__nav-btn').click(function () {
        $(this).toggleClass('toggled');
        $('body, .nav-wrap, .nav-mask').toggleClass('toggled');
    });

    // Nav mask click
    $('.nav-mask').click(function () {
        $(this).toggleClass('toggled');
        $('body, .nav-wrap, .header__nav-btn').toggleClass('toggled');
    });

    // Library detail image click
    $('.lib-detail__img, .lib-detail__img-wrap-icon').click(function () {
        $('.lib-detail__img').toggleClass('toggled');
    });

    // Library detail menu btn click
    $('#libraryMenuBtn').click(function () {
        $(this).toggleClass('toggled');
        $('.lib-nav-wrap').toggleClass('toggled');

        if ($('#libraryContactBtn,.lib-contact').hasClass('toggled')) {
            $('#libraryContactBtn,.lib-contact').removeClass('toggled');
        }
    });

    // Library detail menu btn click
    $('#libraryContactBtn').click(function () {
        $(this).toggleClass('toggled');
        $('.lib-contact').toggleClass('toggled');

        if ($('#libraryMenuBtn,.lib-nav-wrap').hasClass('toggled')) {
            $('#libraryMenuBtn,.lib-nav-wrap').removeClass('toggled');
        }
    });

    // Search page facet btn click
    $('#facetBtn').click(function () {
        $(this).toggleClass('toggled');
        $('body, .search-facet, .search-mask').toggleClass('toggled');
    });

    // Search page search mask click
    $('.search-mask').click(function () {
        $(this).toggleClass('toggled');
        $('body, .search-facet, #facetBtn').toggleClass('toggled');
    });

    $('#marcCardBtn').click(function () {
        $(this).toggleClass('toggled');
        $('.marc-card').toggleClass('toggled');
    });

    $('#recordNavBtn').click(function () {
        $(this).toggleClass('toggled');
        $('body, .record-booking, .record-mask').toggleClass('toggled');
    });

    $('.record-mask').click(function () {
        $(this).toggleClass('toggled');
        $('body, .record-booking, #recordNavBtn').toggleClass('toggled');
    });

    // Ask librarian
    $('#askNavBtn').click(function () {
        $(this).toggleClass('toggled');
        $('body, .ask-facet, .ask-mask').toggleClass('toggled');
    });

    $('.ask-mask').click(function () {
        $(this).toggleClass('toggled');
        $('body, .ask-facet, #askNavBtn').toggleClass('toggled');
    });

});

MicroModal.init({
    openTrigger: 'data-custom-open',
    closeTrigger: 'data-micromodal-close',
    disableScroll: true,
    disableFocus: true,
    // awaitCloseAnimation: false,
});

// Tabs
(function tabComponentIIFE(window) {
    'use strict';

    var TabComponent = function tabComponentConstructor(selector) {
        var element = document.querySelector(selector);
        if (!element || !element.nodeType) {
            return;
            throw new Error('The DOM element was not found when creating the tab component');
        }
        return TabComponent.init(element);
    };

    TabComponent.prototype = {
        handleTabInteraction: function handleTabInteraction(index, direction) {
            var currentIndex = this.currentIndex;
            var newIndex = index;

            if (direction) {
                if (direction === 37) {
                    newIndex = index - 1;
                } else {
                    newIndex = index + 1;
                }
            }

            if (newIndex < 0) {
                newIndex = this.tabs.length - 1;
            } else if (newIndex === this.tabs.length) {
                newIndex = 0;
            }

            // update tabs
            this.tabs[currentIndex].setAttribute('tabindex', '-1');
            this.tabs[currentIndex].removeAttribute('aria-selected');
            this.tabItems[currentIndex].removeAttribute('data-tab-active');

            this.tabs[newIndex].setAttribute('aria-selected', 'true');
            this.tabItems[newIndex].setAttribute('data-tab-active', '');
            this.tabs[newIndex].removeAttribute('tabindex');
            this.tabs[newIndex].focus();

            // update tab panels
            this.tabPanels[currentIndex].setAttribute('hidden', '');
            this.tabPanels[newIndex].removeAttribute('hidden');

            this.currentIndex = newIndex;

            return this;
        },

        handleTabpanelFocus: function handleTabPanelFocus(index) {
            this.tabPanels[index].focus();

            return this;
        }
    };

    // Intialize Tab Component
    TabComponent.init = function tabComponentInit(element) {
        var _this = this;

        this.tabList = element.querySelector('.tab-list');
        this.tabItems = [].slice.call(this.tabList.querySelectorAll('.tab-item'));
        this.tabs = [].slice.call(this.tabList.querySelectorAll('.tab-link'));
        this.tabPanels = [].slice.call(element.querySelectorAll('.tab-panel'));
        this.currentIndex = 0;
        this.tabList.setAttribute('role', 'tablist');

        this.tabItems.forEach(function (item, index) {
            item.setAttribute('role', 'presentation');

            if (index === 0) {
                item.setAttribute('data-tab-active', '');
            }
        });

        this.tabs.forEach(function (item, index) {
            item.setAttribute('role', 'tab');
            item.setAttribute('id', 'tab' + index);

            if (index > 0) {
                item.setAttribute('tabindex', '-1');
            } else {
                item.setAttribute('aria-selected', 'true');
            }
        });

        this.tabPanels.forEach(function (item, index) {
            item.setAttribute('role', 'tabpanel');
            item.setAttribute('aria-labelledby', 'tab' + index);
            item.setAttribute('tabindex', '-1');

            if (index > 0) {
                item.setAttribute('hidden', '');
            }
        });

        this.tabList.addEventListener('click', function (event) {
            event.preventDefault();
            TabComponent.prototype.handleTabInteraction.call(_this, _this.tabs.indexOf(event.target));
        });

        this.tabList.addEventListener('keydown', function (event) {
            var index = _this.tabs.indexOf(event.target);

            // Left and right arrows
            if (event.which === 37 || event.which === 39) {
                event.preventDefault();
                TabComponent.prototype.handleTabInteraction.call(_this, index, event.which);
            }

            // Down arrow
            if (event.which === 40) {
                event.preventDefault();
                TabComponent.prototype.handleTabpanelFocus.call(_this, index);
            }
        });

        return this;
    };

    window.tabs = TabComponent;
})(window);


var tabComponent = tabs('[data-tab-component]');
