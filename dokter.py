import psycopg2
from tabulate import tabulate

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
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM pasien"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

def read_rekam_medis():
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM rekam_medis"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()
    
def search_rekam_pasien():
    conn = connect()
    cur = conn.cursor()
    search_pasien = input("Masukkan nama pasien yang dicari: ")
    query = """SELECT p.id_pasien, p.nama, r.nomor_rekam, r.tanggal_pemeriksaan, r.hasil_pemeriksaan, r.diagnosis
            FROM pasien p
            JOIN rekam_medis r ON(p.id_pasien = r.id_pasien)
            WHERE p.nama ILIKE %s"""
    cur.execute(query, (f"%{search_pasien}%",))
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
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM resep_obat"
    cur.execute(query)
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(data, headers=col_names, tablefmt="outline"))
    cur.close()
    conn.close()

# Menambah obat pada resep obat
def add_resep_obat():
    conn = connect()
    cur = conn.cursor()
    total_input = int(input(f"Mau menambahkan berapa jenis obat?: "))
    for i in range(total_input):
        id_dokter = 1
        daftar_obat = input(f"Masukkan nama obat: ")
        jumlah_obat = int(input(f"Berapa jumlah obat yang dipunyai: "))
        harga = int(input(f"Masukkan harga obat tersebut: "))
        query = f"INSERT INTO resep_obat(id_dokter, daftar_obat, jumlah_obat, harga) VALUES(%s, %s, %s, %s)"
    cur.execute(query, (id_dokter, daftar_obat, jumlah_obat, harga))
    conn.commit()
    query = f"UPDATE resep_obat SET id_dokter = %s, daftar_obat = %s, jumlah_obat = %s, harga = %s"
    read_resep_obat()
    cur.close
    conn.close()
    
def delete_resep():
    conn = connect()
    cur = conn.cursor()
    read_resep_obat()
    id_resep = input('Masukkan id resep obat yang ingin dihapus: ')
    konfirmasi = input(f"Apakah Anda yakin ingin menghapus dengan angka id resep {id_resep} ini?: (yes/no)")
    if konfirmasi.lower() == 'yes':
        query_delete = f"DELETE FROM resep_obat WHERE id_resep = {id_resep}"
        cur.execute(query_delete, (id_resep))
        print(f"Total baris yang diubah: {cur.rowcount}")
        conn.commit()
    elif konfirmasi.lower() == 'no':
        print("Penghapusan dibatalkan")
    else:
        print(f"Pilihan invalid")
        cur.close()
        conn.close()
        return   
    cur.close()
    conn.close()
    
def menuDokter():
    while True:
        print("Selamat Datang, Dokter ")
        print("\nMenu:")
        print("1. Melihat Data Pasien")
        print("2. Melihat Rekam Medis Pasien")
        print("3. Mencari Pasien dari Data Rekam Medis")
        print("4. Melihat Resep Obat")
        print("5. Menambah Resep Obat")
        print("6. Menghapus Resep Obat")
        print("7. Logout")
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
            delete_resep()
        elif pilihan == 7:
            print("Logout dari program")
            break
        else:
            print("Pilihan invalid")
            
if __name__ == "__main__":
    menuDokter()