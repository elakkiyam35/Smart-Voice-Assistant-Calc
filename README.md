# Smart Voice Assistant Calculator Using Artificial Intelligence

A modern, intelligent, responsive web application and voice assistant that performs basic, advanced, scientific, and business mathematical calculations. It understands natural English language commands and provides responses across three distinct output formats: **Voice Output**, **Text Output**, and **Visual Output**.

---

## 🌟 Key Features

### 1. Three Output Formats for Every Calculation
- **Voice Output**: Natural English speech using browser Text-to-Speech (`SpeechSynthesis`) with customizable voices, pitch, and speed.
- **Text Output**: Complete, readable English sentences (e.g. *"Your answer is 100."* or *"The square root of 144 is 12."*).
- **Visual Output**: Beautiful glassmorphic calculation cards featuring:
  - Mathematical operation badge and symbol
  - Clear mathematical expression notation
  - Large highlighted answer
  - Expandable step-by-step solution
  - Action buttons (*Speak Again*, *Copy Result*, *Repeat Calculation*)

### 2. Conversational Voice Assistant & Natural Language Understanding
- Spoken number conversion (e.g., *"twenty five plus one hundred"* ➔ `25 + 100 = 125`).
- Speech recognition via browser Web Speech API.
- Understands all English mathematical expressions:
  - **Addition**: *"2 plus 2"*, *"Add 10 and 20"*, *"What is the sum of 15 and 25?"*
  - **Subtraction**: *"10 minus 5"*, *"Subtract 5 from 10"*, *"What is 100 minus 25?"*
  - **Multiplication**: *"5 into 5"*, *"5 times 5"*, *"Multiply 10 by 20"*, *"Product of 6 and 7"*
  - **Division**: *"20 divided by 5"*, *"Divide 100 by 10"*, *"Quotient of 45 and 9"*
  - **Powers & Roots**: *"2 to the power 5"*, *"5 squared"*, *"Square root of 144"*, *"Cube root of 27"*
  - **Percentages**: *"20% of 500"*, *"Percentage increase from 50 to 75"*, *"Decrease 200 by 15 percent"*
  - **Statistics**: *"Average of 10, 20 and 30"*, *"Mean of 5, 10, 15, 20"*
  - **Business**: *"Cost price 100 selling price 120 find profit"*, *"Discount of 20% on 500"*
  - **Ratio & Modulus**: *"Ratio of 12 to 18"*, *"25 mod 4"*
  - **Scientific & Trig**: *"sin 30 degrees"*, *"cos 0"*, *"tan 45"*, *"5 factorial"*, *"5 P 2"*, *"5 C 2"*, *"log 100"*, *"ln e"*

### 3. Multi-Turn Follow-Up Conversations & Error Handling
- Context-aware follow-up: After every calculation, the assistant asks:
  > *"Would you like to perform another calculation?"*
- Displays selectable chips: **Addition**, **Subtraction**, **Multiplication**, **Division**, **Scientific**, **Main Menu**, **Exit**.
- Follow-up dialog memory:
  - User: *"No, I want subtraction."*
  - Assistant: *"Sure! Let's perform subtraction. Please tell me the numbers."*
  - User: *"50 and 20"* ➔ Assistant: *"Your answer is 30."*
- Intelligent Clarification for Incomplete Inputs:
  - User: *"20 divided by..."* ➔ Assistant: *"What number would you like to divide 20 by?"*
  - User: *"5"* ➔ Assistant: *"Your answer is 4."*
- Friendly error explanations (e.g. division by zero).

### 4. Image-Based Equation Solver (OCR)
- **Upload Image**: Drag and drop equation images (PNG, JPG, WEBP).
- **Camera Capture**: Live webcam photo capture.
- **Draw Scratchpad**: Interactive touchscreen/mouse handwriting scratchpad.
- Extracts mathematical expressions with OCR and solves them step-by-step.

### 5. Scientific Calculator
- Interactive scientific keypad with degree/radian toggle.
- Trigonometry, inverse trig, hyperbolic functions, logarithms, powers, roots, permutations ($nPr$), and combinations ($nCr$).

### 6. Calculation History
- Per-user and guest calculation history stored in SQLite.
- Re-run/repeat past equations, delete entries, and filter by category.
- Export history to CSV or JSON.

### 7. User Authentication & Settings
- Signup, Login, Forgot Password, and Logout with secure salted PBKDF2 hashing.
- Voice settings: Speech rate slider, pitch slider, voice dropdown selector, and voice on/off.
- Theme switch: Dark Mode and Light Mode.

---

## 🚀 How to Run the Application

### 1. Start the Web Server
Run:
```bash
python assist.py
```
Or with custom port / host:
```bash
python assist.py --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

### 2. Run the Interactive CLI Assistant (Optional)
If you wish to use the calculator entirely from the terminal:
```bash
python assist.py --cli
```

---

## 🧪 Running Tests
All unit and integration tests can be run with:
```bash
python -m unittest discover tests
```
Or individually:
```bash
python -m unittest tests/test_math_engine.py
python -m unittest tests/test_conversational.py
python -m unittest tests/test_full_system.py
```

---

## 📁 Project Structure

```
voice_assist/
├── assist.py                   # Main entry point (Web Server & CLI assistant)
├── server.py                   # FastAPI backend server with REST APIs
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── calculator.db               # SQLite database (Users, History, Settings)
├── core/
│   ├── math_engine.py          # SymPy-powered math engine with NLP parsing
│   ├── speech_nlp.py           # Words-to-numbers and intent classifier
│   ├── conversational.py       # Multi-turn conversation state machine
│   ├── ocr_engine.py           # Computer vision & OCR math extractor
│   └── database.py             # SQLite models and authentication
├── static/
│   ├── index.html              # Modern Single Page Application
│   ├── css/
│   │   ├── style.css           # Glassmorphism, themes, responsive layout
│   │   └── animations.css      # Voice waves, ripple effects, transitions
│   └── js/
│       ├── app.js              # Main application controller
│       ├── voice_assistant.js  # Speech recognition & synthesis engine
│       ├── scientific_calc.js  # Scientific calculator keypad controller
│       ├── image_calc.js       # Camera, upload, and scratchpad OCR
│       ├── history.js          # Calculation history manager
│       ├── auth.js             # Authentication controller
│       └── settings.js         # Settings & preference manager
└── tests/
    ├── test_math_engine.py     # Math engine test suite
    ├── test_conversational.py  # Multi-turn dialog test suite
    ├── test_full_system.py     # End-to-end integration test suite
    └── test_api.py             # Server API route tests
```

