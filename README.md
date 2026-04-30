# 🎫 Ticket Sasa — Smart Ticket Management System

Welcome to **Ticket sasa** 🚀 — a powerful backend system built with **Django + Django REST Framework** for managing tickets, assignments, worklogs, and AI-powered summaries.

Think of it as your **helpdesk brain 🧠 + assistant 🤖 + manager 👨‍💼** all in one system.

---

## 🌟 Features

✨ **User Management**

* Register users 📝
* Login with JWT 🔐
* Role-based access (Admin 👑 / Technician 🛠 / User 🙋)

🎟 **Ticket System**

* Create and track tickets
* Update & delete tickets by owner or admin
* Optimized queries using `select_related` & `prefetch_related` ⚡

🤖 **AI Summaries**

* Automatically summarize ticket descriptions
* Generate:

  * Summary 🧾
  * Priority 🚨
  * Category 🗂
  * Suggestions 💡

📌 **Assignments**

* Assign tickets to Technicians
* Manage workload distribution

🗒 **Worklogs**

* Track progress on tickets
* Log notes and updates

---

## 🧠 Core Concept (Simple Mental Model)

```
User 👤 → creates → Ticket 🎟  
Ticket 🎟 → gets → AI Summary 🤖  
Ticket 🎟 → assigned via → Assignment 📌  
Ticket 🎟 → tracked with → Worklogs 🗒  
```

---

## 🔐 Authentication

We use **JWT (JSON Web Tokens)** via:

* Login → returns access + refresh tokens
* Refresh → get new access token

---

## 📡 API Endpoints

Base URL:

```
/api/v1/
```

---

### 🔑 Authentication

| Endpoint          | Method | Description   |
| ----------------- | ------ | ------------- |
| `/auth/users/`    | POST   | Register user   |
| `/auth/jwt/create`| POST   | Login and tokens |

---

### 👤 Users


### 🎟 Tickets

| Endpoint               | Method    | Description           |
| ---------------------- | --------- | --------------------- |
| `/tickets/`            | GET, POST | List / Create tickets |
| `/ticket/<id>/`        | GET       | Retrieve ticket       |
| `/ticket/update/<id>/` | PUT/PATCH | Update ticket         |
| `/ticket/delete/<id>/` | DELETE    | Delete ticket         |
| `/ticket/<id>/ai-summary` | POST , GET  | Post and get ai summarry ticket |
| `/ticket/<id>/worklogs/`| POST,GET,PUT,PATCH,DELETE| ticket worklogs by technician|


---

### 📌 Assignments

| Endpoint                   | Method    | Description               |
| -------------------------- | --------- | ------------------------- |
| `/assignments/`            | GET, POST | List / Create assignments |
| `/assignment/<id>/`        | GET       | Retrieve assignment       |
| `/assignment/update/<id>/` | PUT/PATCH | Update assignment         |
| `/assignment/delete/<id>/` | DELETE    | Delete assignment         |


---

## 🛡 Permissions

✔ Users can:

* Edit/delete **their own data**

✔ Admins can:

* Manage **everything**

👉 Powered by:

```
IsOwnerOrAdmin
```

---

## ⚙️ Tech Stack

* 🐍 Python
* 🌐 Django
* ⚡ Django REST Framework
* 🔐 JWT Authentication (`simplejwt`) with djoser
* 🧠 AI Service Integration - openrouter Api Key

---

## 🚀 Getting Started

### 1️⃣ Clone the repo

```bash
git clone <your-repo-url>
cd ticketingcore
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations

```bash
python manage.py migrate
```

### 5️⃣ Start server

```bash
python manage.py runserver
```

---

## 🎯 Example Flow

1. Register user 📝
2. Login → get token 🔐
3. Create ticket 🎟
4. Generate AI summary 🤖
5. Assign ticket 📌
6. Add worklogs 🗒

---

## 💡 Future Improvements

* 🔍 Search & filtering
* 📊 Dashboard analytics
* 📩 Email notifications
* 🌍 Frontend integration (React / Remix)

---

## 🏁 Final Thoughts

This project is a **solid foundation for a real-world ticketing/helpdesk system**.

It demonstrates:

* Clean API design 🧼
* Proper permissions 🔐
* Performance optimization ⚡
* AI integration 🤖

---

🔥 Built with a goal to get myself out there.
