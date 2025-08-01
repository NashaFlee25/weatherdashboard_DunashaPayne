# **Week 11 Capstone Planning – Dunasha Payne**

## **Fellow Details**

| Field                       | Your Entry        |
| --------------------------- | ----------------- |
| **Name**                    | Dunasha Payne     |
| **GitHub Username**         | NashaFlee25       |
| **Preferred Feature Track** | Visual            |
| **Team Interest**           | Yes — Contributor |

---

## ✍️ **Section 1: Week 11 Reflection**

### **What I’ve Learned So Far:**

* The capstone project is meant to reflect real-world code quality and structure.
* Features should connect and flow together — not feel random or separate.
* It’s important to build something that’s not just functional but also easy and enjoyable to use.
* This project should be portfolio-ready — something I’m proud to share.
* Documentation and testing are just as important as getting the app to work.

### **Skills I’m Most Comfortable With:**

* Using APIs — I’ve had success pulling and working with live data.
* Writing object-oriented code — I understand how to use classes and structure my app well.
* Git/GitHub — I'm confident pushing my work and tracking changes.

### **Skills I’m Still Building:**

* Laying out widgets and styling my app with Tkinter in a clean, organized way.
* Handling errors more gracefully and writing reusable helper functions.
* Adding comments and writing proper documentation for other people to follow.

### **What’s Been Tricky So Far:**

* Figuring out how to organize all the files and folders upfront.
* Getting my API key set up in a secure way without exposing it in the repo.
* Drawing custom visuals using the canvas tool in Tkinter.

### **How I’ll Keep Making Progress:**

* I’ll use office hours to get help when I’m stuck on layout or visual features.
* I’ll watch recorded sessions again to reinforce what I’ve learned.
* I’ll check in with others on Slack when I need feedback or bug help.

---

## 🧠 **Section 2: My Feature Choices**

| # | Feature Name    | Difficulty | Why I Picked It                                                                                                     |
| - | --------------- | ---------- | ------------------------------------------------------------------------------------------------------------------- |
| 1 | City Comparison | 2          | I want to show weather for two cities side-by-side — it’s a helpful, real-world feature I’d like to learn to build. |
| 2 | Weather Icons   | 3          | I want to learn how to create custom visuals using canvas to make the app more interactive and fun.                 |
| 3 | Theme Switcher  | 2          | I want to give users control over how the app looks and get better at building dynamic interfaces.                  |
| — | **Enhancement** | –          | I’ll be adding a day/night mode and custom colors to make the app more polished and personal.                       |

---

## 🗂️ **Section 3: App Structure Plan**

**Main App Folders:**

* `src/main.py` – where the app starts
* `src/config.py` – holds settings and keys
* `src/data/` – for saving files like logs or user settings
* `src/features/` – where all feature code lives

**Feature Files:**

* `src/features/city_comparison.py`
* `src/features/weather_icons.py`
* `src/features/theme_switcher.py`

**How Things Work Together:**

* `src/main.py` pulls from each feature as needed.
* API data is handled in a helper file.
* UI updates in real time when data comes in or user clicks something.

---

## 📊 **Section 4: My Data Plan**

| File Name             | Format | Sample Entry                                  |
| --------------------- | ------ | --------------------------------------------- |
| `weather_history.txt` | txt    | 2025-06-09,New Brunswick,78,Sunny             |
| `user_settings.json`  | json   | { "theme": "dark", "last\_city": "Atlanta" }  |
| `comparison_log.csv`  | csv    | 2025-07-01,New York,85,Cloudy,Boston,78,Sunny |

---

## 📆 **Section 5: My Timeline (Weeks 12–17)**

| Week | Monday                | Tuesday       | Wednesday          | Thursday            | Goal for the Week   |
| ---- | --------------------- | ------------- | ------------------ | ------------------- | ------------------- |
| 12   | Set up API            | Handle errors | Build app layout   | Catch-up day        | Basic app working   |
| 13   | Build City Comparison | —             | —                  | Connect to app      | Feature 1 finished  |
| 14   | Start Weather Icons   | —             | Test and review    | Wrap it up          | Feature 2 finished  |
| 15   | Build Theme Switcher  | Improve UI    | Handle more errors | Clean up code       | All 3 features done |
| 16   | Add Enhancement       | Write Docs    | Add Tests          | Get ready to submit | Full app is ready   |
| 17   | Practice Demo         | Catch up      | Present app        | —                   | Demo Day!           |

---

## ⚠️ **Section 6: Risks I’m Watching For**

| Problem                | Chance | Effect | How I’ll Handle It                                          |
| ---------------------- | ------ | ------ | ----------------------------------------------------------- |
| API Limit              | Medium | Medium | I’ll add a short delay and cache recent results.            |
| Canvas Graphics Issues | High   | Medium | I’ll keep the graphics simple and get feedback early.       |
| Theme Bugs             | Medium | High   | I’ll keep styling separate from core logic to avoid issues. |

---

## 🤝 **Section 7: Help I’ll Be Asking For**

* How to change the app’s theme while it’s running
* How to draw and update canvas weather icons
* How to cleanly organize my code into features
* Getting feedback on the user interface and layout

---

## ✅ **Section 8: Before Monday**

* ✅ Pushed `src/main.py`, `src/config.py`, and `src/data/` folder to my repo
* ✅ Added API key to `.env` file (not committed)
* ✅ Created feature files for:

  * `src/features/city_comparison.py`
  * `src/features/weather_icons.py`
  * `src/features/theme_switcher.py`
* ✅ Started my `README.md` file
* ☐ Will book office hours if anything gets confusing
