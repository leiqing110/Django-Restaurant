from django.shortcuts import HttpResponse,render,redirect#返回完整的html文件
from APP01 import models
from django.db.models import F, Q
from functools import wraps
from django.contrib import auth
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
global flag,flag2,price1,price2,price3
flag = True
flag2 = True
price1 = 0
price2 = 0
price3 = 0
# def check_login(f):
#     def inner(request,*args,**kwargs):
#         if request.session.get("is_login") == "1":
#             return f()
#         else:
#             return redirect("/login/")
#     return inner



def login(request):#实现登陆操作
    #如果你是get请求
    error_msg = ""
    # if request.method == "GET": #这里GET必须是大写
    #     return render(request, "login.html")
    #如果你是Post请求，我就取出提交的数据，做登陆判断
    if request.method == "POST":
        email= request.POST.get("user_email",None)
        pwd1 = request.POST.get("user_pwd",None)
        #print(email,pwd)
    #做是否登陆成功的判断\

        user = models.UserInfo.objects.filter(email=email,pwd=pwd1)[0]#返回一个列表,user[0]即为返回对象
        #将登陆的用户封装到request.user
        if user:
            #登陆成功
            request.session["is_login"] = "1"
            #request.session["username"] = user.name
            request.session["user_id"] = user.id#获取对象的ID
            #1.生成特殊的字符串
            #2.特殊字符串当成KEY，z在数据库中的session表中对应一个session value
            #3.在相应中向浏览器写了一个COOKIE COOKIE的值就是特殊的字符串
            return redirect("/movie_list/")
    return render(request,"login.html")
        #error_msg = "邮箱或密码错误"
    #return HttpResponse('ojbk')
   # return render(request,"login.html",{"error":error_msg} )

def logout(request):
    del request.session["user_id"]
    messages.success(request, "退出成功")
    return redirect("/login/")

def user_list(request):
    user_id = request.session.get("user_id")#获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")
    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    if user_obj.name != 'admin':
        messages.success(request, "对不起，您没有权限查看，请通知管理员")
        return redirect("/movie_list/")


    user_obj = models.AdminInfo.objects.filter(id=user_id)[0]

    #去数据库中查询所有的用户
    #利用ORM这个工具去查询数据库，不用自己去查询
    ret = models.UserInfo.objects.all().order_by("id")
    if user_obj:
        return render(request, "user_list.html", {"user_list": ret,"user":user_obj})

def add_user(request):
    #第一次请求页面的时候就返回一个页面，让用户填写
    err_msg = ""
    if request.method == "POST":

        #用户填写了新的用户名，并发送了POST请求
        new_name = request.POST.get("username",None)
        new_pwd = request.POST.get("userpwd",None)
        new_email = request.POST.get("useremail", None)
        if  new_name:
        #通过ORM去数据库中新创建一条记录
            models.UserInfo.objects.create(name=new_name,pwd=new_pwd,email=new_email)
        #添加完成后跳转到用户列表
            return redirect("/user_list/")
        else:
            err_msg = "名字不能为空!"

    return render(request,"add_user.html",{"error":err_msg})

#删除用户
def delete_user(request):
    #删除指定的id
    del_id = request.GET.get("id",None)
    #如果能取到ID值
    if del_id:
        #去数据库删除当前的id值的数据
        #根据id值查找到的数据
        #del_obj = models.UserInfo.objects.get(id=del_id).delete()
        del_obj = models.UserInfo.objects.get(id=del_id)
        #删除
        del_obj.delete()
        # 返回删除后的页面，跳转到出版社的列表页，查看是否删除成功
        return redirect("/user_list/")
    else:
        return HttpResponse("要删除的数据不存在")
    pass

#编辑用户信息
def edit_user(request):
    #用户修改完用户的名字，点击提交按钮，给我发来新的名字
    if request.method == "POST":
        #取新出版社的名字
        #print(request.POST)
        edit_id = request.POST.get("user_id") #这里获取的是表单的内容，必须匹配name
        #根据ID获取要修改的对象\
        #print(edit_id)

        edit_user = models.UserInfo.objects.get(id=edit_id)

        new_name = request.POST.get("user_name")
        new_pwd = request.POST.get("user_pwd")
        edit_user.name = new_name
        edit_user.pwd = new_pwd
        edit_user.save()#把修改提交到数据库
        #挑转到用户列表页，查看是否修改成功
        return redirect("/user_list/")

    edit_id = request.GET.get("id",None)#从请求URl中获取ID参数
    #如果这个ID存在
    if edit_id:
        user_obj = models.UserInfo.objects.get(id=edit_id)
        #将信息传到页面上
        return render(request,"edit_user.html",{"user":user_obj})
    else:
        return HttpResponse("编辑的用户不存在")

