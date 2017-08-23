import urllib2
from HTMLParser import HTMLParser
import MySQLdb as mysql

class Game:
    def __init__(self):
        self.name = ""
        self.link = ""
        self.platform = ""
        self.genre = ""
        self.date = ""

class MysqlHelper():
    def __init__(self):
        pass
    def InsertUpdateDelete(self, games):
            try:
                con = mysql.connect('localhost', 'root', 'phobos', 'classicbox')
                cur = con.cursor()
                for g in games:
                    sql = "INSERT INTO temp_game (name, link, platform, genre, date) VALUES (%s, %s, %s, %s, %s)"
                    l = [g.name, g.link, g.platform, g.genre, g.date]
                    cur.execute(sql, l)
                con.commit()
            except mysql.Error as e:
                print "Erro executando " + sql + ":", e
                con.rollback()
            finally:    
                if con:    
                    con.close()

class LinksParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.filter_results = False
        self.tbody = False
        self.tr = False
        self.open_count = 0
        self.games = []
        self.game = None

    def handle_starttag(self, tag, attributes):
        if tag == "div":
            for k, v in attributes:
                if k == "id" and v == "filter_results":
                    self.filter_results = True
        
        if self.filter_results and tag == "tbody":
            self.tbody = True
            
        if self.filter_results and self.tbody and tag == "tr":
            self.tr = True
            self.game = Game()

        if self.filter_results and self.tbody and self.tr:
            self.open_count += 1
            
        if self.filter_results and self.tbody and self.tr and self.open_count == 3 and tag == "a":
            for k, v in attributes:
                if k == "href":
                    self.game.link = v.strip()

    def handle_data(self, data):
        if self.filter_results and self.tbody and self.tr:
            if self.game is None:
                print "Erro na logica"
                exit()
            else:
                if self.open_count == 3:
                    self.game.name = self.game.name + data.strip()
                if self.open_count == 5:
                    self.game.platform = self.game.platform + data.strip()
                elif self.open_count == 6:
                    self.game.genre = self.game.genre + data.strip()
                elif self.open_count == 9:
                    self.game.date = self.game.date + data.strip()
    
    def handle_endtag(self, tag):
        if self.tbody and tag == "tbody":
            self.tbody = False

        if self.filter_results and self.tbody:
            if tag == "tr":
                self.open_count = 0
                self.games.append(self.game)

class SiteParser:
    def __init__(self):
        #self.base_link = "http://www.gamespot.com/games.html?platform=21&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page=%PAG%"
        self.base_link = "http://www.gamespot.com/games.html?mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page=%PAG%"
        
    def get_into(self):
        for i in range(3743, 3744):
            print "lendo pagina " + str(i)
            r = urllib2.urlopen(self.base_link.replace("%PAG%", str(i)))
            l = LinksParser()
            l.feed(r.read())
            MysqlHelper().InsertUpdateDelete(l.games)

#            self.local_games.append(l.games)
#        
#        
#        myFile = open('snes.txt', 'w')
#        for lg in self.local_games:
#            for g in lg:
#                myFile.write("name: " + g.name + "\n")
#                myFile.write("link: " + g.link + "\n")
#                myFile.write("platform: " + g.platform + "\n")
#                myFile.write("genre: " + g.genre + "\n")
#                myFile.write("date: " + g.date + "\r\n")
#
#
#        myFile.flush()
#        myFile.close()

sp = SiteParser()
sp.get_into()