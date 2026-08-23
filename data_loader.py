from pypdf import PdfReader
def load_pdf(file):
    reader =PdfReader(file)
    text=""
    for page in reader.pages:
        text+=page.extract_text()
       
    return text

def split_into_chunks(text,chunk_size=500):
    chunks=[]
    for i in range(0,len(text),chunk_size):
        chunk=text[i:i+chunk_size]
        chunks.append(chunk)
    return chunks
if __name__ =="__main__":
    pdf_text=load_pdf("pdfs/sample.pdf")
    chunks=split_into_chunks(pdf_text)
    print(f"Total chunks: {len(chunks)}")
    print(chunks[0])
