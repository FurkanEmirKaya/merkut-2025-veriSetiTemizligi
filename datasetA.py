
# %%
import pandas as pd
import plotly as pt
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import os
import re
# %%
print("Çalışma dizini:", os.getcwd())
os.chdir("C:/Users/furka/Desktop/Furkan_Emir/Merküt_Takımı/LLM/Spyder Works")
print("Yeni Çalışma dizini:", os.getcwd())

# %%
# csv dosyasını yedekleme
def copy_csv(filepath):
    df = pd.read_csv(filepath)
    df.to_csv('copy_of_datasetA.csv', index=False)

# %%
df = pd.read_csv("C:\\Users\\furka\\Downloads\\Yeni Verisetleri\\A\\fazla_veri.csv")

print(df.head())
print(df.info())
print(df.describe())
# %%
copy_csv("C:\\Users\\furka\\Downloads\\Yeni Verisetleri\\A\\fazla_veri.csv")

# Delimiter değiştirme
df_copy = pd.read_csv("copy_of_datasetA.csv", delimiter=',', quotechar='"', skipinitialspace=True)

df_copy.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

# %%
# Sütunları yer değiştirme
df_reordered = df_copy.iloc[:, [0, 2, 1]]
df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

# %%
# Eksik veri içeren sütunları başka bir dosyaya yaz
input_file = 'output_datasetA.csv'
output_file = 'eksik_sutunlar.csv'

expected_delimiters = 2

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

good_lines = []
bad_lines = []

for line in lines:
    line = line.strip()
    delimiter_count = line.count('|')
    
    if delimiter_count == expected_delimiters:
        good_lines.append(line)
    else:
        bad_lines.append(line)

with open(input_file, 'w', encoding='utf-8') as f:
    for line in good_lines:
        f.write(line + '\n')

with open(output_file, 'w', encoding='utf-8') as f:
    for line in bad_lines:
        f.write(line + '\n')

df_reordered = pd.read_csv(input_file, delimiter='|')
# %%
df_reordered = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

# Text sütununda ardışık tırnak işaretlerini tek tırnak işaretine düşür.
df_reordered['text'] = df_reordered['text'].apply(lambda x: re.sub(r'"+', '"', x) if pd.notna(x) else x)

# Text sütununun başındaki ve sonundaki boşlukları sil.
df_reordered['text'] = df_reordered['text'].str.strip()

# Text sütununda NaN değer olan satırları sil.
df_reordered = df_reordered.dropna(subset=['text'])

# 5 karakterden kısa cümleleri sil. 
initial_count = len(df_reordered)
df_reordered = df_reordered[df_reordered['text'].str.len() >= 5]
final_count = len(df_reordered)


df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

print(f"{initial_count - final_count} kısa veya boş satırlar çıkarıldı.")

# %%
# Boş satırları kaldır
df_reordered.dropna(how='all', inplace = True)
df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

df_reordered['text'] = df_reordered['text'].str.strip()

df_reordered = df_reordered.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

# %%

# Dosyayı oku
df_reordered = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

# Sadece tek karakterden oluşan text kolonlarını filtrele
initial_len = len(df)
df_reordered = df_reordered[df_reordered['text'].str.strip().str.len() > 1]
final_len = len(df)

# Kaydet
df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

print(f"{initial_len - final_len} tek harflik satır silindi.")
# %%

def advanced_quote_cleaner(text):
    if pd.isna(text):
        return text
    
    # Birden fazla ardışık tırnak işareti varsa sil.
    text = re.sub(r'"{2,}', '"', text)
    text = re.sub(r'"{3,}', '"', text)

    # 2. Çift tırnak işaretli olan kelimeleri tek tırnak işaretli hale getir.
    text = re.sub(r'""(\w+)""', r'"\1"', text) # Baş
    text = re.sub(r'(\w+)""', r'\1"', text) # Son
    text = re.sub(r'""(\w+)""', r'"\1"', text) # Hem baş hem son
    
    # 3. Baştaki ve sondaki tırnak işaretlerini sil.
    text = re.sub(r'^"+', '"', text)
    text = re.sub(r'"+$', '"', text)

    # 4. Boşlukları sil.
    return text.strip()

df_reordered = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

df_reordered['text'] = df_reordered['text'].apply(advanced_quote_cleaner)

df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')
# %%
df_reordered.to_csv("output_datasetA_backup.csv", sep='|', index=False, lineterminator='\n')

df_reordered = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

# 2. Tırnak içeren satırları filtrele
contains_quote = df_reordered['text'].str.contains('"', na=False)

# 3. Tırnak içeren satırları ayrı bir dosyaya kaydet
df_reordered[contains_quote].to_csv("tirnakli_satirlar.csv", sep='|', index=False, lineterminator='\n')