def movie_list(request):
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")

    user_obj = models.UserInfo.objects.get(id=user_id)

    all_movie = models.Movies.objects.all()
    # 在html页面完成字符串的替换
    if user_obj:
        return render(request, "movie_list.html", {"all_movie": all_movie, "user": user_obj})
    else:
        return render(request, "movie_list.html", {"all_movie": all_movie, "user":"匿名用户"})

def add_cart(request):#电影票加入购物车

    global flag,flag2
    #request.session["cart_id"] = 1  # 获取对象的ID
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")


    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    all_movie = models.Movies.objects.all()
    movie_id = request.GET.get("id")#获取电影ID

    movie_obj = models.Movies.objects.get(id=movie_id)#获取电影对象
    if flag == True:#第一次执行加入购物车的操作
        cart_obj = models.Cart.objects.filter(owner= user_obj)
        flag = False #标志位
        movie_obj.num = 1  # 第一次加入购物车  数量默认为1
        movie_obj.save()#执行保存操作
        cart = models.Cart.objects.create(owner = user_obj)

        cart.movies.add(movie_obj)
        #cart.owner.add(user_obj)

        #print("2")
        cart.save()
        messages.success(request, "加入购物车成功")
        return redirect("/movie_list/")
    else:
        cart_obj = models.Cart.objects.get(owner=user_obj)
        for movie in cart_obj.movies.all():
            if movie_obj == movie:
                movie_obj.num += 1
                movie_obj.save()
                print("ID:")
                print(movie.id)
        #return redirect("/movie_list/")

    if cart_obj and movie_obj:
        cart = models.Cart.objects.get(owner=user_id)
        cart.movies.add(movie_obj)
        # val = val+1
        # cart.save()
        print("数量")
        print(movie_obj.num)
        messages.success(request, "加入购物车成功")
        return redirect("/movie_list/")


    # cart = models.Cart.objects.create(owner=user_obj)
    # cart.owner.id(user_obj)
    # cart.movies.add(movie_obj)
    # # cart_obj.movies.add(movie_obj)
    # print("2")
    # messages.success(request, "加入购物车成功")
    # return redirect("/movie_list/")
    # #movie_obj2 = models.Cart.objects.get(movies= movie_obj)

def delete_cart(request):#清空购物车
    global flag
    flag = True
    global price1
    global price2
    global price3

    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")

    user_obj = models.UserInfo.objects.get(id=user_id)
   # all_good = models.Goods.objects.all()
   # good_id = request.GET.get("id")  # 获取电影ID

   # good_obj = models.Goods.objects.get(id=good_id)  # 获取电影对象
    cart_obj = models.Cart.objects.get(owner=user_obj).delete()
    all_movie = models.Movies.objects.all()
    all_good = models.Goods.objects.all()

    for movie in all_movie:
        movie.num = 1
        movie.save()
    for good in all_good:
        good.num = 1
        good.save()

    price3 = 0
    price2 = 0
    price1 = 0
    messages.success(request,"购物车已清空")
    return redirect("/movie_list/")

