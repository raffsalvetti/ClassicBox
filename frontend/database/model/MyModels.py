from frontend.components.System import SystemButton

class BaseModel(object):
    def __init__(self):
        pass

class Genre(BaseModel):
    def __init__(self):
        self.id = None
        self.name = None

class Emulator(BaseModel, SystemButton):
    def __init__(self):
        self.id = None
        self.name = None
        self.executable_full_path = None
        self.base_arguments = None
        self.rom_dir = None
        self.preview_dir = None
        self.console_image_full_path = None

class Rom(BaseModel, SystemButton):
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
        
class  LogPlayRom(BaseModel):
    def __init__(self, rom = None, pid = None):
        self.id = None
        self.rom = rom
        self.start_time = None
        self.end_time = None
        self.pid = pid