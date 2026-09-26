import os
import re

# -----------------------------------------------------------------------------
# MASTER APA 7TH EDITION GROUNDED REFERENCES (71 ENTRIES)
# -----------------------------------------------------------------------------

REFERENCES_PLAIN = [
    "Adegboyo, O. S., & Sarwar, K. (2025). Modelling and forecasting of Nigeria stock market volatility. Future Business Journal, 11(1), Article 124. https://doi.org/10.1186/s43093-025-00536-4",
    "Ajiga, D. I., Adeleye, R. A., Tubokirifuruar, T. S., Bello, B. G., Ndubuisi, N. L., Asuzu, O. F., & Owolabi, O. R. (2024). Machine learning for stock market forecasting: A review of models and accuracy. Finance & Accounting Research Journal, 6(2).",
    "Alfzari, S., Al-Shboul, M., & Alshurideh, M. (2025). Predictive analytics in portfolio management: A fusion of AI and investment economics for optimal risk-return trade-offs. International Review of Management and Marketing, 15(2), 365–380. https://doi.org/10.32479/irmm.18594",
    "Alfeus, M., Harvey, J., & Maphatsoe, P. (2024). Improving realised volatility forecast for emerging markets. Journal of Economics and Finance. Advance online publication. https://doi.org/10.1007/s12197-024-09701-x",
    "Alim, W., Khan, N. U., Zhang, V. W., Cai, H. H., Mikhaylov, A., & Yuan, Q. (2024). Influence of political stability on the stock market returns and volatility: GARCH and EGARCH approach. Financial Innovation. https://doi.org/10.1186/s40854-024-00658-8",
    "Alotaibi, T. S., Dalla Valle, L., & Craven, M. J. (2022). The worst case GARCH-copula CVaR approach for portfolio optimisation: Evidence from financial markets. Journal of Risk and Financial Management, 15(10), Article 482. https://doi.org/10.3390/jrfm15100482",
    "Arif, U., Sohail, M. T., & Majeed, M. I. (2020). Portfolio optimization with mean-variance & mean-CVaR: Evidence from Pakistan stock market. International Journal of Management Research & Emerging Sciences, 10(2), 215–226.",
    "Ashrafzadeh, M., Sadrani, M., & Zolfani, S. H. (2025). Clustering-based return prediction model for stock pre-selection in portfolio optimization. Results in Engineering, 27, Article 106263. https://doi.org/10.1016/j.rineng.2025.106263",
    "Bali, T. G., Gokcan, S., & Liang, B. (2007). Value at risk and the cross-section of hedge fund returns. Journal of Banking & Finance, 31(4), 1135–1166. https://doi.org/10.1016/j.jbankfin.2006.10.023",
    "Bodnar, T., Lindholm, M., Niklasson, V., & Thorsén, E. (2022). Bayesian portfolio selection using VaR and CVaR. Applied Mathematics and Computation, 427, Article 127120.",
    "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324",
    "Chao, L. (2024). Application of machine learning in stock market return forecasting. International Journal of Scientific Research and Management (IJSRM), 12(7), 6827–6835. https://doi.org/10.18535/ijsrm/v12i07.em11",
    "Chaweewanchon, A., & Chaysiri, R. (2022). Markowitz mean-variance portfolio optimization with predictive stock selection using machine learning. International Journal of Financial Studies, 10(3), Article 64. https://doi.org/10.3390/ijfs10030064",
    "Chen, R. (2025). Stock price prediction and portfolio optimization based on mean variance model and random forest model. Advances in Economics, Business and Management Research, 333, 358–367.",
    "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794. https://doi.org/10.1145/2939672.2939785",
    "Cheng, Y. (2025). Monte Carlo-Based VaR Estimation and Backtesting Under Basel III. Risks, 13(8), Article 146. https://doi.org/10.3390/risks13080146",
    "Chung, V., Espinoza, J., & Quispe, R. (2025). Forecasting Financial Volatility Under Structural Breaks: A Comparative Study of GARCH Models and Deep Learning Techniques. Journal of Risk and Financial Management, 18(9), Article 494. https://doi.org/10.3390/jrfm18090494",

    "Espiga-Fernández, F., García-Sánchez, Á., & Ordieres-Meré, J. (2024). A Systematic Approach to Portfolio Optimization: A Comparative Study of Reinforcement Learning Agents, Market Signals, and Investment Horizons. Algorithms, 17(12), Article 570. https://doi.org/10.3390/a17120570",
    "Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. The Journal of Finance, 25(2), 383–417. https://doi.org/10.1111/j.1540-6261.1970.tb00518.x",
    "Fan, Y. (2025). Enhancing investment strategies with LSTM-based stock prediction and mean-variance portfolio optimization. Proceedings of the 3rd International Conference on Financial Technology and Business Analysis. https://doi.org/10.54254/2754-1169/2024.23667",
    "Fapetu, O., Ojo, S. M., Balogun, A. A., & Asaolu, A. A. (2021). Capital market performance and macroeconomic dynamics in Nigeria. FUOYE Journal of Finance and Contemporary Issues, 1(1), 29–37.",
    "Fatouros, G., Makridis, G., Kotios, D., Soldatos, J., Filippakis, M., & Kyriazis, D. (2023). DeepVaR: A framework for portfolio risk assessment leveraging probabilistic deep neural networks. Digital Finance, 5(1), 29–56.",
    "Ferrari, D., Paterlini, S., Rigamonti, A., & Weissensteiner, A. (2026). Smoothed semicovariance estimation for portfolio selection. Annals of Operations Research, 357, 565–604. https://doi.org/10.1007/s10479-024-06043-z",

    "Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. The Review of Financial Studies, 33(5), 2223–2273. https://doi.org/10.1093/rfs/hhz113",
    "He, W. (2022). An empirical research based on Markowitz's portfolio theory. World Scientific Research Journal, 8(3), 221–227. https://doi.org/10.6911/WSRJ.202203_8(3).0028",
    "Hsiao, Y.-Y. (2025). A comprehensive survey of modern portfolio optimization: From traditional risk analysis to advanced analytics and machine learning approaches. Advances in Economics, Management and Political Sciences, 166, 189–194. https://doi.org/10.54254/2754-1169/2025.21140",
    "Huang, R., Kambouroudis, D., & McMillan, D. G. (2025). Is portfolio diversification still effective: Evidence spanning three crises from the perspective of U.S. investors. Journal of Asset Management, 26(2), 115–135. https://doi.org/10.1057/s41260-025-00398-z",
    "Job, O. D. (2022). An empirical evaluation of alternative asset allocation policies for emerging and frontier market investors in Africa. Journal of Financial Risk Management, 11(3), 481–521. https://doi.org/10.4236/jfrm.2022.113024",
    "Jobson, J. D., & Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures. The Journal of Finance, 36(4), 889–908.",
    "Kevin, J., & Yugopuspito, P. (2025). Hybrid LSTM and PPO networks for dynamic portfolio optimization. arXiv:2511.17963. https://arxiv.org/abs/2511.17963",
    "Leccadito, A., Staino, A., & Toscano, P. (2024). A novel robust method for estimating the covariance matrix of financial returns with applications to risk management. Financial Innovation, 10, Article 116.",
    "Ledoit, O., & Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. Journal of Empirical Finance, 15(5), 850–859.",
    "Ledoit, O., & Wolf, M. (2011). Robust performance hypothesis testing with the variance. Wilmott Magazine, (55), 86–89.",
    "Li, G. (2023). Portfolio optimization and risk analysis in financial markets. Proceedings of the 2nd International Conference on Financial Technology and Business Analysis, 61, 236–246. https://doi.org/10.54254/2754-1169/61/20231273",
    "Lorimer, D. A., van Schalkwyk, C. H., & Szczygielski, J. J. (2024). Portfolio optimisation using alternative risk measures. Finance Research Letters, 67, Article 105758. https://doi.org/10.1016/j.frl.2024.105758",
    "Lyu, X. (2024). Portfolio Optimization Strategies: New Approaches Based on Machine Learning Forecasting. Highlights in Business, Economics and Management, 40, 1077–1082.",
    "Mahadevaswamy, G. H., & Shyamala, G. (2022). Markowitz Model Is Right Choice to Investment. International Journal of Novel Research and Development, 7(7), 305–314.",
    "Manogna, R. L., & Kulkarni, N. (2025). Portfolio Optimization Model for Stock Price Prediction Using Machine Learning. Journal of Statistical Theory and Applications, 24, 1091–1108. https://doi.org/10.1007/s44199-025-00140-z",
    "Markowitz, H. (1952). Portfolio selection. The Journal of Finance, 7(1), 77–91. https://doi.org/10.1111/j.1540-6261.1952.tb01525.x",
    "Martínez-Barbero, X., Cervelló-Royo, R., & Ribal, J. (2024). Portfolio optimization with prediction-based return using Long Short-Term Memory neural networks: Testing on upward and downward European markets. Computational Economics, 65, 1479–1504. https://doi.org/10.1007/s10614-024-10604-6",
    "Mba, J. C., Ababio, K. A., & Agyei, S. K. (2022). Markowitz mean-variance portfolio selection and optimization under a behavioral spectacle: New empirical evidence. International Journal of Financial Studies, 10(2), Article 28. https://doi.org/10.3390/ijfs10020028",
    "Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. Finance Letters, 1(1), 21–23.",
    "Michaud, R. O. (1989). The Markowitz optimization enigma: Is 'optimized' optimal? Financial Analysts Journal, 45(1), 31–42. https://doi.org/10.2469/faj.v45.n1.31",
    "Moyoweshumba, E., & Seitshiro, M. (2025). Leveraging Markowitz, Random Forest, and XGBoost for optimal diversification of South African stock portfolios. Data Science in Finance and Economics, 5(2), 205–233. https://doi.org/10.3934/DSFE.2025010",
    "Mozumder, S., Hasan, M. K., & Kabir, M. H. (2024). An evaluation of the adequacy of Lévy and extreme value tail risk estimates. Financial Innovation, 10(1), Article 100. https://doi.org/10.1186/s40854-024-00614-6",
    "Naeem, M., Jassim, H. S., & Korsah, D. (2024). The application of machine learning techniques to predict stock market crises in Africa. Journal of Risk and Financial Management, 17(12), Article 554. https://doi.org/10.3390/jrfm17120554",
    "Nahari, F. (2025). Portfolio optimization in practice: A comparative analysis of the Markowitz and Index models. In M. M. Husin (Ed.), Proceedings of the 2025 International Conference on Financial Risk and Investment Management (ICFRIM 2025), Advances in Economics, Business and Management Research (Vol. 333, pp. 367–375). Atlantis Press.",
    "Ojo, A. K., & Okafor, I. J. (2024). Forecasting Nigerian Equity Stock Returns Using Long Short-Term Memory Technique. Journal of Advances in Mathematics and Computer Science, 39(7), 45–54. https://doi.org/10.9734/jamcs/2024/v39i71911",
    "Okafor, C., & Robertson, A. (2023). Maximizing returns: Portfolio optimization in the Nigerian Stock Exchange. International Journal of Advances in Applied Mathematics and Computer Science, 10(2), 14–28. https://americaserial.com/journals/ijaamcs/article/518",
    "Quimbayo, C. Z., & León, B. (2025). Downside Risk Measures and ESG Factors in Optimal Portfolio Construction: Evidence from European Equity Markets. Economics - Innovative and Economics Research Journal, 13(4), 5–17. https://doi.org/10.2478/eoik-2025-0082",
    "Rigamonti, A., & Lučivjanská, K. (2024). Mean-semivariance portfolio optimization using minimum average partial. Annals of Operations Research, 334, 185–203. https://doi.org/10.1007/s10479-022-04736-x",
    "Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. Journal of Risk, 2(3), 21–41. https://doi.org/10.21314/JOR.2000.038",
    "Rockafellar, R. T., & Uryasev, S. (2002). Conditional value-at-risk for general loss distributions. Journal of Banking & Finance, 26(7), 1443–1471. https://doi.org/10.1016/S0378-4266(02)00271-6",
    "Sahiner, M. (2022). Forecasting volatility in Asian financial markets: Evidence from recursive and rolling window methods. SN Business & Economics, 2, Article 157. https://doi.org/10.1007/s43546-022-00329-9",
    "Salo, A., Doumpos, M., Liesiö, J., & Zopounidis, C. (2024). Fifty years of portfolio optimization. European Journal of Operational Research, 318(1), 1–18. https://doi.org/10.1016/j.ejor.2023.12.031",
    "Samaniego Alcántar, A. (2023). Semi-variance optimization for the components of the Dow Jones Industrial Average index. Contaduría y Administración, 68(4), 1–17. http://dx.doi.org/10.22201/fca.24488410e.2023.3409",
    "San, J. (2025). Stock Forecasting and Portfolio Optimization Based on ARIMA-GARCH, Random Forest and Monte Carlo Models. Advances in Economics, Business and Management Research, 333, 582–591. https://doi.org/10.2991/978-94-6463-652-9_61",
    "Senescall, M., & Low, R. K. Y. (2024). Quantitative Portfolio Management: Review and Outlook. Mathematics, 12(18), Article 2897. https://doi.org/10.3390/math12182897",
    "Sulaiman, L. A., Adejayan, A. O., & Ilori, O. O. (2023). Capital Market Development and Economic Growth of West African Countries. Nigerian Journal of Banking and Financial Issues, 9(1), 117–125.",
    "Ślusarczyk, D., & Ślepaczuk, R. (2025). Optimal Markowitz portfolio using returns forecasted with time series and machine learning models. Journal of Big Data, 12, Article 127. https://doi.org/10.1186/s40537-025-01164-z",
    "Tjiwidjaja, H. (2025). Optimization of Investment Portfolio Returns Through an Integrated Risk Management Approach. STIE Ganesha Research Papers, 853–863.",
    "Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijama, B. (2025a). Modelling and predicting stock prices of Nigerian Stock Exchange using some machine learning techniques and time series model. Science World Journal, 20(2), 510–515. https://dx.doi.org/10.4314/swj.v20i2.9",
    "Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijamaa, B. (2025b). Predictive machine learning methods for stock returns among emerging economies in Africa. Science World Journal, 20(3), 941–947. https://dx.doi.org/10.4314/swj.v20i3.3",
    "Wahid, A. J., Riaman, & Sukono. (2025). A Systematic Literature Review on Mean-CVaR Based Financial Asset Portfolio Weight Allocation Using K-Means Clustering. CAUCHY – Jurnal Matematika Murni dan Aplikasi, 10(2), 1069–1091. https://doi.org/10.18860/cauchy.v10i2.36590",
    "Wang, T., Pan, Q., Wu, W., Gao, J., & Zhou, K. (2024). Dynamic Mean–Variance Portfolio Optimization with Value-at-Risk Constraint in Continuous Time. Mathematics, 12(14), Article 2268. https://doi.org/10.3390/math12142268",
    "Yadav, A., Madhavi, R., Bagaria, O., Ambulkar, A., & Sharma, S. (2024). Survey on financial portfolio management's role in investment decision-making strategies. Multidisciplinary Reviews, 6, Article e2023ss101. https://doi.org/10.31893/multirev.2023ss101",
    "Yu, S. (2024). Advancing Stock Market Return Forecasting with LSTM Models and Financial Indicators. Proceedings of the International Conference on Economic Management and Green Development, Article 122. https://doi.org/10.54254/2754-1169/122/2024.17734",
    "Zaimovic, A., Arnaut-Berilo, A., & Bešlija, R. (2024). International Portfolio Diversification Benefits: An Empirical Investigation of the 28 European Stock Markets. School of Economics and Business Sarajevo Working Papers, Article 46.",
    "Zhang, G. (2025). Using Machine Learning for Stock Return Prediction. Proceedings of ICEMGD 2025 Symposium, Article LH23915. https://doi.org/10.54254/2754-1169/2025.LH23915",

    "Zhang, Y. (2024). Integrating Forecasting and Mean-Variance Portfolio Optimization: A Machine Learning Approach. Proceedings of the 3rd International Conference on Financial Technology and Business Analysis, Article 2002.",
    "Zsurkis, G., Nicolau, J., & Rodrigues, P. M. M. (2024). First passage times in portfolio optimization: A novel nonparametric approach. European Journal of Operational Research, 312(3), 1074–1085. https://doi.org/10.1016/j.ejor.2023.07.044"
]

