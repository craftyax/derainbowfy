#!/usr/bin/env python
'''
Script for replacing rainbow colormap from images

Todo: The current script execution time is very slow due to the number of loops required in the search/replace section.  Find a way to speed this up.

Scripted by Erik Axdahl
'''

from PIL import Image
import sys
import numpy as np

# File I/O
file_in = sys.argv[1]
file_out = sys.argv[2]

# Number of colors in each quadrant
colorShades = 60

# Create an array with all possible gray values for data
valueMin = 9.
valueMax = 230.
valueShades = np.array([int(valueMin + (valueMax-valueMin)/colorShades/4.*i) for i in range(colorShades*4)])
valueShades = valueShades[::-1]

# Define rainbow palette
paletteRainbow = []
for i in range(0,colorShades):
	paletteRainbow.extend((0,int(i*255./colorShades),255))
for i in range(0,colorShades):
	paletteRainbow.extend((0,255,int(255.-i*255./colorShades)))
for i in range(0,colorShades):
	paletteRainbow.extend((int(i*255./colorShades),255,0))
for i in range(0,colorShades):
	paletteRainbow.extend((255,int(255.-i*255./colorShades),0))

# Define gray colors in palette (e.g. for text and borders)
grayCases = 256-4*colorShades
for i in range(0,grayCases):
	gray = int((i+1)*255/grayCases)
	paletteRainbow.extend((gray,gray,gray))

assert len(paletteRainbow) == 768

# Create a palette list for doing comparisons
paletteList = [(paletteRainbow[i],
	        paletteRainbow[i+1],
		paletteRainbow[i+2]) for i in np.arange(0,768,3)]
paletteListColor = paletteList[0:colorShades*4]

# Load image as RGB
img = Image.open(file_in)

# Determine size of image
r,c = img.size

# Create a new image template with the rainbow palette
rgb_select = Image.new("P", (1,1))
rgb_select.putpalette( paletteRainbow )

# Apply image template to imported image and convert back to RGB
img_conv = img.convert("RGB").quantize(palette=rgb_select)
img_rgb = img_conv.convert("RGB")

# Search through image and replace data colors with gray levels
for i in range(r):
	for j in range(c):
		# Check if current pixel value is in colorlist
		if img_rgb.getpixel((i,j)) in paletteListColor:
			index = paletteListColor.index(
					img_rgb.getpixel((i,j)))
			gray = valueShades[index]
			img_rgb.putpixel((i,j),
					 (gray,gray,gray))
			
			

# Save image
img_rgb.save(file_out)
