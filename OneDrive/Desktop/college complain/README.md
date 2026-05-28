# 🏫 College Complaint Management System

The **College Complaint Management System** is a web-based application built to streamline, organize, and manage student and faculty grievances within an academic institution. The project provides a secure, transparent, and asynchronous platform to file complaints, track their resolution status, and manage administrative workflows efficiently.

## 📁 Technical Architecture & Packages

The repository is structured around a Python virtual environment containing robust libraries tailored for security, concurrency, and web services:

* **Core Framework Stack**: Built on the Python ecosystem using web frameworks designed to separate configuration, localization settings, and modular application logic.
* **Asynchronous & Concurrency Control**: Utilizes **`anyio`** and **`asgiref`** to manage asynchronous tasks and handle multiple incoming requests simultaneously without performance degradation.
* **Security & Encryption**: Integrated with **`cryptography`**, **`cffi`**, and **`certifi`** to enforce secure user authentication, token-based sessions, and encrypted data handling for confidential complaints.
* **Environment & Logs**: Uses a localized **`.env`** configuration file to securely mask sensitive API keys and database credentials. It also incorporates **`colorama`** to provide clean, color-coded administrative logs directly in the terminal interface.

## 🚀 Key Features

* **Grievance Portal**: An intuitive interface for users to submit structured complaints under specific categories (e.g., academics, infrastructure, hostel, ragging).
* **Live Tracking Module**: Allows students to check real-time updates on their tickets (e.g., *Pending, Under Investigation, Resolved*).
* **Admin Dashboard**: A control panel for college administrators to sort, prioritize, assign, and update complaints seamlessly.

## 🔧 Getting Started

1. **Activate Environment**: Navigate to the folder and activate the embedded environment:
```bash
   ux college complain/.venv/Scripts/activate