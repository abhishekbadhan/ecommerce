from django.shortcuts import render, redirect
from django.http import request
from django.http import HttpResponse
from .models import product, contacts, orderupdate, Post, Blogcomment
from .paytm import check
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def home(request):
    prod = product.objects.all()
    rep = {'rep': prod}
    return render(request, 'shop.html', rep)


def quickview(request, my_id):
    if request.method == 'POST':
        loginuser = request.user
        if str(loginuser) != 'AnonymousUser':
            comments = request.POST.get('comment', False)
            postobjects = Blogcomment.objects.filter(comment=comments)
            postsno = request.POST.get('postid', False)
            post = product.objects.filter(id=postsno).first()
            postobjects = Blogcomment.objects.filter(post=post)
            pobj = [i.comment for i in postobjects]
            if comments in pobj:
                pass
            else:
                user = request.user.first_name
                commentdata = Blogcomment(comment=comments, user=user, post=post)
                commentdata.save()
    # NOW SHOWING THE COMMENTS BELOW
    prod = product.objects.filter(id=my_id)[0]
    #INCREMENTING THE VIEWS
    prod.product_views = prod.product_views + 1
    prod.save()

    commentfilter = Blogcomment.objects.filter(post=prod, parent = None)
    commentfilter = commentfilter[::-1]


    # NOW MAKING DICTIONERY OF THE REPLY COMMENTS
    replycomment = Blogcomment.objects.filter(post=prod).exclude(parent=None)
    replydict = {}
    for replies in replycomment:
        if replies.parent.sno not in replydict.keys():
            replydict[replies.parent.sno] = [replies]
        else:
            replydict[replies.parent.sno].insert(0,replies)
    for i in replydict.items() :
        print(i)
    dict = {'house': prod,'comments': commentfilter, 'my_id': my_id,'no_of_comments':len(commentfilter),'parentreply':replydict}
    return render(request, 'quickview.html', dict)


def checkout(request):
    messages.success(request, 'this is success')
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('inputname', '')
        password = request.POST.get('inputpassword', '')
        address = request.POST.get('inputaddress', '')
        city = request.POST.get('inputcity', '')
        state = request.POST.get('inputstate', '')
        zip = request.POST.get('inputzip', '')
        cntc = contacts(items_json=items_json, name=name, password=password,
                        address=address, city=city, state=state, zip=zip)
        cntc.save()
        result = True
        # NOW CALCULATING THE PRICE
        pr = 0
        zzz = json.loads(items_json)
        for i in zzz:
            print(i)
            pr = pr + (zzz[i][0]*int(zzz[i][2]))
        # ORDERUPDATE
        upor = orderupdate(
            order_id=cntc.id, update_desc='successfully order is placed')
        upor.save()
        # requestind for the ptm request
        MERCHANT_KEY = 'Uv1gt5O3u2mW8aji'
        param_dict = {
            'MID': 'hyXvwS67606907268138',
            'ORDER_ID': str(cntc.id),
            'TXN_AMOUNT': str(pr),
            'CUST_ID': str(zip),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/'
        }
        param_dict['CHECKSUMHASH'] = check.generate_checksum(
            param_dict, MERCHANT_KEY)
        print(param_dict)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


def tracker(request):
    if request.method == 'POST':
        orderid = request.POST.get('order_id', '')
        zips = request.POST.get('order_zip', '')
        try:
            exe1 = contacts.objects.filter(id=orderid, zip=zips)
            print(exe1)
            if len(exe1) > 0:
                exe2 = orderupdate.objects.filter(order_id=orderid)
                print('this is exe2', exe2)
                updates = []
                for item in exe2:
                    updates.append(
                        {'item': item.update_desc, 'time': item.timestamp})
                resp = json.dumps([updates, exe1[0].items_json], default=str)
                print('THESE ARE RESP', resp)
                return HttpResponse(resp)
            else:
                return HttpResponse('{}')
        except:
            print('this is error')
            return HttpResponse('{}')

    else:
        return render(request, 'tracker.html')


