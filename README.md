# Tagpro Flair Utility

A Python script that produces a 3x upscaled version of [Tagpro flairs](https://tagpro.koalabeast.com/images/flair.png) as well as a JSON file that pairs each flair with its closest [Material Design color](https://material.io/design/color/the-color-system.html#tools-for-picking-colors).

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
One result of running the script is an image called ```output.png```. As of the last time the script was run, it will look like like this:
![Screenshot of homepage](./output.png)

The JSON file ```colorPairs.json``` is formatted as such:
```json
{
    "a_b": [primary, primaryLight],
     ...
}
```
where for each flair:
- ```a``` is the vertical offset
- ```b``` is the horizontal offset
- ```primary``` and ```primaryLight``` are the closest colors