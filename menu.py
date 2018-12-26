from pygamehelper import PygameHelper
from MenuObjects import Emulator, \
                        Rom, \
                        SystemButton, \
                        EmulatorSQLiteDataAccess, \
                        RomSQLiteDataAccess, \
                        Config, LogPlayRomSQLiteDataAccess, LogPlayRom
import sys
from vec2d import vec2d
import pygame
from subprocess import Popen
import time
import logging

class Starter(PygameHelper):
    def __init__(self):
        logging.basicConfig(filename='log/menu.log', format="%(asctime)s - %(levelname)s - %(funcName)s --> %(message)s", filemode="w", level=logging.DEBUG)
        self.config = Config()
        PygameHelper.__init__(self, size=(self.config.resolution[0], self.config.resolution[1]), fill=((0,0,0)))
        self.j0_START = 9
        self.j0_SELECT = 8
        
        self.rom_list_font = None
        self.generic_font = None
        
        self.select_sound_cursor = None
        self.select_sound_validate = None
        
        self.selection_color = (255, 0, 0)
        self.selection_color_fade_order = False
        
        self.emulators = []
        self.roms = []
        self.system_buttons = []
        
        self.background_image = None
        self.rom_list_select_image = None
        
        self.load_emulators()
        self.load_roms()
        self.load_components()
        
        self.current_selected_item = None
        self.current_selected_emulator = None
        self.current_selected_emulator_process = None
        self.current_selected_rom = None
        
        self.current_page = 0
        self.current_page_itens = list()
        self.current_play_log_rom = None
        
        self.j0select = False
        self.j0start = False
        
        self.all_clickable_list = None
        
        try:
            logging.info("selecionando valores iniciais para emulador e roms")
            if len(self.emulators) > 0:
                self.current_selected_emulator = self.emulators[0]
                self.current_page_itens = self.get_itens_by_page(self.find_roms_by_emulator_code(), 6, self.current_page)
                self.current_selected_item = self.current_selected_emulator
                self.all_clickable_list = [self.emulators, self.current_page_itens, self.system_buttons]
        except Exception, e:
            logging.error("nao foi possivel selecionar valores iniciais para o emulador e as roms do emulador: %s", e)
        
    def load_components(self):
        logging.info("carregando componentes basicos...")
        
        try:
            logging.debug("carregando imagens basicas...")
            self.background_image = pygame.image.load("images/Background" + self.config.get_st_res() + ".png")
            self.rom_list_select_image = pygame.image.load("images/RomListSelect" + self.config.get_st_res() + ".png")
            self.rom_list_font = pygame.font.Font("fonts/" + self.config.fontName + ".ttf", 25)
            self.generic_font = pygame.font.Font("fonts/" + self.config.fontName + ".ttf", 10)
            self.select_sound_cursor = pygame.mixer.Sound("sounds/menu-change-selection.wav")
            self.select_sound_validate = pygame.mixer.Sound("sounds/menu-validate.wav")
        except Exception, e:
            logging.fatal("nao foi possivel carregar imagens basicas: %s", e)
            pygame.quit()

        try:
            logging.debug("carregando emuladores...")
            #carga de icones dos emuladores
            for i in range(0, len(self.emulators)):
                self.emulators[i].icon = pygame.image.load("images/" + self.emulators[i].console_image_full_path + self.config.get_st_res() + ".png")
                self.emulators[i].size = vec2d(self.emulators[i].icon.get_size())
                self.emulators[i].location = vec2d(i * self.emulators[i].size.x, 0)
        except Exception, e:
            logging.fatal("nao foi possivel carregar emuladores: %s", e)
            pygame.quit()
        
        try:
            for i in range(0, len(self.roms)):
                self.roms[i].icon = self.rom_list_select_image
                self.roms[i].size = vec2d(self.roms[i].icon.get_size())
        except Exception, e:
            logging.fatal("nao foi possivel carregar roms: %s", e)
            pygame.quit()
            
        try:
            logging.debug("carregando botao de configuracao...")
            #carga do botao configuracao
            b = SystemButton()
            b.icon = pygame.image.load("images/controlPannel" + self.config.get_st_res() + ".png")
            b.size = vec2d(b.icon.get_size())
            b.location = vec2d((len(self.emulators) + len(self.system_buttons)) * b.size.x, 0)
            b.value = "config"
            self.system_buttons.append(b)
            
            logging.debug("carregando botao sair...")
            #carga do botao sair
            b = SystemButton()
            b.icon = pygame.image.load("images/exit" + self.config.get_st_res() + ".png")
            b.size = vec2d(b.icon.get_size())
            b.location = vec2d((len(self.emulators) + len(self.system_buttons)) * b.size.x, 0)
            b.value = "quit"
            self.system_buttons.append(b)
            
            logging.debug("carregando botao pageup...")
            #carga do botao pagina anterior
            b = SystemButton()
            b.icon = pygame.image.load("images/ScrollArrowUp" + self.config.get_st_res() + ".png")
            b.size = vec2d(b.icon.get_size())
            b.location = vec2d(740, 150)
            b.value = "pageUp"
            self.system_buttons.append(b)
            
            logging.debug("carregando botao pagedown...")
            #carga do botao pagina posterior
            b = SystemButton()
            b.icon = pygame.image.load("images/ScrollArrowDown" + self.config.get_st_res() + ".png")
            b.size = vec2d(b.icon.get_size())
            b.location = vec2d(740, 540)
            b.value = "pageDown"
            self.system_buttons.append(b)
            
            logging.debug("carregando botao orderbyname...")
            b = SystemButton()
            b.icon = pygame.image.load("images/romName" + self.config.get_st_res() + ".png")
            b.size = vec2d(b.icon.get_size())
            b.location = vec2d(140, 100)
            b.value = "orderByName"
            self.system_buttons.append(b)
    
            logging.debug("carregando botao orderbycounter...")
            b = SystemButton()
            b.icon = pygame.image.load("images/playCount" + self.config.get_st_res() + ".png")
            b.size = vec2d(b.icon.get_size())
            b.location = vec2d(200, 100)
            b.value = "orderByCounter"
            self.system_buttons.append(b)
            
        except Exception, e:
            logging.fatal("nao foi possivel carregar botoes de controle: %s", e)
            pygame.quit()

        
    def load_emulators(self):
        try:
            logging.debug("recuperando emuladores da base...")
            emulatorsDA = EmulatorSQLiteDataAccess()
            self.emulators = emulatorsDA.get_all()
        except Exception, e:
            logging.fatal("nao foi possivel recuperar emuladores da base: %s", e)
            sys.exit(1)
        
    def load_roms(self):
        try:
            logging.debug("recuperando roms da base...")
            romsDA = RomSQLiteDataAccess()
            self.roms = romsDA.get_all()
        except Exception, e:
            logging.fatal("nao foi possivel recuperar roms da base: %s", e)
            pygame.quit()

    def update(self): 
        try:
            if self.current_selected_emulator_process.poll() is not None:
                self.current_selected_emulator_process = None
                logging.info("o emulador foi finalizado pelo jogador")
                
                try:
                    LogPlayRomSQLiteDataAccess().update_log(self.current_play_log_rom)
                except Exception, e:
                    print "erro atualizando log da rom: ", e.args
        except:
            pass
        
        if self.current_selected_emulator_process is not None:
            return
        
        #efeito de cor da caixa de selecao
        if self.selection_color[1] >= 245:
            self.selection_color_fade_order = True
        elif self.selection_color[1] <= 10:
            self.selection_color_fade_order = False
        
        if self.selection_color_fade_order:
            c = self.selection_color[1] - 10
        else:
            c = self.selection_color[1] + 10
        self.selection_color = (255, c, c)
        
        for i in range(0, len(self.current_page_itens)):
            self.current_page_itens[i].location = vec2d(0, 150 + self.current_page_itens[i].size.y * i)
            
    def keyUp(self, key): 
        pass

    def mouseUp(self, button, pos):

        if pos is not None and button is not None:
            logging.info("clique de mouse com o botao %s na posicao %s", button, pos)
            self.current_selected_item = self.select_item(pos)
            if(button != 1):
                logging.debug("era esperado um click com o botao 1, saindo da funcao...")
                return
        
        if isinstance(self.current_selected_item, Emulator):
            logging.info("o objeto selecionado eh o emulador %s!", self.current_selected_item.name)
            self.current_selected_emulator = self.current_selected_item
            self.current_page = 0
            self.current_page_itens = self.get_itens_by_page(self.find_roms_by_emulator_code(), 6, self.current_page)
            self.all_clickable_list[1] = self.current_page_itens
                
        elif isinstance(self.current_selected_item, Rom):
            logging.info("o objeto selecionado eh a rom %s!", self.current_selected_item.name)
            self.current_selected_rom = self.current_selected_item
            self.select_sound_validate.play()

            try:
                args = self.current_selected_rom.additional_argument + " " + self.current_selected_emulator.base_arguments
                args = args.replace("%ROM_DIR%", self.current_selected_emulator.rom_dir)
                args = args.replace("%ROM%", self.current_selected_rom.binary_name)
                args = args.replace("%ROM_FULL_PATH%", "\"" + self.current_selected_emulator.rom_dir + self.current_selected_rom.binary_name + "\"")
                logging.info("executando: %s", self.current_selected_emulator.executable_full_path + args)
                self.current_selected_emulator_process = Popen(self.current_selected_emulator.executable_full_path + args)
            except Exception, e:
                logging.error("erro iniciando emulador: %s", e)
                self.current_selected_emulator_process = None
                
            try:
                logging.info("atualizando contador e data de ultimo jogo da rom %s", self.current_selected_rom.name)
                RomSQLiteDataAccess().update_play_time(self.current_selected_rom)
                self.current_play_log_rom = LogPlayRomSQLiteDataAccess().add_log(LogPlayRom(self.current_selected_rom, self.current_selected_emulator_process.pid))
            except Exception, e:
                logging.error("erro atualizando dados da rom %s: %s", self.current_selected_rom.name, e)
            
                    
        elif isinstance(self.current_selected_item, SystemButton):
            logging.info("o objeto selecionado eh um botao de controle!")
            
            if self.current_selected_item.value == "quit":
                print "saindo"
                #pygame.quit()
                sys.exit()
                
                #saindo
            
            elif self.current_selected_item.value == "config":
                print self.current_selected_item.value
                self.screen = pygame.display.set_mode((1024, 768))
            
            elif self.current_selected_item.value == "pageUp":
                print self.current_selected_item.value
                self.prev_page()
            
            elif self.current_selected_item.value == "pageDown":
                print self.current_selected_item.value
                self.next_page()
                
            elif self.current_selected_item.value == "orderByCounter":
                print self.current_selected_item.value
                ol = self.order_rom(self.find_roms_by_emulator_code(), lambda rom: rom.play_count, True)
                self.current_page_itens = self.get_itens_by_page(ol, 6, self.current_page)
            
            elif self.current_selected_item.value == "orderByName":
                print self.current_selected_item.value
                ol = self.order_rom(self.find_roms_by_emulator_code(), lambda rom: rom.name, False)
                self.current_page_itens = self.get_itens_by_page(ol, 6, self.current_page)
            
    def mouseMotion(self, buttons, pos, rel):
        selection = self.select_item(pos)
        if selection is not None and self.current_selected_item != selection:
            self.current_selected_item = selection
            self.select_sound_cursor.play()

    def joyAxisMotion(self, joy, axis, value):
        print joy, axis, value
        
        if joy != 0 or self.current_selected_emulator_process is not None:
            return
        
        if axis == 0:
            if value >= 0.9:
                print "direita"
                if isinstance(self.current_selected_item, Emulator):
                    if self.emulators.index(self.current_selected_item) + 1 >= len(self.emulators):
                        self.current_selected_item = self.emulators[0]
                        return
                    else:
                        self.current_selected_item = self.emulators[self.emulators.index(self.current_selected_item) + 1]
                        return
                        
                if isinstance(self.current_selected_item, Rom):
                    if self.current_page_itens.index(self.current_selected_item) + 1 >= len(self.current_page_itens):
                        self.current_selected_item = self.current_page_itens[0]
                        return
                    else:
                        self.current_selected_item = self.current_page_itens[self.current_page_itens.index(self.current_selected_item) + 1]
                        return
                                    
                if isinstance(self.current_selected_item, SystemButton):
                    if self.system_buttons.index(self.current_selected_item) + 1 >= len(self.system_buttons):
                        self.current_selected_item = self.system_buttons[0]
                        return
                    else:
                        self.current_selected_item = self.system_buttons[self.system_buttons.index(self.current_selected_item) + 1]
                        return            
            elif value <= -0.9:
                print "esquerda"
                if isinstance(self.current_selected_item, Emulator):
                    if self.emulators.index(self.current_selected_item) - 1 < 0:
                        self.current_selected_item = self.emulators[len(self.emulators) - 1]
                        return
                    else:
                        self.current_selected_item = self.emulators[self.emulators.index(self.current_selected_item) - 1]
                        return
                        
                if isinstance(self.current_selected_item, Rom):
                    if self.current_page_itens.index(self.current_selected_item) - 1 < 0:
                        self.current_selected_item = self.current_page_itens[len(self.current_page_itens) - 1]
                        return
                    else:
                        self.current_selected_item = self.current_page_itens[self.current_page_itens.index(self.current_selected_item) - 1]
                        return
                    
                if isinstance(self.current_selected_item, SystemButton):
                    if self.system_buttons.index(self.current_selected_item) - 1 < 0:
                        self.current_selected_item = self.system_buttons[len(self.system_buttons) - 1]
                        return
                    else:
                        self.current_selected_item = self.system_buttons[self.system_buttons.index(self.current_selected_item) - 1]
                        return  
        elif axis == 1:
            if value >= 0.9:
                print "baixo"
                for i in range(0, len(self.all_clickable_list)):
                    for a in self.all_clickable_list[i]:
                        if a == self.current_selected_item:
                            if i + 1 >= len(self.all_clickable_list):
                                self.current_selected_item = self.all_clickable_list[0][0]
                                return
                            else:
                                self.current_selected_item = self.all_clickable_list[i + 1][0]
                                return
                        
            elif value <= -0.9:
                print "cima"
                for i in range(0, len(self.all_clickable_list)):
                    for a in self.all_clickable_list[i]:
                        if a == self.current_selected_item:
                            if i - 1 < 0:
                                self.current_selected_item = self.all_clickable_list[len(self.all_clickable_list) - 1][0]
                                return
                            else:
                                self.current_selected_item = self.all_clickable_list[i - 1][0]
                                return
        
    def joyButtonUp(self, joy, button):
        print "joyButtonUp: ", joy, button
        if joy == 0 and button == self.j0_SELECT:
            self.j0select = False
        
        if joy == 0 and button == self.j0_START:
            self.j0start = False
            
        if self.current_selected_emulator_process is None:
            if joy == 0 and button == 5:
                self.next_page()
            elif joy == 0 and button == 7:
                self.prev_page()
                
        
    def joyButtonDown(self, joy, button):
        print "joyButtonDown: ", joy, button
        if joy == 0 and button == self.j0_SELECT:
            self.j0select = True
            
        if joy == 0 and button == self.j0_START:
            self.j0start = True
            
        if self.current_selected_emulator_process is None:
            if joy == 0 and button == self.j0_START:
                print "iniciando game"
                self.mouseUp(None, None)
            
    #    if self.current_selected_emulator_process is not None and self.j0select and self.j0start:
    #        self.quit_current_game()

    def next_page(self):
        self.current_page = self.current_page + 1
        self.current_page_itens = self.get_itens_by_page(self.find_roms_by_emulator_code(), 6, self.current_page)
        self.all_clickable_list[1] = self.current_page_itens
        
    def prev_page(self):
        self.current_page = self.current_page - 1
        self.current_page_itens = self.get_itens_by_page(self.find_roms_by_emulator_code(), 6, self.current_page)
        self.all_clickable_list[1] = self.current_page_itens
        
    def order_rom(self, object_list, field, reverse = True):
        return sorted(object_list, key=field, reverse = reverse)
    
    def quit_current_game(self):
        print "quit_current_game"
        if self.current_selected_emulator_process is not None:
            try:
                self.current_selected_emulator_process.terminate()
            except Exception, e:
                print "erro encerrando emulador: ", e.args
            finally:
                self.current_selected_emulator_process = None
            
            try:
                LogPlayRomSQLiteDataAccess().update_log(self.current_play_log_rom)
            except Exception, e:
                print "erro atualizando log da rom: ", e.args
    
    def draw(self):
        if self.current_selected_emulator_process is not None:
            return
        
        #imprime background
        self.screen.blit(self.background_image, (0, 0))
        
        #imprime meu nome :p
        label = self.generic_font.render("Raffaello Salvetti - 12/2012 - v1.0a", 1, (255, 255, 255))
        self.screen.blit(label, (10, self.config.resolution[1] - 10))
        
        #imprime emuladores
        for e in self.emulators:
            if e is not None and e.icon is not None and e.location is not None:
                self.screen.blit(e.icon, e.location)
        
        #imprime "Ordenar por: "
        label = self.rom_list_font.render("Ordenar por: ", 1, self.config.font_color)
        self.screen.blit(label, (20, 110))
        
        #imprime botoes de sistema 
        for s in self.system_buttons:
            if s is not None and s.icon is not None and s.location is not None:
                self.screen.blit(s.icon, s.location)
        
        #imprime lista de rom do emulador selecionado
        for i in range(0, len(self.current_page_itens)):
            if self.current_page_itens[i] is not None and \
            self.current_page_itens[i].icon is not None and \
            self.current_page_itens[i].location is not None:
                self.current_page_itens[i].location = vec2d(0, 150 + i * self.current_page_itens[i].size.y)
                self.screen.blit(self.current_page_itens[i].icon, self.current_page_itens[i].location)
                #imprime nome da rom
                label = self.rom_list_font.render(self.current_page_itens[i].name, 1, self.config.font_color)
                self.screen.blit(label, (20, 155 + i * self.current_page_itens[i].size.y))
                #imprime genero da rom
                label = self.rom_list_font.render(self.current_page_itens[i].genre.name, 1, self.config.font_color)
                self.screen.blit(label, (50, 185 + i * self.current_page_itens[i].size.y))
                #imprime quantidades de jogadores da rom
                label = self.rom_list_font.render(str(self.current_page_itens[i].max_players), 1, self.config.font_color)
                self.screen.blit(label, (280, 185 + i * self.current_page_itens[i].size.y))
                #imprime ultima cez que jogou a rom
                if self.current_page_itens[i].last_play is None:
                    data = "Nunca" 
                else:
                    data = time.strftime("%H:%M:%S %d/%m/%Y", time.strptime(self.current_page_itens[i].last_play, "%Y-%m-%d %H:%M:%S"))
                label = self.rom_list_font.render(data, 1, self.config.font_color)
                self.screen.blit(label, (420, 185 + i * self.current_page_itens[i].size.y))
                #imprime contador de vezes que se jogou a rom
                label = self.rom_list_font.render(str(self.current_page_itens[i].play_count), 1, self.config.font_color)
                self.screen.blit(label, (680, 185 + i * self.current_page_itens[i].size.y))
        
        #imprime indicador de selecao nos icones
        if self.current_selected_item is not None:
            pygame.draw.rect(self.screen, self.selection_color, self.current_selected_item.getBounds(10), 4)    
        

    def select_item(self, pos):
        try:
            for e in self.emulators:
                if vec2d(pos).y >= e.location.y and vec2d(pos).y <= e.location.y + e.size.y:
                    if vec2d(pos).x >= e.location.x and vec2d(pos).x <= e.location.x + e.size.x:
                        return e
        except Exception, e:
            print e
            
        try:
            for r in self.current_page_itens:
                if vec2d(pos).y >= r.location.y and vec2d(pos).y <= r.location.y + r.size.y:
                    if vec2d(pos).x >= r.location.x and vec2d(pos).x <= r.location.x + r.size.x:
                        return r
        except Exception, e:
            print e
        
        try:
            for s in self.system_buttons:
                if vec2d(pos).y >= s.location.y and vec2d(pos).y <= s.location.y + s.size.y:
                    if vec2d(pos).x >= s.location.x and vec2d(pos).x <= s.location.x + s.size.x:
                        return s
        except Exception, e:
            print e

        return None
                    
    def find_roms_by_emulator_code(self):
        if self.current_selected_emulator is None:
            return
        
        romList = list()
        for r in self.roms:
            if r.emulator.id == self.current_selected_emulator.id:
                romList.append(r)
        return romList

    def get_itens_by_page(self, item_list, itens_by_page, current_page = 0):
        if len(item_list) <= itens_by_page:
            return item_list
        else:
            llist = list()
            for i in range(0, len(item_list), itens_by_page):
                llist.append(item_list[i : i + itens_by_page])
            try:
                return llist[current_page]
            except:
                return list()

s = Starter()
s.mainLoop(40)                