def add_cart2(request):#商品加入购物车
    global flag2
    # request.session["cart_id"] = 1  # 获取对象的ID
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")

    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    all_good = models.Goods.objects.all()
    good_id = request.GET.get("id")  # 获取电影ID
    good_obj = models.Goods.objects.get(id=good_id)  # 获取电影对象
    if flag2 == True:
        #cart_obj = models.Cart.objects.filter(owner=user_obj)
        flag2 = False  # 标志位
        good_obj.num = 1  # 第一次加入购物车  数量默认为1


        cart = models.Cart.objects.create(owner=user_obj)
        #cart.owner.id(user_obj)
        cart.goods.add(good_obj)
        # cart_obj.movies.add(movie_obj)
        #print("2")
        cart.save()

        good_obj.save()
        messages.success(request, "加入购物车成功")
        return redirect("/goods_list/")

    else:
        cart_obj = models.Cart.objects.get(owner=user_obj)
        for good in cart_obj.goods.all():
            if good_obj == good:
                good_obj.num += 1
                good_obj.save()
                print("ID:")
                print(good.id)
    if cart_obj and good_id:
        messages.success(request, "购物车为空")
        cart = models.Cart.objects.get(owner=user_id)
        cart.goods.add(good_obj)
        #cart.owner.add(user_obj)
        cart.save()
    # elif (not cart_obj) and good_obj:
    #     cart = models.Cart.objects.create(owner=user_obj)
    #     cart.owner.add(user_obj)
    #     cart.goods.add(good_obj)
    #     # cart_obj.movies.add(movie_obj)
    #     print("2")
    messages.success(request, "购物车为空")
    return redirect("/goods_list/")
def cart(request):
    global price1
    global price2
    global price3
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    #cart_id = request.session.get("cart")  # 获取sessiond的user_id 这里是管理员ID
    cart_obj = models.Cart.objects.filter(owner = user_id)
    if cart_obj:
        cart = models.Cart.objects.get(owner=user_id)
        movie_list = cart.movies.all()
        goods_list = cart.goods.all()
    else:
        messages.success(request, "购物车为空")
        return redirect("/movie_list/")
    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    # 在html页面完成字符串的替换

    if user_obj:
        return render(request, "cart.html",
                      {"user": user_obj, "movie_lists": movie_list, "good_lists": goods_list, "all_price": price3})

#退款操作
def refund(request):

    order_id = request.GET.get("id",None)#从请求URl中获取ID参数
    order_obj = models.Order.objects.get(id=order_id).delete()
    messages.success(request, "退款成功")
    return redirect("/huiyuan_list/")

def count(request):
    global price1
    global price2
    global price3
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    #cart_id = request.session.get("cart")  # 获取sessiond的user_id 这里是管理员ID
    cart_obj = models.Cart.objects.filter(owner=user_id)
    if cart_obj:
        cart = models.Cart.objects.get(owner=user_id)
        movie_list = cart.movies.all()
        if movie_list:
            for movie in movie_list:
                price1 += movie.price*movie.num
        goods_list = cart.goods.all()
        if goods_list:
            for good in goods_list:
                price2 += good.price*good.num
        price3 = price1 + price2
    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    return render(request, "cart.html",
                  {"user": user_obj, "movie_lists": movie_list, "good_lists": goods_list, "all_price": price3})
def settle_accounts(request):
    if request.method == "POST":
        search = request.POST.get("huiyuan")  # 获取表单内容进行搜索
        all_price = request.POST.get("all_price")  # 获取总价
        edit_huiyuan_obj = models.Huiyuan.objects.filter(id=search)[0]
        edit_huiyuan_obj.price = edit_huiyuan_obj.price - price3
        edit_huiyuan_obj.save()
        all_huiyuan_obj = models.Huiyuan.objects.all()

        #生成订单操作
        user_id = request.session.get("user_id")  # 获取sessiond的user_id
        cart_obj = models.Cart.objects.filter(owner=user_id)
        if cart_obj:
            cart = models.Cart.objects.get(owner=user_id)
            movie_list = cart.movies.all()
            goods_list = cart.goods.all()

        order = models.Order.objects.create(user_id_id=edit_huiyuan_obj.id,price=price3)
        #order.user_id_id = edit_huiyuan_obj.id #订单所有者
        if movie_list:
            for movie_obj in movie_list:
                order.movies.add(movie_obj)
        if goods_list:
            for good_obj in goods_list:
                order.goods.add(good_obj)
        #order.price = price3
        order.save()
        user_obj = models.UserInfo.objects.filter(id=user_id)[0]
        delete_cart(request)
        return render(request, "huiyuan_list.html", {"all_huiyuan": all_huiyuan_obj})

