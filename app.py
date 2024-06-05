from PIL import Image, ImageDraw, ImageFont
import random, sys

gen_try = 1000000
project_name='halloween'
page_title = ''
page = "01"

#bg_color = (0, 0, 0, 0) #transperance
bg_color = "white"
front_bg = (0, 0, 0, 0)

size=36

header_font_size = 140
header_font_style = "Halloween_Spider.ttf"

puzzle_font_size = int(size*1.5)
puzzle_font_style = "EspenHalloween.ttf"

bottom_font_size = 80
bottom_font_style = "kenyan coffee rg.otf"

page = sys.argv[1]
puzzle = sys.argv[2]
if len(page) < 2:
    page = '0' + page
folder = f"{project_name}/page_{page}"
ref_img = Image.open(f"{folder}/mask.jpg")

puzzle_words = []
if puzzle == "regen_words":
    # open words.txt and read all lines to word_txt
    with open(f"{folder}/words.txt", "r") as f:
        word_txt = f.read()

    # split word_txt by new line, space, or ','
    word_arr = word_txt.split()
    string_set = set(word_arr)
    unique_list = list(string_set)
    random.shuffle(unique_list)
    word_arr = unique_list
    # initialize a counter for the output file index
    i = 0

    # loop through word_arr in chunks of 16 words
    for j in range(0, len(word_arr), 16):
        # get the current chunk of 16 words
        chunk = word_arr[j:j+16]

        # increment the output file index
        i += 1

        # open a new output file with the index in the name
        with open(f"{folder}/words_{i}.txt", "w") as f:
            # write the chunk of words to the output file, separated by spaces
            f.write(",".join(chunk))
    sys.exit()

with open(f"{folder}/words_{puzzle}.txt", 'r') as f:
    puzzle_words =  f.readline().upper().split(",")
with open(f"{folder}/title.txt", 'r') as f:
    page_title =  f.readline()
diagonal_max = int(len(puzzle_words) / 2)
hor_max = int( (len(puzzle_words) - diagonal_max) / 2)

font_path = f"{project_name}/{puzzle_font_style}"
word_locations = {}
#img_width = ref_img.width
#img_height = ref_img.height
img_width = 2480
img_height = 3508

highest_y = 0
for y in range(ref_img.size[1]):
    for x in range(ref_img.size[0]):
        if ref_img.getpixel((x, y)) != (255, 255, 255):
            highest_y = y
            break
    if highest_y != 0:
        break
print(f"highest_y: {highest_y}")

adjusted_y = highest_y - 500
print(f"adjusted_y: {adjusted_y}")
square_size = img_width // size
num_of_col = int(img_width/square_size)
num_of_row = int(img_height/square_size)

valid_cols = [[0 for j in range(num_of_col)] for i in range(num_of_row)]
puzzle_map = [['' for j in range(num_of_col)] for i in range(num_of_row)]
color_map = {}

def set_valid_cols():
    for i in range(num_of_row):
        for j in range(num_of_col):
            colors = ref_img.crop((j * square_size, i * square_size, (j + 1) * square_size, (i + 1) * square_size)).getcolors()
            if colors and colors[0][1] != (255, 255, 255):
                # Check if more than 70% of the colors are not white
                total_pixels = sum(c[0] for c in colors)
                white_pixels = sum(c[0] for c in colors if c[1] == (255, 255, 255))
                if white_pixels / total_pixels < 0.8:
                    valid_cols[i][j] = 1

def gen_font_img(text,font_file,font_size,fill='black'):
    font_style = ImageFont.truetype(f"{project_name}/{font_file}", font_size)
    text_img = Image.new('RGBA', (len(text) * font_size + font_size, font_size * 2), color=front_bg)
    draw_text = ImageDraw.Draw(text_img)
    draw_text.text((0,0), text, fill=fill, font=font_style)
    text_img = text_img.crop(text_img.getbbox())
    return text_img

