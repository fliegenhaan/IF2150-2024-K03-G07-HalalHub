import tkinter as tk
from datetime import datetime

class Footer:
    def __init__(self, parent, colors):
        """Inisialisasi komponen footer"""
        self.parent = parent
        self.colors = colors
        
        # Buat frame footer
        self.footer_frame = tk.Frame(
            self.parent,
            bg=self.colors['primary'],
            height=30
        )
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer_frame.pack_propagate(False)
        
        self.create_footer_content()
        
    def create_footer_content(self):
        """Membuat konten footer"""
        # Copyright dan versi aplikasi
        copyright_label = tk.Label(
            self.footer_frame,
            text="© 2024 HalalHub - Sistem Manajemen Toko Muslim",
            font=('Arial', 9),
            bg=self.colors['primary'],
            fg='white'
        )
        copyright_label.pack(side=tk.LEFT, padx=20)
        
        # Status koneksi database
        self.status_var = tk.StringVar(value="✓ Database Terhubung")
        status_label = tk.Label(
            self.footer_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            bg=self.colors['primary'],
            fg='white'
        )
        status_label.pack(side=tk.RIGHT, padx=20)
        
        # Versi aplikasi
        version_label = tk.Label(
            self.footer_frame,
            text="v1.0.0",
            font=('Arial', 9),
            bg=self.colors['primary'],
            fg='white'
        )
        version_label.pack(side=tk.RIGHT, padx=20)
        
    def update_status(self, message, is_error=False):
        """Update status di footer"""
        self.status_var.set(message)
        
        # Ubah warna text berdasarkan status
        color = self.colors['error'] if is_error else 'white'
        for child in self.footer_frame.winfo_children():
            if isinstance(child, tk.Label) and child.cget('textvariable') == str(self.status_var):
                child.configure(fg=color)
