from typing import Dict, List, Optional
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
                if all(k in data for k in ['id_pesanan', 'id_pelanggan', 'id_produk', 
                                         'jumlah_dipesan', 'total_harga', 'status', 
                                         'tanggal_pesanan']):    
                    data['jumlah_dipesan'] = int(data['jumlah_dipesan'])
                    data['total_harga'] = float(data['total_harga'])
                    
                    pesanan = Pesanan(**data)
                    self.daftar_pesanan.append(pesanan)
                    
        except Exception as e:
            print(f"Error loading pesanan: {str(e)}")
            self.daftar_pesanan = []

    def buat_pesanan(self, data_pesanan: Dict, produk: Produk) -> Optional[Pesanan]:
        """Membuat pesanan baru dengan validasi stok"""
        try:
            # Validasi stok - konversi ke int
            current_stok = int(produk.stok)  # Konversi stok ke integer
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

            if hasattr(self, 'notification'):
                self.notification.check_stock_notification({
                    'id_produk': produk.id_produk,
                    'nama_produk': produk.nama_produk,
                    'stok': current_stok - jumlah_pesan
                })

            return pesanan

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
            pesanan.status = "Dibatalkan"
            
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
            return True
        return False
        
    def mark_as_done(self, id_pesanan: str) -> bool:
        """Menandai pesanan sebagai selesai dan membuat transaksi"""
        try:
            pesanan = self.get_pesanan(id_pesanan)
            if not pesanan or pesanan.status == "Dibatalkan":
                return False
            
            # Update status pesanan
            if self.db.update_pesanan_status(id_pesanan, "Selesai"):
                # Buat transaksi baru
                transaksi_data = {
                    'id_transaksi': f"TRX{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'id_pesanan': id_pesanan,
                    'total_harga': pesanan.total_harga,
                    'metode_pembayaran': 'Tunai',
                    'tanggal_transaksi': datetime.now().isoformat()
                }
                
                # Simpan transaksi
                if self.db.add_transaksi(transaksi_data):
                    return True
            return False
            
        except Exception as e:
            print(f"Error marking order as done: {str(e)}")
            return False
    
    def update_pesanan(self, updated_data: Dict) -> bool:
        """Memperbarui data pesanan"""
        try:
            pesanan_list = self.get_all_pesanan()
            updated = False
            
            for pesanan in pesanan_list:
                if pesanan['id_pesanan'] == updated_data['id_pesanan']:
                    # Update data yang diperlukan
                    pesanan.update({
                        'id_pelanggan': updated_data.get('id_pelanggan', pesanan['id_pelanggan']),
                        'id_produk': updated_data.get('id_produk', pesanan['id_produk']),
                        'jumlah_dipesan': updated_data.get('jumlah_dipesan', pesanan['jumlah_dipesan']),
                        'total_harga': updated_data.get('total_harga', pesanan['total_harga']),
                        'status': updated_data.get('status', pesanan['status']),
                        'tanggal_pesanan': updated_data.get('tanggal_pesanan', pesanan['tanggal_pesanan'])
                    })
                    updated = True
                    break
                
            if updated:
                return self.csv_handler.write_csv(
                    self.file_paths['pesanan'],
                    pesanan_list,
                    self.field_definitions['pesanan']
                )
            return False
        
        except Exception as e:
            print(f"Error updating order: {str(e)}")
            return False