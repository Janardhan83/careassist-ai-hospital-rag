# 🏥 CareAssist AI — Multi-Department Hospital Knowledge Assistant

**An AI-powered hospital information assistant that helps people access hospital-related information virtually, from anywhere.**

CareAssist AI is a Generative AI project built using Retrieval-Augmented Generation (RAG). It allows users to select a hospital department and ask questions in natural language, helping them find relevant information without needing to visit the hospital reception for every basic enquiry.

The project demonstrates how AI can make hospital information more accessible, convenient, and easier to understand.

> **Project status:** Working prototype. The current version uses sample hospital knowledge documents. Real-time hospital integrations, live doctor availability, appointment booking, and production deployment are future enhancements.

---

## 📌 1. Business Problem

Patients and their families often need to contact or visit a hospital simply to obtain basic information, such as:

- What are the hospital's working hours?
- Which doctors or specialists are associated with a department?
- What information is available about consultations and appointments?
- What are the billing and payment procedures?
- Which insurance-related documents may be required?
- What pharmacy services are described in the hospital's information?
- What emergency services and procedures are documented?

Depending on the hospital, obtaining these details may require phone calls, repeated enquiries, or an in-person visit.

### 💡 Proposed Solution

CareAssist AI explores how a virtual hospital information assistant can help users find answers through a simple web interface.

Instead of manually searching through hospital information or visiting the reception for basic enquiries, users can select a department, type a question in natural language, and receive an AI-generated answer based on the available department-specific knowledge base.

**Business vision:** Make reliable hospital information easier to access, reduce repetitive information enquiries, and help patients and caregivers find relevant information more conveniently.

---

## 🎯 2. Project Objectives

- Provide a simple, department-wise hospital information interface.
- Allow users to ask questions using natural language.
- Retrieve relevant information from hospital knowledge documents.
- Generate context-aware responses using a Large Language Model (LLM).
- Keep department knowledge bases separate to reduce irrelevant retrieval.
- Explore how Retrieval-Augmented Generation can support healthcare information services.

---

## ✨ 3. Key Features

### 🏥 Department-Specific Information
Users can select one of seven departments and query its associated knowledge base.

### 🔍 Semantic Search
The application retrieves relevant text chunks using vector similarity search instead of relying only on exact keyword matching.

### 🧠 Retrieval-Augmented Generation (RAG)
Retrieved document content is passed to Gemini as context to help generate answers grounded in the available information.

### 🤖 Generative AI Responses
The Gemini API generates natural-language answers based on the retrieved context.

### 💾 Local Embeddings
Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` model generates embeddings locally, reducing dependence on a paid or rate-limited embedding API.

### 🗂️ Department-Wise ChromaDB
Each department has its own vector database, allowing the application to search the selected department's knowledge base.

### 🌐 Web Interface
A Flask application provides a browser-based interface for selecting a department, entering a question, and viewing the response.

### 📚 Source Document References
The application can display the filenames associated with retrieved documents when the source metadata is available.

---

## 🏥 4. Supported Departments

| Department | Example information area |
|---|---|
| Reception | General hospital information and patient guidance |
| Billing | Billing and payment procedures |
| Insurance | Insurance documentation and claim-related information |
| Cardiology | Cardiology services described in the knowledge base |
| Neurology | Neurology and brain-tumour-related information |
| Pharmacy | Pharmacy information and procedures |
| Emergency | Emergency services and procedures described in the documents |

*The information available for each department depends on its source documents. These departments do not imply that the prototype is connected to live hospital systems.*

---

## 🛠️ 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Flask | Web application and request handling |
| LangChain | Document processing, embeddings integration, retrieval and LLM integration |
| Hugging Face Sentence Transformers | Local text embeddings |
| ChromaDB | Persistent vector storage and similarity search |
| Google Gemini API | Context-aware answer generation |
| HTML | Web interface structure |
| CSS | Styling and responsive presentation |
| python-dotenv | Loading the Gemini API key from environment variables |

---

## 🧠 6. System Architecture

CareAssist AI follows a Retrieval-Augmented Generation workflow with separate indexing and question-answering stages.

### Stage A: Knowledge Base Preparation

1. Load the department text documents.
2. Split the documents into smaller text chunks.
3. Generate embeddings using the local Hugging Face model.
4. Store the chunks and their vector representations in department-specific ChromaDB databases.

### Stage B: User Question Processing

1. The user opens the Flask web application.
2. The user selects a hospital department and enters a question.
3. The application loads the selected department's vector database.
4. ChromaDB retrieves the most relevant text chunks using semantic similarity search.
5. The retrieved chunks and the user's question are sent to Gemini.
6. Gemini generates an answer using the supplied context and instructions.
7. The application displays the response on the web page.

### Architecture Diagram

```text
          Hospital Knowledge Documents
                       |
                       v
              Load Text Documents
                       |
                       v
                 Text Chunking
                       |
                       v
          Hugging Face Embeddings
              (Local Model)
                       |
                       v
       Department-Wise ChromaDB Storage
                       |
             Indexing Complete
                       |
                       v
              User Opens Website
                       |
                       v
          Select Department + Question
                       |
                       v
            Load Selected Database
                       |
                       v
             Semantic Similarity Search
                       |
                       v
             Retrieve Relevant Chunks
                       |
                       v
              Gemini API (LLM)
                       |
                       v
             Context-Aware Answer
                       |
                       v
                Flask Web Interface
