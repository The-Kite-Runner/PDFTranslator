from docx import Document


def writeWord(text_file_path):
    document = Document()
    with open(text_file_path, 'r') as text_file:
        while True:
            try:
                line: str = text_file.readline()
                if not line:
                    break
                paragraph = document.add_paragraph(line)
            except:
                print("Get error in convert text to word")

    # Save word file
    word_file_path = text_file_path.split('.txt')[0] + '.docx'
    print("save to ", word_file_path)
    document.save(word_file_path)
