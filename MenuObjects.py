from SQLiteHelper import SQLiteHelper
from vec2d import vec2d
import time
from ConfigParser import ConfigParser

class SystemButton:
    def __init__(self):
        self.icon = None
        self.location = vec2d(0, 0)
        self.size = vec2d(0, 0)
        self.value = None
        self.is_clicable = True
    def getBounds(self, border = 0):
        return (self.location.x + border / 2, self.location.y + border / 2, self.size.x - border, self.size.y - border)

class Genre:
    def __init__(self):
        self.id = None
        self.name = None

class Emulator(SystemButton):
    def __init__(self):
        self.id = None
        self.name = None
        self.executable_full_path = None
        self.base_arguments = None
        self.rom_dir = None
        self.preview_dir = None
        self.console_image_full_path = None

class Rom(SystemButton):
    def __init__(self):
        self.id = None
        self.name = None
        self.binary_name = None
        self.additional_argument = None
        self.emulator = None
        self.genre = None
        self.year = None
        self.developer = None
        self.publisher = None
        self.install_date = None
        self.max_players = None
        self.last_play = None
        self.play_count = None
        
class  LogPlayRom:
    def __init__(self, rom = None, pid = None):
        self.id = None
        self.rom = rom
        self.start_time = None
        self.end_time = None
        self.pid = pid

class Config(object):
    self._instance = None
    
    def __init__(self):
        cp = ConfigParser()
        cp.read("ClassicBox.cfg")
        # system
        self.override_database = eval(cp.get("system", "override_database"))
        self.log_filename = cp.get("system", "log_filename")
        self.button_start_code = cp.get("system", "button_start_code")
        self.button_select_code = cp.get("system", "button_select_code")
        # paths
        self.log_path = cp.get("paths", "log_path")
        self.font_path = cp.get("paths", "font_path")
        self.sound_path = cp.get("paths", "sound_path")
        self.emulator_path = cp.get("paths", "emulator_path")
        self.rom_path = cp.get("paths", "rom_path")
        self.database_path = cp.get("paths", "database")
        # video
        self.resolution = cp.get("video", "resolution").split('x')
        self.background = cp.get("video", "background")
        self.font = cp.get("video", "font")
        self.fullscreen = eval(cp.get("video", "fullscreen"))
        self.selection_color = eval(cp.get("video", "selection_color"))
        self.font_color = eval(cp.get("video", "font_color"))
        # sound
        self.navigate_sound = cp.get("sound", "navigate")
        self.select_sound = cp.get("sound", "select")
        # database
        self.database_filename = cp.get("database", "filename")

    def get_st_res(self):
        return str(self.resolution[0]) + "x" + str(self.resolution[1])

class MySQLiteDataAccess(SQLiteHelper):
    def __init__(self):
        c = Config()
        super(MySQLiteDataAccess, self, str(c.database_path) + "/" + str(c.database_filename)).__init__()


class LogPlayRomSQLiteDataAccess(MySQLiteDataAccess):
    def __init__(self):
        pass
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
        pass
    
    def get_all(self):
        sql = "SELECT id, name FROM genre ORDER BY name;"
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
        pass
    
    def get_all(self):
        sql = "SELECT id, name, executable_full_path, base_arguments, rom_dir, preview_dir, console_image_full_path FROM emulator ORDER BY name;"
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
        pass
    
    def get_all(self):
        emulatorda = EmulatorSQLiteDataAccess()
        emulators = emulatorda.get_all()
        
        genreda = GenreSQLiteDataAccess()
        genres = genreda.get_all()
        
        sql = "SELECT id, name, binary_name, additional_argument, emulator_id, genre_id, year, developer, publisher, install_date, last_play, max_players, play_count FROM rom ORDER BY name;"
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
    