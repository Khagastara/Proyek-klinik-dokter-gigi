import dokter as dok
import staff as sta
import pasien as pas
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print("\n" + "+" + "-"*60 + "+")
        print("| {:<58} |".format("Selamat Datang di Klinik Dokter Gigi drg. Dewi Kusumawati"))
        print("+" + "-"*60 + "+")
        print("| {:<58} |".format("1. Masuk sebagai Doktor"))
        print("| {:<58} |".format("2. Masuk sebagai Staff"))
        print("| {:<58} |".format("3. Masuk sebagai Pasien"))
        print("+" + "-"*60 + "+")
        login = int(input(f"Masukkan pilihan: "))
        
        if login == 1:
            dok.menuDokter()
            break
        elif login == 2:
            sta.menuStaff()
            break
        elif login == 3:
            pas.menuPasien()
            
        else:
            print("Pilihan invalid")
            
if __name__ == "__main__":
    main()
