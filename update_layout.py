import re

with open('new_layout.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace emerald with rose, mint with amber for classes
content = re.sub(r'\bemerald-(\d+)\b', r'rose-\1', content)
content = re.sub(r'\bmint-(\d+)\b', r'amber-\1', content)
# Ensure tailwind config matches the maroon and gold colors
config = '''          colors: {
            "background": "#ffffff",
            "surface": "#ffffff",
            "surface-container-low": "#faf8f9",
            "surface-container": "#f6f2f4",
            "surface-container-high": "#f0eaec",
            "surface-container-highest": "#eae1e5",
            "surface-container-lowest": "#ffffff",
            "primary": "#5f1235",
            "primary-dark": "#3c0b21",
            "primary-container": "#901b50",
            "on-primary": "#ffffff",
            "on-primary-container": "#faf8f9",
            "primary-fixed": "#faf8f9",
            "secondary": "#d4af37",
            "secondary-container": "#fdf6e7",
            "secondary-fixed": "#fdf6e7",
            "gold-accent": "#d4af37",
            "gold-soft": "#fdf6e7",
            "gold-border": "#e8c564",
            "on-surface": "#2d1620",
            "on-surface-variant": "#5f3d4a",
            "outline": "#906d7b",
            "outline-variant": "#d9bcca",
            "mint-soft": "#fdf6e7",
            "mint-badge": "#d4af37",
            rose: {
              950: '#3c0b21',
              900: '#5f1235',
              850: '#7a1744',
              800: '#901b50',
              700: '#a61f5c',
              600: '#bc2368',
              500: '#d22774',
              400: '#e82b80',
              300: '#e84591',
              200: '#f075ab',
              100: '#f4a3c6',
              50: '#f9d1e2',
            },
            amber: {
              700: '#b4841c',
              600: '#c59b27',
              500: '#d4af37',
              400: '#dcb952',
              300: '#e4c46d',
              200: '#e8c564',
              100: '#f0d99a',
              50: '#fdf6e7',
            }
          },'''
content = re.sub(r'colors:\s*\{.*?\}\s*\}', config + ' }', content, flags=re.DOTALL)

# Insert Logo Header
logo_header = '''<img src="image.png" alt="ASCAS Logo" class="h-12 w-auto object-contain">'''
content = re.sub(r'<div class="w-10 h-10 rounded-full bg-gradient-to-tr from-rose-800.*?</div>', logo_header, content, flags=re.DOTALL)

with open('new_layout_updated.html', 'w', encoding='utf-8') as f:
    f.write(content)
