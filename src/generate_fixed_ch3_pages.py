import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_clean_pages_43_44_pdf(output_path="output/pdf/clean_pages_43_44.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=1.0*inch,
        rightMargin=1.0*inch,
        topMargin=1.0*inch,
        bottomMargin=1.0*inch
    )
    
    styles = getSampleStyleSheet()
    
    section_title_style = ParagraphStyle(
        'AcademicSectionTitle',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'AcademicBodyStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24, # Double spaced (12pt font x 2 = 24pt leading)
        textColor=colors.black,
        spaceAfter=10,
        alignment=4 # Justified
    )
    
    bullet_style = ParagraphStyle(
        'AcademicBulletStyle',
        parent=body_style,
        leftIndent=15,
        spaceAfter=8
    )

    story = []
    
    # 1. Continuation of 3.3.1 Walk-forward window from bottom of Page 42
    story.append(Paragraph(
        "shifts forward by one week. The oldest weekly observation is discarded, the most recent observation is absorbed, and the models are retrained.",
        body_style
    ))
    
    # 2. 3.3.2 Model Training and Hyperparameter Tuning
    story.append(Paragraph("3.3.2 Model Training and Hyperparameter Tuning", section_title_style))
    story.append(Paragraph(
        "Hyperparameters were tuned once on the 2010–2020 in-sample period using GridSearchCV with 5-fold TimeSeriesSplit, focusing on parameters that penalize model complexity:",
        body_style
    ))


    story.append(Paragraph(
        "• <b>Random Forest Parameters:</b> The search optimizes the number of trees in the forest (<i>n_estimators</i>), the maximum depth of each tree (<i>max_depth</i>), and the minimum number of samples required to split an internal node (<i>min_samples_split</i>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>XGBoost Parameters:</b> The search optimizes the learning rate or step size shrinkage (<i>learning_rate</i>), the maximum tree depth (<i>max_depth</i>), and the minimum loss reduction required to make a further partition (<i>gamma</i>), which directly controls the structural regularization.",
        bullet_style
    ))
    
    # 3. 3.3.3 Portfolio Turnover and Transaction Costs
    story.append(Paragraph("3.3.3 Portfolio Turnover and Transaction Costs", section_title_style))
    story.append(Paragraph(
        "To ensure that the optimized Mean-CVaR portfolio strategy is economically viable and not merely theoretically profitable, it is imperative to account for real-world trading frictions, such as brokerage fees and slippage on the Nigerian Exchange Group (NGX) (Ashrafzadeh et al., 2025). This requires measuring the portfolio turnover, which mathematically quantifies the absolute change in the portfolio's asset weights from one weekly rebalancing period to the next (Zsurkis, Nicolau, & Rodrigues, 2024):",
        body_style
    ))
    
    # Turnover formula
    formula_style = ParagraphStyle(
        'FormulaStyle',
        parent=body_style,
        alignment=1, # Centered
        fontName='Times-Italic',
        spaceBefore=6,
        spaceAfter=10
    )
    story.append(Paragraph("Turnover<sub>t</sub> = &Sigma;<sub>i=1..N</sub> |w<sub>t,i</sub> - w<sub>t<sup>-</sup>,i</sub>|", formula_style))
    
    story.append(Paragraph(
        "Following standard empirical finance procedures, transaction costs are deducted from gross returns to construct net returns. This study evaluates portfolio performance across three execution-cost regimes: a gross frictionless baseline (0.00%), an institutional PFA execution scenario applying a fixed 75 basis points (0.75%) per rebalancing trade, and a retail execution friction scenario applying 150 basis points (1.50%) to account for brokerage commissions and market slippage on the NGX. Finally, a Net Returns feature column will be constructed by deducting these calculated transaction costs from the gross portfolio returns, providing a rigorous and realistic evaluation of the portfolio's actual out-of-sample performance.",
        body_style
    ))
    
    # 4. 3.3.4 Feature Importance Extraction
    story.append(Paragraph("3.3.4 Feature Importance Extraction", section_title_style))
    story.append(Paragraph(
        "Due to the criticism of ensemble models of being black boxes in traditional econometrics and to ensure economic interpretability, this study extracts the built-in feature importance scores from the optimized models to determine which of the thirteen technical indicators exert the strongest predictive influence on NGX equity returns.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Random Forest Interpretation:</b> Importance is calculated using the Mean Decrease in Impurity (Gini Importance). It measures the total reduction of the Mean Squared Error (MSE) brought by that specific feature across all trees in the forest.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>XGBoost Interpretation:</b> Importance is measured using Information Gain. It evaluates the relative contribution of each feature to the model by calculating the improvement in accuracy it provides to the branches it is on.",
        bullet_style
    ))
    
    # 5. 3.3.5 Header
    story.append(Paragraph("3.3.5 Evaluation Metrics for Forecasting and Portfolio Performance", section_title_style))

    doc.build(story)
    print(f"[OK] Generated clean replacement pages 43-44: {output_path}")

if __name__ == '__main__':
    generate_clean_pages_43_44_pdf()
