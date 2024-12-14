import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
from views.main_window import MainWindow

class LandingPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to HalalHub")
        
        window_width = 1000
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.colors = {
            'primary': '#2E7D32',
            'secondary': '#81C784',  
            'accent': '#4CAF50',    
            'text': '#1B5E20',      
            'background': '#F1F8E9',
            'warning': '#FF9800',   
            'error': '#F44336',     
            'success': '#4CAF50'    
        }
        
        self.frame = tk.Frame(self.root, bg=self.colors['background'])
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_left_panel()
        self.create_right_panel()
        
    def create_left_panel(self):
        left_panel = tk.Frame(self.frame, bg=self.colors['primary'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        logo_frame = tk.Frame(left_panel, bg=self.colors['primary'])
        logo_frame.pack(pady=(50,0))
        
        try:
            logo_path = os.path.join('img', 'HalalHub_logo.jpg')
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((200, 200), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            
            logo_label = tk.Label(logo_frame, image=logo_photo, bg=self.colors['primary'])
            logo_label.image = logo_photo
            logo_label.pack()
        except:
            tk.Label(logo_frame, text="HalalHub", font=('Arial', 36, 'bold'),
                    bg=self.colors['primary'], fg='white').pack()
        
        tk.Label(left_panel, text="Sistem Manajemen\nToko Muslim Modern", font=('Arial', 18),
                bg=self.colors['primary'], fg='white', justify=tk.CENTER).pack(pady=20)
        
        tk.Label(left_panel, text="Solusi lengkap untuk manajemen\ninventori, pesanan, dan transaksi\nuntuk toko muslim Anda",
                font=('Arial', 12), bg=self.colors['primary'], fg='white', justify=tk.CENTER).pack(pady=20)

    def create_right_panel(self):
        right_panel = tk.Frame(self.frame, bg='white')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_panel, text="Selamat Datang", font=('Arial', 24, 'bold'),
                bg='white', fg=self.colors['primary']).pack(pady=(80,20))
        
        form_frame = tk.Frame(right_panel, bg='white')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username", font=('Arial', 12),
                bg='white', fg=self.colors['text']).pack(anchor='w', padx=50)
        
        username_entry = ttk.Entry(form_frame, width=30, font=('Arial', 12))
        username_entry.pack(pady=(5,15), padx=50)
        
        tk.Label(form_frame, text="Password", font=('Arial', 12),
                bg='white', fg=self.colors['text']).pack(anchor='w', padx=50)
        
        password_entry = ttk.Entry(form_frame, width=30, font=('Arial', 12), show='•')
        password_entry.pack(pady=5, padx=50)
        
        login_button = tk.Button(form_frame, text="Masuk", font=('Arial', 12, 'bold'),
                               bg=self.colors['primary'], fg='white', relief=tk.FLAT,
                               width=25, height=2, command=self.start_application)
        login_button.pack(pady=30)
        
        login_button.bind('<Enter>', lambda e: login_button.config(bg=self.colors['accent']))
        login_button.bind('<Leave>', lambda e: login_button.config(bg=self.colors['primary']))

    def fade_out(self):
        alpha = 1.0
        fade_frame = tk.Frame(self.frame, bg='white',
                            width=self.frame.winfo_width(),
                            height=self.frame.winfo_height())
        fade_frame.place(x=0, y=0)
        
        def fade():
            nonlocal alpha
            alpha -= 0.1
            if alpha > 0:
                fade_frame.configure(bg=f'#{int(alpha*255):02x}' * 3)
                self.frame.after(50, fade)
        fade()

    def show_loading_screen(self):
        loading_frame = tk.Frame(self.frame, bg=self.colors['background'])
        loading_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        loading_text = tk.StringVar(value="Loading")
        loading_label = tk.Label(loading_frame, textvariable=loading_text,
                               font=('Arial', 16, 'bold'), bg=self.colors['background'],
                               fg=self.colors['primary'])
        loading_label.pack()
        
        dots = 0
        def animate_dots():
            nonlocal dots
            dots = (dots + 1) % 4
            loading_text.set("Loading" + "." * dots)
            loading_label.after(300, animate_dots)
        animate_dots()
        return loading_frame

    def start_application(self):
        self.fade_out()
        loading = self.show_loading_screen()
        self.frame.after(1500, lambda: self.launch_main_window(loading))

    def launch_main_window(self, loading_frame):
        try:
            loading_frame.destroy()
            self.frame.destroy()
            self.root.withdraw()
            
            new_window = tk.Tk()
            new_window.title("HalalHub - Sistem Manajemen Toko Muslim")
            new_window.geometry("1200x700")
            
            main_window = MainWindow(new_window, self.colors)
            self.root.destroy()
            new_window.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memulai aplikasi: {str(e)}")
            raise

    def run(self):
        self.root.mainloop()
