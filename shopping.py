#coding:utf-8
import cPickle
from card import mycard

class Shop:
    """
        本类用以模拟商场购物过程
    """
    def __init__(self):
        self.banner()
        # 商品存储格式：{'goods1':{'price':price,'amount':amount},
        #               'goods2':{'price':price,'amount':amount}
        #                …………
        #             }
        self.allGoods = self.openCondo()    # 获取商品房中的商品信息
        self.displayGoods()

    def banner(self):                       # 欢迎界面
        print("""
                ===============================================
                $                                             $
                $    欢      ______________           迎      $
                $           /_____________/|======\\\          $
                $           |             |=======//          $
                $           |   WELCOME   ||                  $
                $           |_____________|/                  $
                $             @         @                     $
                $    光                               临      $
                ===============================================
            """)

    def displayGoods(self):                     # 陈列商品
        print "--------------------当前商品信息概览--------------------"
        print '#'*55
        for goods in self.allGoods.iterkeys():
            print "##   名字：%-10s 价格：%-10d 数量：%-5d   ##" %(goods, self.allGoods[goods]['price'], self.allGoods[goods]['amount'])
        print '#'*55

    def openCondo(self):                        # 打开商品房
        goods_file = open('goods.pkl','rb')
        goods = cPickle.load(goods_file)
        goods_file.close()
        return goods

    def select(self):                       # 开启购物之旅
        shoppingTrolley = {}                # 开始时购物车是空的
        while True:
            which = raw_input("真纠结，该买哪样呢？")
            if which not in self.allGoods:
                print "*********** 真遗憾，没有这样的东西! ***********"
                continue
            try:
                number = input("买多少呢？")
                if number>self.allGoods[which]['amount']:
                    print "*********** 抱歉，目前存货不足，请减少数量或选择其他商品！^_^ ************"
                    continue
                #shoppingTrolley[which] = shoppingTrolley.setdefault(which,0)+number
                shoppingTrolley[which] = number
            except NameError:
                print "############ 问的是数量哦！############"
            if self.ifSettleAccounts():         # 询问是否结账
                self.pay(shoppingTrolley)
                break

    def ifSettleAccounts(self):
        isYes = raw_input("还要买不呢？(y/n)")
        if isYes in ('y','Y'):
            return False
        return True

    def pay(self,goods):
        # 获得所购商品对应的价格
        priceTemp = map(lambda x:self.allGoods[x]['price'],goods.keys())
        total = sum(map(lambda x,y:x*y,priceTemp,goods.values()))
        checkBills = raw_input("显示账单吗？(y/n)")
        if checkBills in ('y','Y'):
            self.showBills(goods)
        print "########### 共计￥%s ###########" % total
        mycard.consume(total)                  # 刷卡走人

    def makeBills(self,goods):                 # 生成账单信息
        bills = ['-'*59, '| 商品名           单价             数量             花费 |']
        for obj in goods:
            goodsInfo = '| %-16s %-16d %-16d %-4d |' %(obj,self.allGoods[obj]['price'],goods[obj],self.allGoods[obj]['price']*goods[obj])
            bills.append(goodsInfo)
        bills.append('_'*59)                   # 画上账单结束线
        return bills

    def showBills(self,goods):                 # 显示账单信息
        for bill in self.makeBills(goods):
            print bill

if __name__ == '__main__':
    shop = Shop()
    shop.select()