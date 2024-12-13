from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Aksi:
    """
    Model untuk aksi sistem
    """
    pilih_aksi: str
    daftar_aksi: List[str] = field(default_factory=list)
    
    def tampilkan_aksi(self) -> List[str]:
        """Menampilkan pilihan aksi yang tersedia"""
        return self.daftar_aksi
    
    def pilih_aksi(self, aksi: str) -> Optional[str]:
        """Memilih aksi tertentu dari daftar pilihan"""
        if aksi not in self.daftar_aksi:
            return None
        self.pilih_aksi = aksi
        return aksi
