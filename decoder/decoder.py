#!/usr/bin/env python
import os
import sys
import argparse
from PIL import Image

DICTIONARY = {
    "the": 0, "this": 0, "a": 0, "an": 0, "that": 0,
    "man": 1, "woman": 1, "boy": 1, "girl": 1, "person": 1, "child": 1,
    "walked": 2, "ran": 2, "jumped": 2, "moved": 2, "went": 2,
    "to": 3, "towards": 3, "into": 3, "onto": 3,
    "park": 4, "school": 4, "university": 4, "market": 4, "library": 4,
    "quickly": 5, "slowly": 5, "carefully": 5, "happily": 5,
    "big": 6, "small": 6, "tall": 6, "young": 6, "old": 6,
    "beautiful": 7, "handsome": 7, "pretty": 7, "smart": 7,
    "good": 8, "bad": 8, "nice": 8, "evil": 8, "kind": 8,
    "harvard": 9, "yale": 9, "mit": 9, "stanford": 9, "berkeley": 9
}

def decode_text_to_coordinates(encoded_text):
    coordinates = []
    for line in encoded_text:
        words = line.strip().split()
        if "and" in words:
            and_index = words.index("and")
            x_words, y_words = words[:and_index], words[and_index+1:]
            x_digits = [str(DICTIONARY.get(word.lower(), -1)) for word in x_words if word.lower() in DICTIONARY]
            y_digits = [str(DICTIONARY.get(word.lower(), -1)) for word in y_words if word.lower() in DICTIONARY]
            if all(d != '-1' for d in x_digits) and all(d != '-1' for d in y_digits):
                try:
                    x, y = int(''.join(x_digits)), int(''.join(y_digits))
                    coordinates.append((x, y))
                except ValueError:
                    continue
    return coordinates

def extract_bits_from_pixels(img, coordinates):
    bits = []
    for x, y in coordinates:
        try:
            r, g, b = img.getpixel((x, y))
            bits.extend([r & 1, g & 1, b & 1])
        except IndexError:
            print >> sys.stderr, "Warning: Coordinates ({0}, {1}) out of image bounds".format(x, y)
    return bits

def bits_to_text(bits):
    text = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char_code = int(''.join(map(str, byte)), 2)
        if 32 <= char_code <= 126:
            text += chr(char_code)
        else:
            break
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True)
    parser.add_argument('-t', '--text', required=True)
    args = parser.parse_args()
    
    if not os.path.exists(args.image) or not os.path.exists(args.text):
        print >> sys.stderr, "Error: Input files not found"
        return 1
    
    img = Image.open(args.image)
    with open(args.text, 'r') as f:
        encoded_text = f.readlines()
    
    coordinates = decode_text_to_coordinates(encoded_text)
    bits = extract_bits_from_pixels(img, coordinates)
    secret_text = bits_to_text(bits)
    
    print "\nExtracted secret message:\n" + "-"*30 + "\n" + secret_text + "\n" + "-"*30
    print "\nExtraction process completed successfully!"
    return 0

if __name__ == "__main__":
    sys.exit(main())
