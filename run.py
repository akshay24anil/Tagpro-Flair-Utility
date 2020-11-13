from PIL import Image, ImageChops
from io import BytesIO
from math import sqrt
import requests
import json
import sys

# Red, Pink, Purple, Blue, Green, Yellow, Orange, Brown, Gray
primaryColors = [[239, 83, 80], [236, 64, 122], [126, 87, 194], [66, 165, 245], [102, 187, 106], [255, 238, 88], [255, 167, 38], [141, 110, 99], [158, 158, 158]]
primaryLColors = [[239, 154, 154], [244, 143, 177], [149, 117, 205], [144, 202, 249], [165, 214, 167], [255, 245, 157], [255, 204, 128], [188, 170, 164], [224, 224, 224]]
colorPairs = dict()

def flairAdded(newImage):
    """Compare fetch of flairs with an existing copy to see if new flairs were added.

    Args:
        newImage (Image): picture containing result of request for flairs.

    Returns:
        Boolean: result of comparing images.
    """
    # Look for differences between images.
    diff = ImageChops.difference(newImage, Image.open('original.png'))
    # New flair was added.
    if diff.getbbox():
        # Overwrite backup with new image.
        newImage.save('original.png', 'PNG')
        return True
    # No difference between the images.
    else:
        return False

def closestColor(rgbArray):
    """Determine index of closest color in primaryColors.

    Args:
        rgbArray (list): list containing red, green, and blue values of dominant color.

    Returns:
        number: index of the closest color.
    """
    minDistance = sys.maxsize
    colorIndex = 8
    r2 = rgbArray[0]
    g2 = rgbArray[1]
    b2 = rgbArray[2]
    index = 0
    for color in primaryColors:
        r1 = color[0]
        g1 = color[1]
        b1 = color[2]
        # Calculate distance using weights for visually close colors.
        d = sqrt(((r2-r1)*0.3)**2 + ((g2-g1)*0.59)**2 + ((b2-b1)*0.11)**2)
        if d < minDistance:
            minDistance = d
            colorIndex = index
        index += 1
    return colorIndex

def dominantColor(image):
    """Determine the most dominant color in a flair.

    Args:
        image (Image): single flair from the spritesheet.

    Returns:
        number: list containing red, green, and blue values of the dominant color.
    """
    # Reduce the number of colors in image to 4.
    reduced = image.convert("P",  palette=Image.ADAPTIVE, colors=4)
    palette = reduced.getpalette()
    palette = [palette[3*n:3*n+3] for n in range(256)]
    # Get the number of pixels of each color.
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    # Reverse sort to get most common color first.
    color_count.sort(reverse=True)
    result = [0,0,0]
    # Find first non-black color if it exists. Images are RGBA so empty spaces count as black.
    for cc in color_count:
        if cc[1] != [0,0,0]:
            result = cc[1]
            break
    return result

def calculateBackgrounds(image):
    """Go through all individual flairs and determine closest primary color. Set up a dictionary with all pairings.

    Args:
        image (Image): spritesheet that will be split into individual sprites for processing.
    """
    # Each flair has a dimension of 16x16 so increment by 16 each time.
    for i in range(0, image.height, 16):
        for j in range(0, image.width, 16):
            # Isolate current flair
            flair = image.crop((j, i, j+16, i+16))
            # Identify index of closest color to those in primaryColors.
            colorIndex = closestColor(dominantColor(flair))
            # Add flair + color (as hex) combination to dictionary.
            colorPairs[str(-j) + '_' + str(-i)] = ['#%02x%02x%02x' % tuple(primaryColors[colorIndex]), '#%02x%02x%02x' % tuple(primaryLColors[colorIndex])]

def main():
    # Load the flairs spritesheet from Tagpro's website.
    spritesheet = Image.open(BytesIO(requests.get('https://tagpro.koalabeast.com/images/flair.png').content))
    # Proceed only if a new flair has been added.
    if flairAdded(spritesheet):
        calculateBackgrounds(spritesheet)
        # Save dictionary as json file.
        with open('colorPairs.json', 'w') as fp:
            json.dump(colorPairs, fp)
        # Save an upscaled version of the spritesheet.
        width, height = spritesheet.size
        spritesheet.resize((width * 3, height * 3), resample=Image.NEAREST).save('output.png', 'PNG')
         
if __name__ == "__main__":
    main()