from PIL import Image, ImageDraw

def draw_character(draw, char_name, char_position, rect_size=(5, 5), text_offset=(2, -13), color="red"):
    rect_start = (char_position[0] - rect_size[0] // 2, char_position[1] - rect_size[1] // 2)
    rect_end = (char_position[0] + rect_size[0] // 2, char_position[1] + rect_size[1] // 2)

    draw.rectangle([rect_start, rect_end], outline=color, width=1)
    draw.text((char_position[0] + text_offset[0], char_position[1] + text_offset[1]), char_name, fill=color)

def zoom_and_draw(image_path, region_center, region_size, characters, output_path):
    img = Image.open(image_path)
    x, y = region_center[0] - region_size[0] // 2, region_center[1] - region_size[1] // 2
    cropped_img = img.crop((x, y, x + region_size[0], y + region_size[1]))
    draw = ImageDraw.Draw(cropped_img)

    draw_character(draw, me['name'], (me['pos'][0] - x, me['pos'][1] - y), me.get('rect_size', (5, 5)), color="green")
    for char in characters:
        draw_character(draw, char['name'], (char['pos'][0] - x, char['pos'][1] - y), char.get('rect_size', (5, 5)))

    cropped_img.save(output_path)

image_path = "Felucca.jpg"
region_center = (1500, 2000)  
region_size = (250, 250)  
me = {'name': "ME", 'pos': (1505, 2005)}
characters = [
    {'name': "VASILIY", 'pos': (1450, 2005)},
    {'name': "PETJA", 'pos': (1485, 1985)}
]
output_path = "output.png"

zoom_and_draw(image_path, region_center, region_size, characters, output_path)
