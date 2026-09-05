from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=500, overlap=20):
    
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=overlap
    )

    chunks = splitter.split_text(text)

    return chunks