from menu import Starter
import logging
from frontend.components.Config import Config

def main():
    c = Config()
    logging.basicConfig(filename=str(c.log_path) + "/" + str(c.log_filename) , format="%(asctime)s - %(levelname)s - %(funcName)s --> %(message)s", filemode="w", level=logging.DEBUG)
    log = logging.getLogger()
    s = Starter(config = c, logSystem = log)
    s.mainLoop(40)

if __name__ == "__main__":
    main()