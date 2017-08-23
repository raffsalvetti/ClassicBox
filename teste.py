from subprocess import Popen
from threading import Thread

class Teste:
    def __init__(self):
        self.proc = None
        self.canRun = True
    
    def QueryProcess(self):
        lpid = 0
        ln = -99
        while self.canRun:
            if self.proc is not None:
                try:
                    n = self.proc.poll()
                    
                    if lpid == self.proc.pid and ln == n:
                        continue
                    
                    if n is None:
                        print "processo ativo, PID:", self.proc.pid
                        lpid = self.proc.pid
                        ln = n
                    else:
                        print "processo finalizado com:", n
                        self.proc = None
                except:
                    pass
                    
    def Execute(self):
        t1 = Thread(target = self.QueryProcess)
        t1.start()
        
        i = None
        while i is not 'q':
            if i is 'o':
                try:
                    self.proc = Popen("notepad.exe");
                except Exception, e:
                    print "nao foi possivel abrir o processo:", e
            elif i is 'k':
                if self.proc is not None:
                    try:
                        self.proc.kill()
                        self.proc = None
                        print "processo morto"
                    except Exception, e:
                        print "nao foi possivel matar o processo:", e
                else:
                    print "nada para matar"
            elif i is 't':
                if self.proc is not None:
                    try:
                        self.proc.terminate()
                        self.proc = None
                        print "processo terminado"
                    except Exception, e:
                        print "nao foi possivel terminar o processo:", e
                else:
                    print "nada para terminar"
            elif i is 's':
                if self.proc is not None:
                    print "pid:", self.proc.pid
                else:
                    print "nao existe processo ativo"
            i = raw_input("digite uma opcao: ")
        
        print "saindo..."
        self.canRun = False        
        
t = Teste()
t.Execute()