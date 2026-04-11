## 🧠 Tech Stack

- **Embedding Model:** Cohere  
- **Vector Database:** Qdrant  
- **Chat Completion Models:** Gemini, GROQ (LLaMA 3.1 8B Instant)  
- **Caching / Storage:** Upstash Redis (Cloud)

---

## ⚙️ Architecture Overview

- User input is processed and converted into embeddings using **Cohere**
- Embeddings are stored and retrieved from **Qdrant** for semantic search
- Relevant context is passed to LLMs (**Gemini / GROQ**) for generating responses
- **Upstash Redis** is used for Async Queues
- **rq** is used for distibuted workers
