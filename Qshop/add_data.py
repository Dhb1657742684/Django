def goods_add(request):
    goods_names = '毛巾、杯子、水桶、筛子、垃圾桶、脚凳、手套、安全帽、工作服、笔记本、笔、文件夹、文具袋、名片盒、毛公仔、变形金刚、西红柿、南瓜、生菜、玉米、韭菜、卷心菜、萝卜、白菜、黄瓜、胡萝卜、大蒜、葱、木耳、豌豆、马铃薯、芋、苦瓜、洋葱、芹菜、地瓜、蘑菇、橄榄、菠菜、冬瓜、莲藕、紫菜、油菜、茄子、香菜、青椒、银耳、牛蒡、竹笋、绿豆、毛豆、豆芽菜'
    g_lst = goods_names.split('、')
    goods_area = '北京，天津，上海，重庆，河北，山西，辽宁，吉林，黑龙江，江苏，浙江，安徽，福建，江西，山东，河南，湖北，湖南，广东，海南，四川，贵州，云南，陕西，甘肃，青海，台湾，内蒙古，广西，西藏，宁夏，新疆，香港，澳门'
    g_area = goods_area.split('，')
    for i in range(100):
        goods = Goods()
        goods.goods_name = str(i + 1).zfill(5)
        goods.goods_num = random.choice(g_lst)
        goods.goods_price = round(random.random() * 100, 2)
        goods.goods_inven = random.randint(20, 100)
        goods.goods_area = random.choice(g_area)
        goods.goods_expr = random.randint(1, 24)
        # goods.save()
    return HttpResponse('hello world')