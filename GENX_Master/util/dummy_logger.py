## having a logger with routes for each severity level allows you to route information in different ways depending on severity!

class DummyLogger():
    
    def debug(self, phrase):
        print(phrase)

    def info(self, phrase):
        print(phrase)    

    def warning(self, phrase):
        print(phrase)
        
    def error(self, phrase):
        print(phrase)
        
    def critical(self, phrase):
        print(phrase)
        
    def exception(self, phrase):
        print(phrase)