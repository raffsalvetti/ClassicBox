import SQLiteHelper
from vec2d import vec2d
import time
import platform

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
        self.os = None
        self.emulator_group_id = None
        self.rom_dir = None
        self.preview_dir = None
        self.console_image_full_path = None

class Rom(SystemButton):
    def __init__(self):
        self.id = None
        self.name = None
        self.binary_name = None
        self.additional_argument = None
        self.emulator_group = None
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

class Config:
    def __init__(self):
        self.resolution = (800, 600)
        self.fontName = "CAFETA__"
        self.fullscreen = False
        #self.font_color = (0, 100, 186)
        self.font_color = (255, 255, 255)
    def get_st_res(self):
        return str(self.resolution[0]) + "x" + str(self.resolution[1])

class LogPlayRomSQLiteDataAccess:
    def __init__(self):
        pass
    def add_log(self, log_play_rom = None):
        if log_play_rom is None:
            return
        sql = "INSERT INTO log_play_rom (rom_id, pid) VALUES (" + str(log_play_rom.rom.id) + ", " + str(log_play_rom.pid) + ")"
        dbhelper = SQLiteHelper.SQLiteHelper("classicbox.sqlite")
        log_play_rom.id = dbhelper.InsertUpdateDelete(sql, True)
        return log_play_rom

    def update_log(self,  log_play_rom = None):
        if log_play_rom is None:
            return
        sql = "UPDATE log_play_rom SET end_time = '" + time.strftime("%Y-%m-%d %H:%M:%S") + "' WHERE id = " + str(log_play_rom.id)
        dbhelper = SQLiteHelper.SQLiteHelper("classicbox.sqlite")
        return dbhelper.InsertUpdateDelete(sql)

class GenreSQLiteDataAccess:
    def __init__(self):
        pass

    def get_all(self):
        sql = "SELECT id, name FROM genre ORDER BY name;"
        dbhelper = SQLiteHelper.SQLiteHelper("classicbox.sqlite")
        genres = []
        rs = dbhelper.Select(sql)
        for row in rs:
            g = Genre()
            g.id = row["id"]
            g.name = row["name"]
            genres.append(g)
        return genres

class EmulatorSQLiteDataAccess:
    def __init__(self):
        pass

    def get_all(self):
        sql = """SELECT
                    e.id,
                    eg.name,
                    e.executable_full_path,
                    e.base_arguments,
                    e.emulator_group_id,
                    eg.rom_dir,
                    eg.preview_dir,
                    eg.console_image_full_path
                FROM
                    emulator e
                JOIN
                    emulator_group eg ON eg.id = e.emulator_group_id
                WHERE
                    e.os = '{os}'
                ORDER BY
                    eg.name;""".format(os=platform.system())
        dbhelper = SQLiteHelper.SQLiteHelper("classicbox.sqlite")
        emulators = []
        rs = dbhelper.Select(sql)
        for row in rs:
            e = Emulator()
            e.id = row["id"]
            e.name = row["name"]
            e.executable_full_path = row["executable_full_path"]
            e.base_arguments = row["base_arguments"]
            e.emulator_group_id = row["emulator_group_id"]
            e.rom_dir = row["rom_dir"]
            e.preview_dir = row["preview_dir"]
            e.console_image_full_path = row["console_image_full_path"]
            emulators.append(e)
        return emulators

class RomSQLiteDataAccess:
    def __init__(self):
        pass

    def get_all(self):
        emulatorda = EmulatorSQLiteDataAccess()
        emulators = emulatorda.get_all()

        genreda = GenreSQLiteDataAccess()
        genres = genreda.get_all()

        sql = """SELECT
                    id,
                    name,
                    binary_name,
                    additional_argument,
                    emulator_group_id,
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
                    name;"""
        dbhelper = SQLiteHelper.SQLiteHelper(dbfile="classicbox.sqlite")
        roms = []
        rs = dbhelper.Select(sql)
        for row in rs:
            r = Rom()
            r.id = row["id"]
            r.name = row["name"]
            r.binary_name = row["binary_name"]
            r.additional_argument = row["additional_argument"]
            for e in emulators:
                if e.id == row["emulator_group_id"]:
                    r.emulator_group = e
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
        dbhelper = SQLiteHelper.SQLiteHelper(dbfile="classicbox.sqlite")
        return dbhelper.InsertUpdateDelete(sql)
