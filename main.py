import dokter as dok
import staff as sta
import pasien as pas

def main():
    while True:
        print("\nSelamat Datang di Klinik Dokter Gigi drg. Dewi Kusumawati")
        print("1. Masuk sebagai Doktor")
        print("2. Masuk sebagai Staff")
        print("3. Masuk sebagai Pasien")
        login = input(f"Masukkan pilihan: ")
        
        if login == 1:
            dok.menuDokter()
        elif login == 2:
            sta.menuStaff()
        elif login == 3:
            pas.menuPasien()
        else:
            print("Pilihan invalid")
            
