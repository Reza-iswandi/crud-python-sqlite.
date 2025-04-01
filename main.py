import sqlite3

# Koneksi ke database
conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    stock INTEGER)''')
conn.commit()

# Fungsi untuk menambah produk
def add_product():
    try:
        name = input("Masukkan nama produk: ")
        price = float(input("Masukkan harga produk: "))
        stock = int(input("Masukkan stok produk: "))
        if price < 0 or stock < 0:
            print("Harga dan stok harus bernilai positif.\n")
            return
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        print("Produk berhasil ditambahkan!\n")
    except ValueError:
        print("Input tidak valid. Pastikan memasukkan angka untuk harga dan stok.\n")
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan pada database: {e}\n")

# Fungsi menampilkan produk
def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    if not products:
        print("Tidak ada produk.\n")
    else:
        for p in products:
            print(f"ID: {p[0]}, Nama: {p[1]}, Harga: {p[2]}, Stok: {p[3]}")
    print()

# Fungsi mengedit produk
def edit_product():
    view_products()
    try:
        prod_id = int(input("Masukkan ID produk yang ingin diedit: "))
        cursor.execute("SELECT * FROM products WHERE id = ?", (prod_id,))
        if cursor.fetchone() is None:
            print("ID produk tidak ditemukan.\n")
            return
        new_price = float(input("Masukkan harga baru: "))
        new_stock = int(input("Masukkan stok baru: "))
        if new_price < 0 or new_stock < 0:
            print("Harga dan stok harus bernilai positif.\n")
            return
        cursor.execute("UPDATE products SET price = ?, stock = ? WHERE id = ?", (new_price, new_stock, prod_id))
        conn.commit()
        print("Produk berhasil diperbarui!\n")
    except ValueError:
        print("Input tidak valid. Pastikan memasukkan angka.\n")

# Fungsi menghapus produk
def delete_product():
    view_products()
    try:
        prod_id = int(input("Masukkan ID produk yang ingin dihapus: "))
        cursor.execute("SELECT * FROM products WHERE id = ?", (prod_id,))
        if cursor.fetchone() is None:
            print("ID produk tidak ditemukan.\n")
            return
        confirm = input("Apakah Anda yakin ingin menghapus produk ini? (y/n): ").lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM products WHERE id = ?", (prod_id,))
            conn.commit()
            print("Produk berhasil dihapus!\n")
        else:
            print("Penghapusan dibatalkan.\n")
    except ValueError:
        print("Input tidak valid. Pastikan memasukkan angka.\n")
      

try:
    # Menu interaktif
    while True:
        print("=== Manajemen Produk ===")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Edit Produk")
        print("4. Hapus Produk")
        print("5. Keluar")
        
        choice = input("Pilih menu: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            edit_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("Pilihan tidak valid, coba lagi!\n")
finally:
    conn.close()
    print("Koneksi database ditutup.")