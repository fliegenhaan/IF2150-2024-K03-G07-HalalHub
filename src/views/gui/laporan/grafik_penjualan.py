# src/views/gui/laporan/grafik_penjualan.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from utils.database import DatabaseManager

class GrafikPenjualan:
    def __init__(self, parent, colors):
        """Inisialisasi halaman grafik penjualan"""
        self.parent = parent
        self.colors = colors
        self.db = DatabaseManager()
        
        # Frame utama
        self.frame = tk.Frame(self.parent, bg=self.colors['background'])
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_filter_section()
        self.create_grafik_section()
        self.create_legend_section()
        
        # Load data awal
        self.update_grafik()
    
    def create_filter_section(self):
        """Membuat bagian filter grafik"""
        filter_frame = tk.LabelFrame(
            self.frame,
            text="Filter Grafik",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=10
        )
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Filter Periode
        tk.Label(
            filter_frame,
            text="Periode:",
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        periods = ["Harian", "Mingguan", "Bulanan", "Tahunan"]
        self.period_var = tk.StringVar(value="Harian")
        period_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.period_var,
            values=periods,
            width=15,
            state="readonly"
        )
        period_cb.pack(side=tk.LEFT, padx=5)
        
        # Filter Jenis Grafik
        tk.Label(
            filter_frame,
            text="Jenis Grafik:",
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)
        
        chart_types = ["Line", "Bar", "Area"]
        self.chart_type_var = tk.StringVar(value="Line")
        chart_type_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.chart_type_var,
            values=chart_types,
            width=15,
            state="readonly"
        )
        chart_type_cb.pack(side=tk.LEFT, padx=5)
        
        # Tombol Update
        ttk.Button(
            filter_frame,
            text="Perbarui Grafik",
            style='Primary.TButton',
            command=self.update_grafik
        ).pack(side=tk.LEFT, padx=10)
    
    def create_grafik_section(self):
        """Membuat bagian grafik"""
        self.grafik_frame = tk.LabelFrame(
            self.frame,
            text="Grafik Penjualan",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        self.grafik_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    def create_summary_section(self):
        """Membuat bagian ringkasan statistik"""
        self.summary_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        self.summary_frame.pack(fill=tk.X, pady=(0, 10))
    
    def get_data_by_period(self):
        """Mengambil data berdasarkan periode yang dipilih"""
        periode = self.period_var.get()
        end_date = datetime.now()
        
        if periode == "Harian":
            start_date = end_date - timedelta(days=7)
            groupby = 'D'
        elif periode == "Mingguan":
            start_date = end_date - timedelta(weeks=12)
            groupby = 'W'
        elif periode == "Bulanan":
            start_date = end_date - timedelta(days=365)
            groupby = 'M'
        else:  # Tahunan
            start_date = end_date - timedelta(days=365*3)
            groupby = 'Y'
        
        # Ambil data dari database
        data = self.db.generate_laporan_penjualan(start_date, end_date)
        
        # Buat DataFrame
        df = pd.DataFrame(data['transaksi_list'])
        df['tanggal_transaksi'] = pd.to_datetime(df['tanggal_transaksi'])
        
        # Grouping berdasarkan periode
        grouped = df.groupby(pd.Grouper(key='tanggal_transaksi', freq=groupby))
        
        return grouped.agg({
            'total_harga': 'sum',
            'id_transaksi': 'count'
        }).reset_index()
    
    def update_grafik(self):
        """Memperbarui tampilan grafik"""
        try:
            # Hapus grafik lama
            for widget in self.grafik_frame.winfo_children():
                widget.destroy()
            
            # Ambil data
            df = self.get_data_by_period()
            
            if df.empty:
                messagebox.showinfo("Info", "Tidak ada data untuk ditampilkan")
                return
            
            # Buat figure baru
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            fig.patch.set_facecolor(self.colors['background'])
            
            # Format date untuk label
            df['tanggal_label'] = df['tanggal_transaksi'].dt.strftime('%Y-%m-%d')
            
            # Grafik Total Penjualan
            if self.chart_type_var.get() == "Line":
                ax1.plot(df['tanggal_label'], df['total_harga'], 
                        color=self.colors['primary'], marker='o')
                ax2.plot(df['tanggal_label'], df['id_transaksi'], 
                        color=self.colors['accent'], marker='o')
            elif self.chart_type_var.get() == "Bar":
                ax1.bar(df['tanggal_label'], df['total_harga'], 
                       color=self.colors['primary'])
                ax2.bar(df['tanggal_label'], df['id_transaksi'], 
                       color=self.colors['accent'])
            else:  # Area
                ax1.fill_between(df['tanggal_label'], df['total_harga'], 
                               color=self.colors['primary'], alpha=0.5)
                ax2.fill_between(df['tanggal_label'], df['id_transaksi'], 
                               color=self.colors['accent'], alpha=0.5)
            
            # Konfigurasi grafik penjualan
            ax1.set_title('Total Penjualan', color=self.colors['text'])
            ax1.tick_params(colors=self.colors['text'])
            ax1.set_xticklabels(df['tanggal_label'], rotation=45)
            ax1.grid(True, linestyle='--', alpha=0.7)
            
            # Konfigurasi grafik jumlah transaksi
            ax2.set_title('Jumlah Transaksi', color=self.colors['text'])
            ax2.tick_params(colors=self.colors['text'])
            ax2.set_xticklabels(df['tanggal_label'], rotation=45)
            ax2.grid(True, linestyle='--', alpha=0.7)
            
            # Atur layout
            plt.tight_layout()
            
            # Tambahkan canvas ke frame
            canvas = FigureCanvasTkAgg(fig, self.grafik_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Update ringkasan statistik
            self.update_summary(df)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui grafik: {str(e)}")
    
    def update_summary(self, df):
        """Memperbarui ringkasan statistik"""
        # Hapus ringkasan lama
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # Hitung statistik
        total_penjualan = df['total_harga'].sum()
        total_transaksi = df['id_transaksi'].sum()
        rata_rata = total_penjualan / total_transaksi if total_transaksi > 0 else 0
        
        summary_data = [
            ("Total Penjualan:", f"Rp {total_penjualan:,.2f}", self.colors['primary']),
            ("Total Transaksi:", str(total_transaksi), self.colors['accent']),
            ("Rata-rata per Transaksi:", f"Rp {rata_rata:,.2f}", self.colors['success'])
        ]
        
        for title, value, color in summary_data:
            container = tk.Frame(self.summary_frame, bg=self.colors['background'])
            container.pack(side=tk.LEFT, padx=20)
            
            tk.Label(
                container,
                text=title,
                font=('Arial', 10),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                text=value,
                font=('Arial', 10, 'bold'),
                bg=self.colors['background'],
                fg=color
            ).pack(side=tk.LEFT, padx=(5, 0))
