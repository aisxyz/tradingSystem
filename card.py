#coding:utf-8
import sqlite3

class Card:
    """
        本类用以模拟消费卡的支付功能
    """
    def login(self,money):
        userId = raw_input("用户ID：")
        password = raw_input("密码：")

        conn,c = '',''
        try:
            conn = sqlite3.connect('userInfo.db')
            c = conn.cursor()
            c.execute('select * from userTable where userId=?',(userId,))

            # userTable(userId,password,balance)
            queryResult = c.fetchone()
            if queryResult and queryResult[1] == password:
                print "############# 登陆成功！#############"
                if queryResult[2] < money:
                    print "############## 抱歉，您的余额不足以支付本次消费！##############"
                    return
                self.settleAccounts(c,userId,queryResult[2]-money)
            else:
                print "############# 认证失败，输入的用户名或密码错误！#############"
        finally:
            conn.commit()
            c.close()
            conn.close()

    def consume(self,money):
        self.login(money)

    def settleAccounts(self,cursor,userId,money):
        confirm = raw_input("确认支付？(y/n)")
        if confirm in ('y','Y'):
            cursor.execute('update userTable set balance=? where userId=?',(money,userId))
            print("############ 付款成功！#############")
        else:
            print("############ 支付失败，您放弃了本次交易！############")

mycard = Card()