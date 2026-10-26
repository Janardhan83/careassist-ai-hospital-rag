import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load environment variables
load_dotenv()

# 2. Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Please add GEMINI_API_KEY to your .env file")

# 3. Create Flask app
app = Flask(__name__)

# 4. Load the same local embedding model used in developer.py
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 5. Create Gemini chat model for answer generation
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0.65,
)

# 6. Map each department to its ChromaDB folder
# These names must match the folders created by developer.py.
department_db = {
    "Reception": "01_reception.txt database",
    "Billing": "02_billing.txt database",
    "Insurance": "03_insurance.txt database",
    "Cardiology": "04_cardiology.txt database",
    "Neurology": "05_neurology_brain_tumor.txt database",
    "Pharmacy": "06_pharmacy.txt database",
    "Emergency": "07_emergency.txt database",
}


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = ""
    sources = []

    if request.method == "POST":
        department = request.form.get("department", "").strip()
        question = request.form.get("question", "").strip()

        # 7. Validate user input
        if department not in department_db:
            answer = "Please select a valid hospital department."

        elif not question:
            answer = "Please enter a question."

        else:
            database_path = os.path.join(
                "db_gemini",
                department_db[department],
            )

            # 8. Check whether the selected department database exists
            if not os.path.isdir(database_path):
                answer = (
                    "The department knowledge base was not found. "
                    "Please run developer.py first."
                )

            else:
                try:
                    # 9. Load the selected department's ChromaDB
                    vector_db = Chroma(
                        persist_directory=database_path,
                        embedding_function=embedding_model,
                    )

                    # 10. Retrieve the five most relevant chunks
                    docs = vector_db.similarity_search(
                        question,
                        k=5,
                    )

                    if not docs:
                        answer = (
                            "I could not find relevant information in "
                            "this department's knowledge base."
                        )

                    else:
                        # 11. Collect source filenames from retrieved documents
                        sources = sorted(set(
                            os.path.basename(
                                document.metadata.get("source", "Unknown document")
                            )
                            for document in docs
                        ))

                        # 12. Combine retrieved chunks into context
                        context = "\n\n".join(
                            document.page_content for document in docs
                        )

                        # 13. Prepare the prompt for Gemini
                        prompt = f"""
                                You are a hospital information assistant.
                                
                                Answer the user's question using only the context provided below.
                                If the context does not contain the answer, clearly say that the
                                information could not be found in this department's knowledge base.
                                Do not guess or invent information.
                                Do not diagnose medical conditions or prescribe medicines.
                                For urgent or life-threatening situations, advise the user to seek
                                immediate professional medical help.
                                
                                Context:
                                {context}
                                
                                Question:
                                {question}
                                
                                Answer:
                                """

                        # 14. Generate the answer using Gemini
                        response = llm.invoke(prompt)
                        answer = response.text

                        if not isinstance(answer, str):
                            answer = str(answer)

                except Exception as error:
                    # Show technical details in the terminal, not on the page
                    print("Error while processing the question:", error)
                    answer = (
                        "Sorry, I could not process your question right now. "
                        "Please check the terminal for the error details."
                    )

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        sources=sources,
    )


if __name__ == "__main__":
    app.run(debug=True)
