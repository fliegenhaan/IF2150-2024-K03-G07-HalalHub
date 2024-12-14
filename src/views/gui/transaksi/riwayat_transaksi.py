import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pandas as pd
from utils.database import DatabaseManager
from .detail_transaksi import DetailTransaksi

class RiwayatTransaksi:
    def __init__(self, parent, colors):
        """
        Inisialisasi halaman riwayat transaksi
        
        Args:
            parent: Widget parent untuk frame ini
            colors: Dictionary berisi kode warna untuk UI
        """
        self.parent = parent
        self.colors = colors
        self.db = DatabaseManager()
        
        # Frame utama
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['background']
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_filter_section()
        self.create_summary_section()
        self.create_table()
        self.create_action_buttons()
        
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
        
        # Label judul dengan icon
        tk.Label(
            header_frame,
            text="💰",  # Money bag emoji
            font=('Arial', 24),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            header_frame,
            text="Riwayat Transaksi",
            font=('Arial', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Total transaksi
        self.total_var = tk.StringVar(value="0 Transaksi")
        tk.Label(
            header_frame,
            textvariable=self.total_var,
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.RIGHT)
        
    def create_filter_section(self):
        """Membuat bagian filter transaksi"""
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
            command=self.refresh_data,
            style='Primary.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # Bind event
        period_cb.bind('<<ComboboxSelected>>', lambda e: self.refresh_data())
        
    def create_summary_section(self):
        """Membuat bagian ringkasan transaksi"""
        self.summary_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        self.summary_frame.pack(fill=tk.X, pady=(0, 20))
        
    def create_table(self):
        """Membuat tabel riwayat transaksi"""
        table_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Buat Treeview
        columns = (
            'ID Transaksi',
            'Tanggal',
            'Pelanggan',
            'Total Item',
            'Total Harga',
            'Metode Pembayaran'
        )
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Setup kolom
        for col in columns:
            self.tree.heading(col, text=col)
            width = 150 if col in ['Pelanggan', 'Metode Pembayaran'] else 100
            self.tree.column(col, width=width, anchor='center')
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click
        self.tree.bind('<Double-1>', self.on_double_click)
        
    def create_action_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(
            self.frame,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X)
        
        # Tombol Export
        tk.Button(
            button_frame,
            text="📊 Export ke Excel",
            font=('Arial', 10),
            bg=self.colors['success'],
            fg='white',
            padx=20,
            pady=10,
            command=self.export_to_excel
        ).pack(side=tk.LEFT)
        
        # Tombol Cetak
        tk.Button(
            button_frame,
            text="🖨 Cetak",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.print_report
        ).pack(side=tk.LEFT, padx=10)
        
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
                    # Convert string to datetime
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
            
    def get_start_date(self):
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
            return datetime.min
            
    def update_summary(self, transactions):
        """Memperbarui ringkasan transaksi"""
        # Clear existing summary
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
            
        # Calculate summary
        total_transactions = len(transactions['transaksi_list'])
        total_revenue = transactions['total_penjualan']
        avg_transaction = total_revenue / total_transactions if total_transactions > 0 else 0
        
        # Create summary cards
        summaries = [
            ("Total Transaksi", str(total_transactions), self.colors['primary']),
            ("Total Pendapatan", f"Rp {total_revenue:,}", self.colors['success']),
            ("Rata-rata Transaksi", f"Rp {avg_transaction:,.2f}", self.colors['accent'])
        ]
        
        for title, value, color in summaries:
            card = tk.Frame(
                self.summary_frame,
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
                text=value,
                font=('Arial', 16, 'bold'),
                bg='white',
                fg=color
            ).pack()
            
    def on_double_click(self, event):
        """Handler untuk double click pada transaksi"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Get selected transaction
        trans_id = self.tree.item(selected[0])['values'][0]
        
        # Show detail window
        DetailTransaksi(self.parent, self.colors, trans_id)
        
    def export_to_excel(self):
        """Export data transaksi ke Excel"""
        # Get date range
        end_date = datetime.now()
        start_date = self.get_start_date()
        
        try:
            # Get transactions
            transactions = self.db.generate_laporan_penjualan(
                start_date,
                end_date
            )
            
            # Create DataFrame
            df = pd.DataFrame(transactions['transaksi_list'])
            
            # Export to Excel
            filename = f"Transaksi_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.xlsx"
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
            
    def print_report(self):
        """Mencetak laporan transaksi"""
        # TODO: Implement print functionality
        messagebox.showinfo(
            "Info",
            "Fitur cetak laporan belum tersedia"
        )