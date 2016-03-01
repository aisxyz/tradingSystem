#coding:utf-8
import sqlite3,time

class Bank(object):
    """
        本类用以模拟银行处理账户过程，包括注册账号，存款、取款、转账等功能
    """
    def __init__(self):
        self.__userId = ''
        self.__balance = 0            # 表示用户余额
        # 存储用户执行过的操作，以打印凭条
        self.__haveDone = ['_'*50,"| 时间                 交易类型            影响  |"]

        # 用户可以执行的操作类型
        self.__operates = {1: self.getMoney, 2: self.saveMoney,
                           3: self.transferAccounts, 4: self.checkBalance,
                           5: self.logout}

    def selectOperates(self):
        try:
            r = input("注册还是登录？（分别用0和1表示）")
            if r == 0:
                self.__regist()
            elif r == 1:
                self.login()
        except NameError:
            print "########## 无效输入！##########"

    def __regist(self):                     # 私有，不该被其子类继承
        conn = ''
        try:
            conn = sqlite3.connect('userInfo.db')
            conn.execute('select * from userTable')     # 用以判断用户表是否存在
        except sqlite3.OperationalError:
            # 表不存在就创建
            conn.execute('create table userTable(userId text,password text,balance int)')

        c = conn.cursor()
        while True:
            userId = raw_input("请输入注册ID：")
            if not userId.isdigit():
                print "########### ID应该为数字类型，请重新输入! ############"
                continue
            password = raw_input("请输入密码：")
            c.execute("select * from userTable where userId = ?",(userId,))
            if not c.fetchone():
                c.execute("insert into userTable values( ?, ?, ?)",(userId,password,0))
                print "########### 注册成功，请牢记您的用户Id和密码。 #############"
                break
            else:
                print "########### 用户已注册，请确认您的ID是否正确.... ############"
        conn.commit()
        c.close()
        conn.close()

    def login(self):
        self.__userId = raw_input("用户ID：")
        password = raw_input("密码：")
        print "################ 系统正在检测，请稍等………… ################"
        time.sleep(3)               # 模拟系统检测

        conn,c = '',''
        try:
            conn = sqlite3.connect('userInfo.db')
            c = conn.cursor()
            c.execute('select * from userTable where userId=?',(self.__userId,))

            # userTable(userId,password,balance)
            queryResult = c.fetchone()
            if queryResult and queryResult[1] == password:
                self.showGui()
                self.__balance = queryResult[2]
                self.handleOperates(c)
                self.updateUserInfo(c,self.__userId,self.__balance)
            else:
                print "############# 认证失败，输入的用户名或密码错误！#############"
        finally:
            conn.commit()
            c.close()
            conn.close()

    def handleOperates(self,cursor):
        while True:
            msg = ''
            try:
                num = input("请选择交易类型：")
                if (type(num) is int) and 1<=num<=5:
                    # 调用对应的处理方法
                    if num == 3:                # 处理转账服务
                        msg = (self.__operates[3])(cursor)
                    elif num == 5:              # 处理退出事务
                        self.__haveDone.append('-'*50)
                        self.logout()
                        break
                    else:
                        msg = (self.__operates[num])()
                else:
                    raise NameError
            except NameError:
                print "############# 无效输入！#############"
            if msg:
                self.__haveDone.append(msg)

    def updateUserInfo(self,cursor,userId,balance):
        cursor.execute('update userTable set balance =? where userId =?',(balance,userId))

    def saveMoney(self):
        try:
            account = input('存款金额？')
            if account >= 0:
                self.__balance += account
            else:
                raise NameError
            msg = '| %-20s %-20s  %-6s|' %(time.strftime('%Y-%m-%d %H:%M:%S'),'存款','+%d' %account)
        except NameError:
            print "################ 请输入有效金额 ^_^ #################"
            msg = ''
        return msg

    def getMoney(self):
        try:
            account = input('取款金额？')
            if account >= 0 and self.__balance >= account:
                self.__balance -= account
            else:
                raise NameError
            msg = '| %-20s %-20s  %-6s|' %(time.strftime('%Y-%m-%d %H:%M:%S'),'取款','-%d' %account)
        except NameError:
            print "################ 请输入有效金额 ^_^ ################## "
            msg = ''
        return msg

    def transferAccounts(self,cursor):
        try:
            toWhom = raw_input("转账对象？")
            cursor.execute('select * from userTable where userId=?',(toWhom,))
            otherInfo = cursor.fetchone()
            if not otherInfo or  otherInfo[0] == self.__userId:        # 不能转账给自己
                raise NameError

            account = input('转账金额？')
            if account >= 0 and self.__balance >= account:
                self.__balance -= account
                otherBalance = otherInfo[2]
                self.updateUserInfo(cursor,toWhom,otherBalance+account)
            else:
                raise NameError
            msg = '| %-20s %-20s   %-5s |' %(time.strftime('%Y-%m-%d %H:%M:%S'),'转账(至 %s)' %toWhom,'-%d' %account)
        except NameError:
            print "################ 请输入有效账户或金额 ^_^ ################## "
            msg = ''
        return msg

    def checkBalance(self):
        print '############### 当前余额为：￥%s #################' % self.__balance
        msg = '| %-20s %-20s    %-6s|' %(time.strftime('%Y-%m-%d %H:%M:%S'),'查询余额','---')
        return msg

    def printSlip(self):           #打印凭条
        for info in self.__haveDone:
            print info

    def logout(self):
        isShowSlip = raw_input("是否打印凭条？(y/no)")
        if isShowSlip.lower() == 'y':
            self.printSlip()

    def showGui(self):
        print """
                 ################# 登录成功，请选择操作类型 ###############
                 #                                                        #
                 #                        虚                              #
                 #  1、取款            /       \            2、存款       #
                 #                   拟   |   行                          #
                 #  3、转账          |   ----   |           4、查询余额   #
                 #                   网   |   银                          #
                 #  5、退出            \      /                           #
                 #                        上                              #
                 #                                                        #
                 ##########################################################
            """

if __name__ == '__main__':
    bank = Bank()
    bank.selectOperates()