def delete_movie(request):
    #删除指定的id
    del_id = request.GET.get("id",None)
    #如果能取到ID值
    if del_id:
        #去数据库删除当前的id值的数据
        #根据id值查找到的数据
        #del_obj = models.UserInfo.objects.get(id=del_id).delete()
        del_obj = models.Movies.objects.get(id=del_id)
        #删除
        del_obj.delete()
        # 返回删除后的页面，跳转到出版社的列表页，查看是否删除成功
        return redirect("/movie_list/")
    else:
        return HttpResponse("要删除的数据不存在")
    pass

def add_movie(request):
    if request.method == "POST":
        # {"book_title":"跟金老板学开车，"publisher_id"：9}
        new_name = request.POST.get("moviename")
        new_intro = request.POST.get("movieintro")
        new_time = request.POST.get("movietime")
        new_yingting = request.POST.get("yingting")
        new_price = request.POST.get("price")


        models.Movies.objects.create(mname=new_name, intro=new_intro,time=new_time,yingting=new_yingting,price=new_price)
        # #返回到书籍列表页
        return redirect("/movie_list/")
    ret = models.Movies.objects.all()
    return render(request, "add_movie.html", {"movie_list": ret})

def search(request):
    if request.method == "POST":

        edit = request.POST.get("search")  # 这里获取的是表单的内容，必须匹配name
        # 根据ID获取要修改的对象\
        # print(edit_id)
        #print(edit_name)
        edit_movie = models.Movies.objects.filter(Q(mname__icontains=edit))

        return render(request, "movie_list.html", {"all_movie": edit_movie})

def search_huiyuan(request): #会员信息查找函数
    if request.method == "POST":

        edit = request.POST.get("search_huiyuan")  # 这里获取的是表单的内容，必须匹配name

        # print(edit_id)
        #print(edit_name)
        edit_huiyuan = models.Huiyuan.objects.filter(Q(name__icontains=edit)|Q(id__icontains=edit))#根据条件筛选

        return render(request, "huiyuan_list.html", {"all_huiyuan": edit_huiyuan})

def search_good(request):#卖品查找
    if request.method == "POST":

        edit = request.POST.get("search_good")  # 这里获取的是表单的内容，必须匹配name
        # 根据ID获取要修改的对象\
        # print(edit_id)
        #print(edit_name)
        edit_good = models.Goods.objects.filter(Q(name__icontains=edit)|Q(type_id__name__icontains=edit))#根据条件筛选

        return render(request, "goods_list.html", {"all_goods": edit_good})
def edit_movie(request):
    #用户修改完用户的名字，点击提交按钮，给我发来新的名字
    if request.method == "POST":
        #取新出版社的名字
        #print(request.POST)
        edit_id = request.POST.get("id") #这里获取的是表单的内容，必须匹配name
        #根据ID获取要修改的对象\
        #print(edit_id)

        edit_movie = models.Movies.objects.get(id=edit_id)

        new_name = request.POST.get("moviename")
        new_intro= request.POST.get("movieintro")
        new_time = request.POST.get("movietime")
        new_yingting = request.POST.get("yingting")
        edit_movie.mname = new_name
        edit_movie.intro = new_intro
        edit_movie.time = new_time
        edit_movie.yingting = new_yingting
        edit_movie.save()#把修改提交到数据库
        #挑转到用户列表页，查看是否修改成功
        return redirect("/movie_list/")

    edit_id = request.GET.get("id",None)#从请求URl中获取ID参数
    #如果这个ID存在
    if edit_id:
        movie_obj = models.Movies.objects.get(id=edit_id)
        #将信息传到页面上
        return render(request,"edit_movie.html",{"movie":movie_obj})
    else:
        return HttpResponse("编辑的用户不存在")

def goods_list(request):
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")

    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    all_goods= models.Goods.objects.all()

    if user_obj:
        return render(request, "goods_list.html", {"all_goods": all_goods,"user": user_obj})


def add_goods(request):
    if request.method == "POST":
        new_good_name = request.POST.get("good_name")
        new_good_intro = request.POST.get("good_intro")
        new_good_price = request.POST.get("good_price")
        new_good_type_id = request.POST.get("good_type")
        models.Goods.objects.create(name=new_good_name, intro=new_good_intro,price=new_good_price,type_id_id=new_good_type_id)
        # #返回到书籍列表页
        return redirect("/goods_list/")
    ret = models.Goods_type.objects.all()
    return render(request, "add_goods.html", {"good_type_list": ret})

