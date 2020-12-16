# Tagpro Flair Utility

A Python script that produces a 3x upscaled version of [Tagpro flairs](https://tagpro.koalabeast.com/images/flair.png) as well as a JSON file that pairs each flair name with its position offset on the spritesheet.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install -r requirements.txt
```

This will install [Pillow](https://pillow.readthedocs.io/en/stable/#), a library for manipulating images, and [requests](https://requests.readthedocs.io/en/master/) to send HTTP requests.

## Usage

Enter the following line in your terminal to run the script.
```bash
python run.py
```

## Output
One result of running the script is an image called `upscaled.png`. As of the last time the script was run, it will look like this:

![Screenshot of homepage](./upscaled.png)

The JSON file `flairLocations.json` is formatted as such:
```json
{
    "a": [b, c],
}
```
where for each flair:
- `a` is the name of the flair such as `boards.day`
- `b` is the vertical offset in pixels
- `c` is the horizontal offset in pixels
