import json
import traceback
import re
from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from Gas.models import *


def index(request):
    assert isinstance(request, HttpRequest)
    if request.method == "GET":
        sql = Gas.objects.filter(Accessories='gas_refill')
        if 'cart' not in request.session.keys():
            request.session['cart'] = {}
        content = {'sql1': sql, }
        templates = 'index.html'
        return render(request, templates, content)


def contact(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        con = Contact()
        context = {'sucessmessage': "Thanks for contacting us hope to get back to you soon", }
        con.subject = request.POST.get('subject')
        con.Email = request.POST.get('Email')
        con.message = request.POST.get('message')
        con.save()
        # subject = [con.subject, con.Email]
        # message = con.message
        # from_mail = settings.EMAIL_HOST_USER
        # to_list = [from_mail]
        # send_mail(subject=subject, message=message, from_email=con.Email, recipient_list=to_list, fail_silently=False)
        return redirect(request.META.get('HTTP_REFERER'), context)


def profile(request):
    if request.method == 'GET':
        context = locals()
        templates = 'profile.html'
        return render(request, templates, context)
        # elif request.method == 'POST':
        #     edit = Register.objects.get(id=request.session['userid'])
        #     edit.Fullname = request.POST.get('Fullname')
        #     edit.Email = request.POST.get('Email')
        #     edit.Phone = request.POST.get('Phone')
        #     edit.Username = request.POST.get('Username')
        #     edit.save()
        #     sql1 = Register.objects.get(id=request.session['userid'])
        #     context = {'prof': sql1, 'msg': "Profile updated successfully", }
        #     templates = 'profile.html'
        #     return render(request, templates, context)


def logout(request):
    if request.method == 'GET':
        request.session.clear()
        return redirect('/')


def cart(request, url_name):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        if url_name == 'clear':
            del request.session['cart']
            # del request.session['total']
            response = {"response": "Success",
                        "details": "Cart cleared"}
            return JsonResponse(response, safe=False)
        elif url_name == 'remove':
            form = json.loads(request.body.decode(encoding='UTF-8'))
            itemid = form['id']
            cart_items = dict(request.session['cart'])
            del cart_items[itemid]
            total = 0
            for order_detail in cart_items.keys():
                total += int(cart_items[order_detail]['Total'])
            request.session['total'] = total
            request.session['cart'] = cart_items
            response = {"response": "Success",
                        "details": "Item Removed"}
            return JsonResponse(response, safe=False)
        elif url_name == 'add':
            form = json.loads(request.body.decode(encoding='UTF-8'))
            if form:
                category = form['category']
                quantity = int(form['quantity'])
                try:
                    item = Gas.objects.get(id=form['id'])
                except:
                    item = None

                if item:
                    if 'cart' not in request.session.keys():
                        request.session['cart'] = {}
                    cart_items = dict(request.session['cart'])
                    data = {
                        str(item.id): {
                            'Name': item.product_name,
                            'Quantity': quantity,
                            'Total': item.price * quantity
                        }
                    }

                    cart_items.update(data)
                    total = 0
                    for order_detail in cart_items.keys():
                        total += int(cart_items[order_detail]['Total'])
                    request.session['total'] = total
                    request.session['cart'] = cart_items
                    response = {"response": "Success",
                                "details": "Added to cart"}
                    return JsonResponse(response, safe=False)
                else:
                    response = {"response": "Error",
                                "details": "Item not found"}
                    return JsonResponse(response, safe=False)
            else:
                response = {"response": "Error",
                            "details": "No Form"}
                return JsonResponse(response, safe=False)


def checkout(request):
    assert isinstance(request, HttpRequest)
    if request.method == "GET":
        request.session['grandtotal'] = int(request.session['total'])
        template = 'checkout.html'
        locs = Location.objects.all()
        return render(request, template, {"locs": locs})
    elif request.method == "POST":
        order = Order()
        order.payment_mode = request.POST.get('pay_mode')
        order.Name = request.POST.get('Name')
        order.Email = request.POST.get('Email')
        order.Phone = request.POST.get('Phone')
        order.address = request.POST.get('address')
        raw_loc = request.POST.get('loc')
        loc_id = raw_loc.split(":")[0]
        location = Location.objects.get(id=loc_id)
        order.loc = location.name
        order.del_charge = location.charge
        order.total = int(request.session['grandtotal'])
        order.sumtotal = int(request.session['grandtotal']) + location.charge
        order.save()
        cart_items = request.session['cart']
        for key, value in cart_items.items():
            gas = Gas.objects.get(id=key)
            order_detail = OrderingDetails()
            order_detail.order = order
            order_detail.item = gas
            order_detail.qty = int(value['Quantity'])
            order_detail.total = int(value['Total'])
            order_detail.save()
        del request.session['cart']
        del request.session['total']
        del request.session['grandtotal']
        messages.success(request, 'Order Successfully Submitted,Kindly wait for our call.Thanks')
        return redirect('/')


def adminpage(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        if 'username' in request.session.keys():
            prod = Gas.objects.all().count()
            comm = Contact.objects.all().count()
            ord = Order.objects.all().count()
            context = {'stats': prod, 'coment': comm, 'orde': ord}
            template = 'adminpage.html'
            return render(request, template, context)
        else:
            return redirect('/Adminlog/')


def show_order(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        holder = []
        for order in Order.objects.all():
            details = OrderingDetails.objects.filter(order=order)
            holder.append((order, details))
        context = {'orders': holder}
        template = 'show_order.html'
        return render(request, template, context)
    elif request.method == 'POST':
        form = json.loads(request.body.decode(encoding='UTF-8'))
        if form:
            try:
                order = Order.objects.get(id=form['id'])
            except:
                order = None

            if order:
                print(form['confirm'])
                order.confirm = bool(form['confirm'])
                order.save()
                response = {"response": "Success",
                            "details": "Order Confirmed"}
                return JsonResponse(response, safe=False)
            else:
                response = {"response": "Error",
                            "details": "Order not found"}
                return JsonResponse(response, safe=False)
        else:
            response = {"response": "Error",
                        "details": "No Form"}
            return JsonResponse(response, safe=False)


def add_product(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        context = locals()
        template = 'add_product.html'
        return render(request, template)
    elif request.method == 'POST' and request.FILES['image']:
        product = Gas()
        product.price = request.POST.get('price')
        product.product_name = request.POST.get('product_name')
        product.Accessories = request.POST.get('Accessories')
        product.supplier = request.POST.get('supplier')
        product.image = request.FILES['image']
        product.save()
    template = 'add_product.html'
    context = {'msg': "New Product Added Successfully", }
    return render(request, template, context)


def change(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        edit = Gas.objects.all()
        context = {'edits': edit}
        templates = "change.html"
        return render(request, templates, context)


def edit(request, edit_id):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        print('am here')
        show = Gas.objects.filter(id=edit_id)
        content = {'showprod': show, }
        templates = 'edit.html'
        return render(request, templates, content)
    elif request.method == 'POST' and request.FILES['image']:
        if request.POST.get('category') == "":
            product = Gas.objects.get(id=edit_id)
            product.price = request.POST.get('price')
            product.product_name = request.POST.get('product_name')
            product.section = request.POST.get('section')
            product.supplier = request.POST.get('supplier')
            product.image = request.FILES['image']
            product.save()
        elif request.POST.get('category') == request.POST.get('category'):
            product = Gas.objects.get(id=edit_id)
            product.price = request.POST.get('price')
            product.product_name = request.POST.get('product_name')
            product.category = request.POST.get('category')
            product.supplier = request.POST.get('supplier')
            product.image = request.FILES['image']
            product.save()
        context = {'msg': "Product Successfully Changed", }
        return redirect('/change/', context)


def prod_del(request, del_id):
    if request.method == 'GET':
        rst = Gas.objects.get(id=del_id)
        rst.delete()
        context = {'msg': "Product Succesfully deleted"}
        return redirect('/change/', context)


def comment(request):
    if request.method == 'GET':
        com = Contact.objects.all()
        context = {'comment': com, }
        template = 'comment.html'
        return render(request, template, context)


def Adminreg(request):
    if request.method == 'GET':
        context = locals()
        templates = "Adminreg.html"
        return render(request, templates, context)
    elif request.method == 'POST':
        admin = adminreg()
        admin.Username = request.POST.get('Username')
        admin.Password = request.POST.get('Password')
        admin.save()
        context = {'successmsg': "Registration successfull Continue to login", 'user': request.POST.get('Username'), }
        templates = 'Adminreg.html'
        return render(request, templates, context)


def Adminlog(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        context = locals()
        templates = 'Adminlog.html'
        return render(request, templates, context)
    elif request.method == 'POST':
        try:
            user = request.POST.get('Username')
            sql = adminreg.objects.get(Username=user)
        except:
            print(traceback.print_exc())
            sql = None
        user = request.POST.get('Username')
        if sql:
            if sql.Password == createHash(request.POST.get('Password')):
                context = {'name': sql.Username, }
                templates = 'adminpage.html'
                request.session['userid'] = sql.id
                request.session['username'] = sql.Username
                print(sql.Password)
                return render(request, templates, context)
        else:
            print('am here')
            # Edward
            messages.error(request, 'Sorry! invalid password')
            return redirect('/Adminlog/')


def Adminlogout(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        del request.session['userid']
        del request.session['username']
        return redirect('/Adminlog/')


def search(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        # fil = ProductFilter(request.GET, queryset=Product.objects.all())
        # if fil:
        #     templates = 'search.html'
        #     context = {'filter': fil}
        # else:
        #     templates = 'search.html'
        #     context = {'nosch': "No such entry, Check another Products."}
        # return HttpResponse(request, templates, context)
        sh = request.POST.get('seach')
        slo = Gas.objects.filter(product_name__icontains=sh)
        if slo:
            context = {'sch': slo}
            print('am fucking heree')
            templates = 'search.html'
            return render(request, templates, context)
        else:
            context = {'nosch': "No such entry, Check another Products."}
            templates = 'search.html'
            return render(request, templates, context)


def gas_repair(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        context = locals()
        templates = 'gas_repair.html'
        return render(request, templates, context)
    elif request.method == 'POST':
        if request.FILES['image1'] or request.FILES['image2']:
            gas = GasRepair()
            fname1 = request.POST.get('fname')
            user_email = request.POST.get('email')
            user_phone = request.POST.get('phone')
            user_loc = request.POST.get('location')
            user_addr = request.POST.get('address')
            user_cooker = request.POST.get('cooker')
            user_desp = request.POST.get('descrip')
            user_image1 = request.FILES['image1']
            user_image2 = request.FILES['image2']

            if fname1 != None:
                match = re.match("^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@"
                                 + "[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$", user_email)
                if match != None:
                    gas.email = user_email
                    gas.fname = fname1
                    gas.phone = user_phone
                    gas.location = user_loc
                    gas.address = user_addr
                    gas.cooker = user_cooker
                    gas.descrip = user_desp
                    gas.image1 = user_image1
                    gas.image2 = user_image2
                    gas.save()
                    messages.success(request, 'Order Successfully Submitted,Kindly wait for our call.Thanks')
                    return redirect('/gas_repair/')
                else:
                    messages.error(request, 'Invalid Email')
                    return redirect('/gas_repair/')
            else:
                messages.error(request, 'Name can not be empty')
                return redirect('/gas_repair/')
        else:
            context = {'err': "Image can't be Empty"}
            return redirect('/gas_repair/', context)


def gas_acc(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        if 'cart' not in request.session.keys():
            request.session['cart'] = {}
        print(request.session['cart'])
        sql = Gas.objects.filter(Accessories='gas_acc')
        if sql:
            context = {'sql1': sql, }
            template = 'gas_acc.html'
            return render(request, template, context)
        else:
            context = {'msg': "No stock available", }
            template = 'index.html'
            return render(request, template, context)


def repair_order(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        try:
            repair = GasRepair.objects.all()
        except:
            repair = None
        if repair != None:
            context = {
                'orders': repair,
            }
            templates = 'repair_order.html'
            return render(request, templates, context)
        elif repair == None:
            messages.error(request, 'Gas-Repair Order Empty')
            return redirect(request.META.get('HTTP_REFERRER'))


def repair_details(request, order_id):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        try:
            repair = GasRepair.objects.get(id=order_id)
        except:
            repair = None
        if repair:
            context = {
                'orderD': repair,
            }
            templates = 'repair_details.html'
            return render(request, templates, context)
        else:
            messages.error(request, 'Nothing to Show')
            return redirect(request.META.get('HTTP_REFERRER'))


def forget_pass(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        context = locals()
        templates = 'forget_pass.html'
        return render(request, templates, context)
    if request.method == 'POST':
        user_name = request.POST.get('Username')
        try:
            user = adminreg.objects.get(Username=user_name)
        except:
            user = None
        request.session['username'] = user.Username
        request.session['userid'] = user.id
        if user:
            messages.error(request, 'Username Verified ,Kindly Enter Your New Password')
            return redirect('/change_pass/', request.session['username'], request.session['userid'])
        else:
            messages.error(request, 'Username Not Verified')
            return redirect(request.META.get('HTTP_REFERRER'))


def change_pass(request):
    if request.method == 'GET':
        context = locals()
        templates = 'change_pass.html'
        return render(request, templates, context)
    if request.method == 'POST':
        rest_pass = request.POST.get('pass')
        user = request.session['username']
        userid = request.session['userid']
        try:
            u_pass = adminreg.objects.get(Username=user)
        except:
            u_pass = None
        if u_pass:
            u_pass.Password = createHash(rest_pass)
            i = u_pass.Password
            u_pass.save()
            context = {
                'success': "Password Reset Successfully"
            }
            templates = 'success.html'
            return render(request, templates, context)
        else:
            context = {
                'errmsg': "Password Reset Not Successfully try Again",
            }
            return redirect('/forget_pass/', context)


def success(request):
    if request.method == 'GET':
        context = locals()
        templates = 'success.html'
        return render(request, templates, context)


def test(request):
    if request.method == 'GET':
        context = locals()
        templates = 'test.html'
        return render(request, templates, context)
    elif request.method == 'POST':
        form = json.loads(request.body.decode(encoding='UTF-8'))
        name = form['name']
        phone = form['phone']
        email = form['email']
        print(name)
        print(email)
        print(phone)
        context = locals()
        templates = 'test.html'
        return redirect(request.META.get('HTTP_REFERRER'))