def delete_goods(request):
    # 从URL里获取要删除书籍的id
    delete_id = request.GET.get("id")
    # 去数据库中删除指点id的书
    models.Goods.objects.get(id=delete_id).delete()
    # 返回书籍列表页，查看是否删除成功
    return redirect("/goods_list")

def edit_goods(request):

    if request.method =="POST":
        new_id = request.POST.get("id")
        new_name = request.POST.get("good_name")
        new_intro = request.POST.get("good_intro")
        new_price = request.POST.get("good_price")
        new_type_id = request.POST.get("good_type")

        edit_good_obj = models.Goods.objects.get(id=new_id)#根据ID获取数据库对象
        #提交到数据库
        edit_good_obj.name = new_name
        edit_good_obj.intro = new_intro
        edit_good_obj.price = new_price
        edit_good_obj. type_id_id = new_type_id
        edit_good_obj.save()
        #返回到列表页查看是否编辑成功
        return redirect("/goods_list/")

    edit_id = request.GET.get("id")
    edit_good_obj = models.Goods.objects.get(id=edit_id)
    ret = models.Goods_type.objects.all()
    return render(request,"edit_goods.html",{"good_obj":edit_good_obj,"good_type":ret})

def huiyuan_list(request):
    user_id = request.session.get("user_id")  # 获取sessiond的user_id
    if user_id == None:
        messages.success(request, "您未登录，请先登陆")
        return redirect("/login/")
    user_obj = models.UserInfo.objects.filter(id=user_id)[0]
    all_huiyuan = models.Huiyuan.objects.all()

    if user_obj:
        return render(request, "huiyuan_list.html", {"all_huiyuan": all_huiyuan,"user": user_obj})



def edit_huiyuan(request):
    if request.method =="POST":
        new_id = request.POST.get("id")
        new_name = request.POST.get("huiyuan_name")
        new_pwd = request.POST.get("huiyuan_pwd")
        new_price = request.POST.get("huiyuan_price")
        edit_huiyuan_obj = models.Book.objects.get(id=new_id)#根据ID获取数据库对象
        edit_huiyuan_obj.name = new_name
        edit_huiyuan_obj.pwd = new_pwd
        edit_huiyuan_obj.price = new_price
        #提交到数据库
        edit_huiyuan_obj.save()
        #返回到列表页查看是否编辑成功
        return redirect("/huiyuan_list/")
    #返回一个页面让用户编辑会员信息
    #取到编辑的会员的ID值
    edit_id = request.GET.get("id")
    #根据id去数据库中把具体的书籍对象拿到
    edit_huiyuan_obj = models.Huiyuan.objects.get(id=edit_id)
    return render(request,"edit_huiyuan.html",{"huiyuan_obj":edit_huiyuan_obj})

def delete_huiyuan(request):
    # 从URL里获取要删除书籍的id

    delete_id = request.GET.get("id")
    # 去数据库中删除指点id的书
    models.Huiyuan.objects.get(id=delete_id).delete()
    # 返回书籍列表页，查看是否删除成功
    return redirect("/huiyuan_list")

def add_huiyuan(request):

    if request.method == "POST":

        new_name = request.POST.get("huiyuan_name")
        new_pwd= request.POST.get("huiyuan_pwd")
        new_price =  request.POST.get("huiyuan_price")
        models.Huiyuan.objects.create(name=new_name, pwd=new_pwd,price=new_price)
        return redirect("/huiyuan_list/")
    ret = models.Huiyuan.objects.all()
    return render(request, "add_huiyuan.html", {"huiyuan": ret})

def edit_huiyuan(request):
    if request.method =="POST":
        new_id = request.POST.get("id")
        new_name = request.POST.get("huiyuan_name")
        new_pwd = request.POST.get("huiyuan_pwd")
        new_price = request.POST.get("huiyuan_price")
        edit_huiyuan_obj = models.Huiyuan.objects.get(id=new_id)#根据ID获取数据库对象
        edit_huiyuan_obj.name = new_name
        edit_huiyuan_obj.pwd = new_pwd
        edit_huiyuan_obj.price = new_price
        #提交到数据库
        edit_huiyuan_obj.save()
        #返回到列表页查看是否编辑成功
        return redirect("/huiyuan_list/")
    edit_id = request.GET.get("id")
    #根据id去数据库中把具体的会员对象拿到
    edit_huiyuan_obj = models.Huiyuan.objects.get(id=edit_id)
    return render(request,"edit_huiyuan.html",{"huiyuan_obj":edit_huiyuan_obj})


