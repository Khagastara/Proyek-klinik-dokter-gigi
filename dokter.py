import psycopg2
from tabulate import tabulate
import os
import main as ma

def connect():
    return psycopg2.connect(
        database='Proyek klinik',
        user='postgres',
        password='082143',
        host='localhost',
        port=5432
        )

# Melihat isi pasien
def read_pasien():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM pasien ORDER BY id_pasien ASC"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

def read_rekam_medis():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM rekam_medis ORDER BY nomor_rekam ASC"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()
    
def search_rekam_pasien():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    search_pasien = input("Masukkan nama pasien yang dicari: ")
    query = f"""SELECT p.id_pasien, p.nama, r.nomor_rekam, r.tanggal_pemeriksaan, r.hasil_pemeriksaan, r.diagnosis
            FROM pasien p
            JOIN rekam_medis r ON(p.id_pasien = r.id_pasien)
            WHERE p.nama ILIKE '{search_pasien}'"""
    cur.execute(query)
    data = cur.fetchall()
    
    if data:
        col_names = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=col_names, tablefmt="outline"))
    else:
        print(f"Tidak ada {search_pasien} di dalam rekam medis tersebut")
        
    cur.close()
    conn.close()
    
# Melihat isi resep obat
def read_resep_obat():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM resep_obat ORDER BY id_resep ASC"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

# Menambah obat pada resep obat
def add_resep_obat():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    total_input = int(input(f"Mau menambahkan berapa jenis obat?: "))
    
    for _ in range(total_input):
        id_dokter = 1
        daftar_obat = input(f"Masukkan nama obat: ")
        jumlah_obat = int(input(f"Berapa jumlah obat yang dipunyai: "))
        harga = int(input(f"Masukkan harga obat tersebut: "))
        query = f"INSERT INTO resep_obat(id_dokter, daftar_obat, jumlah_obat, harga) VALUES(%s, %s, %s, %s)"
    cur.execute(query, (id_dokter, daftar_obat, jumlah_obat, harga))
    conn.commit()
    read_resep_obat()
    cur.close
    conn.close()
    
def renew_resep():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    read_resep_obat()
    id_resep = input('Masukkan id resep obat yang ingin diupdate: ')
    
    print("Pilih atribut yang ingin diperbarui: ")
    print("1. Jumlah Obat")
    print("2. Harga")
    pilihan = int(input("Masukkan pilihan: "))
    
    if pilihan == 1:
        update = input("Masukkan hasil pemeriksaan yang diubah: ")
        update_attribut = 'jumlah_obat'
        
    elif pilihan == 2:
        update = input("Masukkan diagnosis yang diubah: ")
        update_attribut = 'harga'

    else:
        print("Pilihan invalid")
        cur.close()
        conn.close()
        return
    
    while True:
        konfirmasi = input("Apakah Anda yakin ingin menyimpan transaksi ini? (yes/no): ")
        if konfirmasi.lower() == 'yes':
            conn.commit()
            query = f"UPDATE resep_obat SET {update_attribut} = '{update}' WHERE id_resep = '{id_resep}'"
            cur.execute(query)
            conn.commit()
            
            os.system("cls")
            update_rekam = f"SELECT * from resep_obat WHERE id_resep = '{id_resep}'"
            cur.execute(update_rekam)
            
            data = cur.fetchall()               
            col_names = [desc[0] for desc in cur.description]
            print("Update Rekam Medis telah selesai")
            print(tabulate(data, headers=col_names, tablefmt="outline"))
            break
            
        elif konfirmasi.lower() == 'no':
            conn.rollback()
            print("Update Rekam Medis Dibatalkan")
            break
        
        else:
            print("Pilihan invalid")
        
    conn.commit()
    print(f"Total baris yang diperbarui: {cur.rowcount}")
    cur.close()
    conn.close()
    
def delete_resep():
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    read_resep_obat()
    id_resep = input('Masukkan id resep obat yang ingin dihapus: ')
    
    while True:
        konfirmasi = input(f"Apakah Anda yakin ingin menghapus dengan angka id resep {id_resep} ini?: (yes/no)")
        if konfirmasi.lower() == 'yes':
            query_delete = f"DELETE FROM resep_obat WHERE id_resep = {id_resep}"
            cur.execute(query_delete, (id_resep))
            os.system("cls")
            print("Penghapusan jenis obat telah berhasil")
            print(f"Total baris yang diubah: {cur.rowcount}")
            conn.commit()
            break
        elif konfirmasi.lower() == 'no':
            print("Penghapusan dibatalkan")
            break
        else:
            print(f"Pilihan invalid")
            cur.close()
            conn.close()
               
    read_resep_obat()
    cur.close()
    conn.close()
    
def menuDokter():
    os.system("cls")
    while True:
        print("Selamat Datang, Dokter ")
        print("\n" + "+" + "-"*50 + "+")
        print("|" + " " * 22 + "Menu" + " " * 24 + "|")
        print("+" + "-"*50 + "+")
        print("| {:<48} |".format("1. Melihat Data Pasien"))
        print("| {:<48} |".format("2. Melihat Rekam Medis Pasien"))
        print("| {:<48} |".format("3. Mencari Pasien dari Data Rekam Medis"))
        print("| {:<48} |".format("4. Melihat Resep Obat"))
        print("| {:<48} |".format("5. Menambah Resep Obat"))
        print("| {:<48} |".format("6. Menghapus Resep Obat"))
        print("| {:<48} |".format("7. Menghapus Resep Obat"))
        print("| {:<48} |".format("8. Logout"))
        print("| {:<48} |".format("9. Pergi ke Main"))
        print("+" + "-"*50 + "+")
        pilihan = int(input("Masukkan pilihan: "))
        
        if pilihan == 1:
            read_pasien()
        elif pilihan == 2:
            read_rekam_medis()
        elif pilihan == 3:
            search_rekam_pasien()
        elif pilihan == 4:
            read_resep_obat()
        elif pilihan == 5:
            add_resep_obat()
        elif pilihan == 6:
            renew_resep()
        elif pilihan == 7:
            delete_resep()
        elif pilihan == 8:
            print("Logout dari program")
            menuDokter()
            break
        elif pilihan == 9:
            ma.main()
            break
        else:
            print("Pilihan invalid")
            
