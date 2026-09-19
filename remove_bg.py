import numpy as np
from PIL import Image, ImageFilter
from collections import deque

# Load 15.png or 1.jpg
src_path = r'c:\KARTHIKEYAN\Namdu\Ui\images\franch-oil-nh-plus\15.png'
im = Image.open(src_path).convert('RGB')
w, h = im.size

arr = np.array(im, dtype=np.uint8)

# We want to find all background pixels starting from the outer borders that are near-white (e.g. R>240, G>240, B>240)
# A simple breadth-first search (flood fill) from all 4 borders guarantees we don't erase white areas INSIDE the bottle/box!

visited = np.zeros((h, w), dtype=bool)
bg_mask = np.zeros((h, w), dtype=bool)

# Threshold for near white background
# Let's check brightness
is_near_white = (arr[:, :, 0] >= 242) & (arr[:, :, 1] >= 242) & (arr[:, :, 2] >= 242)

queue = deque()

# Add all border pixels that are near white
for x in range(w):
    if is_near_white[0, x]:
        queue.append((0, x))
        visited[0, x] = True
    if is_near_white[h - 1, x]:
        queue.append((h - 1, x))
        visited[h - 1, x] = True

for y in range(h):
    if is_near_white[y, 0]:
        queue.append((y, 0))
        visited[y, 0] = True
    if is_near_white[y, w - 1]:
        queue.append((y, w - 1))
        visited[y, w - 1] = True

# 4-connected BFS
while queue:
    cy, cx = queue.popleft()
    bg_mask[cy, cx] = True

    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < h and 0 <= nx < w:
            if not visited[ny, nx] and is_near_white[ny, nx]:
                visited[ny, nx] = True
                queue.append((ny, nx))

# Now create alpha channel
alpha = np.where(bg_mask, 0, 255).astype(np.uint8)

# Convert alpha to PIL Image and apply smooth edge antialiasing
alpha_im = Image.fromarray(alpha, mode='L')
# A small box blur or min/max filter to eliminate halos
alpha_im = alpha_im.filter(ImageFilter.GaussianBlur(radius=1.2))

# Composite into RGBA
rgba_arr = np.dstack((arr, np.array(alpha_im)))
result_im = Image.fromarray(rgba_arr, mode='RGBA')

# Crop to non-transparent bounding box with slight padding
bbox = result_im.getbbox()
if bbox:
    # Add 10px padding
    pad = 10
    crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(w, bbox[2]+pad), min(h, bbox[3]+pad))
    result_im = result_im.crop(crop_box)

out_path = r'c:\KARTHIKEYAN\Namdu\Ui\images\franch-oil-nh-plus\hero_cutout.png'
result_im.save(out_path, format='PNG')
print(f'Successfully created transparent cutout: {out_path} with size {result_im.size}')
