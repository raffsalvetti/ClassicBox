from ConfigParser import ConfigParser

class Config(object):
    def __init__(self):
        print("lendo configuracoes")
        cp = ConfigParser()
        cp.read("ClassicBox.cfg")
        # system
        self.override_database = eval(cp.get("system", "override_database"))
        self.log_filename = cp.get("system", "log_filename")
        self.button_start_code = cp.get("system", "button_start_code")
        self.button_select_code = cp.get("system", "button_select_code")
        # paths
        self.log_path = cp.get("paths", "log")
        self.font_path = cp.get("paths", "font")
        self.sound_path = cp.get("paths", "sound")
        self.emulator_path = cp.get("paths", "emulator")
        self.rom_path = cp.get("paths", "rom")
        self.database_path = cp.get("paths", "database")
        # video
        self.resolution = tuple([int(i) for i in cp.get("video", "resolution").split('x')])
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