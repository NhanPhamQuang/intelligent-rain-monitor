# 🌧️ Rain Prediction & Monitoring System

An end-to-end Machine Learning system for rainfall prediction and weather monitoring, built with **Python, Streamlit, and Scikit-learn**.

---

## 🚀 Features

* 📊 Interactive dashboard (Streamlit UI)
* 🌦️ Rain prediction using ML models
* 📈 Model performance visualization (Accuracy, F1, Confusion Matrix)
* 🧠 Trained ML pipeline (production-ready structure)
* 📂 Modular codebase (utils, models, data separation)

---

## 🏗️ Project Structure

```
weather-ml-app/
│
├── app.py                  # Main Streamlit app
├── pages/                 # Multi-page UI
│   ├── dashboard.py
│   └── prediction.py
│
├── models/                # Saved ML models (.pkl)
├── data/                  # Dataset (ignored in git)
├── utils/                 # Helper functions
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/weather-ml-app.git
cd weather-ml-app
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate:

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

App will be available at:

```
http://localhost:8501
```

---

## 📊 Model Details

* Algorithm: Random Forest (default)
* Task: Binary Classification (Rain / No Rain)
* Features include:

  * Temperature (Min/Max)
  * Humidity
  * Pressure
  * Wind Speed
  * Cloud coverage
  * Rainfall indicators

---

## 🧠 Workflow

1. Load dataset from `/data`
2. Preprocess (cleaning, encoding, scaling)
3. Train model & save to `/models`
4. Serve predictions via Streamlit UI

---

## 📁 Notes

* `data/` is ignored to avoid large file commits
* `models/` contains trained artifacts
* Use `.env` for sensitive configs if needed

---

## 🔥 Future Improvements

* ✅ MLOps pipeline (CI/CD + model versioning)
* ✅ Docker deployment
* ✅ Real-time weather API integration
* ✅ Model monitoring & drift detection

---

## 👨‍💻 Author

Built as a practical ML system project (not just a notebook 😏)

---

## 📜 License

MIT License
