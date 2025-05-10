# ML‑CR‑PROJECT

**Interactive Web‑based Character Recognition with User Feedback**

A full‑stack application where users draw handwritten characters in the browser, receive predictions from three models (CNN, RNN, Logistic Regression), and submit corrections for future retraining.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [File Structure](#file-structure)  
6. [Model Files](#model-files)  
7. [Results Logging](#results-logging)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Features

- **Interactive Canvas**: Freehand drawing of characters in-browser.  
- **Multi‑Model Prediction**:  
  - Convolutional Neural Network (CNN)  
  - Recurrent Neural Network (RNN)  
  - Logistic Regression (LR)  
- **REST API**: Endpoints for `/predict/cnn`, `/predict/rnn`, `/predict/lr`.  
- **Feedback Loop**: User corrections are logged to improve model accuracy.  
- **Offline CLI**: Run inference locally with `*_infer.py` scripts.  

---

## Prerequisites

- **Backend**  
  - Python 3.8+  
  - pip  
- **Frontend**  
  - Node.js 14+  
  - npm or yarn  

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ML-CR-PROJECT.git
cd ML-CR-PROJECT

Refer to video for further explanation

