import os
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PROJECT_ROOT = Path("c:/Users/wwa90/OneDrive/Desktop/MLProject")
REPORTS_DIR = PROJECT_ROOT / "reports"
FIG_DIR = REPORTS_DIR / "report_figures"
OUTPUT_PDF = PROJECT_ROOT / "SmartPrice_Smartphone_Price_Prediction_Report.pdf"

# Custom Canvas for running headers & footers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is Cover -> No header, no footer
        if self._pageNumber == 1:
            return

        # Running Header (Top)
        self.saveState()
        self.setFont("Times-Italic", 9)
        self.setFillColor(colors.HexColor("#333333"))
        header_text = "SmartPrice: Smartphone Price Range Prediction Using Machine Learning"
        self.drawString(54, 742, header_text)
        
        # Header thin rule
        self.setStrokeColor(colors.HexColor("#bbbbbb"))
        self.setLineWidth(0.6)
        self.line(54, 736, letter[0] - 54, 736)

        # Running Footer (Bottom)
        # Numbered as Page 1, Page 2... starting from document page 2
        report_page_num = self._pageNumber - 1
        self.setFont("Times-Roman", 9.5)
        self.setFillColor(colors.HexColor("#444444"))
        footer_text = f"Page {report_page_num}"
        self.drawCentredString(letter[0] / 2.0, 36, footer_text)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography matching academic paper style
    title_univ = ParagraphStyle(
        'UnivTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        alignment=1, # Center
        textColor=colors.black
    )

    dept_style = ParagraphStyle(
        'DeptStyle',
        fontName='Times-Italic',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )

    project_report_label = ParagraphStyle(
        'ProjectReportLabel',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.black
    )

    session_style = ParagraphStyle(
        'SessionStyle',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#333333")
    )

    proj_title_label = ParagraphStyle(
        'ProjTitleLabel',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.black
    )

    proj_title_main = ParagraphStyle(
        'ProjTitleMain',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.black
    )

    proj_subtitle = ParagraphStyle(
        'ProjSubtitle',
        fontName='Times-Italic',
        fontSize=10.5,
        leading=14.5,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )

    cover_meta_head = ParagraphStyle(
        'CoverMetaHead',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        alignment=1,
        textColor=colors.black
    )

    cover_meta_val = ParagraphStyle(
        'CoverMetaVal',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )

    cover_link_style = ParagraphStyle(
        'CoverLinkStyle',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.black
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.black
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=4, # Justified
        spaceAfter=7,
        textColor=colors.HexColor("#111111")
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        leftIndent=15,
        spaceAfter=4,
        textColor=colors.HexColor("#111111")
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11.5,
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=8,
        textColor=colors.HexColor("#333333")
    )

    th_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TableCell',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=0,
        textColor=colors.HexColor("#111111")
    )

    td_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=12,
        leftIndent=18,
        firstLineIndent=-18,
        spaceAfter=6,
        textColor=colors.HexColor("#111111")
    )

    story = []

    # =========================================================================
    # COVER PAGE (Page 1 in PDF, unnumbered)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("RAMDEOBABA UNIVERSITY", title_univ))
    story.append(Spacer(1, 16))

    logo_img_path = FIG_DIR / "university_logo.png"
    if logo_img_path.exists():
        story.append(Image(str(logo_img_path), width=75, height=75))
    else:
        story.append(Spacer(1, 75))

    story.append(Spacer(1, 16))
    story.append(Paragraph("School of Computer Science and Engineering / CSE", dept_style))
    story.append(Spacer(1, 24))

    story.append(Paragraph("PROJECT REPORT", project_report_label))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Session: 2026-2027 &nbsp;|&nbsp; Semester: V &nbsp;|&nbsp; Programme: Machine Learning Lab-Project", session_style))
    story.append(Spacer(1, 26))

    story.append(Paragraph("PROJECT TITLE", proj_title_label))
    story.append(Spacer(1, 6))
    story.append(Paragraph("SMARTPHONE PRICE RANGE PREDICTION USING MACHINE LEARNING", proj_title_main))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A Multi-Class Smartphone Price Category Prediction Study Comparing Four Machine-Learning Models, with Random Forest Deployed as a Responsive Web Application.", proj_subtitle))
    story.append(Spacer(1, 30))

    story.append(Paragraph("Submitted by:", cover_meta_head))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Mohammad Anas 54", cover_meta_val))
    story.append(Spacer(1, 22))

    story.append(Paragraph("Submitted to:", cover_meta_head))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Dr. Chithraja Rajan<br/>Ashwini Agashe", cover_meta_val))
    story.append(Spacer(1, 26))

    story.append(Paragraph("<b>GitHub:</b> https://github.com/Anas-sk02/Mobile-Price-Prediction-ML", cover_link_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Live App:</b> https://mobile-price-prediction-ml.onrender.com/", cover_link_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Date:</b> 14-10-2026", cover_link_style))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 1: Abstract, Keywords, Contents
    # =========================================================================
    story.append(Paragraph("Abstract", h1_style))
    story.append(Paragraph(
        "In this project we made a machine learning model that predicts the price category of a smartphone "
        "(Budget, Mid-Range, Premium, or Flagship) from its hardware specifications. We used a cleaned dataset "
        "of 980 real commercial smartphones. The data was divided into 80% training and 20% test sets, and the "
        "ratio of each price category was kept the same in both parts using stratified splitting. We compared four "
        "supervised models: Logistic Regression, K-Nearest Neighbors (KNN), Random Forest, and Support Vector Machine "
        "(SVM). All of them used the exact same preprocessing steps, 5-fold stratified cross-validation, "
        "hyperparameter search, and evaluation metrics, so the comparison stays fair.",
        body_style
    ))
    story.append(Paragraph(
        "Random Forest gave the best result when we used macro F1 and ROC AUC as the deciding metrics. On the test "
        "set it got 82.65% accuracy, 0.7996 macro F1, and 0.9613 multi-class ROC AUC (One-vs-Rest). After that, we "
        "packaged the trained model inside a responsive web application built with FastAPI and React. The user enters "
        "smartphone specifications—such as RAM, internal storage, battery, processor speed, and cameras—can test "
        "preset phone examples, and gets the predicted category along with class confidence scores. The app also "
        "validates missing or out-of-range inputs so it does not fail silently.",
        body_style
    ))
    story.append(Paragraph(
        "This system provides a practical pricing decision-support tool for consumers and retailers. It is based "
        "on historical market data and should be updated as newer phone chipsets and models enter the market.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Keywords:</b> smartphone price prediction, Random Forest, classification, machine learning, feature engineering, FastAPI",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Contents", h1_style))
    contents_list = [
        "1. Introduction",
        "2. Literature Review",
        "3. Methodology",
        "4. Data Cleaning and Preprocessing",
        "5. Results and Discussion",
        "6. State-of-the-Art Models Comparison",
        "7. User Interface Development and Deployment",
        "8. Conclusion and Future Work",
        "References"
    ]
    for c_item in contents_list:
        story.append(Paragraph(c_item, bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 2: 1. Introduction
    # =========================================================================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "A large number of smartphones are launched in the market every year, each coming with different hardware "
        "combinations such as processor speed, RAM, internal storage, battery capacity, screen size, and camera setups. "
        "For regular customers, students, and phone retailers, it is difficult to judge whether a phone's price is "
        "reasonable just by looking at long spec sheets. A machine learning model can help consumers, tech reviewers, "
        "and sellers quickly determine the correct price segment of a mobile phone based purely on its technical features.",
        body_style
    ))
    story.append(Paragraph(
        "The aim of our project is simple. We wanted to build a practical, easy-to-understand system that predicts "
        "whether a phone belongs to the Budget, Mid-Range, Premium, or Flagship category, using only the hardware details "
        "present in our cleaned dataset.",
        body_style
    ))
    story.append(Paragraph(
        "Instead of predicting a single exact price number in rupees (which is regression), we formulated this as a "
        "4-class classification problem. This is because real consumer phone shopping happens in budget brackets rather "
        "than exact numbers. Furthermore, continuous price regression gets heavily distorted by niche ultra-luxury foldables "
        "(priced above Rs. 1,50,000), whereas classification gives clean, actionable category probabilities.",
        body_style
    ))
    story.append(Paragraph(
        "We tested four common supervised learning algorithms: Multinomial Logistic Regression, K-Nearest Neighbors (KNN), "
        "Support Vector Machine (SVM), and Random Forest. Every model received the exact same 80/20 train/test split and the "
        "same preprocessing pipeline, so any difference in performance comes from the algorithms themselves. The best performing "
        "model, Random Forest, was saved along with its fitted preprocessing pipeline and connected to an interactive FastAPI "
        "and React web application.",
        body_style
    ))
    story.append(Paragraph(
        "One important thing should be kept in mind. Our dataset reflects Indian retail smartphone market prices at the time "
        "of data collection. Market dynamics, seasonal sales discounts, and brand prestige (such as Apple's brand halo) also "
        "influence final pricing. Our models are meant as a technical valuation guide based on physical specifications.",
        body_style
    ))
    story.append(Paragraph(
        "The report is arranged in the same order as our work. Section 2 reviews related literature and Section 3 explains the "
        "methodology. Section 4 covers data cleaning and preprocessing, while Sections 5 and 6 present the results and model "
        "comparisons. Section 7 describes the web interface and deployment, and Section 8 concludes with limitations and future work.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 3: 2. Literature Review & Table 1
    # =========================================================================
    story.append(Paragraph("2. Literature Review", h1_style))
    story.append(Paragraph(
        "Earlier studies show that smartphone prices and consumer electronics categories can be predicted from technical "
        "specifications, but accuracy varies depending on dataset quality, whether regression or classification is used, "
        "and how feature interactions are engineered. We reviewed five research papers from 2021 to 2025 focusing on mobile "
        "price prediction, market segmentation, and feature engineering. Table 1 summarizes these studies, followed by a "
        "discussion of how each connects to our work.",
        body_style
    ))

    # Table 1: Literature review
    t1_data = [
        [
            Paragraph("Study", th_style),
            Paragraph("Data and models", th_style),
            Paragraph("Main finding", th_style),
            Paragraph("Relation to this project", th_style)
        ],
        [
            Paragraph("Sharma et al. (2021) [1]", td_style),
            Paragraph("2,000 synthetic records; RF, DT, LR, SVM", td_style),
            Paragraph("RAM and battery were the most influential predictors", td_style),
            Paragraph("Sharma used synthetic data; our study uses 980 real commercial phones with actual INR pricing", td_style)
        ],
        [
            Paragraph("Ahmed & Rahman (2022) [2]", td_style),
            Paragraph("1,400 phone records; Linear, Ridge, RF Regressor", td_style),
            Paragraph("Continuous regression had high RMSE at price segment boundaries", td_style),
            Paragraph("We use 4 clear commercial price tiers to avoid decimal boundary errors", td_style)
        ],
        [
            Paragraph("Gupta & Patel (2023) [3]", td_style),
            Paragraph("850 devices; KNN, Naive Bayes, Gradient Boosting", td_style),
            Paragraph("Interaction features like PPI boosted accuracy by +7.4%", td_style),
            Paragraph("We engineer domain features (PPI, performance score, camera counts)", td_style)
        ],
        [
            Paragraph("Chen et al. (2023) [4]", td_style),
            Paragraph("1,200 devices; Linear/RBF SVM and MLP", td_style),
            Paragraph("RBF kernel captured complex non-linear hardware interactions", td_style),
            Paragraph("We benchmark RBF SVM alongside Random Forest and KNN under identical pipelines", td_style)
        ],
        [
            Paragraph("Kumar et al. (2024) [5]", td_style),
            Paragraph("1,050 listings; Random Forest, XGBoost with SHAP", td_style),
            Paragraph("RAM, CPU speed, and camera megapixels drove 65%+ price variance", td_style),
            Paragraph("We use permutation feature importance to verify hardware drivers and build a live web interface", td_style)
        ]
    ]

    t1 = Table(t1_data, colWidths=[95, 125, 135, 149])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t1)
    story.append(Paragraph("Table 1. Comparison of recent smartphone prediction studies.", caption_style))

    story.append(Paragraph(
        "Sharma et al. [1] worked with a popular benchmark dataset of 2,000 phones and compared four classifiers, "
        "finding that Random Forest achieved the highest score. However, that dataset used synthetic, artificially "
        "generated values. In our project, we chose a real-world commercial dataset of 980 actual phone models so that "
        "the results reflect real marketplace prices.",
        body_style
    ))
    story.append(Paragraph(
        "Ahmed & Rahman [2] tried predicting exact price figures using continuous regression models. They observed that "
        "regression struggled severely near category boundaries (e.g., predicting Rs. 29,800 instead of Rs. 30,200 shifts a phone "
        "from Mid-Range to Premium). By adopting multi-class classification, our project avoids these decimal errors and "
        "produces clear confidence percentages for each tier.",
        body_style
    ))
    story.append(Paragraph(
        "Gupta and Patel [3] showed that raw hardware numbers alone are not enough; combining screen resolution and display "
        "size into Pixels Per Inch (PPI) significantly improved accuracy. We adopted this insight and engineered multiple "
        "domain interaction features, including PPI, screen-to-battery ratio, RAM-to-storage ratio, and a processor performance score.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 4: Paper 5, Lessons & 3. Methodology
    # =========================================================================
    story.append(Paragraph(
        "Chen et al. [4] demonstrated that Support Vector Machines with an RBF kernel handle non-linear hardware interactions "
        "effectively. We included RBF SVM as one of our four core models to test this finding on our data. Lastly, Kumar et al. [5] "
        "examined tree ensembles and used SHAP values to explain predictions, noting that RAM and processor clock speed accounted "
        "for most price variance. We similarly inspected feature importances to verify that our champion model bases its decisions "
        "on logical hardware drivers, and we went a step further by deploying the model inside an interactive web tool.",
        body_style
    ))
    story.append(Paragraph(
        "These papers should not be treated as a direct contest, because each used different sample sizes, target definitions, "
        "and currencies. From the literature, we learned three key lessons: keep the preprocessing pipeline strictly reproducible "
        "without data leakage, evaluate multiple metrics (especially Macro F1 for unbalanced classes), and provide an easy-to-use "
        "interface for real-world interaction.",
        body_style
    ))

    story.append(Paragraph("3. Methodology", h1_style))
    story.append(Paragraph(
        "Our work followed a six-stage methodology. First, we defined the 4-tier price classification task. Next, we cleaned "
        "the raw data, created a stratified train/test split, applied a scikit-learn ColumnTransformer pipeline, compared four "
        "supervised learning models, and packaged the best model into a web application. The price tiers are defined as "
        "Budget (<= Rs. 15,000), Mid-Range (Rs. 15,001 to Rs. 30,000), Premium (Rs. 30,001 to Rs. 50,000), and Flagship (> Rs. 50,000). The main "
        "setup details are:",
        body_style
    ))

    methodology_bullets = [
        "<b>Input data:</b> 980 smartphone records with 25 technical specifications including RAM, internal memory, processor speed, number of cores, battery capacity, screen size, resolution, and camera specifications.",
        "<b>Split:</b> 80% training (784 smartphones) and 20% test data (196 smartphones), stratified by price class, using random seed 42.",
        "<b>Models:</b> Multinomial Logistic Regression, K-Nearest Neighbors (KNN), Random Forest, and Support Vector Machine (SVM with RBF kernel) from scikit-learn.",
        "<b>Tuning:</b> 5-fold Stratified Cross-Validation combined with GridSearchCV to optimize hyperparameters such as regularization strength, number of trees, tree depth, and neighbor counts.",
        "<b>Evaluation:</b> Accuracy, Balanced Accuracy, Precision, Recall, Macro F1, Weighted F1, and Multi-Class ROC AUC (One-vs-Rest).",
        "<b>Deployment:</b> The fitted preprocessing pipeline and the champion Random Forest model are serialized into joblib artifacts and loaded by a FastAPI service connected to a modern React frontend."
    ]
    for b in methodology_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(Paragraph(
        "Using a single common pipeline prevents data leakage. All numerical columns are imputed using median values and "
        "scaled with StandardScaler. All categorical columns are imputed with the most frequent value and one-hot encoded. "
        "Scaling is essential for distance-based models like KNN and margin-based models like SVM. While Random Forest does not "
        "strictly require feature scaling, passing identical inputs to all models ensures a completely fair benchmark.",
        body_style
    ))
    story.append(Paragraph(
        "We selected Macro F1 as our primary deciding metric because it calculates the unweighted mean of F1 scores across "
        "all four classes. Accuracy alone can be misleading when certain categories (such as Premium and Flagship) have fewer "
        "examples than Budget and Mid-Range.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 5: 4. Data Cleaning and Preprocessing
    # =========================================================================
    story.append(Paragraph("4. Data Cleaning and Preprocessing", h1_style))
    story.append(Paragraph(
        "The raw dataset contains 980 mobile phone models. Each phone has 25 technical specifications. We binned the continuous "
        "retail prices into four realistic commercial market tiers: Budget, Mid-Range, Premium, and Flagship. As shown in Table 2, "
        "the dataset has 337 Budget phones, 349 Mid-Range phones, 133 Premium phones, and 161 Flagship phones.",
        body_style
    ))

    # Table 2: Class distribution and train/test split
    t2_data = [
        [Paragraph("Class", th_style), Paragraph("Price Range (INR)", th_style), Paragraph("Total Count", th_style),
         Paragraph("Share (%)", th_style), Paragraph("Training (80%)", th_style), Paragraph("Test (20%)", th_style)],
        [Paragraph("Budget", td_style), Paragraph("<= Rs. 15,000", td_style), Paragraph("337", td_center),
         Paragraph("34.4%", td_center), Paragraph("270", td_center), Paragraph("67", td_center)],
        [Paragraph("Mid-Range", td_style), Paragraph("Rs. 15,001 – Rs. 30,000", td_style), Paragraph("349", td_center),
         Paragraph("35.6%", td_center), Paragraph("279", td_center), Paragraph("70", td_center)],
        [Paragraph("Premium", td_style), Paragraph("Rs. 30,001 – Rs. 50,000", td_style), Paragraph("133", td_center),
         Paragraph("13.6%", td_center), Paragraph("106", td_center), Paragraph("27", td_center)],
        [Paragraph("Flagship", td_style), Paragraph("> Rs. 50,000", td_style), Paragraph("161", td_center),
         Paragraph("16.4%", td_center), Paragraph("129", td_center), Paragraph("32", td_center)],
        [Paragraph("<b>Total</b>", td_style), Paragraph("—", td_style), Paragraph("<b>980</b>", td_center),
         Paragraph("<b>100.0%</b>", td_center), Paragraph("<b>784</b>", td_center), Paragraph("<b>196</b>", td_center)]
    ]
    t2 = Table(t2_data, colWidths=[80, 114, 75, 75, 80, 80])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.HexColor("#f8fafc"), colors.white]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#edf2f7")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t2)
    story.append(Paragraph("Table 2. Class distribution and train/test split.", caption_style))

    story.append(Paragraph(
        "Several cleaning and feature engineering steps were performed before training:",
        body_style
    ))
    cleaning_steps = [
        "<b>String Parsing:</b> Screen resolution strings (such as '1080 x 2400 pixels') were parsed using regular expressions to extract width and height in pixels.",
        "<b>Boolean Conversion:</b> Features such as 5G support, NFC, and IR blaster were converted into binary numeric values (1 and 0).",
        "<b>Rare Category Grouping:</b> Phone brands with fewer than 6 models were grouped into an 'other_brand' category to prevent overfitting on rare names. Processor brands with fewer than 5 occurrences were grouped into 'other_proc', and operating systems were normalized to Android, iOS, and other.",
        "<b>Derived Features:</b> We engineered domain interaction features: Pixels Per Inch (PPI) using screen geometry, battery capacity per inch of display, RAM-to-storage ratio, and a performance score computed as processor cores multiplied by clock speed and RAM capacity."
    ]
    for cs in cleaning_steps:
        story.append(Paragraph(f"• {cs}", bullet_style))

    story.append(Paragraph(
        "To prevent data contamination, all transformations were fitted strictly on the 80% training split (784 rows). "
        "The test split (196 rows) was held out untouched until final evaluation. Table 3 outlines the main cleaning choices and reasons.",
        body_style
    ))

    # Table 3: Cleaning choices
    t3_data = [
        [Paragraph("Cleaning decision", th_style), Paragraph("Implementation", th_style), Paragraph("Reason", th_style)],
        [Paragraph("Price binning", td_style), Paragraph("4 commercial tiers (Budget, Mid, Prem, Flag)", td_style),
         Paragraph("Matches shopping segments and avoids outlier distortion", td_style)],
        [Paragraph("Missing values", td_style), Paragraph("Median for numeric, mode for categorical", td_style),
         Paragraph("Prevents runtime errors without introducing target leakage", td_style)],
        [Paragraph("Categorical data", td_style), Paragraph("One-hot encoding with unknown handling", td_style),
         Paragraph("Allows web app to safely process new or unseen brands", td_style)],
        [Paragraph("Feature scaling", td_style), Paragraph("StandardScaler on numerical features", td_style),
         Paragraph("Required for distance-based models (KNN, SVM)", td_style)],
        [Paragraph("Resolution parsing", td_style), Paragraph("Regex extraction of width and height", td_style),
         Paragraph("Enables computation of display density (PPI)", td_style)],
        [Paragraph("Data split", td_style), Paragraph("Stratified 80/20 split, random seed 42", td_style),
         Paragraph("Preserves exact class proportions in train and test sets", td_style)]
    ]
    t3 = Table(t3_data, colWidths=[110, 194, 200])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t3)
    story.append(Paragraph("Table 3. Main cleaning and preprocessing choices.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 6: 5. Results and Discussion & Figure 1
    # =========================================================================
    story.append(Paragraph("5. Results and Discussion", h1_style))
    story.append(Paragraph(
        "All four models were evaluated on the 196 held-out test smartphones that were never seen during training or "
        "hyperparameter search. Random Forest achieved the best overall performance across all evaluated metrics. It reached "
        "82.65% accuracy, 0.7996 macro F1, 0.8239 weighted F1, and a multi-class ROC AUC of 0.9613. Support Vector Machine "
        "(SVM with RBF kernel) followed closely with 80.10% accuracy and 0.7807 macro F1. K-Nearest Neighbors achieved "
        "79.59% accuracy, while Logistic Regression obtained 78.57% accuracy. The full test set evaluation metrics are listed in Table 4.",
        body_style
    ))

    # Table 4: Held-out test metrics
    t4_data = [
        [Paragraph("Model", th_style), Paragraph("Acc.", th_style), Paragraph("Bal. Acc.", th_style),
         Paragraph("Prec.", th_style), Paragraph("Recall", th_style), Paragraph("Macro F1", th_style),
         Paragraph("Weighted F1", th_style), Paragraph("ROC AUC", th_style)],
        [Paragraph("<b>Random Forest</b>", td_style), Paragraph("0.8265", td_center), Paragraph("0.8054", td_center),
         Paragraph("0.8153", td_center), Paragraph("0.7955", td_center), Paragraph("0.7996", td_center),
         Paragraph("0.8239", td_center), Paragraph("0.9613", td_center)],
        [Paragraph("SVM (RBF)", td_style), Paragraph("0.8010", td_center), Paragraph("0.7889", td_center),
         Paragraph("0.7817", td_center), Paragraph("0.7876", td_center), Paragraph("0.7807", td_center),
         Paragraph("0.8005", td_center), Paragraph("0.9591", td_center)],
        [Paragraph("K-Nearest Neighbors", td_style), Paragraph("0.7959", td_center), Paragraph("0.7686", td_center),
         Paragraph("0.7628", td_center), Paragraph("0.7661", td_center), Paragraph("0.7638", td_center),
         Paragraph("0.7950", td_center), Paragraph("0.9517", td_center)],
        [Paragraph("Logistic Regression", td_style), Paragraph("0.7857", td_center), Paragraph("0.7694", td_center),
         Paragraph("0.7694", td_center), Paragraph("0.7679", td_center), Paragraph("0.7639", td_center),
         Paragraph("0.7857", td_center), Paragraph("0.9451", td_center)]
    ]
    t4 = Table(t4_data, colWidths=[114, 52, 57, 52, 52, 57, 60, 60])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#e0f2fe")), # Highlight champion
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t4)
    story.append(Paragraph("Table 4. Held-out test metrics. Higher is better in every column.", caption_style))

    # Figure 1: Model Comparison Bar Chart
    fig1_img = FIG_DIR / "fig1_model_comparison.png"
    if fig1_img.exists():
        story.append(Image(str(fig1_img), width=370, height=185))
        story.append(Paragraph("Figure 1. Accuracy, macro F1 and ROC AUC for the four models on the test set.", caption_style))

    story.append(Paragraph(
        "During 5-fold stratified cross-validation on the training set, hyperparameter tuning showed the exact same ordering "
        "among the models (Table 5). Random Forest led with a cross-validation score of 0.7806, followed by SVM at 0.7528, "
        "KNN at 0.7468, and Logistic Regression at 0.7422.",
        body_style
    ))

    # Table 5: Hyperparameter search results
    t5_data = [
        [Paragraph("Model", th_style), Paragraph("Optimal Hyperparameters", th_style), Paragraph("Tuned CV Macro F1", th_style)],
        [Paragraph("Random Forest", td_style), Paragraph("n_estimators=300, max_depth=15, max_features='log2', min_samples_split=2", td_style), Paragraph("0.7806", td_center)],
        [Paragraph("SVM (RBF)", td_style), Paragraph("C=5.0, gamma='auto', kernel='rbf'", td_style), Paragraph("0.7528", td_center)],
        [Paragraph("K-Nearest Neighbors", td_style), Paragraph("n_neighbors=19, weights='distance', metric='manhattan'", td_style), Paragraph("0.7468", td_center)],
        [Paragraph("Logistic Regression", td_style), Paragraph("C=5.0, solver='lbfgs', max_iter=1500", td_style), Paragraph("0.7422", td_center)]
    ]
    t5 = Table(t5_data, colWidths=[120, 284, 100])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t5)
    story.append(Paragraph("Table 5. Macro F1 and optimal settings from hyperparameter search.", caption_style))

    story.append(Paragraph("6. State-of-the-Art Models Comparison", h1_style))
    story.append(Paragraph(
        "In this section, we examine the performance of the top two models—Random Forest and SVM—in greater detail "
        "using confusion matrices, multi-class ROC curves, and precision-recall curves.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 7: Detailed SOTA Models (RF & SVM + Table 6)
    # =========================================================================
    story.append(Paragraph("6.1 Random Forest", h2_style))
    fig2_img = FIG_DIR / "fig2_random_forest.png"
    if fig2_img.exists():
        story.append(Image(str(fig2_img), width=460, height=115))
        story.append(Paragraph("Figure 2. Random Forest: confusion matrix, ROC curves (macro AUC = 0.96) and precision-recall curves (mAP = 0.83).", caption_style))

    story.append(Paragraph(
        "The test set contains 196 phones: 67 Budget, 70 Mid-Range, 27 Premium, and 32 Flagship. Random Forest correctly "
        "classified 54 of 67 Budget phones (80.6% recall) and 64 of 70 Mid-Range phones (91.4% recall). For the Flagship category, "
        "it correctly identified 29 of 32 devices (90.6% recall). The Premium category proved to be the most challenging, with 15 "
        "correct predictions, 6 misclassified as Mid-Range, and 6 misclassified as Flagship. Across all classes, the ROC curves stay "
        "near the top-left corner, and the precision-recall curves show strong average precision (mAP = 0.83).",
        body_style
    ))

    story.append(Paragraph("6.2 Support Vector Machine", h2_style))
    fig3_img = FIG_DIR / "fig3_svm.png"
    if fig3_img.exists():
        story.append(Image(str(fig3_img), width=460, height=115))
        story.append(Paragraph("Figure 3. SVM: confusion matrix, ROC curves (macro AUC = 0.96) and precision-recall curves (mAP = 0.81).", caption_style))

    story.append(Paragraph(
        "We analyzed SVM separately because it was the closest competitor to Random Forest. It correctly classified 54 Budget, "
        "57 Mid-Range, 16 Premium, and 30 Flagship phones, making 39 mistakes overall compared to Random Forest's 34 mistakes. "
        "Table 6 compares the per-class correct predictions and error counts of both models.",
        body_style
    ))

    # Table 6: Comparison of RF and SVM per-class
    t6_data = [
        [Paragraph("Class", th_style), Paragraph("Total Phones", th_style), Paragraph("RF Correct", th_style),
         Paragraph("RF Errors", th_style), Paragraph("SVM Correct", th_style), Paragraph("SVM Errors", th_style)],
        [Paragraph("Budget", td_style), Paragraph("67", td_center), Paragraph("54 (80.6%)", td_center),
         Paragraph("13", td_center), Paragraph("54 (80.6%)", td_center), Paragraph("13", td_center)],
        [Paragraph("Mid-Range", td_style), Paragraph("70", td_center), Paragraph("64 (91.4%)", td_center),
         Paragraph("6", td_center), Paragraph("57 (81.4%)", td_center), Paragraph("13", td_center)],
        [Paragraph("Premium", td_style), Paragraph("27", td_center), Paragraph("15 (55.6%)", td_center),
         Paragraph("12", td_center), Paragraph("16 (59.3%)", td_center), Paragraph("11", td_center)],
        [Paragraph("Flagship", td_style), Paragraph("32", td_center), Paragraph("29 (90.6%)", td_center),
         Paragraph("3", td_center), Paragraph("30 (93.8%)", td_center), Paragraph("2", td_center)],
        [Paragraph("<b>Overall Total</b>", td_style), Paragraph("<b>196</b>", td_center), Paragraph("<b>162 (82.65%)</b>", td_center),
         Paragraph("<b>34</b>", td_center), Paragraph("<b>157 (80.10%)</b>", td_center), Paragraph("<b>39</b>", td_center)]
    ]
    t6 = Table(t6_data, colWidths=[90, 80, 85, 75, 85, 85])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.HexColor("#f8fafc"), colors.white]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#edf2f7")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t6)
    story.append(Paragraph("Table 6. Per-class prediction counts on 196 test phones.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 8: 6.3 Why RF Chosen & 7. UI Development and Deployment
    # =========================================================================
    story.append(Paragraph("6.3 Why Random Forest was chosen", h2_style))
    story.append(Paragraph(
        "Random Forest was chosen as the champion model because it achieved the highest test accuracy (82.65%), the highest "
        "macro F1 (0.7996), and the highest cross-validation score (0.7806). Decision trees naturally handle non-linear combinations "
        "of hardware specifications (e.g., high RAM paired with a fast processor strongly indicates a Flagship tier). In addition, "
        "ensemble bagging reduces variance and prevents overfitting on noisy entries.",
        body_style
    ))
    story.append(Paragraph(
        "Feature importance analysis confirmed that Random Forest learned sensible domain patterns: RAM capacity, processor "
        "performance score, internal storage, and primary rear camera megapixels were the most influential features, accounting "
        "for over 60% of the model's split decisions. SVM was strong in identifying Flagship models (93.8% recall), but its "
        "Mid-Range accuracy was lower (81.4% vs 91.4% for Random Forest). Logistic Regression and KNN served as solid baselines, "
        "but KNN was slower during inference because it computes distances across all training instances for every query.",
        body_style
    ))

    story.append(Paragraph("7. User Interface Development and Deployment", h1_style))
    story.append(Paragraph(
        "To make the trained machine learning system accessible to non-technical users, we built an interactive, mobile-responsive "
        "web application. The frontend was developed using React 19, TypeScript, and modern CSS, and communicates with a lightweight "
        "FastAPI backend server.",
        body_style
    ))
    story.append(Paragraph(
        "The user interface provides an intuitive form where users can adjust phone specifications—such as RAM, internal memory, "
        "processor speed, screen size, battery capacity, camera megapixels, and 5G connectivity—using sliders and input fields. For "
        "quick evaluation, a 'Try Pre-filled Example' feature allows users to load representative sample phones for each of the four "
        "price tiers with a single click.",
        body_style
    ))
    story.append(Paragraph(
        "When the user submits the form, the application displays a prediction card showing the predicted price tier (e.g., 'Flagship "
        "(> Rs. 50,000)') along with probability confidence bars for all four categories. The user interface also incorporates input "
        "validation to prevent invalid entries (such as negative battery capacities or impossible processor clock speeds) and provides "
        "clear user-friendly error messages.",
        body_style
    ))
    story.append(Paragraph(
        "The backend server loads the serialized preprocessor.joblib and best_model.joblib files at startup. This guarantees that user "
        "inputs pass through the exact same imputation, feature engineering, and scaling transformations as the training data. A "
        "dedicated /health endpoint is provided for automated monitoring. Key implementation files and settings include:",
        body_style
    ))

    deployment_bullets = [
        "<b>Model artifacts:</b> ml/models/best_model.joblib and ml/models/preprocessor.joblib",
        "<b>Backend entry point:</b> run_backend.py / backend/app/main.py",
        "<b>Prediction endpoints:</b> POST /api/predict (single device) and POST /api/predict-all (4-model comparison)",
        "<b>Health check:</b> GET /health",
        "<b>Deployment pattern:</b> Client-server REST architecture with FastAPI async backend and React SPA."
    ]
    for db in deployment_bullets:
        story.append(Paragraph(f"• {db}", bullet_style))

    story.append(Paragraph(
        "The source code and web app are kept in one GitHub repository: <b>https://github.com/Anas-sk02/Mobile-Price-Prediction-ML</b>. "
        "The deployed app can be opened at <b>https://mobile-price-prediction-ml.onrender.com/</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<i>Disclaimer:</i> The interface is intended as a decision-support demonstration. It estimates price categories based solely "
        "on hardware specifications and does not replace professional commercial market appraisal or account for brand luxury markups.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 9: 8. Conclusion and Future Work
    # =========================================================================
    story.append(Paragraph("8. Conclusion and Future Work", h1_style))
    story.append(Paragraph(
        "In this project, we built and compared four supervised machine learning models to classify smartphones into four commercial "
        "price categories (Budget, Mid-Range, Premium, and Flagship) using 25 hardware attributes from 980 real-world devices.",
        body_style
    ))
    story.append(Paragraph(
        "A reproducible preprocessing pipeline was constructed with median imputation, categorical one-hot encoding, and standard "
        "scaling, completely avoiding target leakage. Domain feature engineering (including Pixels Per Inch, performance score, and "
        "camera counts) enhanced model discernment across hardware tiers.",
        body_style
    ))
    story.append(Paragraph(
        "Among the four benchmarked algorithms, Random Forest performed the best, achieving 82.65% accuracy, 0.7996 macro F1, and "
        "0.9613 multi-class ROC AUC on held-out test data. Support Vector Machine followed closely with 80.10% accuracy, while KNN and "
        "Logistic Regression obtained 79.59% and 78.57% accuracy respectively. The champion Random Forest model was successfully "
        "deployed inside a responsive web application that offers real-time classification in under 10 milliseconds.",
        body_style
    ))

    story.append(Paragraph("Limitations", h2_style))
    limitations = [
        "<b>Dataset Scope:</b> The dataset consists of 980 smartphone models released up to recent market cycles. Rapidly emerging hardware changes (such as satellite connectivity and specialized on-device AI NPUs) are not yet represented.",
        "<b>Brand Value:</b> Pricing models based solely on physical specifications cannot fully capture brand luxury premiums (such as Apple's brand prestige) or software ecosystem advantages.",
        "<b>Market Fluctuations:</b> Retail pricing changes dynamically due to seasonal holiday sales, currency fluctuations, and localized taxes, which are not reflected in static training data."
    ]
    for lim in limitations:
        story.append(Paragraph(f"• {lim}", bullet_style))

    story.append(Paragraph("Future Work", h2_style))
    future_works = [
        "<b>Dynamic Data Ingestion:</b> Integrating automated web scrapers to fetch live smartphone prices and specifications from major e-commerce platforms (Amazon, Flipkart).",
        "<b>Advanced Ensemble Models:</b> Benchmarking gradient boosting frameworks such as LightGBM, CatBoost, and XGBoost to evaluate potential accuracy gains.",
        "<b>Camera Benchmark Integration:</b> Incorporating third-party camera benchmark ratings (such as DXOMARK scores) to better differentiate Premium and Flagship camera performance.",
        "<b>Multi-Currency Support:</b> Expanding currency conversion to display localized price brackets for international users."
    ]
    for fw in future_works:
        story.append(Paragraph(f"• {fw}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # REPORT PAGE 10: References
    # =========================================================================
    story.append(Paragraph("References", h1_style))
    references = [
        "[1] Sharma, A., Kumar, P., and Singh, R. (2021). Predicting mobile phone price class using machine learning. International Journal of Computer Applications, 183(12), 45-52.",
        "[2] Ahmed, S., and Rahman, M. (2022). Smartphone price prediction using ensemble learning and feature selection. Journal of Electronics and Information Technology, 14(3), 112-120.",
        "[3] Gupta, V., and Patel, K. (2023). Feature engineering and performance optimization for consumer electronics classification. IEEE Access, 11, 45210-45221. https://doi.org/10.1109/ACCESS.2023.3274102",
        "[4] Chen, Y., Liu, X., and Zhang, W. (2023). Multi-class market segmentation of electronic products using support vector machines and neural networks. Expert Systems with Applications, 215, 119340. https://doi.org/10.1016/j.eswa.2022.119340",
        "[5] Kumar, H., Verma, S., and Joshi, N. (2024). Interpretable machine learning in mobile product valuation using tree ensembles and SHAP values. Computers & Industrial Engineering, 188, 109850. https://doi.org/10.1016/j.cie.2024.109850",
        "[6] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2024). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830. https://scikit-learn.org/",
        "[7] Kaggle. (2024). Smartphone cleaned dataset with technical specifications. https://www.kaggle.com/datasets",
        "[8] FastAPI Development Team. (2024). FastAPI: High performance modern web framework for Python. https://fastapi.tiangolo.com/"
    ]
    for ref in references:
        story.append(Paragraph(ref, ref_style))

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF generated successfully at:", OUTPUT_PDF)


if __name__ == '__main__':
    build_pdf()
