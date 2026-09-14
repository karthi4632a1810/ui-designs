import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Ashwin Muralidharan with Balakrishnan
content = re.sub(r'Dr\. Ashwin Muralidharan', 'Dr. Balakrishnan', content)
content = re.sub(r'FRCR \(London, UK\)\s*Specialist Fetal Imaging', 'Neonatology Lead', content)
content = re.sub(r'MBBS, MDRD, DNB \(Radio-Diagnosis\)', 'MBBS, MD (Pediatrics), DM (Neonatology)', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
