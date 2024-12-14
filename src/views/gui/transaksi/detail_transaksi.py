import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.database import DatabaseManager

class DetailTransaksi:
    def __init__(self, parent, colors, trans_id):
        """
        Inisialisasi window detail transaksi
        
        Args:
            parent: Widget parent untuk window ini
            colors: Dictionary berisi kode warna untuk UI
            trans_id: ID transaksi yang akan ditampilkan
        """
        self.parent = parent
        self.colors = colors
        self.trans_id = trans_id
        self.db = DatabaseManager()
        
        # Buat window baru
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Detail Transaksi - {trans_id}")
        self.window.geometry("600x700")
        self.window.configure(bg=self.colors['background'])
        
        # Load data transaksi
        self.load_transaction_data()
        
        # Jika data transaksi tidak ditemukan, hentikan inisialisasi
        if not hasattr(self, 'transaction'):
            return
        
        # Inisialisasi komponen UI
        self.create_header()
        self.create_transaction_info()
        self.create_items_section()
        self.create_payment_info()
        self.create_buttons()
        
        # Center window dan set modal
        self.window.transient(self.parent)
        self.window.grab_set()
        self.parent.wait_window(self.window)
        
    def load_transaction_data(self):
        """Memuat data transaksi"""
        transactions = self.db.get_all_transaksi()
        self.transaction = next(
            (t for t in transactions if t['id_transaksi'] == self.trans_id),
            None
        )
        
        if not self.transaction:
            messagebox.showerror(
                "Error",
                "Data transaksi tidak ditemukan"
            )
            self.window.destroy()
            return
            
    def create_header(self):
        """Membuat bagian header"""
        header_frame = tk.Frame(
            self.window,
            bg=self.colors['primary'],
            padx=20,
            pady=15
        )
        header_frame.pack(fill=tk.X)
        
        # Icon dan judul
        tk.Label(
            header_frame,
            text="🧾",  # Receipt emoji
            font=('Arial', 24),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            header_frame,
            text=f"Transaksi #{self.trans_id}",
            font=('Arial', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
    def create_transaction_info(self):
        """Membuat bagian informasi transaksi"""
        info_frame = tk.LabelFrame(
            self.window,
            text="Informasi Transaksi",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        info_data = [
            ("ID Transaksi", self.transaction['id_transaksi']),
            ("Tanggal", self.transaction['tanggal_transaksi'].strftime("%d/%m/%Y %H:%M")),
            ("ID Pelanggan", self.transaction['id_pelanggan']),
            ("Status", "Selesai"),
            ("Metode Pembayaran", self.transaction['metode_pembayaran'])
        ]
        
        for i, (label, value) in enumerate(info_data):
            tk.Label(
                info_frame,
                text=f"{label}:",
                font=('Arial', 10),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).grid(row=i, column=0, sticky='w', pady=5)
            
            tk.Label(
                info_frame,
                text=value,
                font=('Arial', 10, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']
            ).grid(row=i, column=1, sticky='w', padx=10, pady=5)
            
    def create_items_section(self):
        """Membuat bagian daftar item"""
        items_frame = tk.LabelFrame(
            self.window,
            text="Detail Item",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ('No', 'Produk', 'Harga', 'Qty', 'Subtotal')
        tree = ttk.Treeview(
            items_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        # Setup kolom
        tree.heading('No', text='No')
        tree.column('No', width=50)
        tree.heading('Produk', text='Produk')
        tree.column('Produk', width=200)
        tree.heading('Harga', text='Harga')
        tree.column('Harga', width=100)
        tree.heading('Qty', text='Qty')
        tree.column('Qty', width=50)
        tree.heading('Subtotal', text='Subtotal')
        tree.column('Subtotal', width=100)
        
        scrollbar = ttk.Scrollbar(
            items_frame,
            orient="vertical",
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if 'items' in self.transaction:
            for i, item in enumerate(self.transaction['items'], 1):
                subtotal = item['harga'] * item['jumlah']
                tree.insert(
                    '',
                    tk.END,
                    values=(
                        i,
                        item['nama_produk'],
                        f"Rp {item['harga']:,}",
                        item['jumlah'],
                        f"Rp {subtotal:,}"
                    )
                )
                
    def create_payment_info(self):
        """Membuat bagian informasi pembayaran"""
        payment_frame = tk.LabelFrame(
            self.window,
            text="Pembayaran",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=20,
            pady=10
        )
        payment_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        details_frame = tk.Frame(
            payment_frame,
            bg=self.colors['background']
        )
        details_frame.pack(fill=tk.X)
        
        payment_details = [
            ("Subtotal", self.transaction['total_harga']),
            ("Diskon", 0),  # Placeholder
            ("Total", self.transaction['total_harga'])
        ]
        
        for i, (label, value) in enumerate(payment_details):
            container = tk.Frame(
                details_frame,
                bg=self.colors['background']
            )
            container.pack(fill=tk.X, pady=2)
            
            tk.Label(
                container,
                text=label,
                font=('Arial', 10),
                bg=self.colors['background'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                container,
                text=f"Rp {value:,}",
                font=(
                    'Arial',
                    12 if label == "Total" else 10,
                    'bold' if label == "Total" else 'normal'
                ),
                bg=self.colors['background'],
                fg=self.colors['primary'] if label != "Total" else self.colors['success']
            ).pack(side=tk.RIGHT)
            
    def create_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(
            self.window,
            bg=self.colors['background']
        )
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Tombol Cetak
        tk.Button(
            button_frame,
            text="🖨 Cetak Struk",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.print_receipt
        ).pack(side=tk.LEFT)
        
        # Tombol Tutup
        tk.Button(
            button_frame,
            text="Tutup",
            font=('Arial', 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.window.destroy
        ).pack(side=tk.RIGHT)
        
    def print_receipt(self):
        """Handler untuk mencetak struk"""
        try:
            # Buat string untuk struk
            receipt_text = f"""
{'=' * 40}
            HALALHUB
       Sistem Manajemen Toko Muslim
{'=' * 40}

No. Transaksi : {self.transaction['id_transaksi']}
Tanggal      : {self.transaction['tanggal_transaksi'].strftime("%d/%m/%Y %H:%M")}
Pelanggan    : {self.transaction['id_pelanggan']}
{'=' * 40}

{'Detail Pembelian:'.center(40)}
{'-' * 40}
"""
            # Format item pembelian
            if 'items' in self.transaction:
                for i, item in enumerate(self.transaction['items'], 1):
                    subtotal = item['harga'] * item['jumlah']
                    receipt_text += f"{item['nama_produk'][:20]}\n"
                    receipt_text += f"{item['jumlah']} x Rp {item['harga']:,}\n"
                    receipt_text += f"{'Subtotal:':<20} Rp {subtotal:,}\n"
                    receipt_text += f"{'-' * 40}\n"

            # Total pembayaran
            receipt_text += f"\n{'Total:':<20} Rp {self.transaction['total_harga']:,}\n"
            receipt_text += f"Metode Bayar : {self.transaction['metode_pembayaran']}\n"

            receipt_text += f"\n{'=' * 40}\n"
            receipt_text += "Terima kasih telah berbelanja!\n"
            receipt_text += "Semoga berkah\n"
            receipt_text += f"{'=' * 40}"

            # Buat window preview struk
            preview_window = tk.Toplevel(self.window)
            preview_window.title("Preview Struk")
            preview_window.geometry("400x600")
            preview_window.configure(bg=self.colors['background'])

            # Area teks untuk preview
            preview_text = tk.Text(
                preview_window,
                font=('Courier New', 10),
                bg='white',
                fg=self.colors['text'],
                padx=10,
                pady=10
            )
            preview_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Masukkan teks struk
            preview_text.insert('1.0', receipt_text)
            preview_text.configure(state='disabled')

            # Frame untuk tombol
            button_frame = tk.Frame(
                preview_window,
                bg=self.colors['background']
            )
            button_frame.pack(fill=tk.X, padx=20, pady=10)

            def save_receipt():
                filename = f"struk_{self.trans_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(receipt_text)
                messagebox.showinfo(
                    "Sukses",
                    f"Struk berhasil disimpan ke file {filename}"
                )

            tk.Button(
                button_frame,
                text="💾 Simpan ke File",
                font=('Arial', 10),
                bg=self.colors['success'],
                fg='white',
                padx=20,
                pady=10,
                command=save_receipt
            ).pack(side=tk.LEFT, padx=5)

            def send_to_printer():
                try:
                    import win32print
                    import win32ui
                    import win32con
                    
                    # Dapatkan printer default
                    printer_name = win32print.GetDefaultPrinter()
                    hprinter = win32print.OpenPrinter(printer_name)
                    printer_info = win32print.GetPrinter(hprinter, 2)

                    # Buat DC printer
                    dc = win32ui.CreateDC()
                    dc.CreatePrinterDC(printer_name)

                    # Mulai dokumen
                    dc.StartDoc('Struk HalalHub')
                    dc.StartPage()

                    y = 100
                    for line in receipt_text.split('\n'):
                        dc.TextOut(100, y, line)
                        y += 50

                    # Selesai
                    dc.EndPage()
                    dc.EndDoc()

                    # Cleanup
                    del dc
                    win32print.ClosePrinter(hprinter)

                    messagebox.showinfo(
                        "Sukses",
                        "Struk berhasil dicetak"
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Gagal mencetak struk: {str(e)}\n"
                        "Pastikan printer sudah terhubung dan terinstall dengan benar"
                    )

            tk.Button(
                button_frame,
                text="🖨 Cetak",
                font=('Arial', 10),
                bg=self.colors['primary'],
                fg='white',
                padx=20,
                pady=10,
                command=send_to_printer
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame,
                text="Tutup",
                font=('Arial', 10),
                bg=self.colors['secondary'],
                fg='white',
                padx=20,
                pady=10,
                command=preview_window.destroy
            ).pack(side=tk.RIGHT)

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan saat membuat struk: {str(e)}"
            )
