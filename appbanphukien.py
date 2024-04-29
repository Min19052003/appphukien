import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox
import sqlite3
import hashlib 
import tkinter as tk
from tkinter import Menu

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ứng dụng quản lý cửa hàng")
        self.geometry("900x550")
        self.configure(bg="light blue")

        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trang quản lý", menu=file_menu)

        file_menu.add_command(label='Tạo đơn hàng', command=self.open_create_order)
        file_menu.add_command(label='Quản lý sản phẩm', command=self.open_product_management)
        file_menu.add_command(label='Quản lý khách hàng', command=self.open_customer_management)
        file_menu.add_command(label='Quản lý đơn hàng', command=self.open_order_management)
        file_menu.add_separator()
        file_menu.add_command(label='Đăng xuất', command=self.destroy)

        self.label_main = tk.Label(self, text="Phần mềm quản lý cửa hàng bán phụ kiện điện thoại",
                                   font=("Times New Roman", 14), bg='black', fg='white')
        self.label_main.pack(pady=20)

    def read_data_from_table(self, table_name, *args):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}", *args)  # Unpack the tuple
        rows = cursor.fetchall()
        conn.close()
        return rows



    def open_product_management(self):
        self.clear_main_screen()

        self.label = tk.Label(self, text="Giao diện quản lý sản phẩm")
        self.label.pack(pady=0)
       
        
        # Tạo frame chứa textbox và nút tìm kiếm
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        self.entry_search = tk.Entry(search_frame)
        self.entry_search.pack(side=tk.LEFT, padx=5)

        btn_search = tk.Button(search_frame, text="Tìm kiếm", command=self.search_product)
        btn_search.pack(side=tk.LEFT, padx=5)

        # Tạo frame chứa entry và treeview
        info_frame = tk.Frame(self)
        info_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Frame bên trái chứa entry
        left_frame = tk.Frame(info_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        # Thêm các entry cho thông tin sản phẩm
        labels = ["Tên sản phẩm:", "Mô tả:", "Giá bán:", "Số lượng:"]
        self.entries = []
        for label_text in labels:
            label = tk.Label(left_frame, text=label_text)
            label.pack(anchor='w', pady=5)
            entry = tk.Entry(left_frame)
            entry.pack(anchor='w', pady=5)
            self.entries.append(entry)
        
        # Thêm nút "Thêm"
        btn_add = tk.Button(left_frame, text="Thêm", command=self.add_product)
        btn_add.pack(anchor='w', pady=5)
        btn_delete = tk.Button(left_frame, text="Xóa", command=self.delete_product)
        btn_delete.pack(anchor='w', pady=5)
        btn_update = tk.Button(left_frame, text="Sửa", command=self.open_update_product)
        btn_update.pack(anchor='w', pady=5)

        # Frame bên phải chứa treeview
        right_frame = tk.Frame(info_frame)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        self.treeview = ttk.Treeview(right_frame)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Thêm cột vào treeview
        self.treeview["columns"] = (1, 2, 3, 4)
        self.treeview.heading("#0", text="ID")
        self.treeview.column("#0", anchor="center", width=50)
        self.treeview.heading(1, text="Tên sản phẩm")
        self.treeview.column(1, anchor="w", width=100)
        self.treeview.heading(2, text="Mô tả")
        self.treeview.column(2, anchor="w", width=200)
        self.treeview.heading(3, text="Giá bán")
        self.treeview.column(3, anchor="center", width=100)
        self.treeview.heading(4, text="Số lượng")
        self.treeview.column(4, anchor="center", width=100)

        self.load_product()

        # Frame dưới cùng chứa nút quay lại
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, anchor="se")

        self.btn_back = tk.Button(bottom_frame, text="Quay lại", command=self.show_main_screen)
        self.btn_back.pack()
    
    def load_product(self, keyword = ''):
        self.treeview.delete(*self.treeview.get_children())
        rows = self.read_data_from_table(f"SanPham WHERE TenSanPham LIKE '%{keyword}%'")
        if rows is None:
            rows = []
        for row in rows:
            self.treeview.insert("", "end", text=row[0], values=row[1:])

    def search_product(self):
        self.load_product(self.entry_search.get())

    def add_product(self):
        if self.entries[0].get() != '' and self.entries[1].get() != '' and str(self.entries[2].get()).isdigit() and int(self.entries[2].get()) > 0 and str(self.entries[3].get()).isdigit() and int(self.entries[3].get()) > 0:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO SanPham (TenSanPham, MoTa, GiaBan, SoLuong) VALUES (?, ?, ?, ?)", (self.entries[0].get(), self.entries[1].get(), int(self.entries[2].get()), int(self.entries[3].get())))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
                self.load_product()
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi", "Lỗi khi thêm sản phẩm: " + str(e))
        else:
            messagebox.showwarning("Cảnh báo", "Thông tin không hợp lệ, vui lòng kiểm tra lại!")

    def delete_product(self):
        selection = self.treeview.selection()
        if selection:
            selected_item_id = selection[0]
            # Lấy thông tin của mục được chọn
            item = self.treeview.item(selected_item_id)
            # Lấy ra giá trị của ô đầu tiên trong dòng được chọn
            first_column_value = item['text']
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM SanPham WHERE MaSanPham = ?", (str(first_column_value)))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Xóa sản phẩm thành công!")
                self.load_product()
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi", "Lỗi khi xóa sản phẩm: " + str(e))
    def open_update_product(self):
        selection = self.treeview.selection()
        if selection:
            selected_item_id = selection[0]
            item = self.treeview.item(selected_item_id)
            first_column_value = item['text']
            product_info = self.read_data_from_table("SanPham WHERE MaSanPham=?", (first_column_value,))
            if product_info:
                product_info = product_info[0]
                update_window = tk.Toplevel(self)
                update_window.title("Cập nhật sản phẩm")

                labels = ["Tên sản phẩm:", "Mô tả:", "Giá bán:", "Số lượng:"]
                entries = []
                for i, label_text in enumerate(labels):
                    label = tk.Label(update_window, text=label_text)
                    label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
                    entry = tk.Entry(update_window)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    entry.insert(0, product_info[i + 1]) 
                    entries.append(entry)

                btn_save = tk.Button(update_window, text="Lưu", command=lambda: self.save_product_update(entries, first_column_value))
                btn_save.grid(row=len(labels), columnspan=2, pady=10)

                update_window.protocol("WM_DELETE_WINDOW", update_window.destroy)
        else:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn sản phẩm cần sửa!")

    def save_product_update(self, entries, product_id):
        # Lấy thông tin cập nhật từ các entry
        updated_info = [entry.get() for entry in entries]
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            # Cập nhật thông tin sản phẩm vào cơ sở dữ liệu
            cursor.execute("UPDATE SanPham SET TenSanPham=?, MoTa=?, GiaBan=?, SoLuong=? WHERE MaSanPham=?", (*updated_info, product_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Cập nhật thông tin sản phẩm thành công!")
            # Load lại danh sách sản phẩm sau khi cập nhật
            self.load_product()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", "Lỗi khi cập nhật sản phẩm: " + str(e))
    def update_customer(self):
        selection = self.treeview.selection()
        if selection:
            selected_item_id = selection[0]
            item = self.treeview.item(selected_item_id)
            first_column_value = item['text']

            # Get current customer information
            current_customer_info = [entry.get() for entry in self.entries]

            # Open a new window/dialog to input updated information
            update_dialog = tk.Toplevel(self)
            update_dialog.title("Cập nhật thông tin khách hàng")

            # Create entry fields for updated information
            labels = ["Tên khách hàng:", "Địa chỉ:", "SĐT:", "Thông tin liên lạc khác:"]
            updated_entries = []
            for i, label_text in enumerate(labels):
                label = tk.Label(update_dialog, text=label_text)
                label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
                entry = tk.Entry(update_dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.insert(0, current_customer_info[i])
                updated_entries.append(entry)
                

            # Function to handle the update action
            def confirm_update():
                new_info = [entry.get() for entry in updated_entries]
                try:
                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE KhachHang SET HoTen = ?, DiaChi = ?, SDT = ?, ThongTinLienLacKhac = ? WHERE MaKhachHang = ?", (new_info[0], new_info[1], new_info[2], new_info[3], first_column_value))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thành công", "Cập nhật thông tin khách hàng thành công!")
                    self.load_customer()  # Reload the customer list
                    update_dialog.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Lỗi", "Lỗi khi cập nhật thông tin khách hàng: " + str(e))

            # Button to confirm update
            btn_confirm = tk.Button(update_dialog, text="Xác nhận", command=confirm_update)
            btn_confirm.grid(row=len(labels), columnspan=2, pady=10)
        else:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn khách hàng cần cập nhật!")
    def open_customer_management(self):
        self.clear_main_screen()

        self.label = tk.Label(self, text="Giao diện quản lý khách hàng")
        self.label.pack(pady=0)
       
        
        # Tạo frame chứa textbox và nút tìm kiếm
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        self.entry_search = tk.Entry(search_frame)
        self.entry_search.pack(side=tk.LEFT, padx=5)

        btn_search = tk.Button(search_frame, text="Tìm kiếm", command=self.search_customer)
        btn_search.pack(side=tk.LEFT, padx=5)

        # Tạo frame chứa entry và treeview
        info_frame = tk.Frame(self)
        info_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Frame bên trái chứa entry
        left_frame = tk.Frame(info_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        # Thêm các entry cho thông tin sản phẩm
        labels = ["Tên khách hàng:", "Địa chỉ:", "SĐT:", "Thông tin liên lạc khác:"]
        self.entries = []
        for label_text in labels:
            label = tk.Label(left_frame, text=label_text)
            label.pack(anchor='w', pady=5)
            entry = tk.Entry(left_frame)
            entry.pack(anchor='w', pady=5)
            self.entries.append(entry)

        # Thêm nút "Thêm"
        btn_add = tk.Button(left_frame, text="Thêm", command=self.add_customer)
        btn_add.pack(anchor='w', pady=5)
        btn_delete = tk.Button(left_frame, text="Xóa", command=self.delete_customer)
        btn_delete.pack(anchor='w', pady=5)
        btn_update = tk.Button(left_frame, text="Cập nhật", command=self.update_customer)
        btn_update.pack(anchor='w', pady=5)
        # Frame bên phải chứa treeview
        right_frame = tk.Frame(info_frame)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        self.treeview = ttk.Treeview(right_frame)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Thêm cột vào treeview
        self.treeview["columns"] = ("1", "2", "3", "4")
        self.treeview.heading("#0", text="ID")
        self.treeview.column("#0", anchor="center", width=50)
        self.treeview.heading("1", text="Họ và tên")
        self.treeview.column("1", anchor="center", width=150)
        self.treeview.heading("2", text="Địa chỉ")
        self.treeview.column("2", anchor="center", width=100)
        self.treeview.heading("3", text="SĐT")
        self.treeview.column("3", anchor="center", width=100)
        self.treeview.heading("4", text="Thông tin liên lạc khác")
        self.treeview.column("4", anchor="center", width=150)

        self.load_customer()

        # Frame dưới cùng chứa nút quay lại
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, anchor="se")

        self.btn_back = tk.Button(bottom_frame, text="Quay lại", command=self.show_main_screen)
        self.btn_back.pack()

    def load_customer(self, keyword = ''):
        self.treeview.delete(*self.treeview.get_children())
        rows = self.read_data_from_table(f"KhachHang WHERE HoTen LIKE '%{keyword}%'")
        if rows is None:
            rows = []
        for row in rows:
            self.treeview.insert("", "end", text=row[0], values=row[1:])
    
    def search_customer(self):
        self.load_customer(self.entry_search.get())
    
    def add_customer(self):
        if self.entries[0].get() != '' and self.entries[1].get() != '' and str(self.entries[2].get()).isdigit() and 10 <= len(str(self.entries[2].get())) <= 12:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO KhachHang (HoTen, DiaChi, SDT, ThongTinLienLacKhac) VALUES (?, ?, ?, ?)", (self.entries[0].get(), self.entries[1].get(), self.entries[2].get(), self.entries[3].get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Thêm khách hàng thành công!")
                self.load_customer()
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi", "Lỗi khi thêm khách hàng: " + str(e))
        else:
            messagebox.showwarning("Cảnh báo", "Thông tin không hợp lệ, vui lòng kiểm tra lại!")
    
    def delete_customer(self):
        selection = self.treeview.selection()
        if selection:
            selected_item_id = selection[0]
            # Lấy thông tin của mục được chọn
            item = self.treeview.item(selected_item_id)
            # Lấy ra giá trị của ô đầu tiên trong dòng được chọn
            first_column_value = item['text']
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM KhachHang WHERE MaKhachHang = ?", (str(first_column_value)))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Xóa khách hàng thành công!")
                self.load_customer()
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi", "Lỗi khi xóa khách hàng: " + str(e))

    def open_order_management(self):
        self.clear_main_screen()
        # Hiển thị giao diện mới cho quản lý đơn hàng
        self.label = tk.Label(self, text="Giao diện quản lý đơn hàng")
        self.label.pack(pady=5)
        

        # Frame cho tìm kiếm
        frame_search = tk.Frame(self)
        frame_search.pack(pady=5)

        self.entry_search = tk.Entry(frame_search)
        self.entry_search.pack(side=tk.LEFT, padx=5)

        btn_search = tk.Button(frame_search, text="Tìm kiếm", command= self.sruearch_order)
        btn_search.pack(side=tk.LEFT, padx=5)

        # Frame chứa treeview
        frame_treeview = tk.Frame(self)
        frame_treeview.pack(pady=10)

        # Tạo Treeview
        self.treeview = ttk.Treeview(frame_treeview)
        self.treeview.pack()

        # Thêm cột vào Treeview
        self.treeview["columns"] = (1, 2, 3, 4, 5, 6)
        self.treeview.heading("#0", text="Mã đơn")
        self.treeview.column("#0", anchor="center", width=50)
        self.treeview.heading(1, text="Tên khách")
        self.treeview.column(1, anchor="center", width=150)
        self.treeview.heading(2, text="Tên sản phẩm")
        self.treeview.column(2, anchor="center", width=150)
        self.treeview.heading(3, text="Số lượng")
        self.treeview.column(3, anchor="center", width=100)
        self.treeview.heading(4, text="Giá bán")
        self.treeview.column(4, anchor="center", width=100)
        self.treeview.heading(5, text="Tổng tiền")
        self.treeview.column(5, anchor="center", width=100)
        self.treeview.heading(6, text="Trạng thái")
        self.treeview.column(6, anchor="center", width=100)

        self.load_order()

        # Frame cho cập nhật trạng thái
        frame_update_status = tk.Frame(frame_treeview)
        frame_update_status.pack(pady=5)

        label_new_status = tk.Label(frame_update_status, text="Trạng thái mới:")
        label_new_status.pack(side=tk.LEFT, padx=5)

        self.entry_new_status = tk.Entry(frame_update_status)
        self.entry_new_status.pack(side=tk.LEFT, padx=5)

        btn_update_status = tk.Button(frame_update_status, text="Cập nhật", command= self.update_order)
        btn_update_status.pack(side=tk.LEFT, padx=5)

        # Button Quay lại
        self.btn_back = tk.Button(self, text="Quay lại", command=self.show_main_screen)
        self.btn_back.pack(side=tk.BOTTOM, padx=10, pady=10, anchor="se")

    def load_order(self, keyword = ''):
        self.treeview.delete(*self.treeview.get_children())
        rows = self.read_data_from_table(f"View_DonHang WHERE TenKhachHang LIKE '%{keyword}%'")
        if rows is None:
            rows = []
        for row in rows:
            self.treeview.insert("", "end", text=row[0], values=row[1:])

    def search_order(self):
        self.load_order(self.entry_search.get())

    def update_order(self):
        if str(self.entry_new_status.get()) not in ('-1', '1'):
            messagebox.showwarning("Cảnh báo", "Trạng thái mới phải là 1 (Đã giao) hoặc -1 (Đã hủy)!")
            return
        selection = self.treeview.selection()
        if selection:
            selected_item_id = selection[0]
            item = self.treeview.item(selected_item_id)
            first_column_value = item['text']
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE DonHang SET TrangThai = ? WHERE MaDonHang = ?", (int(self.entry_new_status.get()), first_column_value))
                conn.commit()
                messagebox.showinfo("Thông báo", f"Cập nhật trạng thái đơn hàng {first_column_value} thành công.")
                self.load_order()
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật trạng thái đơn hàng: {e}")
            finally:
                conn.close()
        else: messagebox.showwarning("Cảnh báo", "Bạn chưa chọn đơn hàng cần cập nhật!")

    def open_create_order(self):
        self.clear_main_screen()
        self.product_table = self.read_data_from_table('SanPham')
        self.customer_table = self.read_data_from_table('khachHang')
        # Hiển thị giao diện mới cho thống kê
        self.label = tk.Label(self, text="Giao diện tạo đơn hàng")
        self.label.pack(pady=5)
       

        # Frame cho Mã khách
        frame_ma_khach = tk.Frame(self)
        frame_ma_khach.pack(pady=5)

        label_ma_khach = tk.Label(frame_ma_khach, text="      Mã khách:")
        label_ma_khach.grid(row=0, column=0)

        self.entry_ma_khach = tk.Entry(frame_ma_khach)
        self.entry_ma_khach.grid(row=0, column=1)

        #Frame cho Mã sản phẩm
        frame_ma_san_pham = tk.Frame(self)
        frame_ma_san_pham.pack(pady=5)

        label_ma_san_pham = tk.Label(frame_ma_san_pham, text="Mã sản phẩm:")
        label_ma_san_pham.grid(row=0, column=0)

        self.entry_ma_san_pham = tk.Entry(frame_ma_san_pham)
        self.entry_ma_san_pham.grid(row=0, column=1)

        #Frame cho nút thêm sản phẩm mua
        frame_add_button = tk.Frame(self)
        frame_add_button.pack(pady=10)

        btn_add = tk.Button(frame_add_button, text="Thêm sản phẩm", command=self.add_purchase_product, width=10)
        btn_add.pack()

        # Frame cho thông tin sản phẩm
        frame_product_info = tk.Frame(self)
        frame_product_info.pack(pady=10)

        label_ten_san_pham = tk.Label(frame_product_info, text="Tên sản phẩm:")
        label_ten_san_pham.grid(row=0, column=0)

        self.entry_ten_san_pham = tk.Entry(frame_product_info, state="readonly")
        self.entry_ten_san_pham.grid(row=0, column=1)

        label_so_luong = tk.Label(frame_product_info, text="Số lượng:")
        label_so_luong.grid(row=0, column=2)

        self.entry_so_luong = tk.Entry(frame_product_info)
        self.entry_so_luong.grid(row=0, column=3)

        label_gia_ban = tk.Label(frame_product_info, text="Giá bán:")
        label_gia_ban.grid(row=0, column=4)

        self.entry_gia_ban = tk.Entry(frame_product_info, state="readonly")
        self.entry_gia_ban.grid(row=0, column=5)

        # Frame cho nút "Tạo"
        frame_create_button = tk.Frame(self)
        frame_create_button.pack(pady=10)

        btn_create = tk.Button(frame_create_button, text="Tạo", command=self.create_order, width=10)
        btn_create.pack()

        self.btn_back = tk.Button(self, text="Quay lại", command=self.show_main_screen)
        self.btn_back.pack(side=tk.BOTTOM, padx=10, pady=10, anchor="se")
    
    def add_purchase_product(self):
        productIDrows = [str(row[0]) for row in self.product_table]
        if str(self.entry_ma_san_pham.get()) in productIDrows:
            product_row = [row for row in self.product_table if str(row[0]) == str(self.entry_ma_san_pham.get())][0]
            
            self.entry_ten_san_pham.config(state="normal")
            self.entry_ten_san_pham.delete(0, tk.END)
            self.entry_ten_san_pham.insert(0, str(product_row[1]))
            self.entry_ten_san_pham.config(state="readonly")

            self.entry_so_luong.delete(0, tk.END)
            self.entry_so_luong.insert(0, "1")

            self.entry_gia_ban.config(state="normal")
            self.entry_gia_ban.delete(0, tk.END)
            self.entry_gia_ban.insert(0, str(product_row[3]))
            self.entry_gia_ban.config(state="readonly")
        else:
            self.entry_ten_san_pham.config(state="normal")
            self.entry_ten_san_pham.delete(0, tk.END)
            self.entry_ten_san_pham.insert(0, '')
            self.entry_ten_san_pham.config(state="readonly")

            self.entry_so_luong.delete(0, tk.END)
            self.entry_so_luong.insert(0, '')

            self.entry_gia_ban.config(state="normal")
            self.entry_gia_ban.delete(0, tk.END)
            self.entry_gia_ban.insert(0, '')
            self.entry_gia_ban.config(state="readonly")

    def create_order(self):
        customerIDrows = [str(row[0]) for row in self.customer_table]
        if str(self.entry_ma_khach.get()) not in customerIDrows:
            messagebox.showerror("Lỗi", "Mã khách không tồn tại")
            return
        if str(self.entry_ten_san_pham.get()) == '':
            messagebox.showerror("Lỗi", "Bạn chưa chọn sản phẩm")
            return
        if not str(self.entry_so_luong.get()).isdigit() or int(self.entry_so_luong.get()) <= 0:
            messagebox.showerror("Lỗi", "Số lượng sản phẩm phải là số dương")
            return
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO DonHang (MaKhachHang, MaSanPham, SoLuong, GiaBan, TrangThai) VALUES (?, ?, ?, ?, ?)", (str(self.entry_ma_khach.get()), str(self.entry_ma_san_pham.get()), str(self.entry_so_luong.get()), str(self.entry_gia_ban.get()), 0))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Thêm đơn hàng thành công!")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", "Lỗi khi thêm đơn hàng: " + str(e))
        
        self.show_main_screen()

    def open_logout(self):
        self.clear_main_screen()
        # Hiển thị giao diện mới cho thống kê
        self.label = tk.Label(self, text="Giao diện thống kê")
        self.label.pack(pady=5)
        self.btn_back = tk.Button(self, text="Quay lại", command=self.show_main_screen)
        self.btn_back.pack(side=tk.BOTTOM, padx=10, pady=10, anchor="se")

    def clear_main_screen(self):
        # Xóa tất cả các widget trên màn hình chính
        for widget in self.winfo_children():
            widget.pack_forget()

    def show_main_screen(self):
        # Hiển thị lại màn hình chính
        self.clear_main_screen()
        self.label_main.pack(pady=20)
        self.btn_create_order.pack(pady=10)
        self.btn_product_management.pack(pady=10)
        self.btn_customer_management.pack(pady=10)
        self.btn_order_management.pack(pady=10)
        self.btn_logout.pack(pady=10)