def searchMatch(query, item):
    if query in item.product_name or query in item.product_desc:
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    if len(query) > 0:
        catprod = product.objects.values('product_desc')
        cats = {i['product_desc'] for i in catprod}
        print(cats)
        prod = []
        for cat in cats:
            prodtemp = product.objects.filter(product_desc=cat)
            for item in prodtemp:
                if searchMatch(query, item):
                    prod.append(item)
            print('this is prod', prod)
            rep = {'rep': prod}
    return render(request, 'search.html', rep)


@csrf_exempt
def handlerequest(request):
    form = request.POST
    MERCHANT_KEY = 'Uv1gt5O3u2mW8aji'
    respons_dict = {}
    for i in form.keys():
        respons_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = check.verify_checksum(respons_dict, MERCHANT_KEY, checksum)
    if verify:
        print(respons_dict['RESPCODE'])
        if respons_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print("order unsuccessful 111 because"+respons_dict['RESPMSG'])
    else:
        print("order unsuccessful because"+respons_dict['RESPMSG'])
    print(respons_dict)
    return render(request, 'paymentstatus.html', {'response': respons_dict})


def sign_up(request):
    if request.method == 'POST':
        name1 = request.POST['inputname']
        email1 = request.POST['address']
        number = request.POST['number']
        pass1 = request.POST['password1']
        confpass1 = request.POST['confirmpassword']
        dob = request.POST['date1']

        # ADDING INTO USER DATABASE
        myuser = User.objects.create_user(email1, email1, pass1)
        myuser.first_name = name1
        # myuser.email1 = email1
        myuser.save()
        # print(myuser)
        print(name1, email1, number, pass1, confpass1, dob)  # TIME PASS
        return redirect('shops')
    else:
        return redirect('shops')


def handlelogin(request):
    if request.method == 'POST':
        email1 = request.POST['loginname']
        password1 = request.POST['loginpassword']
        userss = authenticate(username=email1, password=password1)
        if userss is not None:
            login(request, userss)
        print('this is USERLOGIN DETAILS', userss)
        return redirect('shops')
    else:
        return HttpResponse('THIS DO NOT EXIST')


def handlelogout(request):
    logout(request)
    return redirect('shops')


def blogpost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = Blogcomment.objects.filter(post=post)
    context = {'post': post, 'comments': comments}
    return render(request, 'blogpost.html')


def postcomment(request, slug):
    if request.method == 'POST':
        comment = request.POST['comment']
        user = request.user
        postsno = request.POST['postid']
        post = Post.objects.get(sno=postsno)

        comment = Blogcomment(comment=comment, user=user, post=post)
        comment.save()
        return redirect(f'/shop/aboutproduct/{postsno}')


def showcomment(request, my_id):
    prod = product.objects.filter(id=my_id)
    print('THIS IS PROD', prod)
    return render(request, 'quickview.html')


def takingreply(request):
    if request.method == 'POST':
        reply = request.POST['reply']
        result_page_id = request.POST['result_page_id']
        result_page = product.objects.get(id = result_page_id)
        parent_id = request.POST['parent_id']
        parent = Blogcomment.objects.get(sno = parent_id)
        add_in_database = Blogcomment(comment = reply, user = request.user.first_name, parent = parent, post = result_page)
        add_in_database.save()



        selected = product.objects.get(id=result_page_id)
        prod = product.objects.get(id=result_page_id)
        # commentfilter = Blogcomment.objects.filter(post=prod)
        commentfilter = Blogcomment.objects.all()[::-1]
        print('THESESSSSSSSSSSSSSSSSS',commentfilter[0].parent.comment)
        print('THESESSSSSSSSSSSSSSSSS',commentfilter[0].parent)
        dict = {'house': selected, 'comments': commentfilter}
        return redirect(f"/shop/aboutproduct/{result_page_id}/")