import sys

#verify the file
try:
  filename = sys.argv[1]
  file = open(filename)
except IndexError:
    print("ERROR : Filename not found. Please pass a filename to the program")
except FileNotFoundError:
    print("ERROR : No such file: '" + filename + "'")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

#store the xml data in a string
xml_data = file.read()

