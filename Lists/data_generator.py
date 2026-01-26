import lorem

OUTPUT_FILE = "huge_lorem.txt"
PARAGRAPH_COUNT = 10_000_000_000   # 10 billion paragraphs

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i in range(PARAGRAPH_COUNT):
        paragraph = lorem.paragraph()
        f.write(paragraph + "\n\n")

print("Done! File generated:", OUTPUT_FILE)