# 4. Tırnak içermeyen satırları orijinal dosyaya yaz
df_reordered[~contains_quote].to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

print(f"{contains_quote.sum()} satır 'tirnakli_satirlar.csv' dosyasına kopyalandı ve ana dosyadan çıkarıldı.")

# %%
# 1. Fazla tırnak temizleyici fonksiyon
def clean_extra_quotes(text):
    if pd.isna(text):
        return text
    
    # Fazla tırnakları tek tırnağa indir (""" → ")
    text = re.sub(r'"{2,}', '"', text)
    
    # Baştaki ve sondaki fazla tırnakları sil
    text = re.sub(r'^"+', '', text)
    text = re.sub(r'"+$', '', text)
    
    # Boşlukları temizle
    return text.strip()

# 2. Tırnaklı satırları oku
df_quotes = pd.read_csv("tirnakli_satirlar.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

# 3. 'text' sütunundaki fazla tırnakları temizle
df_quotes['text'] = df_quotes['text'].apply(clean_extra_quotes)

# 4. Temizlenmiş orijinal dosyayı oku
df_clean = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

# 5. Temizlenmiş tırnaklı satırları geri ekle
df_merged = pd.concat([df_clean, df_quotes], ignore_index=True)

# 6. Final dosyayı yaz
df_merged.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

print(f"{len(df_quotes)} satır temizlendi ve yeniden ana dosyaya eklendi.")
# %%
def remove_links_and_hashtags(text):
    if pd.isna(text):
        return text
    
    # 1. URL'leri sil
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # 2. Hashtag'leri sil (#tag)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'#', '', text)
    
    # @ olan cümlelerdeki kelimeler silinecek.
    
    # 3. Fazla boşlukları sadeleştir
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

df_reordered.to_csv("output_datasetA_backup.csv", sep='|', index=False, lineterminator='\n')

df_reordered = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_MINIMAL, dtype=str)

# Temizliği uygula
df_reordered['text'] = df['text'].apply(remove_links_and_hashtags)

# Geri kaydet
df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')

print("Link ve hashtag temizliği tamamlandı.")
# %%

good_lines = []
bad_lines = []

with open("output_datasetA.csv", "r", encoding="utf-8") as f:
    for line in f:
        if line.count('|') == 2:
            good_lines.append(line.strip())
        else:
            bad_lines.append(line.strip())

# Kırık satırları kaydet
with open("kotu_satirlar.csv", "w", encoding="utf-8") as f:
    for line in bad_lines:
        f.write(line + '\n')

# Temiz dosyayı tekrar yaz
with open("output_datasetA.csv", "w", encoding="utf-8") as f:
    for line in good_lines:
        f.write(line + '\n')
        
print("Fazla delimiter tamamlandı.")
# %%

# 1. Emoji tespiti için regex
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # yüz ifadeleri
    "\U0001F300-\U0001F5FF"  # semboller & şekiller
    "\U0001F680-\U0001F6FF"  # araçlar, taşıtlar
    "\U0001F1E0-\U0001F1FF"  # bayraklar
    "\U00002700-\U000027BF"  # çeşitli semboller
    "\U0001F900-\U0001F9FF"  # ekstra ifadeler
    "\U00002600-\U000026FF"  # yıldız, güneş, vs.
    "]+", flags=re.UNICODE
)

def contains_emoji(text):
    if not isinstance(text, str):
        return False
    return bool(emoji_pattern.search(text))

def remove_emojis(text):
    if not isinstance(text, str):
        return ""
    return emoji_pattern.sub('', text).strip()

# 2. Veri setini oku
df_reordered = pd.read_csv("output_datasetA.csv", delimiter='|', quoting=csv.QUOTE_NONE, dtype=str)

# 3. Emojili satırları tespit et
mask_emoji = df_reordered['text'].apply(contains_emoji)

# 4. Emojili satırları ayrı dosyaya kaydet
df_reordered[mask_emoji].to_csv("emojili_satirlar.csv", sep='|', index=False, lineterminator='\n')
print(f" {mask_emoji.sum()} satır 'emojili_satirlar.csv' dosyasına loglandı.")

# 5. Emojileri sil
df_reordered['text'] = df['text'].apply(remove_emojis)

# 6. Boş kalan text hücrelerini sil
before = len(df_reordered)
df_reordered = df_reordered[df_reordered['text'].str.strip().astype(bool)]
after = len(df_reordered)
print(f"{before - after} boş satır silindi.")

# 7. Geriye kalan temiz veri setini kaydet
df_reordered.to_csv("output_datasetA.csv", sep='|', index=False, lineterminator='\n')
print("output_datasetA.csv güncellendi.")
