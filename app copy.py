from PIL import Image, ImageDraw, ImageFont
import random

ref_img = Image.open("p1_pizzle_pumpkin.jpg")
size=30
puzzle_words = ['Pumpkin','lantern','Carve','Seeds','Face','Triangle','Knife','Candle']
puzzle_words = [word.upper() for word in puzzle_words]
font_path = "EspenHalloween.ttf"
word_locations = {}
img_width = ref_img.width
img_height = ref_img.height
square_size = img_width // size
num_of_col = int(img_width/square_size)
num_of_row = int(img_height/square_size)

font_size = int(square_size/2+10)

valid_cols = [[0 for j in range(num_of_col)] for i in range(num_of_row)]
puzzle_map = [['' for j in range(num_of_col)] for i in range(num_of_row)]

def set_valid_cols():
    for i in range(num_of_row):
        for j in range(num_of_col):
            colors = ref_img.crop((j * square_size, i * square_size, (j + 1) * square_size, (i + 1) * square_size)).getcolors()
            if colors and colors[0][1] != (255, 255, 255):
                # Check if more than 70% of the colors are not white
                total_pixels = sum(c[0] for c in colors)
                white_pixels = sum(c[0] for c in colors if c[1] == (255, 255, 255))
                if white_pixels / total_pixels < 0.7:
                    valid_cols[i][j] = 1


def fill_puzzle_map():
    # Fill the puzzle map according to valid_cols
    # This function is to create a num_of_col * num_of_row world search puzzle.
    # But the search words and random characters can only be generated when the same location of valid_cols equals 1
    for word in puzzle_words:
        added = False
        tried = 0
        while not added:
            i = random.randint(0, num_of_row - 1)
            j = random.randint(0, num_of_col - 1)
            if valid_cols[i][j] == 1 and puzzle_map[i][j] == '':
                direction = random.choice(['horizontal', 'vertical', 'diagonal'])
                if direction == 'horizontal' and tried > 10:
                    if j + len(word) < num_of_col and all(puzzle_map[i][j + k] == '' or puzzle_map[i][j + k] == word[k] for k in range(len(word))):
                        for k in range(len(word)):
                            if valid_cols[i][j + k] == 0:
                                break
                            puzzle_map[i][j + k] = word[k]
                        else:
                            added = True
                elif direction == 'vertical' and tried > 5:
                    if i + len(word) < num_of_row and all(puzzle_map[i + k][j] == '' or puzzle_map[i + k][j] == word[k] for k in range(len(word))):
                        for k in range(len(word)):
                            if valid_cols[i + k][j] == 0:
                                break
                            puzzle_map[i + k][j] = word[k]
                        else:
                            added = True
                elif direction == 'diagonal':
                    if i + len(word) < num_of_row and j + len(word) < num_of_col and all(puzzle_map[i + k][j + k] == '' or puzzle_map[i + k][j + k] == word[k] for k in range(len(word))):
                        for k in range(len(word)):
                            if valid_cols[i + k][j + k] == 0:
                                break
                            puzzle_map[i + k][j + k] = word[k]
                        else:
                            added = True
            tried += 1
        # Add the word location to the dictionary
        word_locations[word] = (i, j, direction)
    # Fill empty spaces with random characters
    for i in range(num_of_row):
        for j in range(num_of_col):
            if valid_cols[i][j] == 1 and puzzle_map[i][j] == '':
                puzzle_map[i][j] = chr(random.randint(65, 90)).upper()



def draw_puzzle_map():
    img = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_size = 56
    font = ImageFont.truetype(font_path, font_size)
    # Draw the puzzle map on the image
    for i in range(num_of_row):
        for j in range(num_of_col):
            if puzzle_map[i][j] != '':
                x = j * square_size + square_size // 2 - font_size // 2
                y = i * square_size + square_size // 2 - font_size // 2
                draw.text((x, y), puzzle_map[i][j], fill='black', font=font)
    img.save('puzzle_map.png')

set_valid_cols()
fill_puzzle_map()
draw_puzzle_map()

for word in puzzle_words:
    if word in word_locations:
        location = word_locations[word]
        print(f"The first character of the word '{word}' is located at row {location[0]} and column {location[1]}")
