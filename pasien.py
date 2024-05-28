def add_transaksi(nama):
    os.system("cls")
    conn = connect()
    cur = conn.cursor()
    query_get_id_pasien = f"SELECT id_pasien FROM pasien WHERE nama ILIKE '{nama}'"
    cur.execute(query_get_id_pasien)
    id_pasien = cur.fetchone()

    if not id_pasien:
        print(f"Pasien dengan nama '{nama}' tidak ditemukan.")
        cur.close()
        conn.close()
        return

    id_pasien = id_pasien[0]

    # Choose payment method
    print("Metode Pembayaran:")
    cur.execute("SELECT * FROM metode_pembayaran")
    method_data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(tabulate(method_data, headers=col_names, tablefmt="outline"))
    id_metode = int(input("Pilih ID metode pembayaran: "))

    # Insert payment record
    tanggal_pembayaran = datetime.date.today()
    if id_metode == 1:
        bank = 6  # Default bank for cash payment
    elif id_metode == 2:
        print("Pilih Bank:")
        cur.execute("SELECT * FROM bank WHERE id_bank < 6")
        bank_data = cur.fetchall()
        print(tabulate(bank_data, headers=col_names, tablefmt="outline"))
        bank = int(input("Pilih ID bank: "))
    else:
        print("Metode pembayaran tidak valid.")
        cur.close()
        conn.close()
        return

    cur.execute("INSERT INTO pembayaran(tanggal_pembayaran, id_metode, id_bank) VALUES (%s, %s, %s) RETURNING id_pembayaran", (tanggal_pembayaran, id_metode, bank))
    id_pembayaran = cur.fetchone()[0]

    # Choose prescription purchases
    print("Pilih Resep Obat:")
    cur.execute("SELECT id_resep, daftar_obat, jumlah_obat, harga FROM resep_obat")
    resep_data = cur.fetchall()
    print(tabulate(resep_data, headers=["ID Resep", "Daftar Obat", "Jumlah", "Harga"], tablefmt="outline"))

    total_input = int(input("Masukkan jumlah jenis obat yang ingin dibeli: "))
    for _ in range(total_input):
        id_resep = int(input("Masukkan ID resep yang ingin dibeli: "))
        cur.execute("INSERT INTO detail_pembayaran(id_pasien, id_resep, id_pembayaran) VALUES (%s, %s, %s)", (id_pasien, id_resep, id_pembayaran))
        print(f"Transaksi untuk resep ID {id_resep} berhasil ditambahkan.")

    # Confirmation
    konfirmasi = input("Apakah Anda yakin ingin menyimpan transaksi ini? (yes/no): ")
    if konfirmasi.lower() == 'yes':
        conn.commit()
        print("Pembayaran berhasil ditambahkan.")
    else:
        conn.rollback()
        print("Transaksi dibatalkan.")

    cur.close()
    conn.close()
