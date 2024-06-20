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
    // $('.quantity button').on('click', function () {
    //     var button = $(this);
    //     var oldValue = button.parent().parent().find('input').val();
    //     if (button.hasClass('btn-plus')) {
    //         var newVal = parseFloat(oldValue) + 1;
    //     } else {
    //         if (oldValue > 0) {
    //             var newVal = parseFloat(oldValue) - 1;
    //         } else {
    //             newVal = 0;
    //         }
    //     }
    //     button.parent().parent().find('input').val(newVal);
    // });
    
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
const formSearch = document.getElementById('formSearch')
const inputSearch = document.getElementById('inputSearch')
const searchInput = document.getElementById('searchInput')
const rowData = document.getElementById('rowData')
const navigation = document.getElementById('navigation')
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
            // console.log(res);
            const data = res.data
            if (Array.isArray(data)) {
                results.innerHTML = ``
                data.forEach(product=>{
                    results.innerHTML +=`
                        <a href="${url}products/category/${product.subcategory}/${product.slug}" class="text-decoration-none">
                            <div class="row mt-2 mb-2">
                                <div class="col-2">
                                    <img src="${product.image}" class="game-image" />
                                </div>
                                <div class="col-10 ">
                                    <h5>${product.name}</h5>
                                    <p class="text-muted">${product.price}$</p>
                                </div>
                            </div>
                        </a>
                    `
                })
            }else{
                if (searchInput.value.length > 0) {
                    results.innerHTML = `<b>${data}</b>`
                }else{
                    results.classList.add('not-visible')
                }
            }
        },
        error:  (error)=>{
            console.log(error);
        }
    });
}


searchInput.addEventListener('keyup' , (e)=>{
    // console.log(e.target.value);

    if (results.classList.contains('not-visible')) {
        results.classList.remove('not-visible')
    }
    sendData(e.target.value)
})

const dataSend = (product)=>{
    $.ajax({
        type: "POST",
        url: 'results/',
        data: {
            'csrfmiddlewaretoken':csrf,
            'product':product
        },
        success:  (res)=> {
            console.log(res);
            const data = res.data
            if (Array.isArray(data)) {
                rowData.innerHTML = ``
                data.forEach(product=>{
                    rowData.innerHTML +=`
                        <div class="col-lg-4 col-md-6 col-sm-12 pb-1">
                        <div class="card product-item border-0 mb-4">
                            <div class="card-header product-img position-relative overflow-hidden bg-transparent border p-0">
                                <img class="img-fluid w-100" src="${product.image}" alt="">
                            </div>
                            <div class="card-body border-left border-right text-center p-0 pt-4 pb-3">
                                <h6 class="text-truncate mb-3">${product.name}</h6>
                                <div class="d-flex justify-content-center">
                                    <h6>$${product.price}</h6>
                                </div>
                                <div class="rating-star">
                                    <span>
                                        ${product.avgRate}/5<i class="fa fa-star ms-2"></i>
                                    </span>(${product.rate} reviews)
                                </div>
                            </div>
                            <div class="card-footer d-flex justify-content-between bg-light border">
                                <a href="${url}category/${product.subcategory}/${product.slug}" class="btn btn-sm text-dark p-0"><i class="fas fa-eye text-primary mr-1"></i>View Detail</a>
                                <a href="" class="btn btn-sm text-dark p-0"><i class="fas fa-shopping-cart text-primary mr-1"></i>Add To Cart</a>
                            </div>
                        </div>
                    </div>
                    `
                })
            }else{
                if (inputSearch.value.length > 0) {
                    rowData.innerHTML = `<b >${data}</b>`
                    
                }else{
                    rowData.innerHTML = `
                        <div class="col-12 my-5 mx-5 text-center">
                        <h2>Nothing Found , PLS Try Again</h2>
                    </div>`
                    
                    
                }
            }
        },
        error:  (error)=>{
            console.log(error);
        }
    });
}

inputSearch.addEventListener('keyup' , (e)=>{
    dataSend(e.target.value)
    navigation.classList.add('d-none')
})