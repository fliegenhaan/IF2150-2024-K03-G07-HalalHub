from typing import Dict, List, Optional
from models.produk import Produk
from utils.database import DatabaseManager

class ProdukController:
    def __init__(self, db_path=None):
        self.db = DatabaseManager(db_path)

    def get_all_produk(self) -> List[Dict]:
        """Mengambil semua data produk"""
        return self.db.get_all_produk()
        
    def get_produk(self, id_produk: str) -> Optional[Produk]:
        """Mengambil detail satu produk"""
        try:
            data = self.db.get_produk(id_produk)
            if data and len(data) > 0:
                return Produk(**data[0])
            return None
        except Exception as e:
            print(f"Error getting product: {str(e)}")
            return None
        
    def tambah_produk(self, data_produk: Dict) -> bool:
        """Menambahkan produk baru"""
        if 'deskripsi' not in data_produk:
            data_produk['deskripsi'] = ""
        return self.db.add_produk(data_produk)
        
    def update_produk(self, id_produk: str, data_produk: Dict) -> bool:
        """Memperbarui data produk"""
        if 'deskripsi' not in data_produk:
            data_produk['deskripsi'] = ""
        return self.db.update_produk(id_produk, data_produk)
        
    def delete_produk(self, id_produk: str) -> bool:
        """Menghapus produk"""
        return self.db.delete_produk(id_produk)
        
    def update_stok(self, id_produk: str, jumlah_perubahan: int) -> bool:
        """
        Memperbarui stok produk
        Positif untuk penambahan, negatif untuk pengurangan
        """
        produk = self.get_produk(id_produk)
        if not produk:
            return False
            
        stok_baru = produk.stok + jumlah_perubahan
        if stok_baru < 0:
            return False
            
        # Update stok
        success = self.update_produk(id_produk, {'stok': stok_baru})
        
        # Cek notifikasi stok jika berhasil update
        if success and hasattr(self, 'notification'):
            self.notification.check_stock_notification({
                'id_produk': id_produk,
                'nama_produk': produk.nama_produk,
                'stok': stok_baru
            })
            
        return success