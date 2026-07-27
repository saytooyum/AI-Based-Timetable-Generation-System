# 🎓 AI-Based Timetable Generation System (NEP 2020)

An intelligent, AI-assisted timetable generation system designed to automate and optimize academic scheduling for multidisciplinary higher education programs aligned with NEP 2020.

---

## 🚀 Overview

With the introduction of flexible, credit-based multidisciplinary education under NEP 2020, manual timetable creation has become highly complex.

This project provides a **web-based solution** that:
- Automates timetable generation
- Eliminates scheduling conflicts
- Optimizes faculty workload and infrastructure usage
- Supports dynamic updates and scenario simulation



## ✨ Features

- ✅ Conflict-free timetable generation  
- 📊 Supports FYUP, B.Ed., M.Ed., and ITEP programs  
- 👨‍🏫 Faculty workload balancing  
- 🏫 Smart room allocation (capacity + type)  
- 🔄 Scenario simulation ("what-if" analysis)  
- ✏️ Manual editing with validation  
- 📤 Export to PDF & Excel  
- 🧩 Low-code / no-code compatible design  
- 💬 Natural language interaction (via MCP - experimental)  

---

## 🧠 How It Works

1. Upload structured data (students, courses, faculty, rooms)
2. The system processes constraints:
   - Faculty availability
   - Student course selections
   - Room capacity
3. AI/Optimisation engine generates timetable
4. Admin can:
   - Edit schedules
   - Simulate scenarios
   - Export results

---

## 🏗️ Architecture
```bash
User Interface (React / Bubble / Appsmith)
↓
API Layer (FastAPI)
↓
Solver Engine (OR-Tools)
↓
Database (Supabase / Firebase)
```
---

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Frontend    | React / Appsmith / Bubble |
| Backend     | FastAPI (Python) |
| Solver      | Google OR-Tools |
| Database    | Supabase / Firebase / Airtable |
| Automation  | Zapier / n8n |
| Deployment  | Docker / Render / Vercel |

---

## 📂 Sample Input Format

### courses.csv
course_code,course_name,credits,theory_hours,practical_hours
PHY101,Mechanics,4,3,1

### faculty.csv
faculty_id,name,available_slots,max_load
F001,Dr Rao,Mon_9-11|Tue_10-12,18
---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/saytooyum/AI-Based-Timetable-Generation-System.git
cd .\AI-Based-Timetable-Generation-System\
```

### 2. Backend setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Run solver (optional test)
```bash
cd solver
python timetable_solver.py
```
### 4. Frontend setup
```bash
cd frontend
npm install
npm start
```
## 🧪 Demo
![n8n workflow](Attachment\WhatsApp Image 2026-04-09 at 13.44.04.jpeg)
Upload sample CSV files from /data
Click Generate Timetable
View and edit schedule
Export as PDF/Excel

#### 📈 Evaluation Metrics
Conflict rate (target: 0%)
Faculty workload distribution
Room utilization efficiency
Generation time

#### 🔮 Future Improvements
ML-based demand prediction
Real-time LMS integration
Mobile app for students/faculty
Advanced scheduling (internships, fieldwork)
Full MCP integration for conversational UI

#### 🤝 Contributing
Contributions are welcome!
Feel free to fork the repo and submit a pull request.

#### 📜 License

This project is licensed under the MIT License.

#### 👨‍💻 Author
**Satyam Raina**

**GitHub**: https://github.com/saytooyum/

**LinkedIn**: https://www.linkedin.com/in/satyam-raina-915899323

#### ⭐ Acknowledgements

- NEP 2020 framework
- Google OR-Tools
- Open-source community
