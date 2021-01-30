import sched, time, requests, json, os, re, random
from random import randrange


class SQLiMother:
    def __init__(self, token, chatIDs, admins):
        self.chatIDs = chatIDs
        self.admins = admins
        self.operations = []
        self.barneyPics = []
        self.s = sched.scheduler(time.time, time.sleep)
        self.secondsToWait = 5
        self.url = "https://api.telegram.org/bot" + token
        self.switcher = {"sqli": self.sqli, "wait": self.wait, }

    def sendMessage(self, text):
        for chatID in self.chatIDs:
            url = self.url + "/sendMessage" + "?chat_id=" + chatID + "&text=" + text
            requests.get(url)

    def sendPhoto(self, photo, text):
        for chatID in self.chatIDs:
            url = self.url + "/sendPhoto" + "?chat_id=" + chatID + "&photo=" + photo + "&caption" + text
            requests.get(url)

    def lastMessage(self):
        url = self.url + "/getUpdates"
        response = requests.post(url, data={"offset": -1, "limit": 1})
        messageJson = json.loads(response.text)
        userID = messageJson['result'][0]['message']['from']['id']
        if self.admin(str(userID)):
            message = messageJson['result'][0]['message']['text']
            return message

    def switch(self, l, *args):
        return self.switcher.get(l, self.default)(*args)

    def admin(self, userID):
        for admin in self.admins:
            if admin == userID:
                return True
            return False

    def error(self):
        self.sendMessage("Bir yerde hata yapıyorsun canım!")
        self.sendPhoto("https://watchingtvnow.com/wp-content/uploads/2018/11/barney-1024x715.jpg", "")

    def sqli(self, *args):
        status = self.operationChecker(args[0])
        if status == True:
            if self.urlValidator(args[1]):
                self.sendMessage(
                    "Merhaba Canısı! aşağıdaki adresi senin için tarıyor olacağım. Eğer sqli açığını tespit edebilirsem bunu sana hemen bildireceğim. {0}".format(
                        args[1]))
                self.sendPhoto("https://64.media.tumblr.com/tumblr_m3kigu1Zwj1qg6rkio1_500.gifv", "Challenge Accepted")
                os.system('sqlmap -u "' + args[
                    1] + '" -c sqlmother.ini --alert="python3 mother.py" --flush-session --batch --level 5 --risk 3 --tamper=space2comment </dev/null &>/dev/null &')
            else:
                self.error()

    def wait(self, *args):
        if (self.isAInt(args[0])):
            if args[1]:
                if args[1] == "hour":
                    print(args[0])
                    self.secondsToWait = int(args[0]) * 3600
                    self.sendMessage(
                        "{0} saat boyunca kendimi uyku moduna alacağım. Uyku modundan çıktıktan sonra gönderdiğin son komutu çalıştıracağım.".format(
                            int(args[0])))
                    self.barney()
                elif args[1] == "minute":
                    self.secondsToWait = int(args[0]) * 60
                    self.sendMessage(
                        "{0} dakika boyunca kendimi uyku moduna alacağım. Uyku modundan çıktıktan sonra gönderdiğin son komutu çalıştıracağım.".format(
                            int(args[0])))
                    self.barney()
                elif args[1] == "second":
                    self.sendMessage(
                        "{0} saniye boyunca kendimi uyku moduna alacağım. Uyku modundan çıktıktan sonra gönderdiğin son komutu çalıştıracağım.".format(
                            int(args[0])))
                    self.secondsToWait = int(args[0])
                    self.barney()
                else:
                    pass

    def default(self):
        pass

    def urlValidator(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, url) is not None

    def isAInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def operationChecker(self, text):
        count = self.operations.count(text)
        if count == 1:
            return False
        else:
            self.operations.append(text)
            return True

    def controller(self):
        lastMessage = self.lastMessage()
        if lastMessage:
            try:
                mode = lastMessage.split("|")[1]
                opn = lastMessage.split("|")[2]
                multiple = lastMessage.split("|")[3]
                level = lastMessage.split("|")[4]
                self.switch(mode, opn, multiple, level)
            except IndexError:
                pass

    def barney(self):
        url = "https://api.giphy.com/v1/gifs/search?offset=" + str(randrange(
            10)) + "&type=gifs&sort=recent&explore=true&q=barney%20stinson&api_key=Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g&pingback_id=5faab4ca0a1303c8"
        response = requests.get(url)
        stinson = json.loads(response.text)
        for i in stinson['data']:
            self.barneyPics.append(i["id"])
        barneyPic = "https://media.giphy.com/media/" + str(random.choice(self.barneyPics)) + "/giphy.gif"
        self.sendPhoto(barneyPic, "")

    def index(self, sc):
        self.controller()
        self.s.enter(self.secondsToWait, 1, self.index, (sc,))

    def start(self):
        self.s.enter(5, 1, self.index, (self.s,))
        self.s.run()


if __name__ == "__main__":
    go = SQLiMother("api-key", ["chatid"], ["id"])
    go.start()
