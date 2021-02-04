from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", '--image', 
                    action="store",
                    dest="infile",
                    type= str,
                    required=True)
args = parser.parse_args()
infile = args.infile

size = 800, 600

im = Image.open(infile)
im.thumbnail(size)
im.show()