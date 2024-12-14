from typing import Dict, List, Optional, Tuple
from datetime import datetime
from models.pesanan import Pesanan
from models.produk import Produk
from utils.database import DatabaseManager

class PesananController:
    """Controller untuk manajemen pesanan"""
   
    def __init__(self):
        self.db = DatabaseManager()
        self.daftar_pesanan = []
        self._load_pesanan()
   
    def _load_pesanan(self):
        """Load pesanan dari database"""
        try:
            pesanan_data = self.db.get_all_pesanan()
            self.daftar_pesanan = []
            for data in pesanan_data:
                pesanan = Pesanan(
                    id_pesanan=data['id_pesanan'],
                    id_pelanggan=data['id_pelanggan'],
                    id_produk=data['id_produk'],
                    jumlah_dipesan=int(data['jumlah_dipesan']),
                    total_harga=float(data['total_harga']),
                    status=data['status'],
                    tanggal_pesanan=data['tanggal_pesanan']
                )
                self.daftar_pesanan.append(pesanan)
        except Exception as e:
            print(f"Error loading pesanan: {str(e)}")
            self.daftar_pesanan = []

    def buat_pesanan(self, data_pesanan: Dict, produk: Produk) -> Optional[Pesanan]:
        """Membuat pesanan baru dengan validasi stok"""
        try:
            # Validasi stok - konversi ke int
            current_stok = int(produk.stok)
            jumlah_pesan = int(data_pesanan.get('jumlah_dipesan', 0))
            
            if current_stok < jumlah_pesan:
                print("Stok tidak mencukupi")
                return None
                
            pesanan_data = {
                'id_pesanan': data_pesanan['id_pesanan'],
                'id_pelanggan': data_pesanan['id_pelanggan'],
                'id_produk': data_pesanan['id_produk'],
                'jumlah_dipesan': jumlah_pesan,
                'total_harga': float(produk.harga) * jumlah_pesan,
                'status': 'Pending',
                'tanggal_pesanan': datetime.now().isoformat()
            }
    
            # Simpan ke database
            if self.db.add_pesanan(pesanan_data):
                # Update stok produk
                stok_baru = current_stok - jumlah_pesan
                if self.db.update_produk(produk.id_produk, {'stok': stok_baru}):
                    pesanan = Pesanan(**pesanan_data)
                    self.daftar_pesanan.append(pesanan)
                    print(f"Pesanan berhasil dibuat: {pesanan.id_pesanan}")
                    return pesanan
                    
            return None
    
        except Exception as e:
            print(f"Error membuat pesanan: {str(e)}")
            return None
        
    def lihat_daftar_pesanan(self, filter_status: Optional[str] = None) -> List[Pesanan]:
        """Melihat daftar pesanan dengan optional filter status"""
        self._load_pesanan()  # Refresh data from database
        if not filter_status:
            return self.daftar_pesanan
        return [p for p in self.daftar_pesanan if p.status == filter_status]
        
    def get_pesanan(self, id_pesanan: str) -> Optional[Pesanan]:
        """Mendapatkan detail pesanan berdasarkan ID"""
        return next((p for p in self.daftar_pesanan if p.id_pesanan == id_pesanan), None)
        
    def cancel_pesanan(self, id_pesanan: str) -> bool:
        """Membatalkan pesanan dan mengembalikan stok"""
        pesanan = self.get_pesanan(id_pesanan)
        if not pesanan or pesanan.status == "Selesai":
            return False
            
        # Update status pesanan di database
        if self.db.update_pesanan_status(id_pesanan, "Dibatalkan"):
            # Kembalikan stok
            produk = next(
                (p for p in self.db.get_all_produk() if p['id_produk'] == pesanan.id_produk),
                None
            )
            if produk:
                self.db.update_produk(
                    pesanan.id_produk,
                    {'stok': int(produk['stok']) + pesanan.jumlah_dipesan}
                )
            self._load_pesanan()  # Reload daftar pesanan
            return True
        return False
        
    def mark_as_done(self, id_pesanan: str) -> Tuple[bool, str]:
        """Menandai pesanan sebagai selesai dan membuat transaksi baru"""
        pesanan = self.get_pesanan(id_pesanan)
        if not pesanan:
            return False, "Pesanan tidak ditemukan"

        if pesanan.status == "Dibatalkan":
            return False, "Tidak dapat menyelesaikan pesanan yang sudah dibatalkan"

        if pesanan.status == "Selesai":
            return False, "Pesanan sudah selesai"

        # Update status pesanan ke Selesai
        if self.db.update_pesanan_status(id_pesanan, "Selesai"):
            try:
                # Buat data transaksi baru
                transaksi_data = {
                    'id_transaksi': f"TRX{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'id_pesanan': id_pesanan,
                    'total_harga': pesanan.total_harga,
                    'metode_pembayaran': 'Tunai',  # Default ke Tunai untuk saat ini
                    'tanggal_transaksi': datetime.now().isoformat()
                }

                # Simpan transaksi ke database
                if self.db.add_transaksi(transaksi_data):
                    self._load_pesanan()  # Reload daftar pesanan
                    return True, "Pesanan berhasil diselesaikan"
                else:
                    # Rollback status pesanan jika gagal membuat transaksi
                    self.db.update_pesanan_status(id_pesanan, "Pending")
                    return False, "Gagal membuat transaksi"

            except Exception as e:
                # Rollback status pesanan jika terjadi error
                self.db.update_pesanan_status(id_pesanan, "Pending")
                return False, f"Error saat membuat transaksi: {str(e)}"

        return False, "Gagal menyelesaikan pesanan"

    def update_pesanan(self, data_pesanan: Dict) -> Tuple[bool, str]:
        """Memperbarui data pesanan yang sudah ada"""
        try:
            # Get existing pesanan
            old_pesanan = self.get_pesanan(data_pesanan['id_pesanan'])
            if not old_pesanan:
                return False, "Pesanan tidak ditemukan"

            # Get product info
            product = next(
                (p for p in self.db.get_all_produk() 
                 if p['id_produk'] == data_pesanan['id_produk']),
                None
            )
            if not product:
                return False, "Produk tidak ditemukan"

            # Calculate stock changes
            old_qty = old_pesanan.jumlah_dipesan
            new_qty = int(data_pesanan['jumlah_dipesan'])
            stock_change = old_qty - new_qty

            # Validate new stock
            current_stock = int(product['stok'])
            if current_stock + stock_change < 0:
                return False, "Stok tidak mencukupi"

            # Prepare update data
            update_data = {
                'id_pesanan': data_pesanan['id_pesanan'],
                'id_pelanggan': data_pesanan['id_pelanggan'],
                'id_produk': data_pesanan['id_produk'],
                'jumlah_dipesan': new_qty,
                'total_harga': float(product['harga']) * new_qty,
                'status': 'Pending',
                'tanggal_pesanan': datetime.now().isoformat()
            }

            # Update order in database
            if self.db.update_pesanan(update_data):
                # Update product stock
                new_stock = current_stock + stock_change
                self.db.update_produk(product['id_produk'], {'stok': new_stock})
                self._load_pesanan()  # Reload orders
                return True, "Pesanan berhasil diperbarui"

            return False, "Gagal memperbarui pesanan"

        except Exception as e:
            print(f"Error updating order: {str(e)}")
            return False, str(e)