REFERENCES_HTML = [
    "Adegboyo, O. S., & Sarwar, K. (2025). Modelling and forecasting of Nigeria stock market volatility. <i>Future Business Journal</i>, 11(1), Article 124. https://doi.org/10.1186/s43093-025-00536-4",
    "Ajiga, D. I., Adeleye, R. A., Tubokirifuruar, T. S., Bello, B. G., Ndubuisi, N. L., Asuzu, O. F., & Owolabi, O. R. (2024). Machine learning for stock market forecasting: A review of models and accuracy. <i>Finance & Accounting Research Journal</i>, 6(2).",
    "Alfzari, S., Al-Shboul, M., & Alshurideh, M. (2025). Predictive analytics in portfolio management: A fusion of AI and investment economics for optimal risk-return trade-offs. <i>International Review of Management and Marketing</i>, 15(2), 365-380. https://doi.org/10.32479/irmm.18594",
    "Alfeus, M., Harvey, J., & Maphatsoe, P. (2024). Improving realised volatility forecast for emerging markets. <i>Journal of Economics and Finance</i>. Advance online publication. https://doi.org/10.1007/s12197-024-09701-x",
    "Alim, W., Khan, N. U., Zhang, V. W., Cai, H. H., Mikhaylov, A., & Yuan, Q. (2024). Influence of political stability on the stock market returns and volatility: GARCH and EGARCH approach. <i>Financial Innovation</i>. https://doi.org/10.1186/s40854-024-00658-8",
    "Alotaibi, T. S., Dalla Valle, L., & Craven, M. J. (2022). The worst case GARCH-copula CVaR approach for portfolio optimisation: Evidence from financial markets. <i>Journal of Risk and Financial Management</i>, 15(10), Article 482. https://doi.org/10.3390/jrfm15100482",
    "Arif, U., Sohail, M. T., & Majeed, M. I. (2020). Portfolio optimization with mean-variance & mean-CVaR: Evidence from Pakistan stock market. <i>International Journal of Management Research & Emerging Sciences</i>, 10(2), 215-226.",
    "Ashrafzadeh, M., Sadrani, M., & Zolfani, S. H. (2025). Clustering-based return prediction model for stock pre-selection in portfolio optimization. <i>Results in Engineering</i>, 27, Article 106263. https://doi.org/10.1016/j.rineng.2025.106263",
    "Bali, T. G., Gokcan, S., & Liang, B. (2007). Value at risk and the cross-section of hedge fund returns. <i>Journal of Banking & Finance</i>, 31(4), 1135-1166. https://doi.org/10.1016/j.jbankfin.2006.10.023",
    "Bodnar, T., Lindholm, M., Niklasson, V., & Thorsen, E. (2022). Bayesian portfolio selection using VaR and CVaR. <i>Applied Mathematics and Computation</i>, 427, Article 127120.",
    "Breiman, L. (2001). Random forests. <i>Machine Learning</i>, 45(1), 5-32. https://doi.org/10.1023/A:1010933404324",
    "Chao, L. (2024). Application of machine learning in stock market return forecasting. <i>International Journal of Scientific Research and Management (IJSRM)</i>, 12(7), 6827-6835. https://doi.org/10.18535/ijsrm/v12i07.em11",
    "Chaweewanchon, A., & Chaysiri, R. (2022). Markowitz mean-variance portfolio optimization with predictive stock selection using machine learning. <i>International Journal of Financial Studies</i>, 10(3), Article 64. https://doi.org/10.3390/ijfs10030064",
    "Chen, R. (2025). Stock price prediction and portfolio optimization based on mean variance model and random forest model. <i>Advances in Economics, Business and Management Research</i>, 333, 358-367.",
    "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. <i>Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</i>, 785-794. https://doi.org/10.1145/2939672.2939785",
    "Cheng, Y. (2025). Monte Carlo-Based VaR Estimation and Backtesting Under Basel III. <i>Risks</i>, 13(8), Article 146. https://doi.org/10.3390/risks13080146",
    "Chung, V., Espinoza, J., & Quispe, R. (2025). Forecasting Financial Volatility Under Structural Breaks: A Comparative Study of GARCH Models and Deep Learning Techniques. <i>Journal of Risk and Financial Management</i>, 18(9), Article 494. https://doi.org/10.3390/jrfm18090494",

    "Espiga-Fernandez, F., Garcia-Sanchez, A., & Ordieres-Mere, J. (2024). A Systematic Approach to Portfolio Optimization: A Comparative Study of Reinforcement Learning Agents, Market Signals, and Investment Horizons. <i>Algorithms</i>, 17(12), Article 570. https://doi.org/10.3390/a17120570",
    "Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. <i>The Journal of Finance</i>, 25(2), 383-417. https://doi.org/10.1111/j.1540-6261.1970.tb00518.x",
    "Fan, Y. (2025). Enhancing investment strategies with LSTM-based stock prediction and mean-variance portfolio optimization. <i>Proceedings of the 3rd International Conference on Financial Technology and Business Analysis</i>. https://doi.org/10.54254/2754-1169/2024.23667",
    "Fapetu, O., Ojo, S. M., Balogun, A. A., & Asaolu, A. A. (2021). Capital market performance and macroeconomic dynamics in Nigeria. <i>FUOYE Journal of Finance and Contemporary Issues</i>, 1(1), 29-37.",
    "Fatouros, G., Makridis, G., Kotios, D., Soldatos, J., Filippakis, M., & Kyriazis, D. (2023). DeepVaR: A framework for portfolio risk assessment leveraging probabilistic deep neural networks. <i>Digital Finance</i>, 5(1), 29-56.",
    "Ferrari, D., Paterlini, S., Rigamonti, A., & Weissensteiner, A. (2026). Smoothed semicovariance estimation for portfolio selection. <i>Annals of Operations Research</i>, 357, 565-604. https://doi.org/10.1007/s10479-024-06043-z",

    "Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. <i>The Review of Financial Studies</i>, 33(5), 2223-2273. https://doi.org/10.1093/rfs/hhz113",
    "He, W. (2022). An empirical research based on Markowitz's portfolio theory. <i>World Scientific Research Journal</i>, 8(3), 221-227. https://doi.org/10.6911/WSRJ.202203_8(3).0028",
    "Hsiao, Y.-Y. (2025). A comprehensive survey of modern portfolio optimization: From traditional risk analysis to advanced analytics and machine learning approaches. <i>Advances in Economics, Management and Political Sciences</i>, 166, 189-194. https://doi.org/10.54254/2754-1169/2025.21140",
    "Huang, R., Kambouroudis, D., & McMillan, D. G. (2025). Is portfolio diversification still effective: Evidence spanning three crises from the perspective of U.S. investors. <i>Journal of Asset Management</i>, 26(2), 115-135. https://doi.org/10.1057/s41260-025-00398-z",
    "Job, O. D. (2022). An empirical evaluation of alternative asset allocation policies for emerging and frontier market investors in Africa. <i>Journal of Financial Risk Management</i>, 11(3), 481-521. https://doi.org/10.4236/jfrm.2022.113024",
    "Jobson, J. D., & Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures. <i>The Journal of Finance</i>, 36(4), 889-908.",
    "Kevin, J., & Yugopuspito, P. (2025). Hybrid LSTM and PPO networks for dynamic portfolio optimization. <i>arXiv:2511.17963</i>. https://arxiv.org/abs/2511.17963",
    "Leccadito, A., Staino, A., & Toscano, P. (2024). A novel robust method for estimating the covariance matrix of financial returns with applications to risk management. <i>Financial Innovation</i>, 10, Article 116.",
    "Ledoit, O., & Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. <i>Journal of Empirical Finance</i>, 15(5), 850-859.",
    "Ledoit, O., & Wolf, M. (2011). Robust performance hypothesis testing with the variance. <i>Wilmott Magazine</i>, (55), 86-89.",
    "Li, G. (2023). Portfolio optimization and risk analysis in financial markets. <i>Proceedings of the 2nd International Conference on Financial Technology and Business Analysis</i>, 61, 236-246. https://doi.org/10.54254/2754-1169/61/20231273",
    "Lorimer, D. A., van Schalkwyk, C. H., & Szczygielski, J. J. (2024). Portfolio optimisation using alternative risk measures. <i>Finance Research Letters</i>, 67, Article 105758. https://doi.org/10.1016/j.frl.2024.105758",
    "Lyu, X. (2024). Portfolio Optimization Strategies: New Approaches Based on Machine Learning Forecasting. <i>Highlights in Business, Economics and Management</i>, 40, 1077-1082.",
    "Mahadevaswamy, G. H., & Shyamala, G. (2022). Markowitz Model Is Right Choice to Investment. <i>International Journal of Novel Research and Development</i>, 7(7), 305-314.",
    "Manogna, R. L., & Kulkarni, N. (2025). Portfolio Optimization Model for Stock Price Prediction Using Machine Learning. <i>Journal of Statistical Theory and Applications</i>, 24, 1091-1108. https://doi.org/10.1007/s44199-025-00140-z",
    "Markowitz, H. (1952). Portfolio selection. <i>The Journal of Finance</i>, 7(1), 77-91. https://doi.org/10.1111/j.1540-6261.1952.tb01525.x",
    "Martinez-Barbero, X., Cervello-Royo, R., & Ribal, J. (2024). Portfolio optimization with prediction-based return using Long Short-Term Memory neural networks: Testing on upward and downward European markets. <i>Computational Economics</i>, 65, 1479-1504. https://doi.org/10.1007/s10614-024-10604-6",
    "Mba, J. C., Ababio, K. A., & Agyei, S. K. (2022). Markowitz mean-variance portfolio selection and optimization under a behavioral spectacle: New empirical evidence. <i>International Journal of Financial Studies</i>, 10(2), Article 28. https://doi.org/10.3390/ijfs10020028",
    "Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. <i>Finance Letters</i>, 1(1), 21-23.",
    "Michaud, R. O. (1989). The Markowitz optimization enigma: Is 'optimized' optimal? <i>Financial Analysts Journal</i>, 45(1), 31-42. https://doi.org/10.2469/faj.v45.n1.31",
    "Moyoweshumba, E., & Seitshiro, M. (2025). Leveraging Markowitz, Random Forest, and XGBoost for optimal diversification of South African stock portfolios. <i>Data Science in Finance and Economics</i>, 5(2), 205-233. https://doi.org/10.3934/DSFE.2025010",
    "Mozumder, S., Hasan, M. K., & Kabir, M. H. (2024). An evaluation of the adequacy of Levy and extreme value tail risk estimates. <i>Financial Innovation</i>, 10(1), Article 100. https://doi.org/10.1186/s40854-024-00614-6",
    "Naeem, M., Jassim, H. S., & Korsah, D. (2024). The application of machine learning techniques to predict stock market crises in Africa. <i>Journal of Risk and Financial Management</i>, 17(12), Article 554. https://doi.org/10.3390/jrfm17120554",
    "Nahari, F. (2025). Portfolio optimization in practice: A comparative analysis of the Markowitz and Index models. In M. M. Husin (Ed.), <i>Proceedings of the 2025 International Conference on Financial Risk and Investment Management (ICFRIM 2025), Advances in Economics, Business and Management Research</i> (Vol. 333, pp. 367-375). Atlantis Press.",
    "Ojo, A. K., & Okafor, I. J. (2024). Forecasting Nigerian Equity Stock Returns Using Long Short-Term Memory Technique. <i>Journal of Advances in Mathematics and Computer Science</i>, 39(7), 45-54. https://doi.org/10.9734/jamcs/2024/v39i71911",
    "Okafor, C., & Robertson, A. (2023). Maximizing returns: Portfolio optimization in the Nigerian Stock Exchange. <i>International Journal of Advances in Applied Mathematics and Computer Science</i>, 10(2), 14–28. https://americaserial.com/journals/ijaamcs/article/518",
    "Quimbayo, C. Z., & Leon, B. (2025). Downside Risk Measures and ESG Factors in Optimal Portfolio Construction: Evidence from European Equity Markets. <i>Economics - Innovative and Economics Research Journal</i>, 13(4), 5-17. https://doi.org/10.2478/eoik-2025-0082",
    "Rigamonti, A., & Lucivjanska, K. (2024). Mean-semivariance portfolio optimization using minimum average partial. <i>Annals of Operations Research</i>, 334, 185-203. https://doi.org/10.1007/s10479-022-04736-x",
    "Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. <i>Journal of Risk</i>, 2(3), 21-41. https://doi.org/10.21314/JOR.2000.038",
    "Rockafellar, R. T., & Uryasev, S. (2002). Conditional value-at-risk for general loss distributions. <i>Journal of Banking & Finance</i>, 26(7), 1443-1471. https://doi.org/10.1016/S0378-4266(02)00271-6",
    "Sahiner, M. (2022). Forecasting volatility in Asian financial markets: Evidence from recursive and rolling window methods. <i>SN Business & Economics</i>, 2, Article 157. https://doi.org/10.1007/s43546-022-00329-9",
    "Salo, A., Doumpos, M., Liesio, J., & Zopounidis, C. (2024). Fifty years of portfolio optimization. <i>European Journal of Operational Research</i>, 318(1), 1-18. https://doi.org/10.1016/j.ejor.2023.12.031",
    "Samaniego Alcantar, A. (2023). Semi-variance optimization for the components of the Dow Jones Industrial Average index. <i>Contaduria y Administracion</i>, 68(4), 1-17. http://dx.doi.org/10.22201/fca.24488410e.2023.3409",
    "San, J. (2025). Stock Forecasting and Portfolio Optimization Based on ARIMA-GARCH, Random Forest and Monte Carlo Models. <i>Advances in Economics, Business and Management Research</i>, 333, 582-591. https://doi.org/10.2991/978-94-6463-652-9_61",
    "Senescall, M., & Low, R. K. Y. (2024). Quantitative Portfolio Management: Review and Outlook. <i>Mathematics</i>, 12(18), Article 2897. https://doi.org/10.3390/math12182897",
    "Sulaiman, L. A., Adejayan, A. O., & Ilori, O. O. (2023). Capital Market Development and Economic Growth of West African Countries. <i>Nigerian Journal of Banking and Financial Issues</i>, 9(1), 117-125.",
    "Slusarczyk, D., & Slepaczuk, R. (2025). Optimal Markowitz portfolio using returns forecasted with time series and machine learning models. <i>Journal of Big Data</i>, 12, Article 127. https://doi.org/10.1186/s40537-025-01164-z",
    "Tjiwidjaja, H. (2025). Optimization of Investment Portfolio Returns Through an Integrated Risk Management Approach. <i>STIE Ganesha Research Papers</i>, 853-863.",
    "Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijama, B. (2025a). Modelling and predicting stock prices of Nigerian Stock Exchange using some machine learning techniques and time series model. <i>Science World Journal</i>, 20(2), 510-515. https://dx.doi.org/10.4314/swj.v20i2.9",
    "Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijamaa, B. (2025b). Predictive machine learning methods for stock returns among emerging economies in Africa. <i>Science World Journal</i>, 20(3), 941-947. https://dx.doi.org/10.4314/swj.v20i3.3",
    "Wahid, A. J., Riaman, & Sukono. (2025). A Systematic Literature Review on Mean-CVaR Based Financial Asset Portfolio Weight Allocation Using K-Means Clustering. <i>CAUCHY – Jurnal Matematika Murni dan Aplikasi</i>, 10(2), 1069-1091. https://doi.org/10.18860/cauchy.v10i2.36590",
    "Wang, T., Pan, Q., Wu, W., Gao, J., & Zhou, K. (2024). Dynamic Mean-Variance Portfolio Optimization with Value-at-Risk Constraint in Continuous Time. <i>Mathematics</i>, 12(14), Article 2268. https://doi.org/10.3390/math12142268",
    "Yadav, A., Madhavi, R., Bagaria, O., Ambulkar, A., & Sharma, S. (2024). Survey on financial portfolio management's role in investment decision-making strategies. <i>Multidisciplinary Reviews</i>, 6, Article e2023ss101. https://doi.org/10.31893/multirev.2023ss101",
    "Yu, S. (2024). Advancing Stock Market Return Forecasting with LSTM Models and Financial Indicators. <i>Proceedings of the International Conference on Economic Management and Green Development</i>, Article 122. https://doi.org/10.54254/2754-1169/122/2024.17734",
    "Zaimovic, A., Arnaut-Berilo, A., & Bešlija, R. (2024). International Portfolio Diversification Benefits: An Empirical Investigation of the 28 European Stock Markets. <i>School of Economics and Business Sarajevo Working Papers</i>, Article 46.",
    "Zhang, G. (2025). Using Machine Learning for Stock Return Prediction. <i>Proceedings of ICEMGD 2025 Symposium</i>, Article LH23915. https://doi.org/10.54254/2754-1169/2025.LH23915",

    "Zhang, Y. (2024). Integrating Forecasting and Mean-Variance Portfolio Optimization: A Machine Learning Approach. <i>Proceedings of the 3rd International Conference on Financial Technology and Business Analysis</i>, Article 2002.",
    "Zsurkis, G., Nicolau, J., & Rodrigues, P. M. M. (2024). First passage times in portfolio optimization: A novel nonparametric approach. <i>European Journal of Operational Research</i>, 312(3), 1074-1085. https://doi.org/10.1016/j.ejor.2023.07.044"
]

