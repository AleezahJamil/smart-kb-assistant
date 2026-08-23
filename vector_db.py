import chromadb
client=chromadb.Client()
collection=client.create_collection(name="knowledge_base") #client = chromadb.PersistentClient(path="chroma_db") for creating database and storing it
def add_chunks(chunks):
    ids=[]
    for i,chunk in enumerate(chunks):
        ids.append("chunk_"+str(i))
    collection.add(
        documents=chunks,
        ids=ids
    )
def search(query,top_k=3):
    results=collection.query(
        query_texts=[query],
        n_results=top_k

    )
    return results["documents"][0]
if __name__ =="__main__":
    from data_loader import load_pdf , split_into_chunks
    pdf_text=load_pdf("pdfs/sample.pdf")
    chunks=split_into_chunks(pdf_text)
    add_chunks(chunks)
    results=search("python functions")
    print("top matches: ")
    for r in results:
        print("-",r[:100])