import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
    
        self.init_database()
        self.title("Đăng nhập")
        self.center_window()

        self.label_username = tk.Label(self, text="Tên đăng nhập:")
        self.label_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = tk.Label(self, text="Mật khẩu:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.btn_login = tk.Button(self, text="Đăng nhập", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.btn_register = tk.Button(self, text="Đăng ký", command=self.register_form)
        self.btn_register.grid(row=3, column=0, columnspan=2, pady=10)
    def init_database(self):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS SanPham (
                            MaSanPham INTEGER PRIMARY KEY AUTOINCREMENT,
                            TenSanPham TEXT NOT NULL,
                            MoTa TEXT,
                            GiaBan INTEGER NOT NULL,
                            SoLuong INTEGER NOT NULL)''')

            # Tạo bảng khách hàng
            cursor.execute('''CREATE TABLE IF NOT EXISTS KhachHang (
                            MaKhachHang INTEGER PRIMARY KEY AUTOINCREMENT,
                            HoTen TEXT NOT NULL,
                            DiaChi TEXT,
                            SDT TEXT,
                            ThongTinLienLacKhac TEXT)''')

            # Tạo bảng đơn hàng
            cursor.execute('''CREATE TABLE IF NOT EXISTS DonHang (
                        MaDonHang INTEGER PRIMARY KEY AUTOINCREMENT,
                        MaKhachHang INTEGER,
                        MaSanPham INTEGER,
                        SoLuong INTEGER NOT NULL,
                        GiaBan INTEGER NOT NULL,
                        TrangThai INTEGER,
                        FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),
                        FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham))''')
            
            #View xem đơn hàng
            cursor.execute('''CREATE VIEW IF NOT EXISTS View_DonHang AS
                                SELECT DonHang.MaDonHang, KhachHang.HoTen AS TenKhachHang, SanPham.TenSanPham, 
                                    DonHang.SoLuong, DonHang.GiaBan, DonHang.SoLuong * DonHang.GiaBan AS TongTien,
                                    CASE DonHang.TrangThai
                                        WHEN 0 THEN 'Chờ xác nhận'
                                        WHEN 1 THEN 'Thành công'
                                        WHEN -1 THEN 'Đã bị hủy'
                                        ELSE 'Unknown'
                                    END AS TrangThai
                                FROM DonHang
                                JOIN KhachHang ON DonHang.MaKhachHang = KhachHang.MaKhachHang
                                JOIN SanPham ON DonHang.MaSanPham = SanPham.MaSanPham''')

            #Trigger
            cursor.execute('''CREATE TRIGGER IF NOT EXISTS Trigger_UpdateSoLuongSanPham 
                        AFTER INSERT ON DonHang
                        FOR EACH ROW
                        BEGIN
                            UPDATE SanPham 
                            SET SoLuong = SoLuong - NEW.SoLuong 
                            WHERE MaSanPham = NEW.MaSanPham;
                        END''')

            cursor.execute('''CREATE TRIGGER IF NOT EXISTS Trigger_RollbackSoLuongSanPham 
                            BEFORE UPDATE OF TrangThai ON DonHang
                            FOR EACH ROW
                            WHEN OLD.TrangThai != -1 AND NEW.TrangThai = -1
                            BEGIN
                                UPDATE SanPham 
                                SET SoLuong = SoLuong + OLD.SoLuong 
                                WHERE MaSanPham = OLD.MaSanPham;
                            END''')

            # Lưu các thay đổi và đóng kết nối
            conn.commit()
            conn.close()
    def register_form(self):
        register_window = RegisterForm()
        self.destroy()
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_reqwidth()) / 2
        y = (screen_height - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, plain_password, hashed_password):
        return self.hash_password(plain_password) == hashed_password

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and self.verify_password(password, user[2]):
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            self.destroy()
            app = MainApplication()
            app.mainloop()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
class RegisterForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng ký")
        self.center_window()

        self.label_username = tk.Label(self, text="Tên đăng nhập:")
        self.label_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = tk.Label(self, text="Mật khẩu:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.label_confirm_password = tk.Label(self, text="Xác nhận mật khẩu:")
        self.label_confirm_password.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_confirm_password = tk.Entry(self, show="*")
        self.entry_confirm_password.grid(row=2, column=1, padx=5, pady=5)

        self.btn_register = tk.Button(self, text="Đăng ký", command=self.register)
        self.btn_register.grid(row=3, column=0, columnspan=2, pady=10)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_reqwidth()) / 2
        y = (screen_height - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login_form(self):
        login_window = LoginForm()
        self.destroy()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not self.validate_username(username):
            return
        
        if not self.validate_password(password):
            return

        if username == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập.")
        elif password == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu.")
        elif confirm_password == "":
            messagebox.showerror("Lỗi", "Vui lòng xác nhận mật khẩu.")
        elif password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu và xác nhận mật khẩu không khớp.")
        else:
            hashed_password = self.hash_password(password)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Kiểm tra xem tên người dùng đã tồn tại trong cơ sở dữ liệu hay chưa
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                messagebox.showerror("Lỗi", "Người dùng đã tồn tại trong hệ thống.")
                conn.close()
                return
            
            # Thêm người dùng mới vào cơ sở dữ liệu
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thông báo", "Đăng ký thành công!")
            self.login_form() 

    def validate_username(self, username):
        if not username.isalnum():
            messagebox.showerror("Lỗi", "Tên đăng nhập chỉ có thể chứa các ký tự chữ và số.")
            return False
        return True

    def validate_password(self, password):
        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải chứa ít nhất 6 ký tự.")
            return False
        return True

if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()