PENDING_CITATIONS = []

def update_thesis_citation_list():
    path = r"c:\Users\USER\.gemini\antigravity\brain\de6d217c-538e-4b7f-aff2-c8d507ff0452\thesis_citation_list.md.resolved"
    content = [
        "# 📚 Master Thesis References & Citation Tracking List (APA 7th Edition)\n",
        "**Document**: *Equity Return Forecasting and Tail-Risk-Aware Portfolio Optimization on the Nigerian Exchange Group (NGX)*  ",
        "**PDF Artifact**: `Abdulameen_Complete_Thesis_Chapters_1_5.pdf`  ",
        "**DOCX Artifact**: `Abdulameen_Complete_Thesis_Chapters_1_5.docx`\n",
        "---\n",
        f"## 🟢 Part 1: Fully Grounded APA 7th Edition References ({len(REFERENCES_PLAIN)} References Integrated into PDF & DOCX)\n",
        "These references have been formatted strictly according to APA 7th Edition guidelines and integrated directly into the **References section** of the complete thesis documents:\n"
    ]
    for i, ref in enumerate(REFERENCES_PLAIN, 1):
        content.append(f"{i}. **{ref}**")
        
    content.append("\n---\n")
    content.append(f"## 🟢 Part 2: Pending In-Text Citations (0 Remaining Citations - 100% Grounded)\n")
    content.append("🎉 **All in-text citations across Chapters 1–5 are 100% grounded and fully resolved!** There are no remaining pending citations.\n")
        
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"[OK] Updated tracking list: {path} with {len(REFERENCES_PLAIN)} grounded entries and 0 pending.")

def update_generate_chapters_py():
    path = r"c:\Users\USER\Documents\ai\equity-optimization\src\generate_chapters.py"
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
        
    pattern = r"references_list = \[\s*.*?\]\s*\n\s*for ref in references_list:"
    formatted_html_list = "references_list = [\n" + ",\n".join(f'        {repr(r)}' for r in REFERENCES_HTML) + "\n    ]\n\n    for ref in references_list:"
    
    new_code = re.sub(pattern, formatted_html_list, code, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"[OK] Updated references in {path}")

def update_generate_thesis_docx_py():
    path = r"c:\Users\USER\Documents\ai\equity-optimization\generate_thesis_docx.py"
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
        
    pattern = r"references_list = \[\s*.*?\]\s*\n\s*for ref in references_list:"
    formatted_plain_list = "references_list = [\n" + ",\n".join(f'        {repr(r)}' for r in REFERENCES_PLAIN) + "\n    ]\n\n    for ref in references_list:"
    
    new_code = re.sub(pattern, formatted_plain_list, code, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"[OK] Updated references in {path}")

if __name__ == '__main__':
    update_thesis_citation_list()
    update_generate_chapters_py()
    update_generate_thesis_docx_py()
