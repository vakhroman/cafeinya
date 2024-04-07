import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import Tk, Label
from PIL import Image, ImageTk


class YourClassName(tk.Tk):
    def __init__(self):
        super().__init__()
        self.users = {}

class CafeApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Кофейня")

        self.your_class = YourClassName()
        self.your_class.withdraw()
        self.minsize(800, 600)

        self.configure(bg="lightgreen")
        self.title_font = ("Helvetica", 16, "bold")
        self.option_add("*TCombobox*Listbox.font", self.title_font)
        self.option_add("*TCombobox*Listbox.selectBackground",
                        "lightblue")
        self.option_add("*TCombobox*Listbox.selectForeground",
                        "black")
        # Добавление изображения как шапки страницы
        img = Image.open("cafe.jpg")
        img = img.resize((300, 250))  # Измените размер изображения по вашему усмотрению
        photo = ImageTk.PhotoImage(img)

        header_label = Label(self, image=photo)
        header_label.image = photo  # Оставьте ссылку на фото, чтобы она не удалась
        header_label.pack()  # Размещение изображения в верхней части окна
        self.login_screen()

    def login_screen(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True)

        self.username_label = tk.Label(self.login_frame, text="Логин:", font=("Verdana", 15), fg="red")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame, font=("Verdana", 12), bg="yellow", fg="black")
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Пароль:", font=("Verdana", 15), fg="red")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Verdana", 12), bg="yellow", fg="black")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Войти", command=self.login, bg="yellow", fg="black", font=("Arial Bold", 14))
        self.login_button.pack()

        # Центрирование формы относительно окна
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "администратор" and password == "111":
            self.admin_screen()
        elif username == "официант" and password == "222":
            self.waiter_screen()
        elif username == "повар" and password == "333":
            self.cook_screen()
        else:
            error_label = tk.Label(self.login_frame, text="Неверный логин или пароль")
            error_label.pack()

    def waiter_screen(self):
        self.waiter_window = tk.Toplevel(self)
        self.waiter_window.title("Окно официанта")
        self.waiter_window.geometry("800x58600")
        self.waiter_window.configure(bg="lightgreen")

        self.new_order_button = tk.Button(self.waiter_window, text="Сделать заказ",
                                          command=self.create_new_order_window, bg="lightyellow", fg="black",
                                          font=("Verdana", 12), width=60, height=5)
        self.new_order_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_new_order_window(self):
        self.new_order_window = tk.Toplevel(self.waiter_window)
        self.new_order_window.title("Новый заказ")
        self.new_order_window.geometry("800x600")
        self.new_order_window.configure(bg="lightgreen")

        self.table_label = tk.Label(self.new_order_window, text="Номер посадочного места:", bg="lightyellow", font=("Verdana", 14),
                                    fg="blue")
        self.table_label.pack()
        self.table_entry = tk.Entry(self.new_order_window, font=("Verdana", 15), fg="blue")
        self.table_entry.pack()

        self.customers_label = tk.Label(self.new_order_window, text="Количество клиентов за столом:", bg="lightyellow",
                                        font=("Verdana", 18), fg="blue")
        self.customers_label.pack()
        self.customers_entry = tk.Entry(self.new_order_window, font=("Verdana", 15), fg="blue")
        self.customers_entry.pack()

        self.dishes_label = tk.Label(self.new_order_window, text="Выберите блюда для заказа:", bg="lightpink",
                                     font=("Verdana", 14), fg="blue")
        self.dishes_label.pack()

        self.dishes = {
            "Кофе": 120,
            "Чай": 60,
            "Морс": 75,
            "Напалеон": 280,
            "Прага": 210,
        }

        self.dish_checkboxes = {}
        for dish, price in self.dishes.items():
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.new_order_window, text=f"{dish} - {price} руб.", variable=var,
                                      bg="lightyellow")
            checkbox.dish = dish
            checkbox.price = price
            checkbox.var = var
            checkbox.pack()
            self.dish_checkboxes[dish] = checkbox

        self.status_label = tk.Label(self.new_order_window, text="Статус заказа: Ожидание", bg="lightpink")
        self.status_label.pack()

        confirm_button = tk.Button(self.new_order_window, text="Подтвердить заказ", command=self.confirm_order,
                                   bg="yellow", fg="black", font=("Verdana", 12))
        confirm_button.pack()

    def confirm_order(self):
        table_number = self.table_entry.get()
        customer_count = self.customers_entry.get()
        selected_dishes = [dish for dish, checkbox in self.dish_checkboxes.items() if checkbox.var.get() == 1]
        total_price = sum(self.dishes[dish] for dish in selected_dishes)

        confirmation_text = f"Стол: {table_number}, Клиентов: {customer_count}, Заказ: {', '.join(selected_dishes)}, Итого к оплате: {total_price} руб."
        self.status_label.config(text=confirmation_text)

        with open('zakazes.txt', 'a') as file:
            file.write(f"Стол: {table_number}, Клиентов: {customer_count}, Заказ: {', '.join(selected_dishes)}, Итого к оплате: {total_price} руб.\n")

        messagebox.showinfo("Подтверждение заказа", "Заказ успешно создан!")

    def confirm_order(self):
        selected_dishes = [dish for dish, checkbox in self.dish_checkboxes.items() if checkbox.var.get() == 1]
        total_price = sum(self.dishes[dish] for dish in selected_dishes)

        confirmation_text = f"Заказ принят: {', '.join(selected_dishes)}. Итого к оплате: {total_price} руб."
        self.status_label.config(text=confirmation_text)

        with open('zakazes.txt', 'a') as file:
            file.write(f"Заказ: {', '.join(selected_dishes)}. Сумма к оплате: {total_price} руб.\n")

    def cook_screen(self):
        self.cook_window = tk.Toplevel(self)
        self.cook_window.title("Экран повара")
        self.cook_window.geometry("700x500")
        self.cook_window.configure(bg="lightgreen")  # Устанавливаем фоновый цвет

        self.view_orders_button = tk.Button(self.cook_window, text="Просмотреть все заказы", command=self.view_orders,
                                            width=20, font=("Verdana", 15), bg="lightyellow", fg="black")
        self.view_orders_button.pack(pady=10)

    def view_orders(self):
        orders_window = tk.Toplevel(self.cook_window)
        orders_window.title("Заказы")

        orders_text = tk.Text(orders_window, height=20, width=50)
        orders_text.pack(padx=10, pady=10)

        try:
            with open("zakazes.txt", "r") as file:
                orders = file.read()
                orders_text.insert(tk.END, orders)
        except FileNotFoundError:
            orders_text.insert(tk.END, "Файл с заказами не найден.")

    def change_order_status(self):
        change_status_window = tk.Toplevel(self)
        change_status_window.title("Изменение статуса заказа")
        change_status_window.configure(bg="lightgreen")  # Устанавливаем фоновый цвет

        order_id_label = tk.Label(change_status_window, text="ID заказа:", font=("Verdana", 11), bg="lightgreen")
        order_id_label.pack()

        order_id_entry = tk.Entry(change_status_window, font=("Verdana", 12))
        order_id_entry.pack()

        status_label = tk.Label(change_status_window, text="Новый статус (принят/готов):", font=("Verdana", 11),
                                bg="lightyellow")
        status_label.pack()

        status_entry = tk.Entry(change_status_window, font=("Verdana", 11))
        status_entry.pack()

        confirm_button = tk.Button(change_status_window, text="Подтвердить", command=lambda: self.confirm_status_change(order_id_entry.get(), status_entry.get()), font=("Verdana", 12), bg="lightpink", fg="black")
        confirm_button.pack()

    def admin_screen(self):
        self.admin_window = tk.Toplevel(self)
        self.admin_window.title("Администраторский экран")
        self.admin_window.geometry("700x500")
        self.admin_window.configure(bg="lightgreen")  # Задаем светло-розовый фон

        button_style = {
            "font": ("Verdana", 20),
            "bg": "lightyellow",
            "fg": "black",
            "width": 30
        }

        self.add_user_button = tk.Button(self.admin_window, text="Добавить нового пользователя", command=self.add_user_entry,
                                         **button_style)
        self.add_user_button.pack(pady=10)

        self.delete_user_button = tk.Button(self.admin_window, text="Удалить пользователя",
                                            command=self.delete_user_entry, **button_style)
        self.delete_user_button.pack(pady=10)

        self.fire_user_button = tk.Button(self.admin_window, text="Уволить пользователя", command=self.fire_user_entry,
                                          **button_style)
        self.fire_user_button.pack(pady=10)

        self.assign_shift_button = tk.Button(self.admin_window, text="Назначить на смену", command=self.assign_shift,
                                             **button_style)
        self.assign_shift_button.pack(pady=10)

        self.work_mode_button = tk.Button(self.admin_window, text="Сведения о всех работниках", command=self.work_mode,
                                          **button_style)
        self.work_mode_button.pack(pady=10)

        self.view_orders_button = tk.Button(self.admin_window, text="Просмотреть заказы", command=self.view_orders,
                                            **button_style)
        self.view_orders_button.pack(pady=10)

    def add_user(self):
        username = self.username_entry.get()
        user_exists = False
        with open("polz.txt", "r") as file:
            for user in file:
                if user.strip() == username:
                    user_exists = True
                    break
        if not user_exists:
            self.your_class.users.append(username)
            messagebox.showinfo("Успешно", f"Пользователь {username} добавлен.")
            with open('polz.txt', 'a') as file:
                file.write(username + '\n')
        else:
            messagebox.showerror("Ошибка", f"Пользователь {username} уже существует.")


    def view_order(self):
        orders_text = ""
        try:
            with open('zakazes.txt', 'r') as file:
                orders_text = file.read()
        except FileNotFoundError:
            orders_text = "Файл заказов не найден"

        orders_display = tk.Text(self.admin_window, height=15, width=80)
        orders_display.insert(tk.END, orders_text)
        orders_display.pack(pady=10)

        change_status_button = tk.Button(self.admin_window, text="Изменить статус заказа", command=self.change_order_status, width=20)
        change_status_button.pack(pady=10)

    def fire_user_entry(self):
        username = simpledialog.askstring("Увольнение пользователя", "Введите имя пользователя для увольнения:")

        if username in self.your_class.users:
            self.your_class.users[username] = "уволен"
            messagebox.showinfo("Успешно", f"Пользователь {username} был уволен.")

            # Обновляем информацию о статусе пользователя в файле users.txt
            with open("polz.txt", "r") as file:
                lines = file.readlines()

            with open("polz.txt", "w") as file:
                for line in lines:
                    user_info = line.split(" - ")
                    if user_info[0] == username:
                        file.write(f"{username} - уволен\n")
                    else:
                        file.write(line)

        else:
            messagebox.showerror("Ошибка", f"Пользователь {username} не найден в системе.")

    def assign_shift(self):
        username = simpledialog.askstring("Назначение смены", "Введите имя пользователя для назначения смены:")
        shift_type = simpledialog.askstring("Назначение смены", "Введите тип смены (официант/повар):")

        if username in self.your_class.users:
            self.your_class.users[username] = shift_type  # Назначаем тип смены пользователю
            messagebox.showinfo("Успешно", f"Пользователь {username} назначен на смену типа {shift_type}.")

            # Обновляем информацию о сменах пользователя в файле users.txt
            with open("polz.txt", "r") as file:
                lines = file.readlines()

            with open("polz.txt", "w") as file:
                for line in lines:
                    user_info = line.split(" - ")
                    if user_info[0] == username:
                        file.write(f"{username} - {shift_type}\n")
                    else:
                        file.write(line)

        else:
            messagebox.showerror("Ошибка", f"Пользователь {username} не найден в системе.")

    def work_mode(self):
        shift_info = ""
        for username, shift_type in self.your_class.users.items():
            shift_info += f"{username} - {shift_type}\n"

        # Открываем окно режима работы и отображаем информацию о назначенных сменах
        work_window = tk.Toplevel(self)
        work_window.title("Режим работы")
        work_window.geometry("400x300")

        shift_label = tk.Label(work_window, text=shift_info)
        shift_label.pack(padx=10, pady=10)

        # Сохраняем информацию в файл shifts.txt при открытии режима работы
        with open("shifts.txt", "w") as file:
            file.write(shift_info)

    def delete_user_entry(self):
        self.delete_user_window = tk.Toplevel(self.admin_window)
        self.delete_user_window.title("Удалить пользователя")

        self.username_label = tk.Label(self.delete_user_window, text="Имя пользователя для удаления:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.delete_user_window)
        self.username_entry.pack()

        self.confirm_delete_button = tk.Button(self.delete_user_window, text="Удалить", command=self.delete_user)
        self.confirm_delete_button.pack()

    def read_users_from_file(self):
        with open("polz.txt", "r") as file:
            users = [line.strip() for line in file]  # сохраняем список пользователей из файла
        return users

    def write_users_to_file(self, users):
        with open("polz.txt", "w") as file:
            for user in users:
                file.write(user + '\n')

    def delete_user(self):
        username = self.username_entry.get()
        users = self.read_users_from_file()  # считываем список пользователей из файла
        if username in users:
            users.remove(username)  # удаляем пользователя из списка
            self.write_users_to_file(users)  # перезаписываем список пользователей в файл
            if username in self.your_class.users:  # проверяем наличие пользователя в словаре
                del self.your_class.users[username]  # удаляем пользователя из словаря по ключу (имени)
            messagebox.showinfo("Успешно", f"Пользователь {username} успешно удален.")
        else:
            messagebox.showerror("Ошибка", f"Пользователь {username} не найден.")

    def add_user_entry(self):
        username = simpledialog.askstring("Добавление пользователя", "Введите имя нового пользователя:")
        user_role = simpledialog.askstring("Добавление пользователя",
                                           "Введите роль нового пользователя (admin/waiter/cook):")

        if username not in self.your_class.users:
            self.your_class.users[username] = user_role
            messagebox.showinfo("Успешно", f"Пользователь {username} был добавлен с ролью {user_role}.")

            # Сохраняем информацию о пользователе в файл users.txt
            with open("polz.txt", "a") as file:
                file.write(f"{username} - {user_role}\n")
        else:
            messagebox.showerror("Ошибка", f"Пользователь {username} уже существует в системе.")

    def add_user(self):
        new_user = self.username_entry.get()
        users = self.read_users_from_file()  # считываем список пользователей из файла
        if new_user not in users:
            users.append(new_user)  # добавляем нового пользователя
            self.write_users_to_file(users)  # перезаписываем список пользователей в файл
            self.your_class.users[new_user] = 'some_role'  # добавляем нового пользователя в словарь с ролью
            messagebox.showinfo("Успешно", f"Пользователь {new_user} успешно добавлен.")
        else:
            messagebox.showerror("Ошибка", f"Пользователь {new_user} уже существует.")


app = CafeApp()
app.mainloop()