#订单详情
def order(request):
    movies = []
    s1 = []
    huiyuan_id = request.GET.get("id", None)  # 从请求URl中获取ID参数
    all_order = models.Order.objects.filter(user_id_id=huiyuan_id)
    user_obj = models.Huiyuan.objects.get(id=huiyuan_id)
    user_name = user_obj.name
    #order = models.Order.objects.get(user_id_id = huiyuan_id)
    # for order in all_order:
    #     movies.append(order.movies.all())
    # # s1 = order.movies.all()
    # # for s in s1:
    # #     print(s.mname)
    # for i in range(len(movies)):
    #     for j in range(len(movies[0])):
    #         print(movies[i][j].mname)
    #goods_list = cart.goods.all()
    return render(request,"order.html",{"all_order":all_order,"username":user_name,"movies":movies})

def test(request):
    print(request.GET)
    print(request.GET.get("name"))
    return HttpResponse("ok")

def publisher_list():
    pass
#展示书的列表


def book_list(request):
    #去数据库中查询所有的书籍
    all_book =models.Book.objects.all()
    #在html页面完成字符串的替换
    return render(request,"book_list2.html",{"all_book":all_book})

def add_book(request):
    #取到所有的出版社
    if request.method == "POST":
        #{"book_title":"跟金老板学开车，"publisher_id"：9}
        new_title = request.POST.get("book_title")
        new_publisher_id = request.POST.get("publisher")
        # #创建新书对象
        print("afaf "+new_publisher_id)
        models.Book.objects.create(title=new_title,publisher_id_id =new_publisher_id)
        # #返回到书籍列表页
        return redirect("/book_list/")
    ret = models.Publisher.objects.all()
    return render(request,"add_book.html",{"publisher_list":ret})

from django.views import View
#CBV版添加出版社
class Addbook(View):
    def get(self,request):
        return render(request, "add_book.html")
    def post(self,request):
        # {"book_title":"跟金老板学开车，"publisher_id"：9}
        new_title = request.POST.get("book_title")
        new_publisher_id = request.POST.get("publisher")
        # #创建新书对象
        print("afaf " + new_publisher_id)
        models.Book.objects.create(title=new_title, publisher_id_id=new_publisher_id)
        # #返回到书籍列表页
        return redirect("/book_list/")


def delete_book(request):
    #从URL里获取要删除书籍的id

    delete_id = request.GET.get("id")
    #去数据库中删除指点id的书
    models.Book.objects.get(id=delete_id).delete()
    #返回书籍列表页，查看是否删除成功
    return redirect("/book_list")

def edit_book(request):
    if request.method =="POST":
        new_id = request.POST.get("id")
        new_title = request.POST.get("book_title")
        new_publisher_id = request.POST.get("publisher")
        edit_book_obj = models.Book.objects.get(id=new_id)#根据ID获取数据库对象
        edit_book_obj.title = new_title
        edit_book_obj.publisher_id_id = new_publisher_id
        #提交到数据库
        edit_book_obj.save()
        #返回到列表页查看是否编辑成功
        return redirect("/book_list/")
    #返回一个页面让用户编辑书籍信息
    #取到编辑的书的ID值
    edit_id = request.GET.get("id")
    #根据id去数据库中把具体的书籍对象拿到
    edit_book_obj = models.Book.objects.get(id=edit_id)
    ret = models.Publisher.objects.all()
    return render(request,"edit_book.html",{"publisher_list":ret,"book_obj":edit_book_obj})

#处理上传文件的函数
def upload(request):
    if request.method =="POST":
        #从请求的FILES中获取上传文件的文件名，file为页面上type=files类型
        filename = request.FILES["upload_file"].name
        #在项目目录下新建一个文件
        with open(filename,"wb") as f:
            #从上传的文件对象中一点一点读
            for chunk in request.FILES["upload_file"].chunks():
                #写入本地文件
                f.write(chunk)
        return HttpResponse("上传OK")



