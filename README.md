# 🚀 FlowML

FlowML is a high-performance, real-time data pipeline framework designed to simplify how developers and data practitioners process, transform, and monitor datasets at scale.

In modern data workflows, developers often struggle with fragmented tooling: scripts for preprocessing, separate systems for monitoring, and limited visibility into execution. Traditional pipelines are either slow, difficult to debug, or lack real-time feedback. FlowML addresses these gaps by providing a unified system that combines fast computation, structured pipelines, and live observability.

At its core, FlowML brings together a FastAPI-based backend, a Rust-powered execution layer, and WebSocket-driven real-time updates to create a seamless pipeline experience. Instead of writing isolated scripts or waiting for batch jobs to complete, users can define structured workflows, execute them asynchronously, and observe progress instantly.

---

## 🎯 Problem It Solves

Working with data pipelines often involves:

* Writing repetitive preprocessing scripts
* Handling large datasets with slow performance (pandas bottlenecks)
* Lack of real-time visibility into execution
* Poor orchestration of multiple steps
* Difficulty tracking job status and debugging failures

These challenges lead to inefficient workflows, delayed feedback, and increased development overhead.

---

## 💡 Solution

FlowML introduces a structured and scalable approach to data processing:

* A **pipeline engine** that allows step-by-step transformations
* A **background job system** for asynchronous execution
* A **real-time monitoring layer** using WebSockets
* A **Rust-powered processing core** for high-performance operations
* A **CLI + API interface** for flexible usage

This enables users to move from manual scripting to a **reusable, observable, and high-performance pipeline system**.

---

## ✨ Key Features

* ⚡ FastAPI backend for scalable API-driven workflows
* 🦀 Rust acceleration using Rayon for parallel data processing
* 🔄 Real-time updates via WebSockets (live job tracking)
* 🧠 Modular pipeline execution engine
* 🛠 CLI interface for automation and scripting
* 📂 Support for CSV, Excel, and database sources
* 🧹 Built-in data cleaning operations
* 📊 Data preview and summary statistics
* 🔄 Background job execution with progress tracking

---

## 🏗 System Architecture

FlowML is designed with a clear separation of concerns:

```
CLI / Frontend
      ↓
FastAPI Backend (API + WebSockets)
      ↓
Pipeline Engine (orchestration)
      ↓
Rust Core (parallel computation via Rayon)
```

This architecture ensures:

* Clean orchestration in Python
* High-performance execution in Rust
* Real-time communication via WebSockets

---

## ⚡ Performance Advantage

Unlike traditional pipelines that rely entirely on Python:

* FlowML delegates heavy computation to **Rust**
* Uses **Rayon for parallel execution**
* Avoids Python’s GIL limitations
* Handles large datasets efficiently

This results in significantly faster processing compared to pandas-only workflows.

---

## 🚀 Installation

```bash
pip install flowml-core
```

---

## 🧪 Local Development Setup

```bash
git clone https://github.com/Frosty-8/flowml
cd flowml
pip install -e .
```

---

## ▶️ Run Server

```bash
uvicorn flowml.api.server:create_app --factory --reload
```

---

## 🛠 CLI Usage

```bash
flowml run pipeline.json
flowml jobs
flowml status <job_id>
flowml preview <dataset_id>
```

---

## 📄 Example Pipeline

```json
{
  "dataset_id": "your-dataset-id",
  "steps": [
    { "step": "fill_nulls" },
    { "step": "drop_nulls" },
    { "step": "summary" }
  ]
}
```

---

## 🔄 CI/CD

FlowML includes automated workflows using GitHub Actions:

* ✅ Code linting and testing
* 🦀 Rust build integration
* 📦 Package build and PyPI deployment

---

## 📌 Roadmap

* ⚛️ Full React dashboard integration
* 🧩 Drag-and-drop pipeline builder
* ☁️ Cloud deployment support
* 🔐 Authentication and multi-user support
* 📊 Advanced visualization and analytics

---

## 👨‍💻 Author

Sarthak Dongare

---

## ⭐ Why FlowML Stands Out

FlowML is not just a script or utility—it is a **framework that bridges the gap between data engineering and real-time systems**, combining:

* Backend engineering
* Systems design
* Performance optimization
* Developer experience

It reflects a shift from simple data processing toward **scalable, observable, and high-performance data workflows**.

---

