import customtkinter as ctk
import pyqrcode
from PIL import Image
import threading
import io
import os
import hashlib
import random
import string
import subprocess
import sys
import webbrowser
from tkinter import filedialog, messagebox

# ========== إعدادات النيون والثيم ==========
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ========== كلاس النافذة الرئيسية ==========
class CyberBoxOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة الرئيسية
        self.title("BLACK BOX - ULTIMATE COMMAND CENTER v4.0")
        self.geometry("1200x900")
        self.minsize(1000, 700)

        # متغيرات التشغيل
        self.current_qr = None
        self.py_file_path = ""
        self.icon_file_path = ""
        self.current_tab = None

        # إعداد الجريد الرئيسي
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # إنشاء الواجهات
        self.create_sidebar()
        self.create_main_container()
        
        # عرض التاب الافتراضي
        self.show_compiler_tab()

        # رسالة الترحيب
        self.show_welcome_message()

    # ========== إنشاء القائمة الجانبية ==========
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#050505")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # اللوجو
        self.logo = ctk.CTkLabel(
            self.sidebar, 
            text="┌[ BLACK BOX ]┐\n│  CORE v4.0  │\n└────────────┘", 
            font=("Courier", 18, "bold"), 
            text_color="#00FF00"
        )
        self.logo.pack(pady=40)

        # خط فاصل
        self.separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#00FF00")
        self.separator.pack(fill="x", padx=20, pady=10)

        # أزرار التنقل
        nav_buttons = [
            ("⚡ EXE COMPILER", self.show_compiler_tab),
            ("📱 QR GENERATOR", self.show_qr_tab),
            ("🔐 PASS GENERATOR", self.show_pass_tab),
            ("🔒 HASH CALCULATOR", self.show_hash_tab),
            ("📊 SYSTEM LOGS", self.show_logs_tab),
        ]
        
        self.nav_btns = []
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                command=command, 
                font=("Courier", 13, "bold"), 
                fg_color="transparent", 
                text_color="#00FF00", 
                hover_color="#1a3a1a", 
                anchor="w", 
                height=45, 
                corner_radius=5,
                border_spacing=20
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_btns.append(btn)

        # خط فاصل سفلي
        self.separator2 = ctk.CTkFrame(self.sidebar, height=1, fg_color="#222")
        self.separator2.pack(fill="x", padx=20, pady=20)

        # حقوق الملكية
        copyright_text = ctk.CTkLabel(
            self.sidebar, 
            text="© 2026 BLACK BOX\n@abushama1", 
            font=("Courier", 10), 
            text_color="#555"
        )
        copyright_text.pack(side="bottom", pady=20)

    # ========== إنشاء الحاوية الرئيسية ==========
    def create_main_container(self):
        self.main_view = ctk.CTkFrame(self, corner_radius=0, fg_color="#0a0a0a")
        self.main_view.grid(row=0, column=1, sticky="nsew")
        
        # هيدر مع أنيميشن
        self.header_frame = ctk.CTkFrame(self.main_view, height=60, fg_color="#050505", corner_radius=0)
        self.header_frame.pack(fill="x")
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="▶ BLACK BOX COMMAND CENTER ◀", 
            font=("Courier", 20, "bold"), 
            text_color="#00FF00"
        )
        self.header_label.pack(pady=15)

    def clear_main_view(self):
        """مسح المحتوى مع الحفاظ على الهيدر"""
        for widget in self.main_view.winfo_children():
            if widget != self.header_frame:
                widget.destroy()

    def animate_tab_switch(self, tab_name):
        """أنيميشن بسيط لتبديل التابات"""
        self.header_label.configure(text=f"▶ {tab_name} ◀")
        # تأثير وميض
        self.header_label.configure(text_color="#FFFF00")
        self.after(200, lambda: self.header_label.configure(text_color="#00FF00"))

    def create_tab_title(self, title):
        """إنشاء عنوان التاب"""
        title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        title_frame.pack(pady=30, padx=40, fill="x")
        
        lbl = ctk.CTkLabel(
            title_frame, 
            text=f"$ {title}", 
            font=("Courier", 28, "bold"), 
            text_color="#00FF00"
        )
        lbl.pack(anchor="w")
        
        line = ctk.CTkFrame(title_frame, height=2, fg_color="#00FF00")
        line.pack(fill="x", pady=5)

    def show_welcome_message(self):
        """رسالة ترحيب في الـ logs"""
        pass

    # ========== 1. تاب تحويل بايثون لـ EXE مع تنبيه ==========
    def show_compiler_tab(self):
        self.clear_main_view()
        self.animate_tab_switch("EXE COMPILER")
        self.create_tab_title("EXE COMPILER / PACKAGER")
        self.current_tab = "compiler"

        # ===== تنبيه أحمر للمتطلبات =====
        warning_frame = ctk.CTkFrame(self.main_view, fg_color="#3a0000", border_width=2, border_color="#FF0000", corner_radius=10)
        warning_frame.pack(pady=15, padx=40, fill="x")
        
        warning_title = ctk.CTkLabel(
            warning_frame, 
            text="⚠️ تنبيه هام ⚠️", 
            font=("Courier", 16, "bold"), 
            text_color="#FF4444"
        )
        warning_title.pack(pady=(10,5))
        
        warning_text = ctk.CTkLabel(
            warning_frame, 
            text="هذه العملية تتطلب تثبيت Python ومكتبة PyInstaller\nلتحويل ملف .py إلى ملف تنفيذي .exe",
            font=("Courier", 12), 
            text_color="#FF8888"
        )
        warning_text.pack(pady=5)
        
        # روابط التحميل
        links_frame = ctk.CTkFrame(warning_frame, fg_color="transparent")
        links_frame.pack(pady=10)
        
        def open_python():
            webbrowser.open("https://www.python.org/downloads/")
        
        def open_pyinstaller():
            webbrowser.open("https://pyinstaller.org/en/stable/installation.html")
        
        python_btn = ctk.CTkButton(
            links_frame, 
            text="🐍 تحميل Python", 
            command=open_python, 
            fg_color="#1a4a1a", 
            text_color="#00FF00",
            hover_color="#0a2a0a",
            width=150
        )
        python_btn.pack(side="left", padx=10)
        
        pyinstaller_btn = ctk.CTkButton(
            links_frame, 
            text="📦 تثبيت PyInstaller", 
            command=open_pyinstaller, 
            fg_color="#1a4a1a", 
            text_color="#00FF00",
            hover_color="#0a2a0a",
            width=150
        )
        pyinstaller_btn.pack(side="left", padx=10)
        
        # أمر التثبيت السريع
        install_cmd_frame = ctk.CTkFrame(warning_frame, fg_color="#1a1a1a", corner_radius=5)
        install_cmd_frame.pack(pady=10, padx=20, fill="x")
        
        install_label = ctk.CTkLabel(
            install_cmd_frame, 
            text="أمر التثبيت السريع:", 
            font=("Courier", 11, "bold"), 
            text_color="#00FF00"
        )
        install_label.pack(pady=(10,5))
        
        cmd_text = ctk.CTkLabel(
            install_cmd_frame, 
            text="pip install pyinstaller", 
            font=("Courier", 13, "bold"), 
            text_color="#FFFF00"
        )
        cmd_text.pack(pady=5)
        
        copy_btn = ctk.CTkButton(
            install_cmd_frame, 
            text="📋 نسخ الأمر", 
            command=lambda: self.copy_to_clipboard("pip install pyinstaller"),
            fg_color="#333",
            width=120,
            height=30
        )
        copy_btn.pack(pady=10)

        # ===== اختيار الملفات =====
        file_frame = ctk.CTkFrame(self.main_view, fg_color="#111111", corner_radius=10)
        file_frame.pack(pady=20, padx=40, fill="x")

        self.py_lbl = ctk.CTkLabel(file_frame, text="📄 لا يوجد ملف Python", text_color="#555", font=("Courier", 12))
        self.py_lbl.grid(row=0, column=0, padx=20, pady=15)
        ctk.CTkButton(file_frame, text="اختر ملف PY", command=self.browse_py, width=150, fg_color="#1a4a1a").grid(row=0, column=1, padx=10)

        self.icon_lbl = ctk.CTkLabel(file_frame, text="🎨 لا يوجد ملف Icon", text_color="#555", font=("Courier", 12))
        self.icon_lbl.grid(row=1, column=0, padx=20, pady=15)
        ctk.CTkButton(file_frame, text="اختر ملف ICO", command=self.browse_icon, width=150, fg_color="#1a4a1a").grid(row=1, column=1, padx=10)

        # معلومات البرنامج
        info_frame = ctk.CTkFrame(self.main_view, fg_color="#111111", corner_radius=10)
        info_frame.pack(pady=15, padx=40, fill="x")
        
        ctk.CTkLabel(info_frame, text="معلومات المنتج:", font=("Courier", 14, "bold"), text_color="#00FF00").pack(pady=10)
        
        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(pady=10)
        
        self.pub_name = ctk.CTkEntry(info_inner, placeholder_text="الناشر (مثال: Black Box)", width=250, font=("Courier", 12))
        self.pub_name.grid(row=0, column=0, padx=20, pady=10)
        
        self.version = ctk.CTkEntry(info_inner, placeholder_text="الإصدار (1.0.0)", width=250, font=("Courier", 12))
        self.version.grid(row=0, column=1, padx=20, pady=10)

        # زر البدء
        self.compile_btn = ctk.CTkButton(
            self.main_view, 
            text="▶ START COMPILATION ◀", 
            command=self.compile_exe_logic, 
            fg_color="#00FF00", 
            text_color="#000000", 
            font=("Courier", 16, "bold"), 
            height=55,
            corner_radius=10
        )
        self.compile_btn.pack(pady=25)

        # سجل العمليات
        log_label = ctk.CTkLabel(self.main_view, text="[ CONSOLE OUTPUT ]", font=("Courier", 12, "bold"), text_color="#00FF00")
        log_label.pack(pady=(10,5))
        
        self.comp_logs = ctk.CTkTextbox(
            self.main_view, 
            width=900, 
            height=250, 
            fg_color="#000000", 
            text_color="#00FF00", 
            font=("Courier", 11),
            corner_radius=10
        )
        self.comp_logs.pack(pady=10, padx=40)

    def browse_py(self):
        self.py_file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.py_file_path: 
            self.py_lbl.configure(text=f"📄 {os.path.basename(self.py_file_path)}", text_color="#00FF00")

    def browse_icon(self):
        self.icon_file_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if self.icon_file_path: 
            self.icon_lbl.configure(text=f"🎨 {os.path.basename(self.icon_file_path)}", text_color="#00FF00")

    def copy_to_clipboard(self, text):
        """نسخ النص إلى الحافظة"""
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("تم النسخ", "تم نسخ الأمر إلى الحافظة ✅")

    def compile_exe_logic(self):
        if not self.py_file_path:
            messagebox.showerror("خطأ", "الرجاء اختيار ملف Python أولاً!")
            return
        
        # التحقق من وجود pyinstaller
        def check_pyinstaller():
            try:
                subprocess.run(["pyinstaller", "--version"], capture_output=True, text=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        
        if not check_pyinstaller():
            response = messagebox.askyesno(
                "مكتبة PyInstaller غير مثبتة", 
                "مكتبة PyInstaller غير موجودة!\n\n"
                "هل تريد تثبيتها الآن؟\n"
                "(ستحتاج إلى اتصال بالإنترنت)"
            )
            if response:
                self.install_pyinstaller()
            return
        
        def run_thread():
            self.comp_logs.delete("1.0", "end")
            self.comp_logs.insert("end", ">> بدء عملية التحويل...\n")
            self.comp_logs.insert("end", f">> الملف المصدر: {self.py_file_path}\n")
            if self.icon_file_path:
                self.comp_logs.insert("end", f">> ملف الأيقونة: {self.icon_file_path}\n")
            self.comp_logs.insert("end", "-" * 50 + "\n")
            
            cmd = f'pyinstaller --onefile --windowed --name "BlackBox_App" '
            if self.icon_file_path: 
                cmd += f'--icon="{self.icon_file_path}" '
            cmd += f'"{self.py_file_path}"'
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
            for line in process.stdout:
                self.comp_logs.insert("end", line)
                self.comp_logs.see("end")
                self.update_idletasks()
            
            self.comp_logs.insert("end", "\n" + "-" * 50 + "\n")
            self.comp_logs.insert("end", "✅ اكتملت العملية! تحقق من مجلد 'dist'\n")
            messagebox.showinfo("اكتمل", "تم تحويل الملف بنجاح! 🎉")
        
        threading.Thread(target=run_thread, daemon=True).start()
    
    def install_pyinstaller(self):
        """تثبيت PyInstaller تلقائياً"""
        def install():
            self.comp_logs.delete("1.0", "end")
            self.comp_logs.insert("end", ">> جاري تثبيت PyInstaller...\n")
            self.comp_logs.insert("end", ">> قد يستغرق هذا دقيقة أو دقيقتين\n\n")
            
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "pyinstaller"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            for line in process.stdout:
                self.comp_logs.insert("end", line)
                self.comp_logs.see("end")
                self.update_idletasks()
            
            self.comp_logs.insert("end", "\n✅ تم تثبيت PyInstaller بنجاح!\n")
            self.comp_logs.insert("end", ">> يمكنك الآن محاولة التحويل مرة أخرى.\n")
            messagebox.showinfo("تم التثبيت", "تم تثبيت PyInstaller بنجاح! ✅")
        
        threading.Thread(target=install, daemon=True).start()

    # ========== 2. تاب الـ QR Generator ==========
    def show_qr_tab(self):
        self.clear_main_view()
        self.animate_tab_switch("QR GENERATOR")
        self.create_tab_title("QR GENERATOR")
        self.current_tab = "qr"
        
        # إطار المحتوى
        content_frame = ctk.CTkFrame(self.main_view, fg_color="#111111", corner_radius=10)
        content_frame.pack(pady=30, padx=40, fill="both", expand=True)
        
        entry = ctk.CTkEntry(
            content_frame, 
            placeholder_text="أدخل الرابط أو النص...", 
            width=600, 
            height=50,
            font=("Courier", 14)
        )
        entry.pack(pady=30)

        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        generate_btn = ctk.CTkButton(
            btn_frame, 
            text="🎯 إنشاء QR", 
            command=lambda: self.gen_qr(entry.get()),
            fg_color="#1a4a1a",
            height=40,
            width=150
        )
        generate_btn.pack(side="left", padx=10)
        
        self.save_qr_btn = ctk.CTkButton(
            btn_frame, 
            text="💾 حفظ الصورة", 
            command=self.save_qr, 
            state="disabled",
            fg_color="#333",
            height=40,
            width=150
        )
        self.save_qr_btn.pack(side="left", padx=10)

        self.qr_label = ctk.CTkLabel(content_frame, text="[ في انتظار البيانات ]", text_color="#555", font=("Courier", 14))
        self.qr_label.pack(pady=40)

    def gen_qr(self, text):
        if not text.strip():
            messagebox.showwarning("تنبيه", "الرجاء إدخال نص أو رابط!")
            return
            
        self.current_qr = pyqrcode.create(text)
        buffer = io.BytesIO()
        self.current_qr.png(buffer, scale=10)
        img = Image.open(buffer)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(280, 280))
        self.qr_label.configure(image=ctk_img, text="")
        self.save_qr_btn.configure(state="normal", fg_color="#1a4a1a", text_color="#00FF00")

    def save_qr(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if path: 
            self.current_qr.png(path, scale=15)
            messagebox.showinfo("تم الحفظ", f"تم حفظ QR Code في:\n{path}")

    # ========== 3. تاب الـ Password Generator ==========
    def show_pass_tab(self):
        self.clear_main_view()
        self.animate_tab_switch("PASSWORD GENERATOR")
        self.create_tab_title("PASSWORD GENERATOR")
        self.current_tab = "pass"
        
        content_frame = ctk.CTkFrame(self.main_view, fg_color="#111111", corner_radius=10)
        content_frame.pack(pady=50, padx=40, fill="both", expand=True)
        
        self.pass_entry = ctk.CTkEntry(
            content_frame, 
            width=600, 
            height=60, 
            font=("Courier", 20, "bold"), 
            text_color="#00FF00",
            justify="center"
        )
        self.pass_entry.pack(pady=40)
        
        # خيارات إضافية
        options_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        options_frame.pack(pady=20)
        
        self.length_var = ctk.IntVar(value=16)
        length_label = ctk.CTkLabel(options_frame, text="طول كلمة المرور:", font=("Courier", 12))
        length_label.grid(row=0, column=0, padx=10)
        length_slider = ctk.CTkSlider(options_frame, from_=8, to=32, variable=self.length_var, width=200)
        length_slider.grid(row=0, column=1, padx=10)
        length_value = ctk.CTkLabel(options_frame, textvariable=self.length_var, font=("Courier", 12))
        length_value.grid(row=0, column=2, padx=10)
        
        def gen():
            length = self.length_var.get()
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = "".join(random.choice(chars) for _ in range(length))
            self.pass_entry.delete(0, "end")
            self.pass_entry.insert(0, password)
        
        generate_btn = ctk.CTkButton(
            content_frame, 
            text="🔐 إنشاء كلمة مرور قوية", 
            command=gen, 
            height=50,
            font=("Courier", 14, "bold"),
            fg_color="#1a4a1a"
        )
        generate_btn.pack(pady=20)
        
        copy_btn = ctk.CTkButton(
            content_frame, 
            text="📋 نسخ", 
            command=lambda: self.copy_to_clipboard(self.pass_entry.get()),
            fg_color="#333",
            height=40,
            width=100
        )
        copy_btn.pack(pady=10)
        
        # إنشاء كلمة مرور أولية
        gen()

    # ========== 4. تاب الـ Hash Calculator ==========
    def show_hash_tab(self):
        self.clear_main_view()
        self.animate_tab_switch("HASH CALCULATOR")
        self.create_tab_title("SHA-256 HASH CALCULATOR")
        self.current_tab = "hash"
        
        content_frame = ctk.CTkFrame(self.main_view, fg_color="#111111", corner_radius=10)
        content_frame.pack(pady=30, padx=40, fill="both", expand=True)
        
        self.hash_text = ctk.CTkTextbox(
            content_frame, 
            width=800, 
            height=200, 
            fg_color="#000000", 
            text_color="#00FF00",
            font=("Courier", 12),
            corner_radius=10
        )
        self.hash_text.pack(pady=30, padx=20)
        
        def calculate_hash():
            path = filedialog.askopenfilename(title="اختر ملف لحساب الهاش")
            if path:
                self.hash_text.delete("1.0", "end")
                self.hash_text.insert("end", f"📁 الملف: {os.path.basename(path)}\n")
                self.hash_text.insert("end", "🔄 جاري الحساب...\n")
                self.update_idletasks()
                
                def calc():
                    h = hashlib.sha256()
                    with open(path, "rb") as f:
                        for chunk in iter(lambda: f.read(8192), b""):
                            h.update(chunk)
                    self.hash_text.delete("1.0", "end")
                    self.hash_text.insert("1.0", f"📁 الملف: {os.path.basename(path)}\n")
                    self.hash_text.insert("end", f"🔒 SHA-256:\n{h.hexdigest()}\n")
                    self.hash_text.insert("end", "-" * 60 + "\n")
                    self.hash_text.insert("end", "✅ تم الحساب بنجاح")
                
                threading.Thread(target=calc, daemon=True).start()
        
        select_btn = ctk.CTkButton(
            content_frame, 
            text="🔍 اختيار ملف", 
            command=calculate_hash,
            height=45,
            font=("Courier", 14, "bold"),
            fg_color="#1a4a1a"
        )
        select_btn.pack(pady=20)

    # ========== 5. تاب الـ System Logs ==========
    def show_logs_tab(self):
        self.clear_main_view()
        self.animate_tab_switch("SYSTEM LOGS")
        self.create_tab_title("SYSTEM STATUS & LOGS")
        self.current_tab = "logs"
        
        content_frame = ctk.CTkFrame(self.main_view, fg_color="#111111", corner_radius=10)
        content_frame.pack(pady=30, padx=40, fill="both", expand=True)
        
        log_text = ctk.CTkTextbox(
            content_frame, 
            width=850, 
            height=450, 
            fg_color="#000000", 
            text_color="#00FF00",
            font=("Courier", 12),
            corner_radius=10
        )
        log_text.pack(pady=20, padx=20, fill="both", expand=True)
        
        # معلومات النظام
        log_text.insert("1.0", "=" * 60 + "\n")
        log_text.insert("end", "BLACK BOX COMMAND CENTER v4.0\n")
        log_text.insert("end", "=" * 60 + "\n\n")
        log_text.insert("end", f"▶ التشغيل: {ctk.__version__}\n")
        log_text.insert("end", f"▶ Python: {sys.version.split()[0]}\n")
        log_text.insert("end", f"▶ الحالة: نشط ✅\n")
        log_text.insert("end", f"▶ التاب الحالي: {self.current_tab}\n\n")
        log_text.insert("end", "=" * 60 + "\n")
        log_text.insert("end", "جميع الوحدات تم تحميلها بنجاح\n")
        log_text.insert("end", f"© 2026 BLACK BOX | @abushama1\n")
        log_text.insert("end", "=" * 60 + "\n")

# ========== تشغيل البرنامج ==========
if __name__ == "__main__":
    app = CyberBoxOS()
    app.mainloop()