from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Transaksi:
    """
    Model untuk transaksi
    """
    riwayat_transaksi: List[Dict] = field(default_factory=list)
    
    def tampil_transaksi(self, filter_date: Optional[datetime] = None) -> List[Dict]:
        """Menampilkan daftar transaksi yang telah dilakukan"""
        if not filter_date:
            return self.riwayat_transaksi
            
        return [
            transaksi for transaksi in self.riwayat_transaksi
            if transaksi.get("tanggal_transaksi").date() == filter_date.date()
        ]
    
    def tambah_transaksi(self, pesanan: Dict) -> None:
        """Menambahkan transaksi baru ke riwayat"""
        transaksi = {
            "id_transaksi": f"TRX{len(self.riwayat_transaksi) + 1:04d}",
            "tanggal_transaksi": datetime.now(),
            "detail_pesanan": pesanan,
            "total_harga": pesanan.get("total_harga", 0)
        }
        self.riwayat_transaksi.append(transaksi)
