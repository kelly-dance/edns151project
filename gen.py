import qrcode # !!!
"""
Using this file to create qr code to test with.
The format I am currently using to encode items is
the name of the item on a line
followed by another line with the integer number of days
until it expires.
"""
img = qrcode.make('Apple\n7\nMilk\n12')
img.save("qr.png")