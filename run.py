from PIL import Image, ImageChops
from bs4 import BeautifulSoup
from io import BytesIO
import urllib.request
import requests
import json
import re

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

def getAllFlairs():
    """Determine location of all flairs.

    Returns:
        Dictionary: key-value pairs where keys are flair names and values are lists containing x and y offsets.
    """
    # Open up a profile to access the full list of flairs.
    html_page = urllib.request.urlopen("https://tagpro.koalabeast.com/profile/548a41cee27aa91f22d731a8")
    soup = BeautifulSoup(html_page, "html.parser")
    result = dict()
    # Find the tab containing all flairs.
    all_flairs = soup.find('div', {'id':'all-flair'})
    # Flair names and offsets can be found in the span elements.
    for div in all_flairs.findAll('li'):
        span = div.find('span')
        # Replace hyphens with periods to stick to flair names elsewhere.
        name = span['class'][1].replace('-','.')
        # Regular expression to extract only digits and '-'s from offsets.
        digit_filter = re.compile(r'[^\d\-]+')
        # Offsets are found in the background-position attribute of the style tag.
        offset = span['style'].split(' ')[1:]
        # Perform regex matching and store their results as integers.
        offset[0] = int(digit_filter.sub('', offset[0]))
        offset[1] = int(digit_filter.sub('', offset[1]))
        result[name] = dict()
        result[name]['offset'] = offset
        # Extract flair description.
        description = div.find('div', {'class':'flair-description'}).getText().strip()
        result[name]['description'] = description
    return result

def main():
    # Load the flairs spritesheet from Tagpro's website.
    spritesheet = Image.open(BytesIO(requests.get('https://tagpro.koalabeast.com/images/flair.png').content))
    # Proceed only if a new flair has been added.
    if flairAdded(spritesheet):
        # Save an upscaled version of the spritesheet.
        width, height = spritesheet.size
        spritesheet.resize((width * 3, height * 3), resample=Image.NEAREST).save('upscaled.png', 'PNG')
        # Save the flair offsets to a json file.
        with open('flairLocations.json', 'w') as fp:
            json.dump(getAllFlairs(), fp)

if __name__ == "__main__":
    main()
