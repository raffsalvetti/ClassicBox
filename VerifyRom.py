from subprocess import Popen
from os import listdir
from os.path import isfile, join

class FileRomHelper():
    def __init__(self):
        pass
    def get_rom_files_from_dir(self, path):
        rom_files = []
        for f in listdir(path): 
            if isfile(join(path, f)):
                rom_files.append(f)
        return rom_files

roms = FileRomHelper().get_rom_files_from_dir(r"rom\mame")
f = open("saida.txt", "w")
for r in roms:
    l = r"emulator\mame0140b\mame.exe %ROM% -verifyroms -rompath rom\mame".replace("%ROM%", r.split('.')[0])
    #f.write("executando: %s\n" %l)
    f.flush()
    Popen(l, stdout=f)
f.close()