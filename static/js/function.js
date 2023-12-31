//############## Increment and Increment Quantity ##############//
const $quantity = $("#product-quantity");

// Get plus/minus buttons
const $plusBtn = $("#button-plus");
const $minusBtn = $("#button-minus");

// Increment handler
$plusBtn.click(function () {
    let currVal = parseInt($quantity.val());
    if (currVal < 10) {
        $quantity.val(currVal + 1);
    }
});

// Decrement handler
$minusBtn.click(function () {
    let currVal = parseInt($quantity.val());
    if (currVal > 1) {
        $quantity.val(currVal - 1);
    }
});


//############## add to cart functionality ##############//
$(".add-to-cart-btn").on("click", function () {

    let this_val = $(this)
    let index_val = this_val.attr('data-index')
    console.log("index_val: ", index_val)
    let product_quantity = $(".product-quantity-" + index_val).val()
    let product_name = $(".product-name-" + index_val).val()
    let product_id = $(".product-id-" + index_val).val()
    let product_image = $(".product-image-" + index_val).val()
    let product_price = $(".product-price-" + index_val).text()


    console.log("product_quantity: ", product_quantity)
    console.log("product_name: ", product_name)
    console.log("product_id: ", product_id)
    console.log("product_image: ", product_image)
    console.log("product_price: ", product_price)
    console.log("Current Element: ", this_val)

    $.ajax({
        url: '/store/add-to-cart',
        data: {
            'id': product_id,
            'name': product_name,
            'price': product_price,
            'qty': product_quantity,
            'img': product_image,
        },
        dataType: 'json',
        beforeSend: function () {
            console.log('Adding product to cart..');
        },
        success: function (response) {
            this_val.removeClass("btn-primary").addClass("btn-success").text("Added to Cart!").prop("disabled", true);
            console.log('product added to cart')
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})


//############## Update Cart item Quantity ##############//
function updateCartItemQuantity(indexVal, currentVal) {
    $.ajax({
        url: '/store/update-cart-item-qty',
        data: {
            'id': indexVal,
            'qty': currentVal,
        },
        dataType: 'json',
        success: function (response) {
            console.log('Updated Cart item quantity');
        },
        error: function (error) {
            console.error('Error updating cart item quantity:', error);
        }
    });
}
$(".button-plus").on("click", function () {
    let thisButton = $(this);
    let indexVal = thisButton.attr('itemid');
    let productQuantity = $(".product-quantity-" + indexVal);
    let productQuantityVal = productQuantity.val()
    let currentVal = parseInt(productQuantityVal);

    if (!isNaN(currentVal) && currentVal < 10) {
        currentVal++;
    }
    productQuantity.val(currentVal);
    updateCartItemQuantity(indexVal, currentVal)
});

$(".button-minus").on("click", function () {
    let thisButton = $(this);
    let indexVal = thisButton.attr('itemid');
    let productQuantityInput = $(".product-quantity-" + indexVal);

    let currentVal = parseInt(productQuantityInput.val());

    if (!isNaN(currentVal) && currentVal > 1) {
        currentVal--;
    }
    productQuantityInput.val(currentVal);
    updateCartItemQuantity(indexVal, currentVal)
});

