"""
Usage: openurl URL

Starts the default browser on your system to display the specified URL.

"""

if __name__ == "__main__":

	import sys,webbrowser
	for url in sys.argv[1:]:
		webbrowser.open(url,new=1)
