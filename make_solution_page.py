from PIL import Image
import sys

project_name='halloween'
folder = f"{project_name}/out"
page = sys.argv[1]
if len(page) < 2:
    page = '0' + page


# Open the images and store them in a list
img = [Image.open(f"{folder}/solution/page_{page}_{i+1}_solution.png") for i in range(5)]

# Define the crop box
left, upper, right, lower = 260, 420, 2210, 2700
border = 180
# Crop and resize the images
for i in range(5):
    img[i] = img[i].crop((left, upper, right, lower))
    img[i] = img[i].resize(( int(img[i].width // 2.2), int(img[i].height // 2.2) ))
img_w = img[0].width
img_h = img[0].height
print(img[0].width)
print(img[0].height)

# Create a new image
new_img = Image.new('RGB', (2480, 3508), color="white")

# Define the positions to paste the images
positions = [(border, border), (border*2+img_w,border), (border, border+img_h), (border*2+img_w, 160+img_h), (border, border+img_h*2)]

# Paste the images onto the new image
for i in range(5):
    new_img.paste(img[i], positions[i])

# Save the new image
new_img.save(f"{folder}/page_solution_{page}.png")
