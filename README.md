🧠 NIZEN | Neurodegenerative Clinical Platform

NIZEN is a modular clinical monitoring platform designed for neurodegenerative diseases.

The current implementation focuses on Duchenne Muscular Dystrophy (DMD), with a scalable architecture planned to support additional conditions in future versions.

Built with Streamlit, SQLite, and Google Sheets integration, NIZEN operates in a hybrid local + cloud environment.

🎯 Vision

NIZEN aims to become a unified clinical tracking and collaboration platform for:

Duchenne Muscular Dystrophy (DMD)

ALS (planned)

SMA (planned)

Other neurodegenerative disorders (future expansion)

The system is designed to be disease-modular and extensible.

🚀 Current Module: DMD
🔐 Secure Authentication

Role-based access (Family / Doctor / Researcher / Admin)

Password hashing (bcrypt / fallback support)

Persistent session tokens

Admin bootstrap support

📊 Clinical Tracking

NSAA score monitoring

Weight & age tracking

Historical data logging

Timestamp-based conflict resolution

☁️ Hybrid Architecture

Local-first SQLite storage

Google Sheets cloud sync

Offline-safe sync queue

Automatic health checks

🤖 Optional AI Assistant

OpenAI API integration

Safe medical-response prompting

Escalation guidance for emergencies

📰 Research & News Feed

DMD-related RSS integration

Language filtering (TR / EN)

🏗️ Tech Stack

Python

Streamlit

SQLite

Pandas

streamlit-gsheets

bcrypt

ReportLab

📂 Project Structure
final_v50.py
/data
   ├── dmd_local.db
   ├── dmd_users.json
   ├── dmd_profiles.json
   ├── sync_queue.json
   └── uploads/
⚙️ Installation
pip install -r requirements.txt
streamlit run final_v50.py
🔮 Roadmap

Multi-disease module architecture

Advanced analytics dashboard

Clinical report generation

Research-mode data export

Secure multi-center deployment

Regulatory compliance pathway

⚠️ Disclaimer

NIZEN is currently a research-oriented prototype and is not intended for certified medical deployment without regulatory approval.
