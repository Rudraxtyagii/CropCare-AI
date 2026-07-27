# CropCare AI: Final Project Structure

```text
CropCare-AI (C:\major project)
│
├── backend/
│   ├── __pycache__/
│   ├── disease_info.py           # Structured knowledge base covering 38 PlantVillage disease classes
│   └── main.py                   # Production FastAPI server with CORS, validation, and rich JSON responses
│
├── frontend/
│   ├── index.html                # Modern UI layout with Hero section, result cards, and statistics dashboard
│   ├── script.js                 # Frontend logic: drag-and-drop, API integration, LocalStorage history & stats
│   └── styles.css                # Premium glassmorphism styling, animations, and responsive layout
│
├── model/
│   ├── __pycache__/
│   ├── inference.py              # PyTorch inference engine with MobileNetV2 preprocessing & Mock Mode fallback
│   └── train.py                  # PyTorch transfer learning training script for PlantVillage dataset
│
├── docs/
│   ├── TECHNICAL_REPORT.md       # Full academic project report (Methodology, Architecture, Results)
│   ├── TITLE_PAGE.md             # Formal university project submission title page
│   └── VERIFICATION_REPORT.md    # Complete Quality Assurance, Testing, and Audit Report
│
├── check_dependencies.py         # Verification script testing all Python package imports
├── dependency_check.md           # Generated report verifying dependency imports
├── generate_api_evidence.py      # Script generating live runtime API test evidence
├── api_test_results.md           # Live runtime evidence of /predict endpoint (200 OK, 400 Bad Request, 422)
├── make_pdf.py                   # Script used to generate PDF documentation summaries
├── make_ppt.py                   # Script used to generate Presentation slides
├── Presentation.pptx             # Professional presentation slides for project demonstration
├── README.md                     # Comprehensive project documentation, architecture diagram, and setup instructions
├── requirements.txt              # Production Python dependencies (FastAPI, PyTorch, Uvicorn, Pillow, etc.)
├── Summary.pdf                   # Executable project summary report
├── test_api.py                   # Automated end-to-end API verification test suite
├── test_file.txt                 # Test artifact for verifying invalid text upload rejection (400 Bad Request)
├── test_img.jpg                  # Test artifact for verifying valid image upload (200 OK)
└── test_large.jpg                # Test artifact for verifying oversized file rejection (400 Bad Request)
```
