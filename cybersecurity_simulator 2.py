"""
╔══════════════════════════════════════════════════════════════╗
║   CYBERSECURITY AWARENESS SIMULATOR                          ║
║   ⚠  SAFE, OFFLINE EDUCATIONAL DEMONSTRATION ONLY ⚠         ║
║   No real network requests. No real harm. For training only. ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import font as tkfont
import time
import random

# ── Demo credentials ─────────────────────────────────────────────
DEMO_USERNAME = "demo@gmail.com"
DEMO_PASSWORD = "password123"
MAX_ATTEMPTS  = 3

# ── Google colour palette ────────────────────────────────────────
G_WHITE      = "#ffffff"
G_BG         = "#f1f3f4"          # page background
G_CARD       = "#ffffff"
G_BORDER     = "#dadce0"
G_BLUE       = "#1a73e8"          # primary button / accent
G_BLUE_HOV   = "#1557b0"
G_BLUE_LIGHT = "#e8f0fe"
G_TEXT       = "#202124"          # headings
G_MUTED      = "#5f6368"          # helper / sub text
G_RED        = "#d93025"          # error
G_GREEN      = "#188038"
G_YELLOW_TXT = "#f29900"

# Google logo letter colours
G_BLUE_L  = "#4285F4"
G_RED_L   = "#EA4335"
G_YELLOW_L= "#FBBC05"
G_GREEN_L = "#34A853"

# ── Ransomware palette ───────────────────────────────────────────
RANSOMWARE_BG = "#0a0000"
RANSOMWARE_RD = "#cc0000"
TEXT_YELLOW   = "#d29922"
TEXT_ORANGE   = "#e3b341"
TEXT_MUTED_D  = "#8b949e"
BG_DARK       = "#0d1117"
BG_CARD_D     = "#161b22"
BORDER_D      = "#30363d"
TEXT_PRIMARY  = "#e6edf3"
TEXT_RED_D    = "#f85149"
TEXT_GREEN_D  = "#3fb950"
ACCENT_BLUE_D = "#58a6ff"
BTN_GREEN_D   = "#238636"


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sign in - Google Accounts")
        self.geometry("450x640")
        self.resizable(False, False)
        self.configure(bg=G_BG)
        self._center_window(450, 640)

        self.attempts      = 0
        self.locked        = False
        self.countdown_job = None
        self._pass_visible = False

        self._build_fonts()
        self._build_login_ui()

    # ── helpers ──────────────────────────────────────────────────

    def _center_window(self, w, h):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w)//2}+{(sh - h)//2}")

    def _build_fonts(self):
        self.font_google_logo = tkfont.Font(family="Arial",    size=22, weight="bold")
        self.font_title       = tkfont.Font(family="Google Sans" if self._font_exists("Google Sans") else "Segoe UI",
                                            size=24, weight="bold")
        self.font_sub         = tkfont.Font(family="Roboto" if self._font_exists("Roboto") else "Segoe UI",
                                            size=14)
        self.font_label       = tkfont.Font(family="Roboto" if self._font_exists("Roboto") else "Segoe UI",
                                            size=11)
        self.font_btn         = tkfont.Font(family="Google Sans" if self._font_exists("Google Sans") else "Segoe UI",
                                            size=13, weight="bold")
        self.font_link        = tkfont.Font(family="Roboto" if self._font_exists("Roboto") else "Segoe UI",
                                            size=12)
        self.font_hint        = tkfont.Font(family="Segoe UI", size=8)
        self.font_mono_lg     = tkfont.Font(family="Consolas", size=28, weight="bold")
        self.font_mono_sm     = tkfont.Font(family="Consolas", size=9)
        self.font_warn        = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_ransom      = tkfont.Font(family="Consolas", size=30, weight="bold")
        self.font_sub_ransom  = tkfont.Font(family="Segoe UI", size=10)
        self.font_edu_title   = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.font_edu_body    = tkfont.Font(family="Segoe UI", size=10)

    def _font_exists(self, name):
        return name in tkfont.families()

    # ── Google Login UI ──────────────────────────────────────────

    def _build_login_ui(self):
        # ── edu banner (thin, unobtrusive) ──
        banner = tk.Frame(self, bg="#fff3cd", pady=4)
        banner.pack(fill=tk.X)
        tk.Label(banner,
                 text="⚠  EDUCATIONAL DEMO — SAFE & OFFLINE — NOT THE REAL GOOGLE",
                 bg="#fff3cd", fg="#856404",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold")).pack()

        # ── outer centering frame ──
        outer = tk.Frame(self, bg=G_BG)
        outer.pack(expand=True, fill=tk.BOTH)

        # ── white card ──
        card = tk.Frame(outer, bg=G_CARD,
                        highlightbackground=G_BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=560)

        # ── inner padding frame ──
        inner = tk.Frame(card, bg=G_CARD, padx=44, pady=0)
        inner.pack(fill=tk.BOTH, expand=True)

        # ── Google logo ──
        logo_frame = tk.Frame(inner, bg=G_CARD)
        logo_frame.pack(pady=(32, 0))
        self._draw_google_logo(logo_frame)

        # ── "Sign in" heading ──
        tk.Label(inner, text="Sign in", bg=G_CARD, fg=G_TEXT,
                 font=self.font_title).pack(pady=(12, 0))

        # ── sub heading ──
        tk.Label(inner, text="Use your Google Account",
                 bg=G_CARD, fg=G_MUTED,
                 font=self.font_sub).pack(pady=(4, 0))

        # ── email field ──
        self.email_frame, self.entry_user = self._google_entry(
            inner, label="Email or phone")
        self.email_frame.pack(fill=tk.X, pady=(24, 0))

        # ── "Forgot email?" link ──
        forgot_email = tk.Label(inner, text="Forgot email?",
                                bg=G_CARD, fg=G_BLUE,
                                font=self.font_link, cursor="hand2")
        forgot_email.pack(anchor="w", pady=(6, 0))

        # ── password field ──
        self.pass_frame, self.entry_pass = self._google_entry(
            inner, label="Enter your password", secret=True)
        self.pass_frame.pack(fill=tk.X, pady=(14, 0))

        # ── show password toggle ──
        self.show_pass_var = tk.StringVar(value="Show password")
        show_chk = tk.Checkbutton(inner, textvariable=self.show_pass_var,
                                  bg=G_CARD, fg=G_MUTED,
                                  font=self.font_hint,
                                  activebackground=G_CARD,
                                  command=self._toggle_password,
                                  cursor="hand2")
        show_chk.pack(anchor="w", pady=(4, 0))

        # ── attempt indicator ──
        self.attempt_bar_frame = tk.Frame(inner, bg=G_CARD)
        self.attempt_bar_frame.pack(fill=tk.X, pady=(6, 0))
        self._build_attempt_dots()

        # ── status / error message ──
        self.status_var = tk.StringVar(value="")
        self.status_lbl = tk.Label(inner, textvariable=self.status_var,
                                   bg=G_CARD, fg=G_RED,
                                   font=tkfont.Font(family="Segoe UI", size=9),
                                   wraplength=300, justify="left")
        self.status_lbl.pack(anchor="w", pady=(4, 0))

        # ── bottom row: "Create account" + "Next" button ──
        btn_row = tk.Frame(inner, bg=G_CARD)
        btn_row.pack(fill=tk.X, pady=(16, 0))

        create_lbl = tk.Label(btn_row, text="Create account",
                              bg=G_CARD, fg=G_BLUE,
                              font=self.font_link, cursor="hand2")
        create_lbl.pack(side=tk.LEFT)

        self.btn_login = tk.Button(
            btn_row, text="Next",
            bg=G_BLUE, fg=G_WHITE,
            font=self.font_btn, relief="flat", cursor="hand2",
            activebackground=G_BLUE_HOV, activeforeground=G_WHITE,
            padx=24, pady=8,
            command=self._attempt_login
        )
        self.btn_login.pack(side=tk.RIGHT)
        self.entry_pass.bind("<Return>", lambda e: self._attempt_login())
        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus_set())

        # ── demo hint ──
        hint_box = tk.Frame(inner, bg="#e8f0fe", padx=10, pady=6)
        hint_box.pack(fill=tk.X, pady=(18, 0))
        tk.Label(hint_box,
                 text="🎓  Demo hint — enter wrong credentials 3× to trigger the security simulation",
                 bg="#e8f0fe", fg="#1a73e8",
                 font=self.font_hint,
                 wraplength=290, justify="left").pack()

        # ── Google footer ──
        footer = tk.Frame(card, bg=G_CARD)
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 12))
        tk.Frame(footer, bg=G_BORDER, height=1).pack(fill=tk.X, pady=(0, 8))
        footer_links = tk.Frame(footer, bg=G_CARD)
        footer_links.pack()
        for txt in ["Help", "Privacy", "Terms"]:
            tk.Label(footer_links, text=txt,
                     bg=G_CARD, fg=G_MUTED,
                     font=tkfont.Font(family="Segoe UI", size=9),
                     cursor="hand2").pack(side=tk.LEFT, padx=10)

    def _draw_google_logo(self, parent):
        """Draw the Google wordmark in the four brand colours."""
        letters = [("G", G_BLUE_L), ("o", G_RED_L), ("o", G_YELLOW_L),
                   ("g", G_BLUE_L), ("l", G_GREEN_L), ("e", G_RED_L)]
        for ch, colour in letters:
            tk.Label(parent, text=ch, bg=G_CARD, fg=colour,
                     font=self.font_google_logo).pack(side=tk.LEFT)

    def _google_entry(self, parent, label="", secret=False):
        """Material-style outlined text field (Google design)."""
        container = tk.Frame(parent, bg=G_CARD,
                             highlightbackground=G_BORDER,
                             highlightthickness=1)

        # floating label
        lbl = tk.Label(container, text=label, bg=G_WHITE, fg=G_MUTED,
                       font=self.font_label, padx=3)
        lbl.place(x=11, y=10)

        kwargs = dict(
            bg=G_WHITE, fg=G_TEXT,
            insertbackground=G_BLUE,
            relief="flat",
            font=tkfont.Font(family="Segoe UI", size=12),
            bd=0
        )
        if secret:
            kwargs["show"] = "●"

        entry = tk.Entry(container, **kwargs)
        entry.pack(fill=tk.X, padx=12, pady=(22, 8))

        # floating label animation
        def on_focus_in(e):
            lbl.place(x=11, y=-8)
            lbl.config(fg=G_BLUE,
                       font=tkfont.Font(family="Segoe UI", size=9))
            container.config(highlightbackground=G_BLUE, highlightthickness=2)

        def on_focus_out(e):
            if not entry.get():
                lbl.place(x=11, y=10)
                lbl.config(fg=G_MUTED,
                           font=self.font_label)
            container.config(highlightbackground=G_BORDER, highlightthickness=1)

        entry.bind("<FocusIn>",  on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry._lbl = lbl
        entry._container = container

        return container, entry

    def _toggle_password(self):
        if self._pass_visible:
            self.entry_pass.config(show="●")
            self.show_pass_var.set("Show password")
            self._pass_visible = False
        else:
            self.entry_pass.config(show="")
            self.show_pass_var.set("Hide password")
            self._pass_visible = True

    def _build_attempt_dots(self):
        for w in self.attempt_bar_frame.winfo_children():
            w.destroy()
        dot_frame = tk.Frame(self.attempt_bar_frame, bg=G_CARD)
        dot_frame.pack(anchor="w")
        tk.Label(dot_frame, text="Attempts: ",
                 bg=G_CARD, fg=G_MUTED,
                 font=tkfont.Font(family="Segoe UI", size=9)).pack(side=tk.LEFT)
        for i in range(MAX_ATTEMPTS):
            colour = G_RED if i < self.attempts else G_BORDER
            tk.Label(dot_frame, text="●", bg=G_CARD, fg=colour,
                     font=tkfont.Font(size=13)).pack(side=tk.LEFT, padx=2)
        remaining = MAX_ATTEMPTS - self.attempts
        msg = f"  {remaining} attempt(s) left" if remaining > 0 else "  Locked"
        tk.Label(dot_frame, text=msg, bg=G_CARD,
                 fg=G_MUTED if remaining > 0 else G_RED,
                 font=tkfont.Font(family="Segoe UI", size=9)).pack(side=tk.LEFT)

    # ── Login logic ──────────────────────────────────────────────

    def _attempt_login(self):
        if self.locked:
            return

        user = self.entry_user.get().strip()
        pwd  = self.entry_pass.get().strip()

        if user == DEMO_USERNAME and pwd == DEMO_PASSWORD:
            self._show_success()
            return

        # wrong credentials
        self.attempts += 1

        # red border on both fields
        self.email_frame.config(highlightbackground=G_RED, highlightthickness=2)
        self.pass_frame.config(highlightbackground=G_RED, highlightthickness=2)
        self.after(900, lambda: (
            self.email_frame.config(highlightbackground=G_BORDER, highlightthickness=1),
            self.pass_frame.config(highlightbackground=G_BORDER, highlightthickness=1)
        ))

        self._build_attempt_dots()

        if self.attempts >= MAX_ATTEMPTS:
            self.locked = True
            self.btn_login.config(state="disabled", bg="#dadce0", fg=G_MUTED)
            self.status_var.set("⛔  Account locked — too many failed attempts.")
            self.status_lbl.config(fg=G_RED)
            self.after(900, self._launch_ransomware_overlay)
        else:
            self.status_var.set(
                f"Wrong password. Try again or click 'Forgot email?' "
                f"({MAX_ATTEMPTS - self.attempts} attempt(s) left)"
            )
            self.status_lbl.config(fg=G_RED)
            self.entry_pass.delete(0, tk.END)

    def _show_success(self):
        self.status_lbl.config(fg=G_GREEN)
        self.status_var.set("✅  Signed in successfully! Welcome.")
        self.btn_login.config(bg="#188038", state="disabled")

    # ── Ransomware Overlay ───────────────────────────────────────

    def _launch_ransomware_overlay(self):
        overlay = tk.Toplevel(self)
        overlay.title("⚠ EDUCATIONAL SIMULATION")
        overlay.geometry("740x640")
        overlay.resizable(False, False)
        overlay.configure(bg=RANSOMWARE_BG)
        overlay.grab_set()
        overlay.focus_force()
        self.update_idletasks()
        px = self.winfo_rootx()
        py = self.winfo_rooty()
        overlay.geometry(f"740x640+{px - 145}+{py - 10}")
        self._build_ransom_ui(overlay)

    def _build_ransom_ui(self, win):
        # safe badge
        badge = tk.Frame(win, bg="#1a0000", pady=6)
        badge.pack(fill=tk.X)
        tk.Label(badge, text="🎓  SAFE OFFLINE EDUCATIONAL SIMULATION — NO REAL THREAT",
                 bg="#1a0000", fg=TEXT_YELLOW,
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold")).pack()

        # skull
        tk.Label(win, text="☠", bg=RANSOMWARE_BG, fg=RANSOMWARE_RD,
                 font=tkfont.Font(size=60)).pack(pady=(8, 0))

        tk.Label(win, text="YOUR FILES HAVE BEEN ENCRYPTED",
                 bg=RANSOMWARE_BG, fg=RANSOMWARE_RD,
                 font=self.font_ransom).pack()

        tk.Label(win,
                 text="All documents, databases, and backups on this network have been\n"
                      "encrypted with military-grade AES-256 + RSA-2048 encryption.",
                 bg=RANSOMWARE_BG, fg="#ff4444",
                 font=tkfont.Font(family="Segoe UI", size=11),
                 justify="center").pack(pady=(4, 0))

        # countdown
        tk.Label(win, text="Time remaining to pay ransom:",
                 bg=RANSOMWARE_BG, fg=TEXT_MUTED_D,
                 font=self.font_sub_ransom).pack(pady=(12, 0))
        self.countdown_var = tk.StringVar(value="71:59:59")
        tk.Label(win, textvariable=self.countdown_var,
                 bg=RANSOMWARE_BG, fg=RANSOMWARE_RD,
                 font=self.font_mono_lg).pack()
        tk.Label(win,
                 text="After this time expires, the ransom doubles and files are permanently deleted.",
                 bg=RANSOMWARE_BG, fg="#888",
                 font=tkfont.Font(family="Segoe UI", size=9),
                 wraplength=620).pack(pady=(0, 6))

        tk.Frame(win, bg="#330000", height=1).pack(fill=tk.X, padx=30, pady=4)

        # extortion warning
        ext = tk.Frame(win, bg="#120000", padx=20, pady=10)
        ext.pack(fill=tk.X, padx=30)
        tk.Label(ext, text="⚠  DATA EXPOSURE WARNING",
                 bg="#120000", fg=TEXT_ORANGE,
                 font=self.font_warn).pack(anchor="w")
        tk.Label(ext,
                 text=(
                     "• 47 GB of sensitive data has been exfiltrated to our servers.\n"
                     "• This includes: employee PII, financial records, client contracts.\n"
                     "• Failure to pay will result in public release on dark-web leak sites.\n"
                     "• Your Google credentials were obtained via credential stuffing —\n"
                     "  reused passwords from previous breaches enabled initial access."
                 ),
                 bg="#120000", fg="#ff8888",
                 font=tkfont.Font(family="Consolas", size=10),
                 justify="left").pack(anchor="w", pady=(4, 0))

        tk.Frame(win, bg="#330000", height=1).pack(fill=tk.X, padx=30, pady=6)

        # animated file list
        tk.Label(win, text="Sample of encrypted files:",
                 bg=RANSOMWARE_BG, fg=TEXT_MUTED_D,
                 font=tkfont.Font(family="Segoe UI", size=9)).pack(anchor="w", padx=32)
        self.file_var = tk.StringVar()
        tk.Label(win, textvariable=self.file_var,
                 bg=RANSOMWARE_BG, fg="#555",
                 font=self.font_mono_sm).pack(anchor="w", padx=32)
        self._animate_files()

        tk.Frame(win, bg="#330000", height=1).pack(fill=tk.X, padx=30, pady=(8, 4))

        # buttons
        btn_row = tk.Frame(win, bg=RANSOMWARE_BG)
        btn_row.pack(pady=6)
        tk.Button(btn_row,
                  text="📖  What just happened? (Educational Explanation)",
                  bg="#1f1f00", fg=TEXT_YELLOW,
                  font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=lambda: self._show_education(win)).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_row,
                  text="✕  Close Simulation",
                  bg="#1a0000", fg="#888",
                  font=tkfont.Font(family="Segoe UI", size=10),
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=lambda: self._close_overlay(win)).pack(side=tk.LEFT, padx=6)

        self._run_countdown(win, 72 * 3600 - 1)

    # ── countdown ────────────────────────────────────────────────

    def _run_countdown(self, win, seconds_left):
        if not win.winfo_exists():
            return
        h = seconds_left // 3600
        m = (seconds_left % 3600) // 60
        s = seconds_left % 60
        self.countdown_var.set(f"{h:02d}:{m:02d}:{s:02d}")
        if seconds_left > 0:
            self.countdown_job = win.after(
                1000, self._run_countdown, win, seconds_left - 1)

    # ── file animation ───────────────────────────────────────────

    def _animate_files(self):
        exts  = [".docx", ".xlsx", ".pdf", ".db", ".sql", ".bak", ".pst", ".csv"]
        dirs  = ["C:\\Users\\admin\\Documents\\", "D:\\Backup\\",
                 "\\\\FILESERVER01\\shares\\HR\\",
                 "C:\\ProgramData\\", "D:\\Finance\\Q4\\"]
        names = ["payroll_2024", "client_contracts", "passwords", "database_dump",
                 "backup_2024", "employee_data", "financial_report", "source_code"]
        line  = random.choice(dirs) + random.choice(names) + random.choice(exts) + "  →  .LOCKED"
        self.file_var.set(line)
        self.after(600, self._animate_files)

    # ── Educational panel ────────────────────────────────────────

    def _show_education(self, parent):
        edu = tk.Toplevel(parent)
        edu.title("🎓 Educational Explanation")
        edu.geometry("660x580")
        edu.resizable(False, False)
        edu.configure(bg=BG_DARK)
        edu.grab_set()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        edu.geometry(f"660x580+{px + 30}+{py + 20}")

        hdr = tk.Frame(edu, bg="#0d2137", pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🎓  Cybersecurity Awareness — What Just Happened?",
                 bg="#0d2137", fg=ACCENT_BLUE_D,
                 font=tkfont.Font(family="Segoe UI", size=13, weight="bold")).pack()
        tk.Label(hdr, text="Safe, offline educational content. No real systems were harmed.",
                 bg="#0d2137", fg=TEXT_MUTED_D,
                 font=tkfont.Font(family="Segoe UI", size=8)).pack()

        canvas = tk.Canvas(edu, bg=BG_DARK, highlightthickness=0)
        scroll = tk.Scrollbar(edu, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        inner = tk.Frame(canvas, bg=BG_DARK)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        sections = [
            ("1️⃣  Credential Stuffing", TEXT_YELLOW,
             "Credential stuffing is an automated attack where hackers use large lists of "
             "leaked username/password pairs (from previous data breaches) and systematically "
             "try them against other services.\n\n"
             "Real-world impact: Billions of credentials are available on dark-web markets. "
             "Attackers use bots to try thousands per second, exploiting password reuse.\n\n"
             "Defence: Use a unique, strong password for every account. Use a password manager."),

            ("2️⃣  Account Lockout Mechanisms", ACCENT_BLUE_D,
             "Account lockout policies are a core defence against brute-force and credential "
             "stuffing. After a set number of failures (typically 3–10), the account is locked.\n\n"
             "This simulation locked after 3 attempts — consistent with real banking/corporate systems.\n\n"
             "Modern enhancements: progressive delays, CAPTCHA, IP rate-limiting, "
             "device fingerprinting, and MFA which makes stolen passwords largely useless."),

            ("3️⃣  Ransomware Attacks — How They Work", TEXT_RED_D,
             "Ransomware encrypts a victim's files and demands payment for the decryption key.\n\n"
             "  1. Initial Access — phishing email, credential stuffing, or RDP brute-force.\n"
             "  2. Lateral Movement — attackers spread through the network.\n"
             "  3. Data Exfiltration — data stolen BEFORE encryption (double extortion).\n"
             "  4. Encryption — all accessible files locked with strong algorithms.\n"
             "  5. Ransom Demand — payment deadline set with a countdown timer.\n\n"
             "Real examples: WannaCry (2017) — 200,000+ systems across 150 countries. "
             "Colonial Pipeline (2021) — $4.4M paid. Average demand in 2024: $2.7M."),

            ("4️⃣  Double Extortion", TEXT_ORANGE,
             "Modern ransomware groups also threaten to publish stolen data on dark-web leak "
             "sites if the ransom isn't paid — pressuring victims even when clean backups exist.\n\n"
             "Triple extortion goes further: contacting the victim's customers or regulators.\n\n"
             "Defence: Prevent initial access (patching, MFA, least-privilege) and maintain "
             "a data-classification policy so you know what exists and where."),

            ("5️⃣  How to Protect Yourself", TEXT_GREEN_D,
             "✅  Use a unique, strong password for every account (use a password manager).\n"
             "✅  Enable Multi-Factor Authentication (MFA/2FA) everywhere possible.\n"
             "✅  Never reuse passwords across work and personal accounts.\n"
             "✅  Maintain offline or immutable backups (the 3-2-1 rule).\n"
             "✅  Keep systems and software fully patched and up-to-date.\n"
             "✅  Be suspicious of unexpected emails, links, and attachments.\n"
             "✅  Apply least-privilege: users should only access what they need.\n"
             "✅  Monitor for anomalous login attempts and unusual network traffic.\n"
             "✅  Have and regularly test an Incident Response plan.\n"
             "✅  Train all staff in security awareness — the human layer is critical."),
        ]

        for title, colour, body in sections:
            sec = tk.Frame(inner, bg=BG_CARD_D, padx=16, pady=12,
                           highlightbackground=BORDER_D, highlightthickness=1)
            sec.pack(fill=tk.X, pady=6, padx=4)
            tk.Label(sec, text=title, bg=BG_CARD_D, fg=colour,
                     font=self.font_edu_title, anchor="w").pack(fill=tk.X)
            tk.Label(sec, text=body, bg=BG_CARD_D, fg=TEXT_PRIMARY,
                     font=self.font_edu_body,
                     wraplength=580, justify="left", anchor="w").pack(fill=tk.X, pady=(6, 0))

        tk.Button(edu, text="✓  Got it — Close",
                  bg=BTN_GREEN_D, fg=TEXT_PRIMARY,
                  font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
                  relief="flat", cursor="hand2", pady=8,
                  command=edu.destroy).pack(fill=tk.X, padx=20, pady=10)

    # ── close overlay ─────────────────────────────────────────────

    def _close_overlay(self, win):
        if self.countdown_job:
            try:
                win.after_cancel(self.countdown_job)
            except Exception:
                pass
        win.destroy()
        self.locked   = False
        self.attempts = 0
        self.btn_login.config(state="normal", bg=G_BLUE, fg=G_WHITE)
        self.status_lbl.config(fg=G_GREEN)
        self.status_var.set("ℹ  Simulation complete. Account reset. Try again.")
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)
        self._build_attempt_dots()


# ── Entry point ──────────────────────────────────────────────────

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
