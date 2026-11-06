import math
import tkinter as tk
from tkinter import ttk

class PositionSizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MTJ 戰術算倉器 (If-Then 契約版)")
        self.root.geometry("340x480")
        self.root.configure(bg="#1e1e2e")
        self.root.attributes("-topmost", True)  # 強制視窗永遠置頂
        self.root.resizable(False, False)

        self.calculated_shares = 0
        self.entries = {}
        self._build_ui()

    def _build_ui(self):
        style_lbl = {"bg": "#1e1e2e", "fg": "#cdd6f4", "font": ("Segoe UI", 10)}
        style_ent = {
            "bg": "#313244", "fg": "#ffffff", "insertbackground": "#ffffff",
            "relief": "flat", "font": ("Consolas", 11, "bold")
        }

        # 1. 頂部設定區
        frame_top = tk.Frame(self.root, bg="#1e1e2e")
        frame_top.pack(fill="x", padx=15, pady=(10, 5))

        self.topmost_var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(
            frame_top, text="視窗永遠置頂", var=self.topmost_var,
            command=self._toggle_topmost, bg="#1e1e2e", fg="#a6adc8",
            selectcolor="#313244", activebackground="#1e1e2e", activeforeground="#ffffff"
        )
        chk.grid(row=0, column=0, columnspan=4, sticky="w")

        # 隱藏的基礎參數 (1R, Buffer, Max BP) - 排列緊湊
        tk.Label(frame_top, text="1R($):", **style_lbl).grid(row=1, column=0, sticky="e", pady=4)
        ent_1r = tk.Entry(frame_top, width=6, justify="center", **style_ent)
        ent_1r.insert(0, "25")
        ent_1r.grid(row=1, column=1, padx=4)
        ent_1r.bind("<KeyRelease>", self._calculate)
        self.entries[0] = ent_1r

        tk.Label(frame_top, text="Buffer($):", **style_lbl).grid(row=1, column=2, sticky="e")
        ent_buffer = tk.Entry(frame_top, width=5, justify="center", **style_ent)
        ent_buffer.insert(0, "0.02")
        ent_buffer.grid(row=1, column=3, padx=4)
        ent_buffer.bind("<KeyRelease>", self._calculate)
        self.entries[3] = ent_buffer

        tk.Label(frame_top, text="最大資金上限($):", **style_lbl).grid(row=2, column=0, columnspan=2, sticky="e", pady=4)
        ent_max = tk.Entry(frame_top, width=10, justify="center", **style_ent)
        ent_max.insert(0, "20000")
        ent_max.grid(row=2, column=2, columnspan=2, sticky="w", padx=4)
        ent_max.bind("<KeyRelease>", self._calculate)
        self.entries[4] = ent_max

        # 2. 核心：If-Then 契約區
        frame_contract = tk.Frame(self.root, bg="#181825", bd=1, relief="solid")
        frame_contract.pack(fill="x", padx=15, pady=10)
        
        tk.Label(frame_contract, text="進場前行動契約 (If-Then Protocol)", bg="#181825", fg="#89b4fa", font=("Segoe UI", 11, "bold")).pack(pady=(10, 5))

        # IF 1
        frame_if1 = tk.Frame(frame_contract, bg="#181825")
        frame_if1.pack(fill="x", padx=10, pady=2)
        tk.Label(frame_if1, text="IF 現價觸發進場點 $", bg="#181825", fg="#cdd6f4", font=("Segoe UI", 10)).pack(side="left")
        ent_entry = tk.Entry(frame_if1, width=8, bg="#313244", fg="#a6e3a1", font=("Consolas", 12, "bold"), justify="center", insertbackground="white", relief="flat")
        ent_entry.pack(side="left")
        ent_entry.bind("<KeyRelease>", self._calculate)
        self.entries[1] = ent_entry

        tk.Label(frame_contract, text="THEN 我將毫不猶豫執行掛單，", bg="#181825", fg="#a6adc8", font=("Segoe UI", 10)).pack(anchor="w", padx=10)

        # IF 2
        frame_if2 = tk.Frame(frame_contract, bg="#181825")
        frame_if2.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_if2, text="IF 行情反轉打到止損 $", bg="#181825", fg="#cdd6f4", font=("Segoe UI", 10)).pack(side="left")
        ent_stop = tk.Entry(frame_if2, width=8, bg="#313244", fg="#f38ba8", font=("Consolas", 12, "bold"), justify="center", insertbackground="white", relief="flat")
        ent_stop.pack(side="left")
        ent_stop.bind("<KeyRelease>", self._calculate)
        self.entries[2] = ent_stop

        tk.Label(frame_contract, text="THEN 我將無條件認賠，絕不凹單！", bg="#181825", fg="#a6adc8", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(0, 10))

        # 3. 結果顯示面板
        self.res_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.res_frame.pack(fill="x", padx=15, pady=5)

        self.dir_label = tk.Label(self.res_frame, text="等待完整 If-Then 輸入...", bg="#1e1e2e", fg="#bac2de", font=("Segoe UI", 10, "bold"))
        self.dir_label.pack()

        self.shares_label = tk.Label(self.res_frame, text="-- 股", bg="#1e1e2e", fg="#f9e2af", font=("Consolas", 24, "bold"))
        self.shares_label.pack(pady=2)

        self.detail_label = tk.Label(
            self.res_frame, text="實際止損價: --  |  每股風險: --\n目標 2R: --  |  目標 3R: --",
            bg="#1e1e2e", fg="#a6adc8", font=("Consolas", 9), justify="center"
        )
        self.detail_label.pack()

        # 4. 按鈕列
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.copy_btn = tk.Button(
            btn_frame, text="複製股數", command=self._copy_shares,
            bg="#89b4fa", fg="#11111b", font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2"
        )
        self.copy_btn.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=4)

        clear_btn = tk.Button(
            btn_frame, text="清空重置", command=self._clear_prices,
            bg="#45475a", fg="#ffffff", font=("Segoe UI", 10),
            relief="flat", cursor="hand2"
        )
        clear_btn.pack(side="right", ipady=4, ipadx=8)
        
        self.entries[1].focus_set()

    def _toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    def _calculate(self, event=None):
        try:
            risk_1r = float(self.entries[0].get())
            entry = float(self.entries[1].get())
            raw_stop = float(self.entries[2].get())
            buffer = float(self.entries[3].get() or 0.0)
            max_bp = float(self.entries[4].get() or 0.0)

            if entry <= 0 or raw_stop <= 0 or risk_1r <= 0 or entry == raw_stop:
                raise ValueError

            # 自動判斷做空 (Short) 或做多 (Long)
            if raw_stop > entry:
                direction = "SHORT 做空 (止損設於上方)"
                dir_color = "#f38ba8"
                actual_stop = raw_stop + buffer
                risk_per_share = actual_stop - entry
                target_2r = entry - (2 * risk_per_share)
                target_3r = entry - (3 * risk_per_share)
            else:
                direction = "LONG 做多 (止損設於下方)"
                dir_color = "#a6e3a1"
                actual_stop = raw_stop - buffer
                risk_per_share = entry - actual_stop
                target_2r = entry + (2 * risk_per_share)
                target_3r = entry + (3 * risk_per_share)

            if risk_per_share <= 0:
                raise ValueError

            shares_by_risk = math.floor(risk_1r / risk_per_share)
            shares_by_bp = math.floor(max_bp / entry) if max_bp > 0 else shares_by_risk
            final_shares = max(0, min(shares_by_risk, shares_by_bp))
            self.calculated_shares = final_shares

            cap_note = " (已觸及上限)" if shares_by_bp < shares_by_risk else ""
            self.dir_label.config(text=f"{direction}{cap_note}", fg=dir_color)
            self.shares_label.config(text=f"{final_shares} 股")
            self.detail_label.config(
                text=(
                    f"掛單止損: ${actual_stop:.2f} (每股風險 ${risk_per_share:.2f})\n"
                    f"目標 2R: ${target_2r:.2f}  |  目標 3R: ${target_3r:.2f}"
                )
            )
        except ValueError:
            self.calculated_shares = 0
            self.dir_label.config(text="等待完整 If-Then 輸入...", fg="#bac2de")
            self.shares_label.config(text="-- 股", fg="#f9e2af")
            self.detail_label.config(text="實際止損價: --  |  每股風險: --\n目標 2R: --  |  目標 3R: --")

    def _copy_shares(self):
        if self.calculated_shares > 0:
            self.root.clipboard_clear()
            self.root.clipboard_append(str(self.calculated_shares))
            self.copy_btn.config(text=f"已複製: {self.calculated_shares}", bg="#a6e3a1")
            self.root.after(1000, lambda: self.copy_btn.config(text="複製股數", bg="#89b4fa"))

    def _clear_prices(self):
        self.entries[1].delete(0, tk.END)
        self.entries[2].delete(0, tk.END)
        self.entries[1].focus_set()
        self._calculate()

if __name__ == "__main__":
    root = tk.Tk()
    app = PositionSizerApp(root)
    root.mainloop()