def fill_puzzle_map():
    # Fill the puzzle map according to valid_cols
    # This function is to create a num_of_col * num_of_row world search puzzle.
    # But the search words and random characters can only be generated when the same location of valid_cols equals 1
    diagonal_count = 0
    hor_count = 0

    for word in puzzle_words:
        added = False
        tried = 0
        try_num = 0
        r, g, b = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
        color_map[word] = (r,g,b)
        while not added:
            if try_num > gen_try:
                return False
            try_num = try_num + 1
            # Randomly select a starting position for the word
            row_idx = random.randint(0, num_of_row - 1) 
            col_idx = random.randint(0, num_of_col - 1)
            # Check if the starting position is valid and empty
            if valid_cols[row_idx][col_idx] == 1 and puzzle_map[row_idx][col_idx] == '':
                direction = random.choice(['horizontal', 'vertical', 'diagonal.left', 'diagonal.right'])
                # Randomly select a direction for the word
                # Check if the word can be added horizontally
                if direction == 'horizontal' and hor_count < hor_max: # and tried > 10: :# and tried > 0:
                    # Check if the word fits within the puzzle map horizontally
                    if col_idx + len(word) < num_of_col and all(puzzle_map[row_idx][col_idx + k] == '' or puzzle_map[row_idx][col_idx + k].split("-")[0] == word[k] for k in range(len(word))):
                        temp_row_idx = []
                        temp_col_idx = []
                        origin_val = []
                        # Check if all positions for the word are valid
                        for k in range(len(word)):
                            if valid_cols[row_idx][col_idx + k] == 0:
                                for idx in range(len(temp_row_idx)):
                                    puzzle_map[temp_row_idx[idx]][temp_col_idx[idx]] = origin_val[idx]
                                break
                            # Add the word to the puzzle map
                            temp_row_idx.append(row_idx)
                            temp_col_idx.append(col_idx + k)
                            origin_val.append(puzzle_map[row_idx][col_idx + k])
                            puzzle_map[row_idx][col_idx + k] = f"{word[k]}-{word}"
                        else:
                            hor_count += 1
                            added = True
                # Check if the word can be added vertically        
                elif direction == 'vertical':# and tried > 0:
                    # Check if the word fits within the puzzle map vertically
                    if row_idx + len(word) < num_of_row and all(puzzle_map[row_idx + k][col_idx] == '' or puzzle_map[row_idx + k][col_idx].split("-")[0] == word[k] for k in range(len(word))):
                        temp_row_idx = []
                        temp_col_idx = []
                        temp_val = []
                        # Check if all positions for the word are valid
                        for k in range(len(word)):
                            if valid_cols[row_idx + k][col_idx] == 0:
                                for idx in range(len(temp_row_idx)):
                                    puzzle_map[temp_row_idx[idx]][temp_col_idx[idx]] = temp_val[idx]
                                break
                            # Add the word to the puzzle map
                            temp_row_idx.append(row_idx + k)
                            temp_col_idx.append(col_idx) 
                            temp_val.append(puzzle_map[row_idx + k][col_idx] )
                            puzzle_map[row_idx + k][col_idx] = f"{word[k]}-{word}"
                        else:
                            added = True
                # Check if the word can be added diagonally left to right  
                elif direction == 'diagonal.left' and diagonal_count < diagonal_max:# and tried > 10:
                    # Check if the word fits within the puzzle map diagonally left to right
                    if row_idx + len(word) < num_of_row and col_idx - len(word) >= 0 and all(puzzle_map[row_idx + k][col_idx - k].split("-")[0] == '' or puzzle_map[row_idx + k][col_idx - k] == word[k] for k in range(len(word))):
                        temp_row_idx = []
                        temp_col_idx = []
                        temp_val = []
                        # Check if all positions for the word are valid
                        for k in range(len(word)):
                            if valid_cols[row_idx + k][col_idx - k] == 0:
                                for idx in range(len(temp_row_idx)):
                                    puzzle_map[temp_row_idx[idx]][temp_col_idx[idx]] = temp_val[idx]
                                break
                            # Add the word to the puzzle map 
                            temp_row_idx.append(row_idx + k)
                            temp_col_idx.append(col_idx - k)
                            temp_val.append(puzzle_map[row_idx + k][col_idx - k])
                            puzzle_map[row_idx + k][col_idx - k] = f"{word[k]}-{word}"
                        else:
                            diagonal_count += 1
                            added = True
                # Check if the word can be added diagonally right to left
                elif direction == 'diagonal.right' and diagonal_count < diagonal_max:# and tried > 10:
                    # Check if the word fits within the puzzle map diagonally right to left
                    if row_idx + len(word) < num_of_row and col_idx + len(word) < num_of_col and all(puzzle_map[row_idx + k][col_idx + k].split("-")[0] == '' or puzzle_map[row_idx + k][col_idx + k] == word[k] for k in range(len(word))):
                        temp_row_idx = []
                        temp_col_idx = []
                        temp_val = []
                        # Check if all positions for the word are valid
                        for k in range(len(word)):
                            if valid_cols[row_idx + k][col_idx + k] == 0:
                                for idx in range(len(temp_row_idx)):
                                    puzzle_map[temp_row_idx[idx]][temp_col_idx[idx]] = temp_val[idx]
                                break
                            # Add the word to the puzzle map
                            temp_row_idx.append(row_idx + k)
                            temp_col_idx.append(col_idx + k)
                            temp_val.append(puzzle_map[row_idx + k][col_idx + k])
                            puzzle_map[row_idx + k][col_idx + k] = f"{word[k]}-{word}"
                        else:
                            diagonal_count += 1
                            added = True
            tried += 1
            # Add the word location to the dictionary
            if added:
                word_locations[word] = (row_idx, col_idx, direction)
    # Fill empty spaces with random characters
    
    for row_idx in range(num_of_row):
        for col_idx in range(num_of_col):
            if valid_cols[row_idx][col_idx] == 1 and puzzle_map[row_idx][col_idx] == '':
                puzzle_map[row_idx][col_idx] = chr(random.randint(65, 90)).upper() 
    print(diagonal_count)
    return True

