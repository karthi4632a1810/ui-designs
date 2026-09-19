import numpy as np
from PIL import Image, ImageFilter
from collections import deque

src_path = r'c:\KARTHIKEYAN\Namdu\Ui\images\franch-oil-nh-plus\8.webp'
im = Image.open(src_path).convert('RGB')
w, h = im.size
arr = np.array(im, dtype=np.uint8)

# Check near white threshold
# Notice the reflection at the bottom: we can choose to either include or exclude the faint reflection,
# or cleanly cut it. Most e-commerce hero cutouts look best with either no reflection or faint reflection.
# Let's see: the reflection has y > 1150 and is quite faint/white.
# Let's cut the background cleanly.

visited = np.zeros((h, w), dtype=bool)
bg_mask = np.zeros((h, w), dtype=bool)

# Threshold for white background
is_near_white = (arr[:, :, 0] >= 245) & (arr[:, :, 1] >= 245) & (arr[:, :, 2] >= 245)

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

while queue:
    cy, cx = queue.popleft()
    bg_mask[cy, cx] = True

    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < h and 0 <= nx < w:
            if not visited[ny, nx] and is_near_white[ny, nx]:
                visited[ny, nx] = True
                queue.append((ny, nx))

# Alpha mask: 0 where background, 255 where foreground
alpha = np.where(bg_mask, 0, 255).astype(np.uint8)

# Smooth edges with Gaussian Blur
alpha_im = Image.fromarray(alpha, mode='L')
alpha_im = alpha_im.filter(ImageFilter.GaussianBlur(radius=1.0))

rgba_arr = np.dstack((arr, np.array(alpha_im)))
result_im = Image.fromarray(rgba_arr, mode='RGBA')

# Crop to content
bbox = result_im.getbbox()
if bbox:
    pad = 10
    crop_box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(w, bbox[2] + pad), min(h, bbox[3] + pad))
    result_im = result_im.crop(crop_box)

out_path = r'c:\KARTHIKEYAN\Namdu\Ui\images\franch-oil-nh-plus\franch_oil_hero_transparent.png'
result_im.save(out_path, format='PNG')
print(f'Done! Saved {out_path} with size {result_im.size}')
