(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });
    
})(jQuery);

let counterValue = 1;

    function increment() {
      counterValue++;
      document.getElementById('counter').value = counterValue;
    }

    function decrement() {
      if (counterValue > 1) {
        counterValue--;
        document.getElementById('counter').value = counterValue;
      }
    }


setTimeout(function(){
    $('#message').fadeOut('slow')
},4000)

$("#newsletter_form").submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function (data) {
                document.getElementById('main_form_div').style.display = "none";
                document.getElementById('success_div').style.display = "block";
            }
        })
    })

const searchForm = document.getElementById('searchForm')
const searchInput = document.getElementById('searchInput')
const results = document.getElementById('results')
const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
const url = window.location.href

const sendData = (product)=>{
    $.ajax({
        type: "POST",
        url: 'products/results/',
        data: {
            'csrfmiddlewaretoken':csrf,
            'product':product
        },
        success:  (res)=> {
            console.log(res);
        },
        error:  (error)=>{
            console.log(error);
        }
    });
}


searchInput.addEventListener('keyup' , (e)=>{
    console.log(e.target.value);

    if (results.classList.contains('not-visible')) {
        results.classList.remove('not-visible')
    }
    sendData(e.target.value)
})