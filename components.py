from dom import *
import db


unit = pygame.image.load('img/item/unit.png').convert_alpha()
class itemInv:
    def __init__(self, Frame, imgData, Title = 'Item', Para = 'Item use description'):
        self.upgradable = False
        self.extendable = False
        self.buyable = False

        self.Title = Title
        self.Para = Para
        if 'Life' in Title:
            self.item_name = 'life'
        else:
            self.item_name = Title.lower()

        self.inv = Rect((Frame.rect.left + 8, 8 + Frame.rect.top + (8+100)*len(Frame.children), Frame.rect.width - 16, 100), bgColor = (255,255,255,205))
        self.inv.borderWidth(1)
        self.compClass = self

        self.imgBox = Rect((self.inv.rect.left + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.19, self.inv.rect.height - 8), bgColor = (255,255,255,255))
        self.imgBox.borderWidth(2)### 1
        self.image = Img(imgData['img'], imgData['w'], imgData['h'])# 1.1
        self.image.rect.center = self.imgBox.rect.center
        self.imgBox.addChild(self.image)#1 ###

        self.infoBox = Rect((self.imgBox.rect.right + 4, self.imgBox.rect.top, (self.inv.rect.width - 20) * 0.3, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 2
        self.infoBox.borderWidth(2)

        self.title = Text(self.Title, color = (255,0,255), font_size = 18)# 2.1
        self.title.rect.topleft = (self.infoBox.rect.left + 4, self.infoBox.rect.top + 6)

        self.para = Text(self.Para, color = (255,255,255), font_size = 10)# 2.2
        self.para.rect.topleft = (self.title.rect.left, self.title.rect.bottom + 8)
        self.para.setPara()
        self.infoBox.addChildren([self.title, self.para])#2 ###

    def addTo(self, Frame):
        self.index = len(Frame.children)
        Frame.addChild(self.inv)

    def reAddTo(self, Frame):
        Frame.children[self.index] = self.inv

    def updateDb(self, dbDoc):
        db.save(dbDoc)
        return db.document


class itemInv1(itemInv):
    def __init__(self, Frame, imgData, Title = 'Item', Para = 'Item use description', itemDoc = {}):
        super().__init__(Frame, imgData, Title, Para)
        self.upgradable = True

        self.itemDoc = itemDoc
        self.multiDoc = self.itemDoc["multi"]
        self.multiState = self.multiDoc['state']

        self.upgradeBox = Rect((self.infoBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 4
        self.upgradeBox.borderWidth(2)

        self.multiTxt = Text('x'+str(self.multiDoc["multis"][self.multiDoc['state']]["n"]), color = (255,125,255), font_size = 24)# 4.1
        self.multiTxt.rect.midtop = (self.upgradeBox.rect.centerx, self.upgradeBox.rect.top + 6)
        if self.multiState + 1 < len(self.multiDoc["multis"]):
            self.upgradeStr2 = 'Upgrade to x'+str(self.multiDoc["multis"][self.multiState + 1]["n"])
            self.upgradePrice = self.multiDoc["multis"][self.multiState + 1]["price"]
            self.upgradePurchasable = self.multiDoc["purchasable"] = True
        else:
            self.upgradeStr2 = 'Reached peak'
            self.upgradePrice = 0
            self.upgradePurchasable = self.multiDoc["purchasable"] = False
        self.upgradePriceStr = str(self.upgradePrice)

        self.upgradeTxt2 = Text(self.upgradeStr2, color = (255,255,255), font_size = 11)# 4.2
        self.upgradeTxt2.rect.centerx = self.upgradeBox.rect.centerx
        self.upgradeTxt2.rect.top = self.multiTxt.rect.bottom + 8

        self.upgradeBtn = Rect((self.upgradeBox.rect.left + 8, self.upgradeBox.rect.bottom - 26-8, self.upgradeBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.upgradeBtn.borderWidth(1)
        self.upgradeUnitImg = Img(unit.copy(), self.upgradeBtn.rect.height - 6, self.upgradeBtn.rect.height - 6)# 4.3.1
        self.upgradeUnitImg.rect.top = self.upgradeBtn.rect.top + 3
        self.upgradePriceTxt = Text(self.upgradePriceStr, color = (255,255,255), font_size = 14)# 4.3.2
        self.upgradeUnitImg.rect.left = self.upgradeBtn.rect.left + int((self.upgradeBtn.rect.width - (self.upgradeUnitImg.rect.width + self.upgradePriceTxt.rect.width)) / 2)
        self.upgradePriceTxt.rect.midleft = self.upgradeUnitImg.rect.midright
        self.upgradeBtn.addChildren([self.upgradeUnitImg, self.upgradePriceTxt])# 4.3 ###
        self.upgradeBox.addChildren([self.multiTxt, self.upgradeTxt2, self.upgradeBtn])# 4 ###

        self.inv.addChildren([self.imgBox, self.infoBox, self.upgradeBox])


    def render(self):
        self.upgradeBox = Rect((self.infoBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 4
        self.upgradeBox.borderWidth(2)

        self.multiTxt = Text('x'+str(self.multiDoc["multis"][self.multiDoc['state']]["n"]), color = (255,125,255), font_size = 24)# 4.1
        self.multiTxt.rect.midtop = (self.upgradeBox.rect.centerx, self.upgradeBox.rect.top + 6)
        if self.multiState + 1 < len(self.multiDoc["multis"]):
            self.upgradeStr2 = 'Upgrade to x'+str(self.multiDoc["multis"][self.multiState + 1]["n"])
            self.upgradePrice = self.multiDoc["multis"][self.multiState + 1]["price"]
            self.upgradePurchasable = self.multiDoc["purchasable"] = True
        else:
            self.upgradeStr2 = 'Reached peak'
            self.upgradePrice = 0
            self.upgradePurchasable = self.multiDoc["purchasable"] = False
        self.upgradePriceStr = str(self.upgradePrice)

        self.upgradeTxt2 = Text(self.upgradeStr2, color = (255,255,255), font_size = 11)# 4.2
        self.upgradeTxt2.rect.centerx = self.upgradeBox.rect.centerx
        self.upgradeTxt2.rect.top = self.multiTxt.rect.bottom + 8

        self.upgradeBtn = Rect((self.upgradeBox.rect.left + 8, self.upgradeBox.rect.bottom - 26-8, self.upgradeBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.upgradeBtn.borderWidth(1)
        self.upgradeUnitImg = Img(unit.copy(), self.upgradeBtn.rect.height - 6, self.upgradeBtn.rect.height - 6)# 4.3.1
        self.upgradeUnitImg.rect.top = self.upgradeBtn.rect.top + 3
        self.upgradePriceTxt = Text(self.upgradePriceStr, color = (255,255,255), font_size = 14)# 4.3.2
        self.upgradeUnitImg.rect.left = self.upgradeBtn.rect.left + int((self.upgradeBtn.rect.width - (self.upgradeUnitImg.rect.width + self.upgradePriceTxt.rect.width)) / 2)
        self.upgradePriceTxt.rect.midleft = self.upgradeUnitImg.rect.midright
        self.upgradeBtn.addChildren([self.upgradeUnitImg, self.upgradePriceTxt])# 4.3 ###
        self.upgradeBox.addChildren([self.multiTxt, self.upgradeTxt2, self.upgradeBtn])# 4 ###

        self.inv.children = []
        self.inv.addChildren([self.imgBox, self.infoBox, self.upgradeBox])

    def updateDb(self, dbDoc):
        if self.multiState + 1 < len(self.multiDoc["multis"]):
            self.multiDoc["purchasable"] = True
        else:
            self.multiDoc["purchasable"] = False
        self.multiDoc["state"] = self.multiState
        self.itemDoc["multi"] = self.multiDoc
        dbDoc["item"]['items'][self.item_name] = self.itemDoc
        dbDoc = itemInv.updateDb(self, dbDoc)

        self.itemDoc = dbDoc["item"]['items'][self.item_name]
        self.multiDoc = self.itemDoc["multi"]
        self.multiState = self.multiDoc['state']

        return dbDoc


class itemInv12(itemInv1):
    def __init__(self, Frame, imgData, Title = 'Item', Para = 'Item use description', itemDoc = {}, periodsDoc = {}):
        super().__init__(Frame, imgData, Title, Para, itemDoc)
        self.extendable = True

        self.periodDoc = self.itemDoc["period"]
        self.periodState = self.periodDoc["state"]
        self.periodsDoc = periodsDoc

        self.periodBox = Rect((self.upgradeBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 3
        self.periodBox.borderWidth(2)
        self.periodTxt = Text(str(self.periodsDoc[self.periodState]["t"])+'sec.', color = (255,125,255), font_size = 18)# 3.1
        self.periodTxt.rect.midtop = (self.periodBox.rect.centerx, self.periodBox.rect.top + 10)
        if self.periodState + 1 < len(self.periodsDoc):
            self.periodStr2 = 'Extend to %ds'%(self.periodsDoc[ self.periodState + 1 ]["t"])
            self.extendPrice = self.periodsDoc[ self.periodState + 1 ]["price"]
            self.extendPurchasable = self.periodDoc["purchasable"] = True
        else:
            self.periodStr2 = 'Reached limite'
            self.extendPrice = 0
            self.extendPurchasable = self.periodDoc["purchasable"] = False

        self.extendPriceStr = str(self.extendPrice)
        self.periodTxt2 = Text(self.periodStr2, color = (255,255,255), font_size = 11)# 4.2
        self.periodTxt2.rect.centerx = self.periodBox.rect.centerx
        self.periodTxt2.rect.top = self.periodTxt.rect.bottom + 10
        
        self.extendBtn = Rect((self.periodBox.rect.left + 8, self.periodBox.rect.bottom - 26-8, self.periodBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.extendBtn.borderWidth(1)
        self.periodUnitImg = Img(unit.copy(), self.extendBtn.rect.height - 6, self.extendBtn.rect.height - 6)# 4.3.1
        self.periodUnitImg.rect.top = self.extendBtn.rect.top + 3
        self.extendPriceTxt = Text(self.extendPriceStr, color = (255,255,255), font_size = 14)# 4.3.2
        self.periodUnitImg.rect.left = self.extendBtn.rect.left + int((self.extendBtn.rect.width - (self.periodUnitImg.rect.width + self.extendPriceTxt.rect.width)) / 2)
        self.extendPriceTxt.rect.midleft = self.periodUnitImg.rect.midright
        self.extendBtn.addChildren([self.periodUnitImg, self.extendPriceTxt])# 4.3 ###
        self.periodBox.addChildren([self.periodTxt, self.periodTxt2, self.extendBtn])

        self.inv.addChildren([self.periodBox])

    def render(self):
        itemInv1.render(self)
        self.periodBox = Rect((self.upgradeBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 3
        self.periodBox.borderWidth(2)
        self.periodTxt = Text(str(self.periodsDoc[self.periodState]["t"])+'sec.', color = (255,125,255), font_size = 18)# 3.1
        self.periodTxt.rect.midtop = (self.periodBox.rect.centerx, self.periodBox.rect.top + 10)
        if self.periodState + 1 < len(self.periodsDoc):
            self.periodStr2 = 'Extend to %ds'%(self.periodsDoc[ self.periodState + 1 ]["t"])
            self.extendPrice = self.periodsDoc[ self.periodState + 1 ]["price"]
            self.extendPurchasable = self.periodDoc["purchasable"] = True
        else:
            self.periodStr2 = 'Reached limite'
            self.extendPrice = 0
            self.extendPurchasable = self.periodDoc["purchasable"] = False

        self.extendPriceStr = str(self.extendPrice)
        self.periodTxt2 = Text(self.periodStr2, color = (255,255,255), font_size = 11)# 4.2
        self.periodTxt2.rect.centerx = self.periodBox.rect.centerx
        self.periodTxt2.rect.top = self.periodTxt.rect.bottom + 10
        
        self.extendBtn = Rect((self.periodBox.rect.left + 8, self.periodBox.rect.bottom - 26-8, self.periodBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.extendBtn.borderWidth(1)
        self.periodUnitImg = Img(unit.copy(), self.extendBtn.rect.height - 6, self.extendBtn.rect.height - 6)# 4.3.1
        self.periodUnitImg.rect.top = self.extendBtn.rect.top + 3
        self.extendPriceTxt = Text(self.extendPriceStr, color = (255,255,255), font_size = 14)# 4.3.2
        self.periodUnitImg.rect.left = self.extendBtn.rect.left + int((self.extendBtn.rect.width - (self.periodUnitImg.rect.width + self.extendPriceTxt.rect.width)) / 2)
        self.extendPriceTxt.rect.midleft = self.periodUnitImg.rect.midright
        self.extendBtn.addChildren([self.periodUnitImg, self.extendPriceTxt])# 4.3 ###
        self.periodBox.addChildren([self.periodTxt, self.periodTxt2, self.extendBtn])

        self.inv.addChildren([self.periodBox])

    def updateDb(self, dbDoc):
        dbDoc = itemInv1.updateDb(self, dbDoc)

        if self.periodState + 1 < len(self.periodsDoc):
            self.periodDoc["purchasable"] = True
        else:
            self.periodDoc["purchasable"] = False
        self.periodDoc["state"] = self.periodState
        self.itemDoc["period"] = self.periodDoc
        dbDoc["item"]['items'][self.item_name] = self.itemDoc
        itemInv.updateDb(self, dbDoc)

        self.periodDoc = self.itemDoc["period"]
        self.periodState = self.periodDoc["state"]




class itemInv2(itemInv):
    def __init__(self, Frame, imgData, Title = 'Item', Para = 'Item use description', itemDoc = {}, periodsDoc = {}):
        super().__init__(Frame, imgData, Title, Para)
        self.extendable = True

        self.itemDoc = itemDoc
        self.periodDoc = self.itemDoc["period"]
        self.periodState = self.periodDoc["state"]
        self.periodsDoc = periodsDoc

        self.periodBox = Rect((self.infoBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 3
        self.periodBox.borderWidth(2)
        self.periodTxt = Text(str(self.periodsDoc[self.periodState]["t"])+'sec.', color = (255,125,255), font_size = 18)# 3.1
        self.periodTxt.rect.midtop = (self.periodBox.rect.centerx, self.periodBox.rect.top + 10)
        if self.periodState + 1 < len(self.periodsDoc):
            self.periodStr2 = 'Extend to %ds'%(self.periodsDoc[ self.periodState + 1 ]["t"])
            self.extendPrice = self.periodsDoc[ self.periodState + 1 ]["price"]
            self.extendPurchasable = self.periodDoc["purchasable"] = True
        else:
            self.periodStr2 = 'Reached limite'
            self.extendPrice = 0
            self.extendPurchasable = self.periodDoc["purchasable"] = False

        self.extendPriceStr = str(self.extendPrice)
        self.periodTxt2 = Text(self.periodStr2, color = (255,255,255), font_size = 11)# 4.2
        self.periodTxt2.rect.centerx = self.periodBox.rect.centerx
        self.periodTxt2.rect.top = self.periodTxt.rect.bottom + 10
        
        self.extendBtn = Rect((self.periodBox.rect.left + 8, self.periodBox.rect.bottom - 26-8, self.periodBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.extendBtn.borderWidth(1)
        self.periodUnitImg = Img(unit.copy(), self.extendBtn.rect.height - 6, self.extendBtn.rect.height - 6)# 4.3.1
        self.periodUnitImg.rect.top = self.extendBtn.rect.top + 3
        self.extendPriceTxt = Text(self.extendPriceStr, color = (255,255,255), font_size = 14)# 4.3.2
        self.periodUnitImg.rect.left = self.extendBtn.rect.left + int((self.extendBtn.rect.width - (self.periodUnitImg.rect.width + self.extendPriceTxt.rect.width)) / 2)
        self.extendPriceTxt.rect.midleft = self.periodUnitImg.rect.midright
        self.extendBtn.addChildren([self.periodUnitImg, self.extendPriceTxt])# 4.3 ###
        self.periodBox.addChildren([self.periodTxt, self.periodTxt2, self.extendBtn])

        self.inv.addChildren([self.imgBox, self.infoBox, self.periodBox])
    

    def render(self):
        self.periodBox = Rect((self.infoBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 3
        self.periodBox.borderWidth(2)
        self.periodTxt = Text(str(self.periodsDoc[self.periodState]["t"])+'sec.', color = (255,125,255), font_size = 18)# 3.1
        self.periodTxt.rect.midtop = (self.periodBox.rect.centerx, self.periodBox.rect.top + 10)
        if self.periodState + 1 < len(self.periodsDoc):
            self.periodStr2 = 'Extend to %ds'%(self.periodsDoc[ self.periodState + 1 ]["t"])
            self.extendPrice = self.periodsDoc[ self.periodState + 1 ]["price"]
            self.extendPurchasable = self.periodDoc["purchasable"] = True
        else:
            self.periodStr2 = 'Reached limite'
            self.extendPrice = 0
            self.extendPurchasable = self.periodDoc["purchasable"] = False

        self.extendPriceStr = str(self.extendPrice)
        self.periodTxt2 = Text(self.periodStr2, color = (255,255,255), font_size = 11)# 4.2
        self.periodTxt2.rect.centerx = self.periodBox.rect.centerx
        self.periodTxt2.rect.top = self.periodTxt.rect.bottom + 10
        
        self.extendBtn = Rect((self.periodBox.rect.left + 8, self.periodBox.rect.bottom - 26-8, self.periodBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.extendBtn.borderWidth(1)
        self.periodUnitImg = Img(unit.copy(), self.extendBtn.rect.height - 6, self.extendBtn.rect.height - 6)# 4.3.1
        self.periodUnitImg.rect.top = self.extendBtn.rect.top + 3
        self.extendPriceTxt = Text(self.extendPriceStr, color = (255,255,255), font_size = 14)# 4.3.2
        self.periodUnitImg.rect.left = self.extendBtn.rect.left + int((self.extendBtn.rect.width - (self.periodUnitImg.rect.width + self.extendPriceTxt.rect.width)) / 2)
        self.extendPriceTxt.rect.midleft = self.periodUnitImg.rect.midright
        self.extendBtn.addChildren([self.periodUnitImg, self.extendPriceTxt])# 4.3 ###
        self.periodBox.addChildren([self.periodTxt, self.periodTxt2, self.extendBtn])

        self.inv.children = []
        self.inv.addChildren([self.imgBox, self.infoBox, self.periodBox])

    def updateDb(self, dbDoc):
        if self.periodState + 1 < len(self.periodsDoc):
            self.periodDoc["purchasable"] = True
        else:
            self.periodDoc["purchasable"] = False
        self.periodDoc["state"] = self.periodState
        self.itemDoc["period"] = self.periodDoc
        dbDoc["item"]['items'][self.item_name] = self.itemDoc
        itemInv.updateDb(self, dbDoc)

        self.periodDoc = self.itemDoc["period"]
        self.periodState = self.periodDoc["state"]




class itemInv3(itemInv):
    def __init__(self, Frame, imgData, Title = 'Item', Para = 'Item use description', itemDoc = {}):
        super().__init__(Frame, imgData, Title, Para)
        self.buyable = True

        self.itemDoc = itemDoc
        self.bought = self.itemDoc["bought"]
        self.price = self.itemDoc["price"]

        self.buyBox = Rect((self.infoBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 4
        self.buyBox.borderWidth(2)
        self.boughtTxt = Text(str(self.bought), color = (255,125,255), font_size = 24)# 4.1
        self.boughtTxt.rect.midtop = (self.buyBox.rect.centerx, self.buyBox.rect.top + 6)
        self.boughtTxt2 = Text('Buy', color = (255,255,255), font_size = 14)# 4.2
        self.boughtTxt2.rect.centerx = self.buyBox.rect.centerx
        self.boughtTxt2.rect.top = self.boughtTxt.rect.bottom + 8
        self.buyBtn = Rect((self.buyBox.rect.left + 8, self.buyBox.rect.bottom - 26-8, self.buyBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.buyBtn.borderWidth(1)
        self.unitImg = Img(unit.copy(), self.buyBtn.rect.height - 6, self.buyBtn.rect.height - 6)# 4.3.1
        self.unitImg.rect.top = self.buyBtn.rect.top + 3
        self.priceTxt = Text(str(self.price), color = (255,255,255), font_size = 14)# 4.3.2
        self.unitImg.rect.left = self.buyBtn.rect.left + int((self.buyBtn.rect.width - (self.unitImg.rect.width + self.priceTxt.rect.width)) / 2)
        self.priceTxt.rect.midleft = self.unitImg.rect.midright
        self.buyBtn.addChildren([self.unitImg, self.priceTxt])# 4.3 ###
        self.buyBox.addChildren([self.boughtTxt, self.boughtTxt2, self.buyBtn])# 4 ###

        self.inv.addChildren([self.imgBox, self.infoBox, self.buyBox])

    def render(self):
        self.buyBox = Rect((self.infoBox.rect.right + 4, self.inv.rect.top + 4, (self.inv.rect.width - 20) * 0.255, self.inv.rect.height - 8), bgColor = (255,255,255,255))### 4
        self.buyBox.borderWidth(2)
        self.boughtTxt = Text(str(self.bought), color = (255,125,255), font_size = 24)# 4.1
        self.boughtTxt.rect.midtop = (self.buyBox.rect.centerx, self.buyBox.rect.top + 6)
        self.boughtTxt2 = Text('Buy', color = (255,255,255), font_size = 14)# 4.2
        self.boughtTxt2.rect.centerx = self.buyBox.rect.centerx
        self.boughtTxt2.rect.top = self.boughtTxt.rect.bottom + 8
        self.buyBtn = Rect((self.buyBox.rect.left + 8, self.buyBox.rect.bottom - 26-8, self.buyBox.rect.width - 8*2, 26), bgColor = (255,255,255,255))# 4.3
        self.buyBtn.borderWidth(1)
        self.unitImg = Img(unit.copy(), self.buyBtn.rect.height - 6, self.buyBtn.rect.height - 6)# 4.3.1
        self.unitImg.rect.top = self.buyBtn.rect.top + 3
        self.priceTxt = Text(str(self.price), color = (255,255,255), font_size = 14)# 4.3.2
        self.unitImg.rect.left = self.buyBtn.rect.left + int((self.buyBtn.rect.width - (self.unitImg.rect.width + self.priceTxt.rect.width)) / 2)
        self.priceTxt.rect.midleft = self.unitImg.rect.midright
        self.buyBtn.addChildren([self.unitImg, self.priceTxt])# 4.3 ###
        self.buyBox.addChildren([self.boughtTxt, self.boughtTxt2, self.buyBtn])# 4 ###

        self.inv.children = []
        self.inv.addChildren([self.imgBox, self.infoBox, self.buyBox])
    
    def updateDb(self, dbDoc):
        self.itemDoc["bought"] = self.bought
        dbDoc["item"]['items'][self.item_name] = self.itemDoc
        dbDoc = itemInv.updateDb(self, dbDoc)
        self.itemDoc = dbDoc["item"]['items'][self.item_name]
        self.bought = self.itemDoc["bought"]














lifeGem = pygame.image.load('img/item/gem.png').convert_alpha()
lifeGemAR = lifeGem.get_width() / lifeGem.get_height()
class Modal:
    def __init__(self, Frame):
        self.lifeGemImg = Img(lifeGem, w = 30, h = round(30/lifeGemAR))
        self.lifeGemCount = db.document["item"]["items"]["life"]["bought"]
        self.lifeGemCountTxt = Text(str(self.lifeGemCount), color = (255,255,255,75), font_size = 28)
        self.lifeGemCountTxt.rect.left = self.lifeGemImg.rect.right = Frame.rect.centerx
        self.lifeGemImg.rect.top = Frame.rect.top + 10
        self.lifeGemCountTxt.rect.centery = self.lifeGemImg.rect.centery

        self.header = Text('CONTINUE', color = (255,255,255,75), font_size = 18)
        self.header.rect.midtop = (Frame.rect.centerx, self.lifeGemImg.rect.bottom + 16)

        self.infoTxt = Text('Use 1 life Gem out of '+str(self.lifeGemCount), color = (255,255,255,75), font_size = 13)
        self.infoTxt.rect.midtop = (self.header.rect.centerx, self.header.rect.bottom + 6)

        self.yesBtn = Rect((0,0,65,35), bgColor = (255,255,255,75))
        self.yesBtn.rect.left = Frame.rect.left + 30
        self.yesBtn.rect.top = self.infoTxt.rect.bottom + 18
        self.yesBtn.borderWidth(2)
        self.yesBtn.addChild( Text('Yes', color = (255,255,255,75)) )
        self.yesBtn.center_children()

        self.noBtn = Rect((0,0,65,35), bgColor = (255,255,255,75))
        self.noBtn.rect.right = Frame.rect.right - 30
        self.noBtn.rect.top = self.infoTxt.rect.bottom + 18
        self.noBtn.borderWidth(2)
        self.noBtn.addChild( Text('No', color = (255,255,255,75)) )
        self.noBtn.center_children()

        Frame.addChildren([self.lifeGemImg, self.lifeGemCountTxt, self.header, self.infoTxt, self.yesBtn, self.noBtn])

    def render(self, Frame):
        self.lifeGemImg = Img(lifeGem, w = 30, h = round(30/lifeGemAR))
        self.lifeGemCount = db.document["item"]["items"]["life"]["bought"]
        self.lifeGemCountTxt = Text(str(self.lifeGemCount), color = (255,255,255,75), font_size = 28)
        self.lifeGemCountTxt.rect.left = self.lifeGemImg.rect.right = Frame.rect.centerx
        self.lifeGemImg.rect.top = Frame.rect.top + 10
        self.lifeGemCountTxt.rect.centery = self.lifeGemImg.rect.centery

        self.header = Text('CONTINUE', color = (255,255,255,75), font_size = 18)
        self.header.rect.midtop = (Frame.rect.centerx, self.lifeGemImg.rect.bottom + 16)

        self.infoTxt = Text('Use 1 life Gem out of '+str(self.lifeGemCount), color = (255,255,255,75), font_size = 12)
        self.infoTxt.rect.midtop = (self.header.rect.centerx, self.header.rect.bottom + 6)

        self.yesBtn = Rect((0,0,65,35), bgColor = (255,255,255,75))
        self.yesBtn.rect.left = Frame.rect.left + 30
        self.yesBtn.rect.top = self.infoTxt.rect.bottom + 18
        self.yesBtn.borderWidth(2)
        self.yesBtn.addChild( Text('Yes', color = (255,255,255,75)) )
        self.yesBtn.center_children()

        self.noBtn = Rect((0,0,65,35), bgColor = (255,255,255,75))
        self.noBtn.rect.right = Frame.rect.right - 30
        self.noBtn.rect.top = self.infoTxt.rect.bottom + 18
        self.noBtn.borderWidth(2)
        self.noBtn.addChild( Text('No', color = (255,255,255,75)) )
        self.noBtn.center_children()

        Frame.children = []
        Frame.addChildren([self.lifeGemImg, self.lifeGemCountTxt, self.header, self.infoTxt, self.yesBtn, self.noBtn])

