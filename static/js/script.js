function call_api(method, url, headers, data) {
    var xhttp = new XMLHttpRequest();
    xhttp.open(method, url, false);
    var result = $.parseJSON(headers);
    $.each(result, function (k, v) {
        xhttp.setRequestHeader(k, v);
    });
    xhttp.send(data);
    return JSON.parse(xhttp.responseText);
}

function add_to_cart(id, csrf, category) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/cart/add/";
    var inpObj = document.getElementById(id + '_quantity');
    if (inpObj.checkValidity() === false) {
        alert('Please enter quantity');
        inpObj.focus();
        return;
    } else {
        var quantity = inpObj.value
    }
    // var quantity = document.getElementById(id + '_quantity').value;
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{' +
        '"id": "' + id + '",' +
        '"quantity": "' + quantity + '",' +
        '"category": "' + category + '"' +
        '}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    location.reload(true);
}

function add_to_gcart(id, csrf, category) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/gcart/add/";
    var inpObj = document.getElementById(id + '_quantity');
    if (inpObj.checkValidity() === false) {
        alert('Please enter quantity');
        inpObj.focus();
        return;
    } else {
        var quantity = inpObj.value
    }
    // var quantity = document.getElementById(id + '_quantity').value;
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{' +
        '"id": "' + id + '",' +
        '"quantity": "' + quantity + '",' +
        '"category": "' + category + '"' +
        '}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    location.reload(true);
}

function clear_cart(csrf) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/cart/clear/";
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    location.reload(true);
}

function clear_gcart(csrf) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/gcart/clear/";
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    location.reload(true);
}

function remove_from_cart(id, csrf) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/cart/remove/";
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{' +
        '"id": "' + id + '"' +
        '}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    location.reload(true);
}

function remove_from_gcart(id, csrf) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/gcart/remove/";
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{' +
        '"id": "' + id + '"' +
        '}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    location.reload(true);
}

function paystack(amount, csrf) {
    var date = new Date();
    var del = document.getElementById('del_charge').innerHTML;
    var ref = "f4all-" + date.getFullYear() + "" + (date.getMonth() + 1) + "" + date.getDate() + "-" + date.getHours() + "" + date.getMinutes() + "" + date.getSeconds();
    var email = document.getElementById('email').value;
    // var amount = document.getElementById(id + '_pay_amount').value;
    // if (email === ''){
    //     email = document.getElementById(id + '_pay_email').value;
    // }
    // var inpObj = document.getElementById('name');
    // if (inpObj.checkValidity() === false) {
    //     alert('Please enter full name');
    //     inpObj.focus();
    //     return;
    // } else {
    //     var name = inpObj.value
    // }
    //
    // inpObj = document.getElementById('email');
    // if (inpObj.checkValidity() === false) {
    //     alert('Please enter a valid email');
    //     inpObj.focus();
    //     return;
    // } else {
    //     var email = inpObj.value
    // }
    //
    // inpObj = document.getElementById('number');
    // if (inpObj.checkValidity() === false || inpObj.value.length < 13) {
    //     alert('Please a valid number');
    //     inpObj.focus();
    //     return;
    // } else {
    //     var number = inpObj.value
    // }
    //
    // inpObj = document.getElementById('location');
    // if (inpObj.checkValidity() === false || inpObj.value === '- Select Location -') {
    //     alert('Please select a location');
    //     inpObj.focus();
    //     return;
    // } else {
    //     var location = inpObj.value
    // }
    //
    // inpObj = document.getElementById('address');
    // if (inpObj.checkValidity() === false) {
    //     alert('Please enter an address');
    //     inpObj.focus();
    //     return;
    // } else {
    //     var address = inpObj.value
    // }
    //
    // var amount = document.getElementById('sum_total2').value;
    // var email = document.getElementById('email').value;
    var handler = PaystackPop.setup({
        key: 'pk_test_e3fc790b33042081a09723fb112c5c4fbe041baa',
        email: email,
        amount: (parseInt(amount) + parseInt(del)) * 100,
        ref: ref,
        // metadata: {
        //     custom_fields: [
        //         {
        //             display_name: "Mobile Number",
        //             variable_name: "mobile_number",
        //             value: number,
        //         },
        //         {
        //             display_name: "Full Name",
        //             variable_name: "full_name",
        //             value: name,
        //         }
        //     ]
        // },
        callback: function (response) {
            // var method = "POST";
            // var url = window.location.href;
            // var arr = url.split("/");
            // var result = arr[0] + "//" + arr[2];
            // url = result + "/checkout/";
            // var headers = '{' +
            //     '"X-CSRFToken":"' + csrf + '",' +
            //     '"Content-Type":"application/json"}';
            // var data =
            //     '{' +
            //     '}';
            // call_api(method, url, headers, data);
            document.getElementById("pay_mode").value = "online";
            document.getElementById("checkout_form").submit();
        },
        onClose: function () {

        }
    });
    handler.openIframe();
}

function confirm_order(csrf, id, value) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/show_order/";
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{' +
        '"id": "' + id + '",' +
        '"confirm": "' + value + '"' +
        '}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    // location.reload(true);
}

function paymode(csrf, pay_mode) {
    var method = "POST";
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    url = result + "/checkout/";
    var headers = '{' +
        '"X-CSRFToken":"' + csrf + '",' +
        '"Content-Type":"application/json"}';
    var data =
        '{' +
        '"pay": "' + pay_mode + '",' +
        '}';
    var response = call_api(method, url, headers, data);
    console.log(response);
    if (response['response'] = !'Success') {
        alert(response['details']);
    }
    // location.reload(true);
}