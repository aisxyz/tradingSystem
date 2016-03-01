#coding:utf-8
import cPickle

class Merchant:
    """
        本类用以模拟店主管理商场的过程
    """
    def __init__(self):
        self.current_goods = self.get_former_goods()
        self.display_goods()

    def choose_action(self):
        '''
            代表店主的动作行为
        '''
        choose = input("添加商品选1，修改商品价格选2：")
        if choose == 1:
            goods = self.get_add_goods()
            self.add_goods(goods)
        elif choose == 2:
            self.adjust_price()

    def display_goods(self):
        '''展示当前商店里的商品'''
        print "--------------------当前商品信息概览--------------------"
        print '#'*55
        for goods in self.current_goods.iterkeys():
            print "##   名字：%-10s 价格：%-10d 数量：%-5d   ##" %(goods, self.current_goods[goods]['price'], self.current_goods[goods]['amount'])
        print '#'*55

    def get_add_goods(self):
        '''
            获得要添加的商品信息
        '''
        goods = {}
        while True:
            try:
                variety = raw_input("商品名：")
                price = input("价格：")
                amount = input("数量：")
                goods[variety] = {'price':price,'amount':amount}
                answer = raw_input('继续添加吗？(y/n)')
                if answer in ('n','N'):
                    break
            except NameError:
                print "############ 商品信息输入格式不准确哦！请重新再输一遍！^_^ ##############"
        return goods

    def add_goods(self,goods):
        """
            用以添加商品
        """
        for add in goods.iterkeys():
            if self.current_goods.has_key(add):                     # 有这种商品时就只需修改其数量
                self.current_goods[add]['amount'] = self.current_goods[add]['amount'] + goods[add]['amount']
            else:                                                   # 假如以前店里没有这种商品，就添加该商品
                self.current_goods.update({add:goods[add]})

        with open("goods.pkl",'wb') as f:                           # 最后再将修改后的商品信息保存起来
            cPickle.dump(self.current_goods,f,cPickle.HIGHEST_PROTOCOL)

    def get_former_goods(self):
        '''
           获得商店目前的商品
        '''
        try:
            with open('goods.pkl','rb') as f:
                former_goods = cPickle.load(f)
        except IOError:
            former_goods = {}
        return former_goods

    def adjust_price(self):
        '''
            用来调整商品的市场价格
        '''
        try:
            whichGoods = raw_input("调整哪种商品的价格？")
            if self.current_goods.get(whichGoods) is not None:
                price = input('现在的市场价为：')
                self.current_goods[whichGoods]['price'] = price
            else:
                print "############# 目前店内没有这种商品！################"
        except NameError:
            print "############ 商品信息输入格式不准确哦！请重新再输一遍！^_^ ##############"

if __name__ == '__main__':
    merchant = Merchant()
    merchant.choose_action()