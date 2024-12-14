from typing import List, Dict, Optional
from datetime import datetime

class NotificationController:
    """Controller untuk sistem notifikasi"""
    
    def __init__(self):
        self.BATAS_STOK_MINIMUM = 10  # Batas minimum stok sebelum notifikasi
        self.notifikasi_list = []
        
    def cek_stok_menipis(self, produk: Dict) -> bool:
        """
        Mengecek apakah stok produk sudah menipis
        """
        return int(produk['stok']) <= self.BATAS_STOK_MINIMUM
        
    def beri_notifikasi(self, stok_info: Dict) -> Optional[Dict]:
        """
        Memberikan notifikasi berdasarkan info stok
        """
        if not self.cek_stok_menipis(stok_info):
            return None
            
        stok = int(stok_info['stok'])
        notif_type = 'error' if stok == 0 else 'warning'
            
        notifikasi = {
            'id_produk': stok_info['id_produk'],
            'nama_produk': stok_info['nama_produk'],
            'stok_tersisa': stok,
            'timestamp': datetime.now(),
            'title': 'Peringatan Stok',
            'message': f"Stok {stok_info['nama_produk']} tinggal {stok} unit!",
            'type': notif_type
        }
        
        self.notifikasi_list.append(notifikasi)
        return notifikasi
        
    def get_semua_notifikasi(self) -> List[Dict]:
        """
        Mengambil semua notifikasi yang ada
        """
        return self.notifikasi_list
        
    def hapus_notifikasi(self, id_produk: str) -> bool:
        """
        Menghapus notifikasi untuk produk tertentu
        """
        initial_length = len(self.notifikasi_list)
        self.notifikasi_list = [n for n in self.notifikasi_list 
                               if n['id_produk'] != id_produk]
        return len(self.notifikasi_list) < initial_length
