# src/views/gui/laporan/laporan_stok.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.database import DatabaseManager
from datetime import datetime

class LaporanStok:
    def __init__(self, parent, colors):
        """Inisialisasi halaman laporan stok"""
        self.parent = parent
        self.colors = colors
        self.db = DatabaseManager()
        
        # Frame utama
        self.frame = tk.Frame(self.parent, bg=self.colors['background'])
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_filter_section()
        self.create_status_section()
        self.create_table_section()
        self.create_chart_section()
        
        # Load data awal
        self.update_report()
    
    def create_filter_section(self):
        """Membuat bagian filter laporan stok"""
        filter_frame = tk.LabelFrame(
            self.frame,
            text="Filter Stok",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Filter Kategori
        tk.Label(
            filter_frame,
            text="Kategori:",
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        categories = [
            "Semua",
            "Pakaian Muslim Pria",
            "Pakaian Muslim Wanita",
            "Perlengkapan Ibadah",
            "Aksesoris Muslim"
        ]
        
        self.category_var = tk.StringVar(value="Semua")
        category_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=categories,
            width=20,
            state="readonly"
        )
        category_cb.pack(side=tk.LEFT, padx=5)
        
        # Tombol Filter
        ttk.Button(
            filter_frame,
            text="Tampilkan",
            style='Primary.TButton',
            command=self.update_report
        ).pack(side=tk.LEFT, padx=10)
        
        # Tombol Export
        ttk.Button(
            filter_frame,
            text="Export ke Excel",
            style='Secondary.TButton',
            command=self.export_report
        ).pack(side=tk.LEFT, padx=5)
    
    def create_status_section(self):
        """Membuat bagian status stok"""
        self.status_frame = tk.Frame(self.frame, bg=self.colors['background'])
        self.status_frame.pack(fill=tk.X, pady=(0, 20))
    
    def create_table_section(self):
        """Membuat tabel laporan stok"""
        table_frame = tk.LabelFrame(
            self.frame,
            text="Daftar Stok Produk",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buat Treeview
        columns = ('ID', 'Nama Produk', 'Kategori', 'Stok', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Atur heading dan kolom
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Tambah scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_chart_section(self):
        """Membuat grafik stok"""
        self.chart_frame = tk.LabelFrame(
            self.frame,
            text="Grafik Stok per Kategori",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
    
    def update_report(self):
        """Memperbarui laporan berdasarkan filter"""
        try:
            kategori = self.category_var.get()
            
            # Ambil data dari database
            if kategori == "Semua":
                produk_list = self.db.get_all_produk()
            else:
                produk_list = [p for p in self.db.get_all_produk() if p['kategori'] == kategori]
            
            # Update status
            self.update_status_section(produk_list)
            
            # Update tabel
            self.update_table(produk_list)
            
            # Update grafik
            self.update_chart(produk_list)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat laporan: {str(e)}")
    
    def update_status_section(self, produk_list):
        """Memperbarui bagian status"""
        # Hapus widget lama
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Hitung statistik
        total_produk = len(produk_list)
        stok_menipis = len([p for p in produk_list if int(p['stok']) <= 10])
        stok_habis = len([p for p in produk_list if int(p['stok']) == 0])
        
        status_data = [
            ("Total Produk", str(total_produk), self.colors['primary']),
            ("Stok Menipis", str(stok_menipis), self.colors['warning']),
            ("Stok Habis", str(stok_habis), self.colors['error'])
        ]
        
        for title, value, color in status_data:
            card = tk.Frame(self.status_frame, bg='white', padx=15, pady=10)
            card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            
            tk.Label(
                card,
                text=title,
                font=('Arial', 10),
                bg='white',
                fg=self.colors['text']
            ).pack(anchor='w')
            
            tk.Label(
                card,
                text=value,
                font=('Arial', 16, 'bold'),
                bg='white',
                fg=color
            ).pack(anchor='w')
    
    def update_table(self, produk_list):
        """Memperbarui tabel produk"""
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Masukkan data baru
        for produk in produk_list:
            # Tentukan status stok
            stok = int(produk['stok'])
            if stok == 0:
                status = "Habis"
                tag = 'habis'
            elif stok <= 10:
                status = "Menipis"
                tag = 'menipis'
            else:
                status = "Tersedia"
                tag = 'tersedia'
            
            self.tree.insert('', tk.END, values=(
                produk['id_produk'],
                produk['nama_produk'],
                produk['kategori'],
                stok,
                status
            ), tags=(tag,))
        
        # Set warna baris berdasarkan status
        self.tree.tag_configure('habis', foreground=self.colors['error'])
        self.tree.tag_configure('menipis', foreground=self.colors['warning'])
        self.tree.tag_configure('tersedia', foreground=self.colors['success'])
    
    def update_chart(self, produk_list):
        """Memperbarui grafik stok"""
        # Hapus widget lama
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Buat DataFrame dari produk
        df = pd.DataFrame(produk_list)
        if not df.empty:
            # Hitung total stok per kategori
            stok_per_kategori = df.groupby('kategori')['stok'].sum()
            
            # Buat grafik baru
            fig = Figure(figsize=(10, 4))
            ax = fig.add_subplot(111)
            
            # Plot data
            stok_per_kategori.plot(kind='bar', ax=ax, color=self.colors['primary'])
            ax.set_title('Total Stok per Kategori')
            ax.set_ylabel('Jumlah Stok')
            
            # Rotasi label
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Tambahkan canvas ke frame
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def export_report(self):
        """Mengekspor laporan ke Excel"""
        try:
            kategori = self.category_var.get()
            
            # Ambil data
            if kategori == "Semua":
                produk_list = self.db.get_all_produk()
            else:
                produk_list = [p for p in self.db.get_all_produk() if p['kategori'] == kategori]
            
            # Buat DataFrame
            df = pd.DataFrame(produk_list)
            
            # Simpan ke Excel
            filename = f"Laporan_Stok_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            
            messagebox.showinfo("Sukses", f"Laporan berhasil diekspor ke {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor laporan: {str(e)}")