```

**Important distinction:** Hugging Face handles embedding generation locally, while Gemini is used for answer generation through the API. The current application does not automatically receive live hospital data from external hospital systems.

---

## 📂 7. Project Structure

```text
careassist-ai-hospital-rag/
│
├── app.py
├── developer.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   ├── 01_reception.txt
│   ├── 02_billing.txt
│   ├── 03_insurance.txt
│   ├── 04_cardiology.txt
│   ├── 05_neurology_brain_tumor.txt
│   ├── 06_pharmacy.txt
│   └── 07_emergency.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── db_gemini/              # Generated locally
    ├── 01_reception.txt database/
    ├── 02_billing.txt database/
    └── ...                 # Remaining department databases
```

The `db_gemini/` directory is generated by `developer.py`. It does not need to be committed to GitHub when the databases can be rebuilt from the source documents.

The `.env` file is created locally and should never be uploaded because it contains the private API key.

---

## ⚙️ 8. Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version for the installed dependencies
- Git
- A Google Gemini API key
- Internet access for Gemini API requests and the initial model download

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/careassist-ai-hospital-rag.git
cd careassist-ai-hospital-rag
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure the Gemini API Key

Create a local `.env` file in the project root using `.env.example` as a template.

Add your own API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

Do not commit `.env` to GitHub.

### Step 5: Build the Vector Databases

Run:

```bash
python developer.py
```

This processes the department documents, generates local embeddings, and creates the ChromaDB databases.

The first execution may take additional time to download the Hugging Face model.

### Step 6: Start the Application

Run:

```bash
python app.py
```

### Step 7: Open the Application

Visit the local address shown in your terminal. With the default Flask configuration, this is:

```text
http://127.0.0.1:5000
```

Select a department, enter a question, and submit it to receive an answer.

---

## 📸 9. Application Screenshots

Screenshots of the running application will be added here to demonstrate the user interface and the question-answering workflow.

Create a folder named `screenshots/` in the project root and add your actual screenshots.

### Home Page

![CareAssist AI Home Page](screenshots/home.png)

### Department Selection

![Department Selection](screenshots/departments.png)

### AI-Generated Answer

![CareAssist AI Response](screenshots/answer.png)

*Replace these example image paths with your actual screenshot filenames. GitHub will display the images when the files exist at the specified paths.*

---

## 🚀 10. Future Enhancements

The long-term vision is to evolve CareAssist AI into a more comprehensive virtual hospital information service.

### Phase 1: Improve the Current Prototype
- Improve answer reliability and retrieval quality.
- Add automated tests and structured error handling.
- Improve source attribution and user experience.
- Evaluate answers against a set of representative questions.

### Phase 2: Connect Real Hospital Information
- Integrate verified hospital working hours and contact information.
- Connect to authorised doctor directories and appointment schedules.
- Add a reliable process for keeping hospital information up to date.
- Introduce multilingual support for users who prefer regional languages.

### Phase 3: Develop Patient-Facing Services
- Enable appointment enquiries and, where supported, secure appointment booking.
- Add approved hospital-system integrations.
- Introduce authentication and access controls where required.
- Add privacy, monitoring, reliability and deployment controls.
- Evaluate security and healthcare-specific compliance requirements before public deployment.

### Long-Term Vision

Enable patients and caregivers to access verified hospital information virtually, reducing unnecessary visits for basic enquiries and making hospital services easier to navigate.

These are planned improvements, not features currently implemented in the prototype.

---

## ⚠️ 11. Limitations and Responsible Use

- This project is a prototype and is not a production-ready healthcare system.
- Answers depend on the quality, completeness and accuracy of the supplied knowledge documents.
- The application is not connected to live doctor schedules, hospital databases, or real appointment-booking systems.
- The application does not provide a verified real-time availability service.
- It must not be used as a substitute for professional medical advice, diagnosis or treatment.
- Users should contact the hospital directly to confirm important details, such as current schedules, fees, insurance acceptance and service availability.
- Emergency situations require immediate contact with local emergency services or qualified medical professionals.

Before deployment for public use, the system would require appropriate security, privacy, data validation, monitoring, reliability testing and authorised integrations.

---

## 👨‍💻 12. Learning Outcomes

This project demonstrates practical experience with:

- Building a RAG pipeline from document ingestion to answer generation.
- Implementing local text embeddings with Hugging Face.
- Storing and retrieving vector embeddings using ChromaDB.
- Integrating an LLM API into a Python application.
- Building a Flask-based web interface.
- Managing environment variables and application configuration.
- Organising department-specific knowledge bases.

---

## 📄 13. License

Choose and add a suitable open-source license before distributing the project. Ensure that you have permission to publish the source documents and any third-party material included in the repository.

---

## ⭐ Final Note

CareAssist AI is a learning and portfolio project exploring how Retrieval-Augmented Generation can make hospital information easier to access.

The goal is to build a foundation that could eventually support a more reliable, connected and accessible virtual hospital information service.
