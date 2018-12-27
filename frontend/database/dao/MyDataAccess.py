from SQLiteHelper import SQLiteHelper

from frontend.components.Config import Config
from frontend.database.model.MyModels import Genre, Emulator, Rom

import time

class MySQLiteDataAccess(SQLiteHelper):
    def __init__(self):
        config = Config()
        super(MySQLiteDataAccess, self).__init__(str(config.database_path) + "/" + str(config.database_filename))

class LogPlayRomSQLiteDataAccess(MySQLiteDataAccess):
    def __init__(self):
        super(LogPlayRomSQLiteDataAccess, self).__init__()

    def add_log(self, log_play_rom = None):
        if log_play_rom is None:
            return
        sql = "INSERT INTO log_play_rom (rom_id, pid) VALUES (" + str(log_play_rom.rom.id) + ", " + str(log_play_rom.pid) + ")"
        log_play_rom.id = self.InsertUpdateDelete(sql, True)
        return log_play_rom
    
    def update_log(self,  log_play_rom = None):
        if log_play_rom is None:
            return
        sql = "UPDATE log_play_rom SET end_time = '" + time.strftime("%Y-%m-%d %H:%M:%S") + "' WHERE id = " + str(log_play_rom.id)
        return self.InsertUpdateDelete(sql)
        
class GenreSQLiteDataAccess(MySQLiteDataAccess):
    def __init__(self):
        super(GenreSQLiteDataAccess, self).__init__()
    
    def get_all(self):
        sql = """
                SELECT 
                    id, 
                    name 
                FROM 
                    genre 
                ORDER BY 
                    name;
        """
        genres = []
        rs = self.Select(sql)
        for row in rs:
            g = Genre()
            g.id = row["id"]
            g.name = row["name"]
            genres.append(g)
        return genres

class EmulatorSQLiteDataAccess(MySQLiteDataAccess):
    def __init__(self):
        super(EmulatorSQLiteDataAccess, self).__init__()
    
    def get_all(self):
        sql = """
                SELECT 
                    id, 
                    name, 
                    executable_full_path, 
                    base_arguments, 
                    rom_dir, 
                    preview_dir, 
                    console_image_full_path 
                FROM 
                    emulator 
                ORDER BY 
                    name;
        """
        emulators = []
        rs = self.Select(sql)
        for row in rs:
            e = Emulator()
            e.id = row["id"]
            e.name = row["name"]
            e.executable_full_path = row["executable_full_path"]
            e.base_arguments = row["base_arguments"]
            e.rom_dir = row["rom_dir"]
            e.preview_dir = row["preview_dir"]
            e.console_image_full_path = row["console_image_full_path"]
            emulators.append(e)
        return emulators

class RomSQLiteDataAccess(MySQLiteDataAccess):
    def __init__(self):
        super(RomSQLiteDataAccess, self).__init__()
    
    def get_all(self):
        emulatorda = EmulatorSQLiteDataAccess()
        emulators = emulatorda.get_all()
        
        genreda = GenreSQLiteDataAccess()
        genres = genreda.get_all()
        
        sql = """
                SELECT 
                    id, 
                    name, 
                    binary_name, 
                    additional_argument, 
                    emulator_id, 
                    genre_id, 
                    year, 
                    developer, 
                    publisher, 
                    install_date, 
                    last_play, 
                    max_players, 
                    play_count 
                FROM 
                    rom 
                ORDER BY 
                    name;
        """
        roms = []
        rs = self.Select(sql)
        for row in rs:
            r = Rom()
            r.id = row["id"]
            r.name = row["name"]
            r.binary_name = row["binary_name"]
            r.additional_argument = row["additional_argument"]
            for e in emulators:
                if e.id == row["emulator_id"]:
                    r.emulator = e
                    break
            for g in genres:
                if g.id == row["genre_id"]:
                    r.genre = g
                    break
            r.year = row["year"]
            r.developer = row["developer"]
            r.publisher = row["publisher"]
            r.install_date = row["install_date"]
            r.last_play = row["last_play"]
            r.max_players = row["max_players"]
            r.play_count = row["play_count"]
            roms.append(r)
        return roms
    
    def update_play_time(self, rom):
        rom.last_play = time.strftime("%Y-%m-%d %H:%M:%S")
        rom.play_count = rom.play_count + 1
        sql = "UPDATE rom SET last_play = '" + rom.last_play + "', play_count = " + str(rom.play_count) + " WHERE id = " + str(rom.id)
        return self.InsertUpdateDelete(sql)