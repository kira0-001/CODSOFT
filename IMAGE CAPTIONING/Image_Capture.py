import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore")

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import matplotlib.pyplot as plt
import requests
from io import BytesIO

print("Enter image path or URL:")
while True:
    x = input(">>> ").strip().strip("'\"")
    try:
        if x.lower().startswith(('http://', 'https://')):
            print("Fetching image...")
            r = requests.get(x, timeout=15, stream=True)
            r.raise_for_status()


            final_url = r.url.lower()
            if not any(final_url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']):

                content_type = r.headers.get('content-type', '')
                if not content_type.startswith('image'):
                    print("URL doesn't point to a direct image (try a .jpg or .png link)")
                    continue

            i = Image.open(BytesIO(r.content)).convert("RGB")
        else:
            if not os.path.exists(x):
                print("File not found!")
                continue
            i = Image.open(x).convert("RGB")
        break
    except Exception as e:
        print("Load failed:", str(e)[:50] + "..." if len(str(e)) > 50 else str(e))
        print("👉 Try again:")

print("Generating caption...")
p = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
m = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

inp = p(i, return_tensors="pt")
out = m.generate(**inp, max_new_tokens=50, num_beams=5)
cap = p.decode(out[0], skip_special_tokens=True).capitalize()
if cap and cap[-1] not in '.!?': cap += '.'

def w(t, l=50):
    wds, ln, ls = t.split(), "", []
    for wd in wds:
        if len(ln + wd) <= l: ln += wd + " "
        else: ls.append(ln); ln = wd + " "
    ls.append(ln)
    return '\n'.join(ls)

plt.figure(figsize=(10, 7))
plt.imshow(i)
plt.axis("off")
plt.title(f"{w(cap)}", fontsize=12, loc='left')
plt.tight_layout()
plt.show()

print("\n" + "="*80)
print("Caption:", cap)
print("="*80)