def draw_puzzle_map():

    #img = Image.new('RGBA', (img_width, img_height), color=(0, 0, 0, 0))
    #img = Image.new('RGBA', (img_width, img_height), "white")
    img = Image.new('RGBA', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    #solution_img = Image.new('RGBA', (img_width, img_height), color="white")
    solution_img = Image.new('RGBA', (img_width, img_height), color=bg_color)
    draw_solution = ImageDraw.Draw(solution_img)


    font_style = ImageFont.truetype(font_path, puzzle_font_size)
    background_img = Image.open(f"{folder}/background.png")
    #if background_img.size[0] > img.size[0] or background_img.size[1] > img.size[1]:
    #    background_img = background_img.crop((0, 0, img.size[0], img.size[1]))
    #if img.size[1] + adjusted_y < background_img.size[1]:
    #    background_img = background_img.crop((0, adjusted_y, img.size[0], img.size[1] + adjusted_y))
    img.paste(background_img, (0, 0 - adjusted_y),mask=background_img)
    solution_img.paste(background_img, (0, 0 - adjusted_y),mask=background_img)

    # Draw the puzzle map on the image
    for i in range(num_of_row):
        for j in range(num_of_col):
            if puzzle_map[i][j] != '':
                #x = (j * square_size) + square_size // 2 - puzzle_font_size // 2
                #y = (i * square_size) + square_size // 2 - puzzle_font_size // 2
                x = int((j * square_size) + square_size // 2 - puzzle_font_size // 2)
                y = int((i * square_size) + square_size // 2 - puzzle_font_size // 2) - adjusted_y
                gen_font_img
                if len(puzzle_map[i][j].split("-")) > 1:
                    char = puzzle_map[i][j].split("-")[0]
                    word = puzzle_map[i][j].split("-")[1]
                    #draw.text((x, y + adjusted_y), char, fill='black', font=font_style)
                    text_img = gen_font_img(char,puzzle_font_style,puzzle_font_size)
                    img.paste(text_img, (x,y),mask=text_img)

                    #enable this to draw solution text in color
                    text_img = gen_font_img(char,puzzle_font_style,puzzle_font_size,color_map[word])
                    #text_img = gen_font_img(char,puzzle_font_style,puzzle_font_size)
                    solution_img.paste(text_img, (x,y),mask=text_img)
                else:
                    char = puzzle_map[i][j].split("-")[0]
                    #draw.text((x, y + adjusted_y), char, fill='black', font=font_style)
                    text_img = gen_font_img(char,puzzle_font_style,puzzle_font_size)
                    img.paste(text_img, (x,y),mask=text_img)
    
    # draw word list at the bottom
    font_style = ImageFont.truetype(f"{project_name}/{bottom_font_style}", bottom_font_size)
    words_width = int(img_width * 0.8)
    for i, word in enumerate(puzzle_words):
        x = ((i % 4) * words_width // 4 + words_width // 8 ) + 20
        y = ((i // 4) * square_size + 4 * square_size + (i // 4) * 50 ) + 2500
        if y + square_size < img_height:
            draw.text((x, y), word, fill='black', font=font_style)

    #Draw header
    text_img = gen_font_img(page_title,header_font_style,header_font_size)
    #text_img = text_img.crop((text_img.getbbox()[0]-30, text_img.getbbox()[1]+30, text_img.getbbox()[2]+30, text_img.getbbox()[3]+30))
    img.paste(text_img, ((img_width - text_img.width) // 2, int(text_img.height/2)+200), mask=text_img)
    text_img.save(f"{folder}/text.png")

    img.save(f"{folder}/puzzle_map_{puzzle}.png")
    solution_img.save(f"{folder}/puzzle_map_{puzzle}_solution.png")
    
    img.save(f"{project_name}/out/page_{page}_{puzzle}.png")
    solution_img.save(f"{project_name}/out/solution/page_{page}_{puzzle}_solution.png")


set_valid_cols()
try_count = 0
while not fill_puzzle_map():
    print("Gen Fail")
    try_count += 1
    puzzle_map = [['' for j in range(num_of_col)] for i in range(num_of_row)]
    if try_count > 100:
        exit(0)
draw_puzzle_map()

for word in puzzle_words:
    if word in word_locations:
        location = word_locations[word]
        print(f"The first character of the word '{word}' is located at row {location[0]} and column {location[1]} as {location[2]}")
