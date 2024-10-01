$(function(){


    $('.banner__section-slider').slick({
        dots:true,
        prevArrow: '<button class="banner__section-slider-btn banner__section-slider-btnprev"><img src="images/arrow-left.svg" alt=""></button>',
        nextArrow: '<button class="banner__section-slider-btn banner__section-slider-btnnext"><img src="images/arrow-right.svg" alt=""></button>',
    });

    $('.tab').on('click', function(e){
        e.preventDefault();
        $($(this).siblings()).removeClass('tab--active');
        $($(this).parent().siblings().find('div')).removeClass('tabs__content--active');

        $(this).addClass('tab--active');
        $($(this).attr('href')).addClass('tabs__content--active');

    });

    $('.product__item-favorite').on('click', function(){
        $(this).toggleClass('product__item-favorite--active')
    })
    $('.product__slider').slick({
        slidesToShow: 4,
        slidesToScroll:1,
        prevArrow: '<button class="product__slider-slider-btn product__slider-slider-btnprev"><img src="images/arrow-black-left.svg" alt=""></button>',
        nextArrow: '<button class="product__slider-slider-btn product__slider-slider-btnnext"><img src="images/arrow-black-right.svg" alt=""></button>',
    });

    $('.filter-stayle').styler();

    $('.filter__item-drop, .filtr__extra').on('click', function(){
        $(this).toggleClass('filter__item-drop--active');
        $(this).next().slideToggle('200');
    });
    $(".js-range-slider").ionRangeSlider({
        type:"double",
        min: 100000,
        max: 500000,
    });
    $('.catalog__filtor-btngrid').on('click', function () {
        $(this).addClass('catalog__filtor-button-active');
        $('.catalog__filtor-btnline').removeClass('catalog__filtor-button-active');
        $('.product__item-wrapper').removeClass('product__item-wrapper-list');
    });
    $('.catalog__filtor-btnline').on('click', function () {
        $(this).addClass('catalog__filtor-button-active');
        $('.catalog__filtor-btngrid').removeClass('catalog__filtor-button-active');
        $('.product__item-wrapper').addClass('product__item-wrapper-list');
    });

    $(".rateYo").rateYo({
        ratedFill: "#1C62CD",
        spacing   : "7px",
        normalFill: "#C4C4C4"
      });
});