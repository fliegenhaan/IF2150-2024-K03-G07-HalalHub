import tkinter as tk

class Sidebar:
    def __init__(self, parent, colors, menu_commands):
        """
        Inisialisasi komponen sidebar
        
        Args:
            parent: Parent widget
            colors: Dictionary warna tema
            menu_commands: Dictionary berisi pasangan nama menu dan command-nya
        """
        self.parent = parent
        self.colors = colors
        self.menu_commands = menu_commands
        
        # Buat frame sidebar
        self.sidebar_frame = tk.Frame(
            self.parent,
            bg=self.colors['secondary'],
            width=200
        )
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        self.create_title_section()
        self.create_menu_buttons()
        
    def create_title_section(self):
        """Membuat bagian judul di sidebar"""
        title_frame = tk.Frame(
            self.sidebar_frame,
            bg=self.colors['secondary'],
            pady=20
        )
        title_frame.pack(fill=tk.X)
        
        # Logo aplikasi
        logo_label = tk.Label(
            title_frame,
            text="🕌",
            font=('Arial', 48),
            bg=self.colors['secondary'],
            fg=self.colors['text']
        )
        logo_label.pack()
        
        # Nama aplikasi
        app_name = tk.Label(
            title_frame,
            text="HalalHub",
            font=('Arial', 14, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['text']
        )
        app_name.pack(pady=(5, 0))
        
    def create_menu_buttons(self):
        """Membuat tombol-tombol menu"""
        # Emoji untuk setiap menu
        menu_icons = {
            "Beranda": "🏠",
            "Produk": "📦",
            "Pesanan": "📝",
            "Laporan": "📊",
            "Transaksi": "💰"
        }
        
        # Container untuk menu
        menu_frame = tk.Frame(
            self.sidebar_frame,
            bg=self.colors['secondary']
        )
        menu_frame.pack(fill=tk.X, pady=20)
        
        # Buat tombol untuk setiap menu
        for menu_name, command in self.menu_commands.items():
            icon = menu_icons.get(menu_name, "")
            button = tk.Button(
                menu_frame,
                text=f" {icon} {menu_name}",
                font=('Arial', 11),
                bg=self.colors['secondary'],
                fg=self.colors['text'],
                bd=0,
                relief=tk.FLAT,
                anchor='w',
                padx=20,
                pady=10,
                command=command,
                width=25,
                cursor='hand2'
            )
            button.pack(fill=tk.X, pady=2)
            
            # Hover effect
            button.bind('<Enter>', lambda e, btn=button: self.on_hover(btn, True))
            button.bind('<Leave>', lambda e, btn=button: self.on_hover(btn, False))
            
    def on_hover(self, button, entering):
        """Efek hover untuk tombol menu"""
        if entering:
            button.config(
                bg=self.colors['accent'],
                fg='white'
            )
        else:
            button.config(
                bg=self.colors['secondary'],
                fg=self.colors['text']
            )
