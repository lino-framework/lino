"""
Usage: openurl URL

Starts the default browser on your system to display the specified URL.

"""

import sys
import webbrowser

def main(argv):
	for url in argv:
		webbrowser.open(url,new=1)

if __name__ == "__main__":
	main(sys.argv[1:])

