from lino.console.application import Application

class Hello(Application):
    name="Hello"
    author="Luc Saffre"

    def run(self):
        print "Hello, world!"
                 

if __name__ == '__main__':
    Hello().main()

