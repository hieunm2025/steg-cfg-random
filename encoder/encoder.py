#!/usr/bin/env python
import os
import sys
import argparse
import random
from PIL import Image

DICTIONARY = {
    0: ["the", "this", "a", "an", "that"],
    1: ["man", "woman", "boy", "girl", "person", "child"],
    2: ["walked", "ran", "jumped", "moved", "went"],
    3: ["to", "towards", "into", "onto"],
    4: ["park", "school", "university", "market", "library"],
    5: ["quickly", "slowly", "carefully", "happily"],
    6: ["big", "small", "tall", "young", "old"],
    7: ["beautiful", "handsome", "pretty", "smart"],
    8: ["good", "bad", "nice", "evil", "kind"],
    9: ["harvard", "yale", "mit", "stanford", "berkeley"]
}

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_chunks(binary, chunk_size=3):
    chunks = [binary[i:i+chunk_size] for i in range(0, len(binary), chunk_size)]
    if len(chunks[-1]) < chunk_size:
        chunks[-1] = chunks[-1].ljust(chunk_size, '0')
    return chunks

def select_random_pixels(img, num_pixels):
    width, height = img.size
    coords = [(x, y) for x in range(width) for y in range(height)]
    selected_coords = random.sample(coords, num_pixels)
    return [((x, y), img.getpixel((x, y))) for x, y in selected_coords]

def embed_data_in_pixels(pixels, chunks):
    modified_pixels = []
    for i, (coords, (r, g, b)) in enumerate(pixels):
        if i < len(chunks):
            chunk = chunks[i]
            r_bit, g_bit, b_bit = [int(chunk[j]) if j < len(chunk) else 0 for j in range(3)]
            r_new = (r & 0xFE) | r_bit
            g_new = (g & 0xFE) | g_bit
            b_new = (b & 0xFE) | b_bit
            modified_pixels.append((coords, (r_new, g_new, b_new)))
        else:
            modified_pixels.append((coords, (r, g, b)))
    return modified_pixels

def encode_coordinates_to_text(coords):
    sentences = []
    for x, y in coords:
        x_str, y_str = str(x).zfill(4), str(y).zfill(4)
        words = [random.choice(DICTIONARY[int(d)]) for d in x_str]
        words.append("and")
        words.extend(random.choice(DICTIONARY[int(d)]) for d in y_str)
        sentences.append(" ".join(words))
    return sentences

def create_stego_image(original_img, modified_pixels):
    stego_img = original_img.copy()
    for (x, y), (r, g, b) in modified_pixels:
        stego_img.putpixel((x, y), (r, g, b))
    return stego_img

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-t', '--text', required=True)
    parser.add_argument('-d', '--data', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print >> sys.stderr, "Error: Input image '{}' not found".format(args.image)
        return 1

    img = Image.open(args.image)
    if img.format != 'BMP':
        img = img.convert('RGB')

    binary_data = text_to_binary(args.data)
    chunks = binary_to_chunks(binary_data)
    num_pixels_needed = len(chunks)
    width, height = img.size

    if width * height < num_pixels_needed:
        print >> sys.stderr, "Error: Image too small"
        return 1

    selected_pixels = select_random_pixels(img, num_pixels_needed)
    modified_pixels = embed_data_in_pixels(selected_pixels, chunks)
    stego_img = create_stego_image(img, modified_pixels)
    stego_img.save(args.output, 'BMP')

    pixel_coords = [coords for coords, _ in selected_pixels]
    encoded_text = encode_coordinates_to_text(pixel_coords)

    with open(args.text, 'w') as f:
        for sentence in encoded_text:
            f.write(sentence + "\n")

    print "Steganography process completed successfully!"
    return 0

if __name__ == "__main__":
    sys.exit(main())
