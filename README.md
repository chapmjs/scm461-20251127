# Process Bottleneck Analyzer

A Streamlit web application for identifying and analyzing process bottlenecks based on Iravani's Operations Engineering and Management methodology.

## 🚀 Live Demo

Deploy this app on Streamlit Cloud by clicking the button below:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

## 📚 About

This application helps operations managers and students identify bottlenecks in multi-step processes by:
- Calculating capacity for each process step
- Identifying the constraining bottleneck
- Analyzing resource utilization
- Providing improvement recommendations

## 🛠️ Installation & Local Setup

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the app:
```bash
streamlit run bottleneck_analyzer.py
```

## 📋 Features

- **Process Input**: Define process steps with resources and processing times
- **Bottleneck Analysis**: Automatic identification of system constraints
- **Visualizations**: Interactive charts for capacity and utilization
- **Reporting**: Downloadable analysis reports in Markdown and CSV formats

## 🎓 Educational Use

This tool is designed for:
- Operations Management courses (SCM 361, 461, 478)
- Teaching bottleneck theory from Chapters 2 & 4 of Iravani's textbook
- Demonstrating capacity calculations and process improvement concepts

## 📁 Files

- `bottleneck_analyzer.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🚢 Deployment on Streamlit Cloud

1. Push these files to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and branch
5. Set the main file path as `bottleneck_analyzer.py`
6. Click "Deploy"

## 📧 Support

For questions or improvements, please open an issue on GitHub or contact your instructor.

## 📖 References

Based on concepts from:
- Iravani, S. *Operations Engineering and Management: Concepts, Analytics and Principles for Improvement*

---
*Built for BYU-Idaho Operations Management Education*
