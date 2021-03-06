# Program to convert font bitmap generated by Codeheads Bitmap Font Generator
# http://www.codehead.co.uk/cbfg/
#
# into a .dmd font file which can be used by pyprocgame.  The file from the
# generator needs to be cropped to 250x250 or 120x120 (see instruction PDF)
# before running in this program.
#
# Written by Mark Sunnucks, with initial bmp to dmd code from dmdconvert.py
# by Adam Preble
#
# Usage :
# python fontconvert.py <inputfont.bmp> <widthfile.csv> <outputfont.dmd>
#
# eg :
# python fontconvert.py beware20.bmp fontdata.csv beware20.dmd


from procgame import *
import procgame.dmd
import sys

inputbmp = sys.argv[1]
widthfile = sys.argv[2]
outputdmd = sys.argv[3]

anim = procgame.dmd.Animation()
print "Appending bitmap from", inputbmp
	
tmp = procgame.dmd.Animation().load(inputbmp, allow_cache=False)
if len(tmp.frames) > 0:
    first_frame = tmp.frames[0]
    anim.width, anim.height = first_frame.width, first_frame.height
    anim.frames += tmp.frames
anim.save(outputdmd)
print "Character frame saved to",outputdmd,", loading width information"

print first_frame.width

if first_frame.width == 250: maxwidth=25
else: maxwidth = 12

print "Max character width fixed at", str(maxwidth)

widths = []
counting = False
for line in open(widthfile):
    parse=line.split(',')
    if parse[0]=='Char 32 Base Width':
        counting = True
    if parse[0]=='Char 132 Base Width':
        counting = False
    if counting:
        widths.append(min(int(parse[1][:-1]),maxwidth))
print "Width information read:"
print widths

font = dmd.Font(outputdmd)
font.char_widths = widths
font.save(outputdmd)

print outputdmd, "updated and ready to use"
