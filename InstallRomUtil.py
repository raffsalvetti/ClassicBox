from os import listdir
from os.path import isfile, join
import re
import MySQLdb as mysql
from SQLiteHelper import SQLiteHelper
import MenuObjects
import sys
import os
from MenuObjects import EmulatorSQLiteDataAccess, GenreSQLiteDataAccess

class MysqlHelper():
    def __init__(self):
        pass
    def Select(self, console):
        data = None
        try:
            con = mysql.connect('localhost', 'root', 'phobos', 'classicbox')
            cur = con.cursor()
            sql = "select name, genre , date, id from temp_game where platform = '%s' order by name"
            cur.execute(sql %console)
            data = cur.fetchall()
        except mysql.Error as e:
            print "Erro executando " + sql + ":", e
        finally:    
            if con:    
                con.close()
        return data

class FileRomHelper():
    def __init__(self):
        pass
    def get_rom_files_from_dir(self, path):
        rom_files = []
        for f in listdir(path): 
            if isfile(join(path, f)):
                rom_files.append(f)
        return rom_files

class InstallRomHelper():
    def __init__(self):
        pass
    
    def clean_name(self, name):
        return re.sub(r'\.zip', '', re.sub(r'\[[^]]*\]', '' ,re.sub(r'\([^)]*\)', '', name))).strip()
    
    def run(self):
        emulador = (2, 'SNES') #(codigo da tabela emulator, descricao da plataforma na tabela temp_game do mysql)
        insert_file = open(emulador[1] + ".txt", "w")
        emu = EmulatorSQLiteDataAccess().get_all()
        rom_files = []
        all_games = MysqlHelper().Select(emulador[1])
        genres = GenreSQLiteDataAccess().get_all()
        counter = 0
        for e in emu:
            if e.id == emulador[0]:
                rom_files = FileRomHelper().get_rom_files_from_dir(e.rom_dir)
                break
        for g in all_games:
            for rf in rom_files[:]:
                if self.clean_name(rf) == g[0].strip():
                    for gen in genres:
                        if gen.name == g[1].strip():
                            sql = "INSERT INTO rom (name, binary_name, emulator_id, genre_id, year, max_players) VALUES ('%s', '%s', %s, %s, '%s', %s);\n" %(g[0].strip(), rf.strip(), emulador[0], gen.id, g[2].strip(), 2)
                            counter += 1
                            rom_files.remove(rf)
                            insert_file.write(sql)
        insert_file.write("as seguinte roms nao foram encontradas:\n")
        for rf in rom_files:
            insert_file.write(rf + "\n")
        insert_file.write("total de roms instaladas: %s" % counter)
        insert_file.flush()
        insert_file.close()
        

InstallRomHelper().run()
