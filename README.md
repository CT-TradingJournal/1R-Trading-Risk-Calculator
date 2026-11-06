# 1R Day Trading Risk Calculator & Position Sizer 📊

## 💡 Overview / 專案簡介
In fast-paced day trading (specifically US Equities short selling), executing trades with strict risk management is crucial. Human emotions often lead to over-leveraging or hesitation during market hours. 

I developed this Python-based Risk Calculator to eliminate subjective emotional bias and strictly enforce a **1R (1 Risk) discipline**. By inputting the entry price and hard stop-loss level based on pre-market technical setups (VWAP, 9/20 EMA), this tool instantly calculates the exact maximum position size (number of shares) allowed.

This project transforms a discretionary trading process into a **systematic, rule-based workflow**.

## 🔥 Key Features / 核心功能
* **Automated Position Sizing:** Instantly calculates the precise number of shares to short/buy to ensure the maximum potential loss never exceeds the predefined 1R account threshold.
* **Risk-First Architecture:** Forces the user to define the "Stop Loss" *before* entering a trade, reinforcing strict execution discipline.
* **Streamlined UI:** Executed as a `.pyw` script to run seamlessly as a lightweight desktop tool alongside heavy trading platforms (Charles Schwab / ThinkorSwim).

## 🛠️ Tech Stack / 技術棧
* **Language:** Python 3
* **Deployment:** Standalone `.pyw` script for GUI/background execution on Windows without invoking the command-line console.

## 📈 Why I Built This / 開發動機與業務價值
Before developing this tool, manual position sizing was prone to calculation errors and FOMO (Fear Of Missing Out) during high-volatility market opens. 

By automating this mathematical process, I achieved:
1. **0% manual calculation errors** during active market hours.
2. **100% compliance** with my 90-day strict risk management challenge.
3. Enhanced execution speed, allowing me to focus entirely on order flow and price action reading.

This project demonstrates my ability to identify a real-world operational bottleneck, write programmatic logic to solve it, and deploy an automated tool that strictly enforces business rules.

---
*Created by [CT-TradingJournal] - Continuously building automated tools for disciplined execution.*
