"""
SmartPrice: Smartphone Price Category Prediction & ML Model Benchmarking System
================================================================================
Academic Viva Voce & Technical Defense Preparation Guide: 50 Questions & Answers
Generates a publication-grade PDF document containing complete, in-depth questions
and answers directly aligned with the SmartPrice repository codebase.
"""

import sys
import os
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Reconfigure stdout for UTF-8 in Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PDF = PROJECT_ROOT / "SmartPrice_50_ML_Viva_Questions_and_Answers.pdf"

# Register TrueType Arial fonts if available on Windows for native unicode rendering (₹, μ, σ, etc.)
FONT_FAMILY = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"
FONT_BOLD_ITALIC = "Helvetica-BoldOblique"

arial_path = Path("C:/Windows/Fonts/arial.ttf")
arialbd_path = Path("C:/Windows/Fonts/arialbd.ttf")
ariali_path = Path("C:/Windows/Fonts/ariali.ttf")
arialbi_path = Path("C:/Windows/Fonts/arialbi.ttf")

if arial_path.exists() and arialbd_path.exists():
    try:
        pdfmetrics.registerFont(TTFont("Arial", str(arial_path)))
        pdfmetrics.registerFont(TTFont("Arial-Bold", str(arialbd_path)))
        if ariali_path.exists():
            pdfmetrics.registerFont(TTFont("Arial-Italic", str(ariali_path)))
        if arialbi_path.exists():
            pdfmetrics.registerFont(TTFont("Arial-BoldItalic", str(arialbi_path)))
        FONT_FAMILY = "Arial"
        FONT_BOLD = "Arial-Bold"
        FONT_ITALIC = "Arial-Italic" if ariali_path.exists() else "Arial"
        FONT_BOLD_ITALIC = "Arial-BoldItalic" if arialbi_path.exists() else "Arial-Bold"
    except Exception as e:
        print(f"Font registration notice: {e}, falling back to standard Helvetica")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to compute total page count and render running headers and footers."""
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        
        # Running Header (pages 2 onwards)
        if self._pageNumber > 1:
            self.setFont(FONT_BOLD, 7.5)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(40, 754, "SMARTPRICE: SMARTPHONE PRICE PREDICTION & MODEL BENCHMARKING SYSTEM")
            self.setFont(FONT_FAMILY, 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(letter[0] - 40, 754, "50 Machine Learning Viva Voce & Technical Defense Q&As")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(40, 748, letter[0] - 40, 748)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(40, 36, letter[0] - 40, 36)

        self.setFont(FONT_FAMILY, 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 24, "Course: Machine Learning Laboratory Project | Tech: Python, Scikit-Learn, FastAPI, React 19")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 24, page_str)
        self.restoreState()


def create_viva_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=44,
        bottomMargin=44
    )

    # Custom typography
    title_style = ParagraphStyle(
        'DocTitle',
        fontName=FONT_BOLD,
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName=FONT_BOLD,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        fontName=FONT_FAMILY,
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        fontName=FONT_BOLD,
        fontSize=10.5,
        leading=14,
        textColor=colors.white
    )

    q_title_style = ParagraphStyle(
        'QTitle',
        fontName=FONT_BOLD,
        fontSize=9.2,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    ans_bullet_style = ParagraphStyle(
        'AnsBullet',
        fontName=FONT_FAMILY,
        fontSize=8.4,
        leading=11.8,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName=FONT_BOLD,
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName=FONT_FAMILY,
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#1E293B"),
        alignment=1
    )

    table_cell_left = ParagraphStyle(
        'TableCellLeft',
        fontName=FONT_BOLD,
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # Title & Metadata Header Box
    story.append(Paragraph("SmartPrice — Machine Learning Viva Voce & Technical Defense Guide", title_style))
    story.append(Paragraph("50 In-Depth Technical & Conceptual Viva Questions with Repository-Verified Answers", subtitle_style))
    
    meta_text = (
        "<b>Project Domain:</b> Supervised Machine Learning / Multi-Class Smartphone Price Category Classification<br/>"
        "<b>Dataset Profile:</b> 980 Real-World Smartphone Models, 28 Numerical + 3 Categorical Features (62 Transformed Dimensions)<br/>"
        "<b>Models Benchmarked:</b> Random Forest (Champion: <b>82.65% Test Acc, 0.9613 ROC-AUC</b>), SVM (80.10%), KNN (79.59%), Logistic Regression (78.57%)<br/>"
        "<b>Full-Stack Tech:</b> Scikit-Learn 1.4+, Python 3.11, FastAPI REST API, Pydantic v2, React 19, TypeScript, Tailwind CSS, Vercel/Render"
    )
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 8))

    # Benchmark Summary Table
    bench_data = [
        [
            Paragraph("Model Architecture", table_header_style),
            Paragraph("Model Family", table_header_style),
            Paragraph("5-Fold CV Acc", table_header_style),
            Paragraph("Test Accuracy", table_header_style),
            Paragraph("Macro F1", table_header_style),
            Paragraph("Weighted F1", table_header_style),
            Paragraph("ROC-AUC (OvR)", table_header_style),
            Paragraph("Status", table_header_style)
        ],
        [
            Paragraph("Random Forest", table_cell_left),
            Paragraph("Ensemble Trees", table_cell_style),
            Paragraph("78.06%", table_cell_style),
            Paragraph("<b>82.65%</b>", table_cell_style),
            Paragraph("0.7996", table_cell_style),
            Paragraph("0.8239", table_cell_style),
            Paragraph("<b>0.9613</b>", table_cell_style),
            Paragraph("<b>Champion</b>", table_cell_style)
        ],
        [
            Paragraph("Support Vector Machine", table_cell_left),
            Paragraph("Kernel RBF", table_cell_style),
            Paragraph("75.28%", table_cell_style),
            Paragraph("80.10%", table_cell_style),
            Paragraph("0.7807", table_cell_style),
            Paragraph("0.8005", table_cell_style),
            Paragraph("0.9591", table_cell_style),
            Paragraph("Baseline", table_cell_style)
        ],
        [
            Paragraph("K-Nearest Neighbors", table_cell_left),
            Paragraph("Instance-Based", table_cell_style),
            Paragraph("74.68%", table_cell_style),
            Paragraph("79.59%", table_cell_style),
            Paragraph("0.7638", table_cell_style),
            Paragraph("0.7950", table_cell_style),
            Paragraph("0.9517", table_cell_style),
            Paragraph("Baseline", table_cell_style)
        ],
        [
            Paragraph("Multinomial Logistic Reg.", table_cell_left),
            Paragraph("Linear Model", table_cell_style),
            Paragraph("74.22%", table_cell_style),
            Paragraph("78.57%", table_cell_style),
            Paragraph("0.7639", table_cell_style),
            Paragraph("0.7857", table_cell_style),
            Paragraph("0.9451", table_cell_style),
            Paragraph("Baseline", table_cell_style)
        ]
    ]

    bench_table = Table(bench_data, colWidths=[112, 70, 56, 56, 48, 52, 68, 50])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 10))

    # Helper function to create section header banner
    def create_section_banner(title: str):
        banner_data = [[Paragraph(title, section_header_style)]]
        banner_table = Table(banner_data, colWidths=[532])
        banner_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1E3A8A")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return banner_table

    # Helper function to add question and answer
    def add_qa(q_num: int, question: str, bullet_points: list[str]):
        elements = []
        q_heading = f"Q{q_num}: {question}"
        elements.append(Paragraph(q_heading, q_title_style))
        for bp in bullet_points:
            elements.append(Paragraph(f"• {bp}", ans_bullet_style))
        elements.append(Spacer(1, 4))
        return elements

    # =========================================================================
    # PART 1: PROBLEM FORMULATION, DATASET & DOMAIN CONTEXT (Q1 - Q7)
    # =========================================================================
    story.append(create_section_banner("PART 1: PROBLEM FORMULATION, DATASET & DOMAIN CONTEXT (Q1 – Q7)"))
    story.append(Spacer(1, 4))

    # Q1
    story.extend(add_qa(1, "What is the core problem statement of this project, and why formulate it as classification instead of regression?", [
        "<b>Core Problem Statement:</b> To accurately predict the commercial price tier of any smartphone based strictly on its physical, architectural, and hardware specifications (RAM, processor clock speed, camera megapixels, display refresh rate, battery capacity, 5G/NFC, etc.).",
        "<b>Why Not Continuous Regression:</b> Real-world retail smartphone pricing is heavily distorted by ultra-premium niche devices (e.g., luxury foldables priced at ₹1,50,000+) which introduce massive right-skew and non-linear outliers into regression models. A regression model predicting ₹34,219.45 conveys false mathematical precision and produces large root-mean-square errors on tier boundaries.",
        "<b>Why 4-Class Classification:</b> Consumer electronics marketing and purchasing decisions naturally operate in discrete commercial economic brackets (Budget, Mid-Range, Premium, Flagship). Multi-class classification yields well-calibrated class probability distributions (e.g., 88.5% confidence of Mid-Range vs 11.5% Premium), allowing buyers, inventory managers, and OEMs to make categorical decisions."
    ]))

    # Q2
    story.extend(add_qa(2, "What is the dataset used, its source, sample size, and granularity?", [
        "<b>Dataset Profile:</b> The system utilizes <code>smartphone_cleaned_v5.csv</code> comprising exactly <b>980 unique, verified commercial smartphone records</b>.",
        "<b>Granularity:</b> Each row corresponds to a unique retail smartphone model available in the Indian and global market, containing 25 raw technical hardware specifications alongside the actual retail price (in Indian Rupees, ₹) and brand metadata.",
        "<b>Distinction from Synthetic Benchmarks:</b> Academic benchmark datasets (such as Kaggle's 2,000-row synthetic mobile dataset) use artificially synthesized integer values. SmartPrice uses actual real-world hardware specifications, retail brand names (Samsung, Apple, Xiaomi, OnePlus), and actual commercial prices."
    ]))

    # Q3
    story.extend(add_qa(3, "What are the 4 target price categories and their exact financial threshold boundaries?", [
        "<b>Tier 0 — Budget:</b> Retail price ≤ ₹15,000 (entry-level phones focused on core connectivity, high battery capacity 5000–6000mAh, 4GB/64GB, 60Hz displays).",
        "<b>Tier 1 — Mid-Range:</b> Retail price ₹15,001 to ₹30,000 (mainstream commercial sweet spot; 6–8GB RAM, 120Hz AMOLED panels, Dimensity/Snapdragon 7-series, fast charging).",
        "<b>Tier 2 — Premium:</b> Retail price ₹30,001 to ₹50,000 ('flagship killers' and sub-flagships; 8–12GB RAM, premium glass/metal builds, OIS cameras, high-wattage charging).",
        "<b>Tier 3 — Flagship:</b> Retail price > ₹50,000 (top-tier luxury devices like iPhone Pro, Samsung Galaxy Ultra; 12–16GB RAM, flagship Apple Bionic / Snapdragon 8 Gen-series, periscope zoom lenses, ceramic/titanium chassis)."
    ]))

    # Q4
    story.extend(add_qa(4, "What is the distribution of classes in your dataset? Is there class imbalance, and how is it addressed?", [
        "<b>Class Breakdown (980 Total Samples):</b> Mid-Range: 349 (35.6%), Budget: 337 (34.4%), Flagship: 161 (16.4%), Premium: 133 (13.6%).",
        "<b>Class Imbalance Reality:</b> This distribution accurately reflects real consumer electronics economics — budget and mid-range devices constitute ~70% of the market volume, while premium and flagship tiers account for ~30%.",
        "<b>Mitigation Techniques:</b> (1) <b>Stratified 80/20 Splitting:</b> Preserves the exact class proportion in both train (784 samples) and test (196 samples) splits. (2) <b>Stratified 5-Fold Cross-Validation:</b> Guarantees every validation fold contains balanced representative proportions. (3) <b>Evaluation via Macro F1-Score:</b> Unlike standard accuracy, Macro F1 gives equal weight to all four classes, penalizing models that ignore minority classes (Premium/Flagship)."
    ]))

    # Q5
    story.extend(add_qa(5, "What makes predicting smartphone price categories challenging from a Machine Learning standpoint?", [
        "<b>Non-Linear Synergies:</b> A phone's price is not a linear sum of individual components. For example, high RAM alone does not make a phone flagship; it must be coupled with an expensive SoC (e.g., Apple A17 Pro or Snapdragon 8 Gen 3), high PPI display, and advanced camera sensors.",
        "<b>Brand Premium Bias:</b> Devices with identical hardware specs can differ significantly in price based on brand equity and operating system (e.g., an Apple iPhone with 6GB RAM commands flagship pricing, whereas an Android phone with 6GB RAM falls into budget or mid-range).",
        "<b>Inverse Feature Trends:</b> Budget phones often feature larger batteries (6,000 mAh) than flagship phones (4,000–4,800 mAh), which can confuse naive linear classifiers without interaction features."
    ]))

    # Q6
    story.extend(add_qa(6, "What are the commercial and industrial use cases of the SmartPrice system?", [
        "<b>E-Commerce & Dynamic Valuation:</b> Automated price benchmarking for refurbished and second-hand smartphone marketplaces (e.g., Cashify, Amazon Renewed, eBay).",
        "<b>OEM Competitive Intelligence:</b> Smartphone manufacturers (e.g., Realme, OnePlus, Xiaomi) can input proposed Bill-of-Materials (BOM) specs into SmartPrice during R&D to test which market tier their hardware configuration will compete in.",
        "<b>Consumer 'Value-for-Money' Detection:</b> Consumers can verify if an advertised device is genuinely priced fairly relative to its hardware peers or if it carries an excessive brand markup."
    ]))

    # Q7
    story.extend(add_qa(7, "What are the input features in your dataset, and how many are there before and after preprocessing?", [
        "<b>Raw Input Specifications (31 Features total):</b> 28 numerical features (processor clock speed, cores, RAM, internal storage, battery capacity, fast charging watts, screen size, refresh rate, front/rear camera megapixels, front/rear camera counts, resolution width/height, PPI, rating, etc.) and 3 categorical features (brand name, processor brand, OS).",
        "<b>Transformed Pipeline Vector (62 Numerical Dimensions):</b> After standard scaling the 28 numerical features and one-hot encoding the categorical features (including low-frequency grouping), each smartphone is represented as a dense 62-dimensional numerical vector."
    ]))

    # =========================================================================
    # PART 2: DATA PREPROCESSING, IMPUTATION & ZERO DATA LEAKAGE (Q8 - Q15)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(create_section_banner("PART 2: PREPROCESSING, IMPUTATION & ZERO DATA LEAKAGE PROTOCOL (Q8 – Q15)"))
    story.append(Spacer(1, 4))

    # Q8
    story.extend(add_qa(8, "What is 'Data Leakage' in Machine Learning, and how did you guarantee zero leakage in SmartPrice?", [
        "<b>Definition of Data Leakage:</b> Data leakage occurs when information from outside the training dataset (such as the test set or holdout validation set) inadvertently influences the model training process, leading to falsely optimistic evaluation metrics that fail in production.",
        "<b>Strict Zero-Leakage Protocol in SmartPrice:</b>",
        "1. <b>Strict Split Prior to Preprocessing:</b> The dataset was split into 80% Train (784 samples) and 20% Test (196 samples) using <code>stratify=y</code> and <code>random_state=42</code> before computing any transformation statistics.",
        "2. <b>Fit on Train, Transform on Test:</b> The Scikit-learn <code>ColumnTransformer</code> pipeline computes imputer medians, scaler means (μ), and standard deviations (σ) <b>strictly on the 784 training rows</b> using <code>.fit_transform()</code>. The test set is transformed blindly using <code>.transform()</code>.",
        "3. <b>Target Isolation:</b> The continuous <code>price</code> column was strictly isolated and dropped from the feature matrix X immediately after computing the 4-tier target categories."
    ]))

    # Q9
    story.extend(add_qa(9, "Why must feature scaling parameters (mean and standard deviation) be computed only on training data?", [
        "<b>Theoretical Justification:</b> If you calculate the mean (μ) and standard deviation (σ) across all 980 rows, the scaling of the training samples is influenced by the values in the test set.",
        "<b>Consequence of Global Scaling:</b> In real-world production, the model receives future unseen data that it has never observed. Global scaling gives the training model implicit knowledge about the range and variance of test samples, resulting in artificially inflated test accuracy.",
        "<b>Scikit-Learn Implementation:</b> In <code>03_data_preprocessing.py</code>, we call <code>preprocessor.fit_transform(X_train)</code> and then <code>preprocessor.transform(X_test)</code>."
    ]))

    # Q10
    story.extend(add_qa(10, "What missing values existed in the raw dataset, and what imputation strategies did you apply?", [
        "<b>Missing Value Breakdown:</b> Raw retail specs had missing entries: <code>battery_capacity</code> (18 missing), <code>ram_capacity</code> (11 missing), <code>refresh_rate</code> (13 missing), <code>processor_speed</code> (14 missing), <code>primary_camera_front</code> (12 missing).",
        "<b>Numerical Strategy:</b> <code>SimpleImputer(strategy='median')</code>. Median is chosen because it is robust against extreme outliers (unlike the mean, which is pulled by skewed high-wattage charging or extreme megapixels).",
        "<b>Categorical Strategy:</b> <code>SimpleImputer(strategy='most_frequent')</code> (mode imputation) for missing processor brands and operating systems (defaulting to Android as it represents >90% of non-Apple smartphones)."
    ]))

    # Q11
    story.extend(add_qa(11, "Why is Median Imputation preferred over Mean Imputation for hardware specifications?", [
        "<b>Skewness in Hardware Specs:</b> Features such as internal memory (64GB to 1TB), fast charging wattage (10W to 240W), and camera megapixels (8MP to 200MP) exhibit heavy right-skewed distributions.",
        "<b>Mean Sensitivity:</b> A single 200MP camera or a 240W charger dramatically shifts the arithmetic mean upward, causing imputed values to be uncharacteristically high for average devices.",
        "<b>Median Robustness:</b> The median represents the 50th percentile (the central tendency), ensuring that missing values are imputed with realistic, representative commercial hardware values."
    ]))

    # Q12
    story.extend(add_qa(12, "How did you encode categorical variables, and why choose One-Hot Encoding over Label Encoding for nominal categories?", [
        "<b>Nominal vs. Ordinal:</b> Brand names (Samsung, Apple, Xiaomi) and Processor brands (Snapdragon, Dimensity, Bionic) are nominal categorical variables with no inherent mathematical hierarchy or ordering.",
        "<b>Failure of Label Encoding:</b> Assigning Apple=1, Samsung=2, Xiaomi=3 implies an artificial mathematical order (Xiaomi > Samsung > Apple) and creates false Euclidean distances in distance-based models (KNN and SVM).",
        "<b>One-Hot Encoding Implementation:</b> We applied <code>OneHotEncoder(handle_unknown='ignore', sparse_output=False)</code>. The <code>handle_unknown='ignore'</code> flag ensures that if a new unseen brand appears in production, all its one-hot columns are set to 0 without throwing a runtime crash."
    ]))

    # Q13
    story.extend(add_qa(13, "What is high cardinality in categorical variables, and how did you resolve it?", [
        "<b>Cardinality Challenge:</b> The raw dataset had dozens of boutique smartphone brands with only 1 or 2 entries each (e.g., Lyf, Vertu, Sharp, Duo). One-hot encoding every rare brand would cause extreme feature space sparsity.",
        "<b>Frequency-Based Grouping Threshold:</b>",
        "• Brands with ≥ 6 occurrences were retained as discrete categories (Apple, Samsung, Xiaomi, Vivo, Realme, Oppo, OnePlus, Poco, Motorola, iQOO, Honor, Huawei, Nokia, Google, Tecno, Infinix).",
        "• Brands with < 6 occurrences were lumped into a single robust category: <code>'other_brand'</code>.",
        "• Similarly, processor brands with < 5 occurrences were mapped to <code>'other_proc'</code>. This reduced noise and avoided overfitting on rare labels."
    ]))

    # Q14
    story.extend(add_qa(14, "Why is Standard Scaling (Z-Score Normalization) necessary, and which models depend on it?", [
        "<b>Mathematical Formula:</b> z = (x - μ) / σ where μ is the training mean and σ is the standard deviation, producing a distribution with μ=0 and σ=1.",
        "<b>Models that Require Scaling:</b>",
        "1. <b>K-Nearest Neighbors (KNN):</b> Calculates Euclidean distance d(p, q) = √(∑(p_i - q_i)²). Without scaling, battery capacity (5000 mAh) completely dwarfs processor speed (2.8 GHz), rendering processor speed effectively zero in distance calculations.",
        "2. <b>Support Vector Machines (SVM):</b> RBF kernel K(x, x') = exp(-γ ||x - x'||²) relies on squared Euclidean norm. Unscaled large-magnitude features dominate the kernel matrix.",
        "3. <b>Logistic Regression:</b> Regularization penalties (L2 penalty λ ||w||₂²) penalize all coefficients equally. If features are on different scales, coefficients cannot be penalized fairly, distorting gradient descent convergence."
    ]))

    # Q15
    story.extend(add_qa(15, "Why is Random Forest unaffected by feature scaling, whereas SVM and Logistic Regression are?", [
        "<b>Tree Split Mechanics:</b> Decision trees make orthogonal splits based on monotonic ordering: <code>if feature_i > threshold: split</code>. The exact numerical scale of the feature does not change its percentile ordering.",
        "<b>Invariance to Monotonic Transformations:</b> Whether battery capacity is expressed as 5000 mAh or standardized to z = +0.42, the information gain and Gini impurity reduction at any candidate split point remain identical.",
        "<b>Architectural Uniformity:</b> In SmartPrice, we standardized all numerical features in the unified <code>ColumnTransformer</code> pipeline so that all 4 models (Linear, Distance, Kernel, Tree) could be trained and benchmarked on identical, fair representations."
    ]))

    # =========================================================================
    # PART 3: FEATURE ENGINEERING & DOMAIN INDICATORS (Q16 - Q22)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(create_section_banner("PART 3: FEATURE ENGINEERING & DOMAIN HARDWARE INDICATORS (Q16 – Q22)"))
    story.append(Spacer(1, 4))

    # Q16
    story.extend(add_qa(16, "What is Feature Engineering, and why is domain knowledge essential for ML modeling?", [
        "<b>Definition:</b> Feature engineering is the process of using domain expertise to transform raw data into informative input features that make machine learning algorithms converge faster and achieve higher predictive accuracy.",
        "<b>Why Domain Knowledge Matters:</b> Raw specifications such as screen resolution (e.g., '1080 x 2400') are unreadable text strings to a mathematical model. By parsing width and height and computing Pixels Per Inch (PPI), we provide the model with a direct physical metric of display sharpness and manufacturing cost."
    ]))

    # Q17
    story.extend(add_qa(17, "How did you extract resolution width/height and compute Pixels Per Inch (PPI)? What is its physical significance?", [
        "<b>Parsing Algorithm:</b> In <code>parse_resolution()</code>, regular expressions extract both dimension integers, ordering them such that width = min(v₁, v₂) and height = max(v₁, v₂) to account for horizontal vs. vertical orientation strings.",
        "<b>Mathematical Formula:</b> PPI = √(width² + height²) / screen_size (inches).",
        "<b>Physical Significance:</b> Screen size alone doesn't reflect price. A large 6.7-inch screen with 720p resolution is cheap (<300 PPI, Budget), whereas a 6.1-inch screen with 460 PPI is an expensive Retina/OLED panel (Flagship). PPI is one of the top 8 most influential features in our model."
    ]))

    # Q18
    story.extend(add_qa(18, "What is the 'Performance Score' feature, and what is the mathematical rationale behind it?", [
        "<b>Mathematical Formula:</b> Performance Score = CPU Cores × Clock Speed (GHz) × RAM Capacity (GB).",
        "<b>Hardware Synergy Intuition:</b> An 8-core CPU clocked at 3.2 GHz with 16GB RAM represents exponential computing throughput compared to a 4-core 1.8 GHz chip with 3GB RAM. Rather than forcing a tree or linear model to learn complex three-way multiplicative interactions, this single interaction feature provides a direct proxy for computational capability.",
        "<b>Empirical Verification:</b> In our Permutation Importance analysis, <code>performance_score</code> emerged as the <b>#1 most important feature</b> with the highest mean drop in Macro F1 when permuted."
    ]))

    # Q19
    story.extend(add_qa(19, "What is the 'Screen-to-Battery Ratio' (Battery Density Index), and what counter-intuitive trend did it reveal?", [
        "<b>Formula:</b> Battery Density = Battery Capacity (mAh) / Screen Size (Inches).",
        "<b>Counter-Intuitive Market Reality:</b> Budget smartphones (₹8,000 – ₹15,000) typically have high battery densities (e.g., 6,000 mAh on a 6.5-inch screen = 923 mAh/inch) because budget consumers prioritize multi-day battery endurance. Flagships feature smaller batteries (4,000–4,500 mAh = ~650 mAh/inch) to maintain slim profiles, wireless charging coils, and vapor chambers.",
        "<b>Classification Utility:</b> This feature acts as an inverted discriminator that helps the classifier separate thick budget phones from slim flagship devices."
    ]))

    # Q20
    story.extend(add_qa(20, "What is the 'RAM-to-Storage Ratio', and how does it separate Premium/Flagship devices?", [
        "<b>Formula:</b> RAM-to-Storage Ratio = RAM (GB) / Internal Storage (GB).",
        "<b>Domain Intuition:</b> High-capacity budget phones might offer 128GB of slow eMMC storage paired with only 4GB RAM (ratio = 0.031). Premium and flagship smartphones pair 12GB–16GB of fast LPDDR5X RAM with 256GB–512GB UFS 4.0 storage (ratio = 0.047–0.062).",
        "<b>Benefit:</b> Normalizes memory balance, providing the model with a metric of component tiering."
    ]))

    # Q21
    story.extend(add_qa(21, "How were boolean features (5G, NFC, IR Blaster) parsed and represented?", [
        "<b>Normalization:</b> Raw data contained heterogeneous boolean representations ('True', 'true', '1', 1, 'False', '0', 0, NaN).",
        "<b>Encoding:</b> Converted to clean binary integer indicators (0 or 1) with missing values explicitly filled with 0 (absence of feature).",
        "<b>Commercial Relevance:</b> NFC is virtually absent in Indian budget phones (<₹15k) and ubiquitous in devices >₹30k (contactless payments). NFC alone provides high mutual information for separating Budget from Mid-Range/Premium."
    ]))

    # Q22
    story.extend(add_qa(22, "What is the final dimensionality of the feature vector, and why is ColumnTransformer the industry-standard way to build it?", [
        "<b>Transformed Dimensionality:</b> 28 numerical features (scaled) + 34 one-hot encoded categories (brands, processors, OS) = <b>62 numerical dimensions</b>.",
        "<b>Why ColumnTransformer:</b> Scikit-learn's <code>ColumnTransformer</code> encapsulates preprocessing steps into a single immutable, serializable object. When new raw input arrives at the FastAPI endpoint, calling <code>pipeline.transform(input_df)</code> automatically executes imputation, resolution parsing, scaling, and one-hot encoding in one atomic call, eliminating inference-time feature mismatches."
    ]))

    # =========================================================================
    # PART 4: ML ALGORITHMS & MATHEMATICAL FOUNDATIONS (Q23 - Q31)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(create_section_banner("PART 4: MACHINE LEARNING ALGORITHMS & MATHEMATICAL FOUNDATIONS (Q23 – Q31)"))
    story.append(Spacer(1, 4))

    # Q23
    story.extend(add_qa(23, "Why did you choose these specific 4 algorithms for benchmarking?", [
        "<b>Algorithmic Diversity:</b> To conduct a rigorous academic study, we selected representatives from 4 distinct fundamental machine learning paradigms:",
        "1. <b>Multinomial Logistic Regression:</b> Linear, parametric baseline with probabilistic soft-margin decision boundaries.",
        "2. <b>K-Nearest Neighbors (KNN):</b> Non-parametric, instance-based memory classifier using spatial distance metrics.",
        "3. <b>Support Vector Machine (SVM with RBF Kernel):</b> Maximum-margin geometric classifier projecting into infinite-dimensional Hilbert space.",
        "4. <b>Random Forest Classifier:</b> Non-linear, non-parametric ensemble of bootstrap-aggregated decorrelated decision trees.",
        "<b>Scientific Goal:</b> Compare how linear vs. distance vs. kernel vs. ensemble approaches handle heterogeneous tabular consumer hardware data."
    ]))

    # Q24
    story.extend(add_qa(24, "Explain the mathematical formulation of Multinomial Logistic Regression and the Softmax function.", [
        "<b>Linear Predictor:</b> For each class k ∈ {0, 1, 2, 3}, a linear combination of features is computed: z_k = w_k^T x + b_k.",
        "<b>Softmax Activation:</b> To convert unconstrained real values (z_k) into a valid probability distribution where ∑ P(y=k|x) = 1: P(y=k|x) = exp(z_k) / ∑ exp(z_j).",
        "<b>Decision Rule:</b> Predict the class with the maximum posterior probability: y_pred = argmax_k P(y=k|x)."
    ]))

    # Q25
    story.extend(add_qa(25, "What loss function is minimized in Multinomial Logistic Regression, and what regularization was used?", [
        "<b>Loss Function:</b> Categorical Cross-Entropy Loss (Multinomial Negative Log-Likelihood): L_CE = -∑ ∑ y_ik log(p̂_ik) where y_ik = 1 if instance i belongs to class k, and p̂_ik is the predicted softmax probability.",
        "<b>Regularization Applied:</b> L2 Ridge Regularization (0.5 ||w||₂²) with inverse regularization strength parameter C = 5.0.",
        "<b>Solver:</b> L-BFGS (Limited-memory Broyden–Fletcher–Goldfarb–Shanno), a quasi-Newton optimization algorithm well-suited for smooth multi-class convex problems."
    ]))

    # Q26
    story.extend(add_qa(26, "Explain the working principle of K-Nearest Neighbors (KNN). What hyperparameter configuration was optimal?", [
        "<b>Working Principle:</b> To classify an unseen query point x*, KNN locates the k nearest training samples in the 62-dimensional feature space based on a chosen distance metric and assigns the label via majority or weighted vote.",
        "<b>Optimal Hyperparameters Discovered:</b>",
        "• k = 19 (odd integer to avoid tie-breaks; large enough to smooth out noisy boundaries).",
        "• <b>Distance Metric:</b> Manhattan Distance (L₁ norm: d(p, q) = ∑ |p_i - q_i|). Manhattan outperformed Euclidean (L₂) because L₁ is less sensitive to dimensionality inflation.",
        "• <b>Weighting Strategy:</b> <code>weights='distance'</code> (closer neighbors have greater weight w_i = 1/d_i in the voting decision)."
    ]))

    # Q27
    story.extend(add_qa(27, "What is the 'Curse of Dimensionality', and why did KNN achieve lower performance (79.59%)?", [
        "<b>Curse of Dimensionality:</b> As the number of dimensions D increases, the volume of the feature space grows exponentially (V ∝ r^D). Data points become extremely sparse and isolated from each other.",
        "<b>Distance Concentration:</b> In high dimensions (D = 62), the ratio between the distance to the nearest neighbor and the distance to the farthest neighbor approaches 1: lim (dist_max - dist_min) / dist_min = 0.",
        "<b>Impact on KNN:</b> The concept of 'proximity' loses its discriminative power because all training points become roughly equidistant from the test query, reducing KNN's test accuracy to 79.59% compared to Random Forest's 82.65%."
    ]))

    # Q28
    story.extend(add_qa(28, "Explain the working principle of Support Vector Machines (SVM) and the role of the RBF Kernel.", [
        "<b>Maximum-Margin Principle:</b> SVM seeks an optimal hyperplane that maximizes the geometric margin 2 / ||w|| separating different classes while penalizing margin violations.",
        "<b>Why Linear Hyperplanes Fail:</b> Smartphone specifications have complex non-linear boundaries (e.g., combinations of screen type and processor). A flat hyperplane cannot linearly separate all 4 tiers.",
        "<b>Radial Basis Function (RBF) Kernel:</b> K(x, x') = exp(-γ ||x - x'||²). The RBF kernel maps 62-dimensional input vectors into an infinite-dimensional reproducing kernel Hilbert space (RKHS) where non-linear patterns become linearly separable without ever explicitly computing the high-dimensional coordinates (the 'Kernel Trick')."
    ]))

    # Q29
    story.extend(add_qa(29, "What do the hyperparameters C and γ (gamma) control in an RBF-SVM, and what values were selected?", [
        "<b>Regularization Parameter C:</b> Controls the tradeoff between achieving a smooth decision boundary and correctly classifying every training point (penalty for slack variables ξ_i). Large C prioritizes zero training errors (risk of overfitting); small C allows larger margins (risk of underfitting).",
        "<b>Kernel Bandwidth γ:</b> Determines the influence radius of individual support vectors. High γ creates tight, localized Gaussian bells around points (high variance); low γ creates broad, smooth decision surfaces (high bias).",
        "<b>Tuned Configuration in SmartPrice:</b> C = 5.0, γ = 'auto' (where γ = 1 / n_features = 1/62 = 0.0161), achieving <b>80.10% Test Accuracy</b> and 0.9591 ROC-AUC."
    ]))

    # Q30
    story.extend(add_qa(30, "How does Random Forest work, and what makes it an ensemble method (Bagging / Bootstrap Aggregating)?", [
        "<b>Ensemble Principle:</b> Random Forest combines B individual decision trees to produce a collective prediction that has lower variance than any single tree.",
        "<b>Bootstrap Aggregation (Bagging):</b> Each of the 300 trees is trained on an independent bootstrap sample of the training set (sampled with replacement from the 784 training rows, containing ~63.2% unique rows; remaining ~36.8% form Out-of-Bag samples).",
        "<b>Feature Subsampling (Random Subspace Method):</b> At every candidate split within every tree, only a random subset of features is evaluated: m = log₂(D) = log₂(62) ≈ 6 features. This deliberately decorrelates the trees, preventing strong features (like RAM) from dominating every single split.",
        "<b>Aggregation:</b> Classification is determined by soft voting (averaging predicted class probability distributions across all 300 trees)."
    ]))

    # Q31
    story.extend(add_qa(31, "Why did Random Forest outperform all other models (82.65% Test Acc, 0.9613 ROC-AUC)?", [
        "1. <b>Natural Step-Function Thresholds:</b> Electronics pricing is defined by discrete hardware thresholds (e.g., if RAM ≥ 12GB and SoC = Snapdragon 8, price tier = Flagship). Decision trees capture these orthogonal step boundaries naturally.",
        "2. <b>Immunity to Multi-Collinearity:</b> Correlated features (such as pixel count, resolution width, and PPI) degrade regression and distance models, but Random Forest handles them seamlessly by evaluating splits independently.",
        "3. <b>Variance Reduction via Averaging:</b> Averaging 300 decorrelated trees eliminates the high variance of individual deep trees, maintaining robust generalization across all 4 price classes."
    ]))

    # =========================================================================
    # PART 5: MODEL TRAINING, CROSS-VALIDATION & TUNING (Q32 - Q38)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(create_section_banner("PART 5: MODEL TRAINING, CROSS-VALIDATION & HYPERPARAMETER TUNING (Q32 – Q38)"))
    story.append(Spacer(1, 4))

    # Q32
    story.extend(add_qa(32, "What train-test split ratio did you choose, and why was Stratified Splitting critical?", [
        "<b>Split Ratio:</b> 80% Training (784 samples) and 20% Test (196 samples), fixed with <code>random_state=42</code>.",
        "<b>Why Stratified Splitting:</b> In non-stratified random splitting, minority classes (such as Premium with only 133 total samples) could easily be under-represented or over-represented in the test set by chance.",
        "<b>Mathematical Guarantee:</b> <code>stratify=y</code> guarantees that both training and test sets contain exactly 35.6% Mid-Range, 34.4% Budget, 16.4% Flagship, and 13.6% Premium samples, preserving empirical distribution fidelity."
    ]))

    # Q33
    story.extend(add_qa(33, "What is 5-Fold Stratified Cross-Validation, and why is it preferred over a single validation set?", [
        "<b>Mechanics:</b> The 784 training instances are partitioned into 5 equal, stratified folds (~156–157 samples each). In 5 successive rounds, 4 folds (627 samples) are used to train the model, and the remaining 1 fold is used for validation.",
        "<b>Why Preferred over Single Split:</b> A single validation split can produce high or low accuracy purely by luck of the partition. 5-Fold CV tests the model across 5 distinct holdouts, producing a mean validation score and standard deviation (μ ± σ).",
        "<b>SmartPrice 5-Fold Results:</b> Random Forest achieved 78.06% ± 1.4% across folds, proving that its high performance is robust and stable."
    ]))

    # Q34
    story.extend(add_qa(34, "What hyperparameter optimization method did you use (GridSearchCV vs. RandomizedSearchCV)?", [
        "<b>Method:</b> <code>GridSearchCV</code> with 5-Fold Stratified Cross-Validation and <code>scoring='accuracy'</code> in <code>05_hyperparameter_tuning.py</code>.",
        "<b>Why Exhaustive Grid Search:</b> With 4 classic ML models and bounded parameter grids, GridSearchCV exhaustively evaluated every parameter combination across all 5 folds, ensuring no high-performing configuration was overlooked.",
        "<b>Parallel Execution:</b> Optimized using <code>n_jobs=-1</code> across all available CPU cores."
    ]))

    # Q35
    story.extend(add_qa(35, "What hyperparameters were tuned for the Champion Random Forest model, and what were the optimal values?", [
        "<b>Tuned Hyperparameters & Search Space:</b>",
        "• <code>n_estimators</code>: Evaluated [100, 200, 300] → <b>Optimal: 300</b> (more trees reduced ensemble variance).",
        "• <code>max_depth</code>: Evaluated [10, 15, 20, None] → <b>Optimal: 15</b> (prevented trees from growing infinitely deep and memorizing training noise).",
        "• <code>max_features</code>: Evaluated ['sqrt', 'log2'] → <b>Optimal: 'log2'</b> (≈ 6 features per split, maximizing tree decorrelation).",
        "• <code>min_samples_split</code>: Evaluated [2, 5] → <b>Optimal: 2</b>.",
        "• <code>min_samples_leaf</code>: Evaluated [1, 2] → <b>Optimal: 1</b>."
    ]))

    # Q36
    story.extend(add_qa(36, "What is the Bias-Variance Tradeoff, and where do your benchmarked models lie on this spectrum?", [
        "<b>Bias:</b> Error from erroneous assumptions in the learning algorithm (underfitting, model too simple).",
        "<b>Variance:</b> Error from sensitivity to small fluctuations in the training set (overfitting, model memorizes noise).",
        "<b>SmartPrice Model Mapping:</b>",
        "• <b>Multinomial Logistic Regression:</b> High Bias / Low Variance. Constrained by linear decision boundaries (underfits complex non-linear specs, achieving 78.57%).",
        "• <b>Unpruned Single Decision Tree:</b> Low Bias / High Variance. Memorizes specific training phones.",
        "• <b>Random Forest (Ensemble):</b> Low Bias / Low Variance. Individual deep trees maintain low bias, while bagging 300 trees drives variance down asymptotically.",
        "• <b>KNN (k=19):</b> Moderate Bias / Moderate Variance. Sensitive to local neighborhood density in high dimensions."
    ]))

    # Q37
    story.extend(add_qa(37, "How did you verify that your Random Forest model is not suffering from severe overfitting?", [
        "<b>Cross-Validation vs. Test Alignment:</b>",
        "• 5-Fold CV Accuracy on Training Set: <b>78.06%</b>",
        "• Test Accuracy on Completely Unseen Holdout Set: <b>82.65%</b>",
        "<b>Interpretation:</b> The test accuracy closely aligns with (and slightly exceeds) the 5-fold CV score. An overfitted model would show 99% train accuracy and 60% test accuracy. The small positive delta confirms robust generalization without memorization.",
        "<b>Regularization via max_depth:</b> Restricting tree depth to <code>max_depth=15</code> explicitly limited leaf node purity, halting memorization of idiosyncratic single-phone records."
    ]))

    # Q38
    story.extend(add_qa(38, "Why is setting a fixed random seed (random_state=42) necessary in machine learning experiments?", [
        "<b>Scientific Reproducibility:</b> Algorithms involving stochastic processes (such as train-test splitting, bootstrap sampling in Random Forest, and fold assignment in K-Fold) utilize pseudo-random number generators.",
        "<b>Consistent Benchmarking:</b> Without fixing <code>random_state=42</code>, running the benchmark script twice would yield different training splits and slightly differing accuracy scores, preventing fair head-to-head comparison between models.",
        "<b>Academic Rigor:</b> Ensures any external researcher or examiner can re-run the code and obtain the exact same 82.65% test accuracy and confusion matrix."
    ]))

    # =========================================================================
    # PART 6: MODEL EVALUATION METRICS & ERROR ANALYSIS (Q39 - Q44)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(create_section_banner("PART 6: EVALUATION METRICS, CONFUSION MATRIX & ERROR ANALYSIS (Q39 – Q44)"))
    story.append(Spacer(1, 4))

    # Q39
    story.extend(add_qa(39, "What is a Confusion Matrix? Walk through the exact confusion matrix of your champion Random Forest model.", [
        "<b>Definition:</b> A C × C table comparing ground truth labels against model predictions, where diagonal elements represent correct classifications and off-diagonals represent errors.",
        "<b>SmartPrice Champion Confusion Matrix (196 Unseen Test Samples):</b>",
        "• <b>Budget (67 actual):</b> <b>54 Correct</b>, 13 misclassified as Mid-Range, 0 as Premium, 0 as Flagship (Recall = 80.6%, Precision = 94.7%).",
        "• <b>Mid-Range (70 actual):</b> 3 misclassified as Budget, <b>64 Correct</b>, 3 as Premium, 0 as Flagship (Recall = 91.4%, Precision = 77.1%).",
        "• <b>Premium (27 actual):</b> 0 as Budget, 6 misclassified as Mid-Range, <b>15 Correct</b>, 6 as Flagship (Recall = 55.6%, Precision = 71.4%).",
        "• <b>Flagship (32 actual):</b> 0 as Budget, 0 as Mid-Range, 3 misclassified as Premium, <b>29 Correct</b>, (Recall = 90.6%, Precision = 82.9%).",
        "<b>Total Correct:</b> 54 + 64 + 15 + 29 = 162 / 196 = <b>82.65%</b>."
    ]))

    # Q40
    story.extend(add_qa(40, "What is the difference between Precision and Recall, and what do they signify in this project?", [
        "<b>Precision:</b> Of all phones predicted as Class k, what fraction actually belonged to Class k? Precision_k = TP_k / (TP_k + FP_k). High precision means low false-alarm rate (e.g., Budget Precision = 94.7% means when model predicts Budget, it is almost certainly correct).",
        "<b>Recall:</b> Of all actual phones belonging to Class k, what fraction did the model correctly identify? Recall_k = TP_k / (TP_k + FN_k). High recall means low miss rate (e.g., Mid-Range Recall = 91.4%, Flagship Recall = 90.6%)."
    ]))

    # Q41
    story.extend(add_qa(41, "What is the difference between Macro F1-score and Weighted F1-score, and which one is more trustworthy here?", [
        "<b>Formulas:</b>",
        "• <b>Macro F1:</b> Simple unweighted arithmetic average of F1-scores across all classes: Macro F1 = (1/4) ∑ F1_k = <b>0.7996</b>. Treats every class as equally important.",
        "• <b>Weighted F1:</b> Average of F1-scores weighted by the support (number of samples) of each class: Weighted F1 = ∑ w_k F1_k = <b>0.8239</b>.",
        "<b>Which is More Trustworthy:</b> <b>Macro F1</b> is far more stringent and trustworthy in imbalanced domains. If a model performs poorly on minority classes (e.g., Premium with only 27 test samples), Weighted F1 can hide the flaw because the majority classes (Budget & Mid-Range, 137 samples) overpower the score. SmartPrice reports both, prioritizing Macro F1."
    ]))

    # Q42
    story.extend(add_qa(42, "What is One-vs-Rest (OvR) ROC-AUC, and how did Random Forest achieve 0.9613?", [
        "<b>Multi-Class ROC-AUC:</b> The Receiver Operating Characteristic curve plots True Positive Rate vs. False Positive Rate across all probability thresholds. In multi-class classification, One-vs-Rest (OvR) treats each class as a binary problem against all other 3 classes combined.",
        "<b>AUC Interpretation:</b> An AUC of 0.5 corresponds to random guessing; an AUC of 1.0 represents perfect class ranking. Random Forest's Macro ROC-AUC of <b>0.9613</b> demonstrates that the model possesses exceptional discriminative capability to rank positive instances above negative instances across all decision thresholds."
    ]))

    # Q43
    story.extend(add_qa(43, "In your confusion matrix, why did the 'Premium' tier show lower recall (55.6%) than Budget and Flagship?", [
        "<b>Domain Reason — The 'Sandwich Effect':</b> Premium smartphones (₹30,001 to ₹50,000) sit directly between Mid-Range and Flagship. Manufacturers frequently blur this boundary:",
        "1. High-spec 'Flagship Killers' (like OnePlus or iQOO) pack flagship processors (Snapdragon 8 Gen-series) into ₹35,000 bodies, causing the model to predict them as Flagship.",
        "2. Expensive Mid-Range devices pack budget processors into ₹32,000 bodies with high brand markup, causing the model to predict them as Mid-Range.",
        "<b>Notice Adjacent Misclassifications:</b> Out of 12 misclassified Premium phones, 6 were predicted as Mid-Range and 6 as Flagship. <b>Zero Premium phones were ever misclassified as Budget</b>, proving errors are strictly confined to adjacent economic tiers."
    ]))

    # Q44
    story.extend(add_qa(44, "Summarize the final comparative metrics table of all 4 models.", [
        "• <b>Random Forest (Champion):</b> Test Acc = <b>82.65%</b> | CV Acc = 78.06% | Macro F1 = <b>0.7996</b> | Weighted F1 = 0.8239 | ROC-AUC = <b>0.9613</b>.",
        "• <b>Support Vector Machine (RBF):</b> Test Acc = 80.10% | CV Acc = 75.28% | Macro F1 = 0.7807 | Weighted F1 = 0.8005 | ROC-AUC = 0.9591.",
        "• <b>K-Nearest Neighbors (KNN):</b> Test Acc = 79.59% | CV Acc = 74.68% | Macro F1 = 0.7638 | Weighted F1 = 0.7950 | ROC-AUC = 0.9517.",
        "• <b>Logistic Regression:</b> Test Acc = 78.57% | CV Acc = 74.22% | Macro F1 = 0.7639 | Weighted F1 = 0.7857 | ROC-AUC = 0.9451."
    ]))

    # =========================================================================
    # PART 7: EXPLAINABILITY & PRODUCTION DEPLOYMENT (Q45 - Q50)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(create_section_banner("PART 7: EXPLAINABILITY, DEPLOYMENT & PRODUCTION ARCHITECTURE (Q45 – Q50)"))
    story.append(Spacer(1, 4))

    # Q45
    story.extend(add_qa(45, "What is Model Explainability, and why is it essential in modern Machine Learning?", [
        "<b>Definition:</b> Model explainability refers to the methods and techniques that allow human practitioners to understand, interpret, and trust the decisions made by machine learning models.",
        "<b>Why Black-Box Models Are Insufficient:</b> In commercial and academic deployment, predicting 'Tier 3 (Flagship)' without rationale is unactionable. Stakeholders need to know <i>why</i> a device was categorized as Flagship (e.g., '16GB RAM + 3.2GHz CPU drove the prediction by +38%').",
        "<b>Trust & Regulatory Compliance:</b> Explainability reveals potential data bias (e.g., whether the model over-relies on brand name rather than genuine hardware performance)."
    ]))

    # Q46
    story.extend(add_qa(46, "What is Permutation Feature Importance, and why is it superior to Default Tree Impurity (MDI)?", [
        "<b>How Permutation Importance Works:</b> On the unseen test set, the values of a single feature column are randomly shuffled, breaking its relationship with the target y. The drop in model evaluation metric (Macro F1) is measured. Features causing the largest performance drops are ranked highest.",
        "<b>Why Superior to Mean Decrease in Impurity (MDI / Gini Importance):</b>",
        "1. <b>MDI is Biased toward High-Cardinality Continuous Features:</b> MDI artificially favors features with many unique numerical values over informative binary/categorical features.",
        "2. <b>MDI is Computed on Training Data:</b> MDI reflects training fit, which can over-estimate importance if features overfit. Permutation importance is computed on unseen test data, reflecting genuine out-of-sample generalization value."
    ]))

    # Q47
    story.extend(add_qa(47, "What were the top 5 most influential features discovered in SmartPrice, and do they match market reality?", [
        "<b>Top 5 Permutation Importance Rankings:</b>",
        "1. <code>performance_score</code> (Mean Drop = <b>0.0369</b>): Compound computing metric (Cores × Clock × RAM).",
        "2. <code>processor_speed</code> (Mean Drop = <b>0.0298</b>): Clock frequency in GHz separating budget SoCs (1.8GHz) from flagship chipsets (>3.2GHz).",
        "3. <code>ram_capacity</code> (Mean Drop = <b>0.0242</b>): 4GB/6GB (Budget) vs 12GB/16GB (Flagship).",
        "4. <code>rating</code> (Mean Drop = <b>0.0242</b>): Consumer satisfaction score reflecting build and user experience.",
        "5. <code>primary_camera_front</code> (Mean Drop = <b>0.0189</b>): Premium 32MP/4K selfie sensors found primarily in upper tiers.",
        "<b>Market Reality Alignment:</b> Silicon computing power and camera hardware represent the largest direct component costs in modern smartphone manufacturing."
    ]))

    # Q48
    story.extend(add_qa(48, "How are the trained models serialized, stored, and loaded in the production backend?", [
        "<b>Serialization via Joblib:</b> In <code>05_hyperparameter_tuning.py</code>, trained pipelines and models are serialized to disk using <code>joblib.dump()</code> with compression: <code>ml/models/best_model.joblib</code>, <code>preprocessor.joblib</code>, <code>tuned_random_forest.joblib</code>, <code>tuned_svm.joblib</code>, etc.",
        "<b>Singleton Inference Engine:</b> In <code>backend/app/predictor.py</code>, the <code>ModelEngine</code> class follows the singleton pattern. Pipelines and weights are loaded into memory once during FastAPI startup (in <150ms), avoiding disk I/O on individual user requests and enabling sub-10ms real-time inference."
    ]))

    # Q49
    story.extend(add_qa(49, "Describe the complete full-stack architecture of the SmartPrice web application.", [
        "<b>Backend (FastAPI REST Engine):</b>",
        "• Written in Python 3.11 with FastAPI and Uvicorn.",
        "• Strict Pydantic v2 schemas (<code>SmartphoneInputSchema</code>) validate ranges (RAM between 1 and 24 GB, screen size between 3.0 and 8.0 inches, etc.).",
        "• 10 Verified REST Endpoints (<code>POST /api/predict</code>, <code>POST /api/predict/all</code>, <code>GET /api/analytics/records</code>, <code>GET /api/models/metrics</code>, <code>GET /api/health</code>).",
        "<b>Frontend (Modern React 19 + TypeScript + Tailwind CSS):</b>",
        "• Built with Vite 8 and React 19.",
        "• 5 Modular Views: <b>Dashboard Overview</b>, <b>Interactive Predictor</b> (with pre-filled flagship/budget presets and sliders), <b>Model Benchmarking Lab</b>, <b>Dataset Analytics Explorer</b>, and <b>Explainability Visualizer</b>.",
        "• Responsive design with slide-over drawer and luxury card elevation styling."
    ]))

    # Q50
    story.extend(add_qa(50, "How does the system handle cloud deployment, and how does the live prediction pipeline execute end-to-end?", [
        "<b>End-to-End Pipeline Execution:</b>",
        "1. <b>Client Request:</b> User adjusts hardware sliders in React UI or clicks a device preset (e.g., iPhone 15 Pro, Galaxy S24 Ultra, Redmi Note 13).",
        "2. <b>JSON Transmission:</b> Frontend sends a <code>POST /api/predict</code> request with technical specifications.",
        "3. <b>Schema Validation:</b> FastAPI Pydantic validator validates data types and ranges.",
        "4. <b>Dynamic Feature Derivation:</b> Backend parses resolution, calculates aspect ratio, PPI, performance score, battery density, and RAM-to-storage ratio.",
        "5. <b>ColumnTransformer Execution:</b> Standardizes numerical features and one-hot encodes brand and processor.",
        "6. <b>Model Inference:</b> Champion Random Forest calculates predicted class and softmax probability array (e.g., 94.8% Flagship, 4.2% Premium, 1.0% Mid-Range, 0.0% Budget).",
        "7. <b>JSON Response & Display:</b> Response returned in <10ms; React UI smoothly displays confidence bars and key driving feature badges.",
        "<b>Cloud & Production Setup:</b> Configured with <code>api/index.py</code> using <code>Mangum</code> for Vercel serverless deployment, <code>render.yaml</code> for Render deployment, and <code>start_project.bat</code> for 1-click local launch."
    ]))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Viva PDF at: {OUTPUT_PDF}")


if __name__ == "__main__":
    create_viva_pdf()
