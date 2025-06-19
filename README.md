# Construction Documentation Agent

This repository contains the implementation of a Retrieval-Augmented Generation (RAG) pipeline designed to query and reason over structured document logs. Each log record represents a snapshot of the status of key project-related documents — such as inspection requests, shop drawings, and management documents — at a specific point in time.

---

## 📌 Project Overview

This RAG pipeline allows users to query a document tracking log using natural language. It leverages retrieval techniques to fetch relevant records from the log and then uses a language model to generate informative and context-aware responses.

### ✅ Features

- Efficient retrieval of relevant document records
- Natural language question-answering over structured log data
- Handles time-series records representing document status snapshots
- Supports inspection, shop drawing, and management documents
- Modular and extensible RAG design for easy adaptation

---

## 🧠 Background

In many construction and engineering projects, document control is critical. Logs tracking the status of inspection requests, shop drawings, and various management approvals are often used to monitor project progress. This project explores using a RAG pipeline to make these logs more accessible and queryable by natural language.

