# src/views/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from ttkthemes import ThemedTk
from .gui.halaman_utama import HalamanUtama
from .gui.produk.daftar_produk import DaftarProduk
from .gui.pesanan.daftar_pesanan import DaftarPesanan
from .gui.laporan.laporan_penjualan import LaporanPenjualan
from .gui.transaksi.riwayat_transaksi import RiwayatTransaksi
from .gui.components.sidebar import Sidebar
from .gui.components.header import Header
from .gui.components.footer import Footer

class MainWindow:
    def __init__(self):
        """Inisialisasi jendela utama dengan styling kustom"""
        self.root = ThemedTk(theme="arc")  
        self.root.title("HalalHub - Sistem Manajemen Toko Muslim")
        self.root.geometry("1200x700")
        
        # Skema warna kustom
        self.colors = {
            'primary': '#2E7D32',    
            'secondary': '#81C784',   # Hijau terang
            'accent': '#4CAF50',      # Hijau sedang
            'text': '#1B5E20',        # Hijau lebih gelap untuk teks
            'background': '#F1F8E9',  # Hijau sangat terang untuk latar
            'warning': '#FF9800',     # Oranye untuk peringatan
            'error': '#F44336',       # Merah untuk kesalahan
            'success': '#4CAF50'      # Hijau untuk pesan sukses
        }
        
        # Konfigurasi style
        self.setup_styles()
        
        # Inisialisasi komponen UI
        self.initialize_components()
    
    def setup_styles(self):
        """Mengatur style untuk widget"""
        self.style = ttk.Style()
        self.style.configure('Primary.TButton', 
                           background=self.colors['primary'],
                           foreground='white',
                           padding=10)
        self.style.configure('Secondary.TButton',
                           background=self.colors['secondary'],
                           foreground=self.colors['text'],
                           padding=10)
    
    def initialize_components(self):
        """Inisialisasi komponen-komponen utama"""
        # Inisialisasi Header
        self.header = Header(self.root, self.colors)
        
        # Inisialisasi Sidebar
        self.sidebar = Sidebar(self.root, self.colors, {
            "Beranda": self.show_home,
            "Produk": self.show_products,
            "Pesanan": self.show_orders,
            "Laporan": self.show_reports,
            "Transaksi": self.show_transactions
        })
        
        # Inisialisasi area konten utama
        self.main_content = tk.Frame(self.root, bg=self.colors['background'])
        self.main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.footer = Footer(self.root, self.colors)
        
        self.show_home()
    
    def show_home(self):
        """Menampilkan halaman utama"""
        self.clear_main_content()
        HalamanUtama(self.main_content, self.colors)
    
    def show_products(self):
        """Menampilkan halaman produk"""
        self.clear_main_content()
        DaftarProduk(self.main_content, self.colors)
    
    def show_orders(self):
        """Menampilkan halaman pesanan"""
        self.clear_main_content()
        DaftarPesanan(self.main_content, self.colors)
    
    def show_reports(self):
        """Menampilkan halaman laporan"""
        self.clear_main_content()
        LaporanPenjualan(self.main_content, self.colors)
    
    def show_transactions(self):
        """Menampilkan halaman transaksi"""
        self.clear_main_content()
        RiwayatTransaksi(self.main_content, self.colors)
    
    def clear_main_content(self):
        """Membersihkan area konten utama"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def run(self):
        """Menjalankan aplikasi"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
