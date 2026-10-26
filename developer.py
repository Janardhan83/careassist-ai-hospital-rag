import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
# 1. Load environment variables
load_dotenv()

# 2. Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Please add GEMINI_API_KEY to your .env file")

# 3. Set project folders
project_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(project_folder, "data")
database_folder = os.path.join(project_folder, "db_gemini")
os.makedirs(database_folder, exist_ok=True)


# 4. Create  HuggingFaceEmbeddings model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2" )
# 4. Create Gemini embedding model
# embedding_model = GoogleGenerativeAIEmbeddings(
#     model="gemini-embedding-2",
#     google_api_key=api_key,
# )


# 5. Set up text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size= 500,
    chunk_overlap= 200,
)

# 6. Load each department document and create its ChromaDB
for file_name in sorted(os.listdir(data_folder)):
    if not file_name.endswith(".txt"):
        continue

    database_path = os.path.join(
        database_folder,
        file_name + " database",
    )

    # Skip databases that have already been created
    if os.path.isfile(os.path.join(database_path, "chroma.sqlite3")):
        print(f"Database already exists for {file_name}. Skipping it.")
        continue

    file_path = os.path.join(data_folder, file_name)

    print(f"\nLoading document: {file_name}")

    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    chunks = text_splitter.split_documents(documents)
    print("Number of chunks:", len(chunks))

    Chroma.from_documents( documents=chunks,
                           embedding=embedding_model,
                           persist_directory=database_path,)

    print(f"Gemini database created: {database_path}")

print("\nDepartment document processing completed.")
