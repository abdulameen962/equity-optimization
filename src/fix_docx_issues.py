import os
import sys
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK

sys.stdout.reconfigure(encoding='utf-8')

def remove_paragraph(paragraph):
    if paragraph._element.getparent() is not None:
        paragraph._element.getparent().remove(paragraph._element)

def fix_docx(input_path="Abdulameen_Complete_Thesis_Chapters_1_5.docx", output_path="output/pdf/justified_thesis_fixed.docx"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = Document(input_path)
    print(f"Loading DOCX: {input_path}")

    # ==========================================
    # 1. FIX DUPLICATE TABLE HEADERS (Group B)
    # ==========================================
    if len(doc.tables) > 0:
        t0 = doc.tables[0]
        if len(t0.rows) > 8:
            cell_txt = t0.rows[8].cells[0].text.strip()
            if 'Variable' in cell_txt and 'Symbol' in cell_txt:
                print("Removing duplicate header row in Table 0 (row 8)...")
                t0._tbl.remove(t0.rows[8]._tr)
                
    if len(doc.tables) > 5:
        t5 = doc.tables[5]
        if len(t5.rows) > 19:
            cell_txt = t5.rows[19].cells[0].text.strip()
            if 'Ticker' in cell_txt:
                print("Removing duplicate header row in Table 5 (row 19)...")
                t5._tbl.remove(t5.rows[19]._tr)

    # Re-clean Table 0 math cells to ensure pristine math formulations
    if len(doc.tables) > 0:
        t0 = doc.tables[0]
        math_fixes = {
            "Weekly Logarithmic Return": "R_{i,t+1} = ln(P_{i,t} / P_{i,t-1})",
            "Moving Average Convergence Divergence": "MACD_t = EMA_{12}(P_t) - EMA_{26}(P_t)",
            "Percentage Price Oscillator": "PPO_t = [ (EMA_{12}(P_t) - EMA_{26}(P_t)) / EMA_{26}(P_t) ] × 100",
            "Relative Strength Index": "RSI_t = 100 - [ 100 / (1 + RS) ]",
            "Stochastic Oscillator (%K)": "STOCH_t = [ (P_t - L_{14}) / (H_{14} - L_{14}) ] × 100",
            "Lagged Log Returns": "R_{i,t-1}, R_{i,t-2}, R_{i,t-3}, R_{i,t-4}",
            "Simple Moving Average": "SMA_t = (1 / n) ∑_{k=0..n-1} P_{t-k}",
            "Average Directional Index": "ADX_t = 100 × MA( |+DI - -DI| / (+DI + -DI) )",
            "Parabolic Stop and Reverse": "SAR_t = SAR_{t-1} + α(EP_{t-1} - SAR_{t-1})",
            "Average True Range": "ATR_t = (1 / n) ∑_{i=1..n} TR_i",
            "On-Balance Volume": "OBV_t = OBV_{t-1} ± V_t",
            "Risk-Free Rate": "R_f = (1 + R_{annual})^{1/52} - 1"
        }
        for row in t0.rows:
            var_name = row.cells[1].text.strip()
            for key, val in math_fixes.items():
                if key in var_name:
                    row.cells[3].text = val
                    break

    # Track fixed sections to ensure single execution
    fixed_sections = set()

    for p in list(doc.paragraphs):
        txt = p.text.strip()
        if not txt:
            continue

        # 1. Turnover + Transaction costs merged block
        if "Turnover = " in txt and "Following standard empirical finance procedures" in txt and "turnover" not in fixed_sections:
            fixed_sections.add("turnover")
            print("Fixing merged Turnover & Transaction Costs paragraph...")
            p.text = "Turnover_t = ∑_{i=1..N} |w_{t,i} - w_{t^-,i}|"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            p_next = p.insert_paragraph_before(
                "Following standard empirical finance procedures, transaction costs are deducted from gross returns to construct net returns. "
                "This study evaluates portfolio performance across three execution-cost regimes: a gross frictionless baseline (0.00%), "
                "an institutional PFA execution scenario applying a fixed 75 basis points (0.75%) per rebalancing trade, and a retail execution friction scenario "
                "applying 150 basis points (1.50%) to account for brokerage commissions and market slippage on the NGX. "
                "Finally, a Net Returns feature column will be constructed by deducting these calculated transaction costs from the gross portfolio returns, "
                "providing a rigorous and realistic evaluation of the portfolio's actual out-of-sample performance."
            )
            p_next.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # 2. Feature Vector definition
        if "The feature vector" in txt and "13" in txt and "column vector" in txt and "feature_vector" not in fixed_sections:
            fixed_sections.add("feature_vector")
            print("Fixing Feature Vector definition...")
            p.text = "The feature vector x_t is mathematically defined as a 13 × 1 column vector:"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before(
                "x_t = [ x_{1,t}, x_{2,t}, ..., x_{13,t} ]ᵀ = [ MACD_t, PPO_t, RSI_t, STOCH_t, R_{t-1}, R_{t-2}, R_{t-3}, R_{t-4}, SMA_t, ADX_t, SAR_t, ATR_t, OBV_t ]ᵀ"
            )
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 3. Node split Rnode formula
        if "algorithm determines the optimal splitting variable" in txt and "split point" in txt and "node_split" not in fixed_sections:
            fixed_sections.add("node_split")
            print("Fixing Node Split Rnode formula...")
            p.text = "The algorithm determines the optimal splitting variable j (from the m features) and split point s by minimizing the Mean Squared Error (MSE) across the resulting regions R_1(j,s) and R_2(j,s):"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before("min_{(j,s)} [ ∑_{x_i ∈ R_1(j,s)} (y_i - ŷ_{R1})² + ∑_{x_i ∈ R_2(j,s)} (y_i - ŷ_{R2})² ]")
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 4. Rockafellar CVaR auxiliary function
        if "Rockafellar and Uryasev (2000)" in txt and "seamlessly integrated" in txt and "rockafellar" not in fixed_sections:
            fixed_sections.add("rockafellar")
            print("Fixing Rockafellar CVaR formula...")
            p.text = "Following the formulation by Rockafellar and Uryasev (2000), CVaR can be seamlessly integrated into a linear programming problem by minimizing an auxiliary continuous and convex function F_α(w, γ):"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before("F_α(w, γ) = γ + (1 / (1 - α)) E[ max(0, -wᵀR - γ) ]")
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 5. CVaR Optimization Objective
        if "ultimate objective of the model is to minimize the tail risk" in txt and "cvar_obj" not in fixed_sections:
            fixed_sections.add("cvar_obj")
            print("Fixing CVaR Optimization Objective formula...")
            p.text = "The ultimate objective of the model is to minimize the tail risk (CVaR) while achieving a minimum acceptable expected return driven by the machine learning forecasts. The optimization problem is specified as:"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before("min_{w} F_α(w, γ)   s.t.   wᵀ E[R] ≥ r_{target},   ∑_{i=1}^N w_i = 1,   w_i ≥ 0")
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 6. MAE & Predictive Metrics
        if "Mean Absolute Error (MAE):" in txt and "mae" not in fixed_sections:
            fixed_sections.add("mae")
            print("Fixing MAE formula...")
            p.text = "• Mean Absolute Error (MAE): Measures the average absolute magnitude of the prediction errors, providing a baseline view of model accuracy without directional bias:"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before("MAE = (1 / n) ∑_{i=1}^n |y_i - ŷ_i|")
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 7. Risk-Adjusted Portfolio Metrics (Sharpe)
        if "Sharpe Ratio: Measures the excess return per unit" in txt and "sharpe" not in fixed_sections:
            fixed_sections.add("sharpe")
            print("Fixing Sharpe Ratio formula...")
            p.text = "• Sharpe Ratio: Measures the excess return per unit of total portfolio risk (standard deviation σ_p):"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before("Sharpe Ratio = ( E[R_p] - R_f ) / σ_p")
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 8. Buy-and-Hold Weights
        if "The Buy-and-Hold Market Index Strategy:" in txt and "buy_hold" not in fixed_sections:
            fixed_sections.add("buy_hold")
            print("Fixing Buy-and-Hold weight drift formula...")
            p.text = (
                "• The Buy-and-Hold Market Index Strategy: A passive strategy where capital is initialized at equal weights w_{0,i} = 1/N at t = 0. "
                "Post-initialization, asset weights drift passively with market price returns (w_{t+1,i} ∝ w_{t,i}(1 + R_{t+1,i})) with zero weekly rebalancing turnover."
            )
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # 9. Hypothesis Testing Framework
        if "Jobson and Korkie (1981) Test with Memmel (2007) Correction" in txt and "jobson" not in fixed_sections:
            fixed_sections.add("jobson")
            print("Fixing Jobson-Korkie Memmel Z-test formula...")
            p.text = (
                "1. Jobson and Korkie (1981) Test with Memmel (2007) Correction: Evaluates the null hypothesis of Sharpe ratio equality H_0: Sharpe_A = Sharpe_B for two correlated portfolios. "
                "Memmel (2007) corrects the asymptotic variance under portfolio return correlation ρ:"
            )
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p_form = p.insert_paragraph_before("Z = (Sharpe_A - Sharpe_B) / √[ (1 / T) ( 2(1 - ρ) + 0.5(Sharpe_A² + Sharpe_B² - 2 Sharpe_A Sharpe_B ρ²) ) ]")
            p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Delete stray formula fragment paragraphs (e.g. '????', '?????', '0\tA\tB', '2\t2]')
        if txt in ['????', '?????', '0\tA\tB', '2\t2]', '???  ??|', '?=1']:
            remove_paragraph(p)

    # ==========================================
    # 3. ENFORCE JUSTIFY & PAGE BREAK BEFORE REFERENCES (Group C)
    # ==========================================
    print("Enforcing JUSTIFY alignment and page break before References...")
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue

        # Page break before References
        if txt == 'References':
            print("Adding page break before References heading...")
            p.insert_paragraph_before().add_run().add_break(WD_BREAK.PAGE)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            continue

        # Skip cover page (first 16 paragraphs)
        # Skip headings & centered formulas
        is_heading = (
            txt.startswith('Chapter') or txt.startswith('CHAPTER') or
            txt == 'LITERATURE REVIEW' or txt == 'RESEARCH METHODOLOGY' or
            bool(re.match(r'^\d+\.\d+', txt)) or
            (txt.isupper() and len(txt) < 60)
        )
        if is_heading or p.alignment == WD_ALIGN_PARAGRAPH.CENTER:
            continue

        # Enforce JUSTIFY
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.save(output_path)
    print(f"[OK] Successfully saved fixed DOCX: {output_path}")
    return output_path

if __name__ == '__main__':
    fix_docx()
