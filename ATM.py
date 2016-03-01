#coding:utf-8
from bank import Bank

class Atm(Bank):
    """
        本类用以模拟取款机的功能
    """
    def __init__(self):
        super(Atm,self).__init__()

if __name__=='__main__':
    atm = Atm()
    atm.login()