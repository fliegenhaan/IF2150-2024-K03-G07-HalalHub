# src/views/gui/laporan/laporan_penjualan.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from utils.database import DatabaseManager

class LaporanPenjualan:
    def __init__(self, parent, colors):
        """Inisialisasi halaman laporan penjualan"""
        self.parent = parent
        self.colors = colors
        self.db = DatabaseManager()

        # Initialize variables
        self.total_var = tk.StringVar(value="0 Transaksi")

        # Frame utama
        self.frame = tk.Frame(self.parent, bg=self.colors['background'])
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create header
        self.create_header()

        # Inisialisasi komponen UI
        self.create_filter_section()
        self.create_summary_section()
        self.create_table_section()
        self.create_chart_section()

        # Load data awal
        self.refresh_data()

    def create_header(self):
        """Membuat bagian header"""
        header_frame = tk.Frame(
            self.frame,
            bg=self.colors['primary'],
            padx=20,
            pady=15
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Label judul
        tk.Label(
            header_frame,
            text="Laporan Penjualan",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)

        # Total transaksi
        tk.Label(
            header_frame,
            textvariable=self.total_var,
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.RIGHT)
    
    def create_filter_section(self):
        """Membuat bagian filter laporan"""
        filter_frame = tk.LabelFrame(
            self.frame,
            text="Filter",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=10,
            pady=10
        )
        filter_frame.pack(fill=tk.X, pady=(0, 20))

        # Periode filter
        tk.Label(
            filter_frame,
            text="Periode:",
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=5)

        periods = [
            "Hari Ini",
            "7 Hari Terakhir", 
            "30 Hari Terakhir",
            "Bulan Ini",
            "Semua"
        ]

        self.period_var = tk.StringVar(value="Hari Ini")
        period_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.period_var,
            values=periods,
            width=15,
            state="readonly"
        )
        period_cb.pack(side=tk.LEFT, padx=5)

        # Tombol refresh
        ttk.Button(
            filter_frame,
            text="🔄 Refresh",
            command=self.refresh_data,  # Tambahkan di sini
            style='Primary.TButton'
        ).pack(side=tk.RIGHT, padx=5)

        # Bind event
        period_cb.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())  # Dan di sini
    
    def create_summary_section(self):
        """Membuat bagian ringkasan"""
        summary_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Initialize summary variables
        self.summary_vars = {
            'total_penjualan': tk.StringVar(value="Rp 0"),
            'total_transaksi': tk.StringVar(value="0"),
            'rata_rata': tk.StringVar(value="Rp 0")
        }
        
        # Create summary cards
        summaries = [
            ("Total Penjualan", self.summary_vars['total_penjualan'], self.colors['success']),
            ("Total Transaksi", self.summary_vars['total_transaksi'], self.colors['primary']),
            ("Rata-rata Transaksi", self.summary_vars['rata_rata'], self.colors['accent'])
        ]
        
        for title, var, color in summaries:
            card = tk.Frame(
                summary_frame,
                bg='white',
                padx=15,
                pady=10,
                relief=tk.RAISED,
                bd=1
            )
            card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            
            tk.Label(
                card,
                text=title,
                font=('Arial', 10),
                bg='white',
                fg=self.colors['text']
            ).pack()
            
            tk.Label(
                card,
                textvariable=var,
                font=('Arial', 16, 'bold'),
                bg='white',
                fg=color
            ).pack()

    def update_summary(self, report):
        """Update bagian ringkasan dengan data baru"""
        try:
            total_penjualan = report['total_penjualan']
            total_transaksi = report['jumlah_transaksi']
            rata_rata = total_penjualan / total_transaksi if total_transaksi > 0 else 0
            
            self.summary_vars['total_penjualan'].set(f"Rp {total_penjualan:,.2f}")
            self.summary_vars['total_transaksi'].set(str(total_transaksi))
            self.summary_vars['rata_rata'].set(f"Rp {rata_rata:,.2f}")
        except Exception as e:
            print(f"Error updating summary: {str(e)}")

    def create_table_section(self):
        """Membuat tabel laporan penjualan"""
        table_frame = tk.LabelFrame(
            self.frame,
            text="Detail Transaksi",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buat Treeview
        columns = ('ID Transaksi','Tanggal', 'Produk', 'Qty', 'Total')
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
        """Membuat grafik penjualan"""
        self.chart_frame = tk.LabelFrame(
            self.frame,
            text="Grafik Penjualan",
            bg=self.colors['background'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
    
    def update_table(self, transactions):
        """Memperbarui tabel transaksi"""
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Masukkan data baru
        for trans in transactions:
            try:
                tanggal = datetime.fromisoformat(trans['tanggal_transaksi'])
                self.tree.insert(
                    '',
                    tk.END,
                    values=(
                        tanggal.strftime("%d/%m/%Y %H:%M"),  # Tanggal
                        trans['id_transaksi'],               # No Transaksi
                        trans.get('nama_produk', '-'),       # Produk
                        trans.get('jumlah', '1'),            # Qty
                        f"Rp {float(trans['total_harga']):,}" # Total
                    )
                )
            except Exception as e:
                print(f"Error displaying transaction: {str(e)}")
                continue
    
    def update_chart(self, transactions):
        """Memperbarui grafik penjualan"""
        # Hapus widget lama
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if not transactions:
            tk.Label(
                self.chart_frame,
                text="Tidak ada data transaksi",
                font=('Arial', 12),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(pady=20)
            return
            
        try:
            # Buat DataFrame dari transaksi
            df = pd.DataFrame(transactions)
            df['tanggal_transaksi'] = pd.to_datetime(df['tanggal_transaksi'])
            daily_sales = df.groupby('tanggal_transaksi')['total_harga'].sum()
            
            # Buat grafik baru
            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            
            ax.plot(daily_sales.index, daily_sales.values, color=self.colors['primary'], marker='o')
            ax.set_title('Trend Penjualan Harian', color=self.colors['text'])
            ax.tick_params(colors=self.colors['text'])
            
            # Rotasi label tanggal
            plt.xticks(rotation=45)
            
            # Tambahkan canvas ke frame
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        except Exception as e:
            print(f"Error creating chart: {str(e)}")

    def export_report(self):
        """Export data laporan ke Excel"""
        try:
            # Refresh data terlebih dahulu
            self.refresh_data()  # Tambahkan di sini

            # Get date range
            end_date = datetime.now()
            start_date = self.get_start_date()

            # Create filename
            filename = f"Laporan_Penjualan_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.xlsx"

            # Get data from treeview
            data = []
            for item in self.tree.get_children():
                data.append(self.tree.item(item)['values'])

            # Create DataFrame
            df = pd.DataFrame(data, columns=[
                'ID Transaksi',
                'Tanggal',
                'Produk',
                'Total Item',
                'Total Harga',
                'Metode Pembayaran'
            ])

            # Export to Excel
            df.to_excel(filename, index=False)

            messagebox.showinfo(
                "Sukses",
                f"Data berhasil diekspor ke {filename}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal mengekspor data: {str(e)}"
            )

    def refresh_data(self):
        """Memperbarui tampilan data"""
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Get date range
            end_date = datetime.now()
            start_date = self.get_start_date()

            # Get report data
            report = self.db.generate_laporan_penjualan(start_date, end_date)

            # Update total
            self.total_var.set(f"{report['jumlah_transaksi']} Transaksi")

            # Update summary
            self.update_summary(report)

            # Display transactions
            for trans in report['transaksi_list']:
                try:
                    tanggal = datetime.fromisoformat(trans['tanggal_transaksi'])
                    self.tree.insert(
                        '',
                        tk.END,
                        values=(
                            trans['id_transaksi'],
                            tanggal.strftime("%d/%m/%Y %H:%M"),
                            trans.get('id_pelanggan', '-'),
                            trans.get('total_item', '1'),
                            f"Rp {float(trans['total_harga']):,}",
                            trans.get('metode_pembayaran', 'Tunai')
                        )
                    )
                except Exception as e:
                    print(f"Error displaying transaction: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error refreshing data: {str(e)}")
            messagebox.showerror(
                "Error",
                "Gagal memuat data. Silakan coba lagi."
            )

    def get_start_date(self) -> datetime:
        """Mendapatkan tanggal awal berdasarkan periode yang dipilih"""
        period = self.period_var.get()
        now = datetime.now()

        if period == "Hari Ini":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "7 Hari Terakhir":
            return now - timedelta(days=7)
        elif period == "30 Hari Terakhir":
            return now - timedelta(days=30)
        elif period == "Bulan Ini":
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:  # Semua
            # Kembali ke tanggal paling awal (misalnya 1 tahun yang lalu)
            return now - timedelta(days=365)