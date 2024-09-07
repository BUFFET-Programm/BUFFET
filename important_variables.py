BASE_DIR = 'C:/BUFFET'
SPECIAL_EXTENSION = '.BUFT'
THEME_PATH = BASE_DIR+'/data/text/theme'+SPECIAL_EXTENSION
BUFFET_EXTENSIONS_PATH = BASE_DIR+'/extensions'
ALGORITHM_PATH = BUFFET_EXTENSIONS_PATH+'/haarcascade_frontalface_alt.xml'
TRAINER_FILE_PATH = BASE_DIR+'/data/trainer/trainer.yml'
DATABASE_PATH = BASE_DIR + "/data/database.db"
FONT_PATH = BUFFET_EXTENSIONS_PATH+'/iransans.ttf'
LANGUAGE_PATH = BASE_DIR + "/data/text/language" + SPECIAL_EXTENSION
COLORS = [
    "Red",
    "Purple",
    "DeepPurple",
    "Blue",
    "LightBlue",
    "Green",
    "Amber",
    "DeepOrange"
]
LANGUAGES_DIALOGS_PER = {
    "title": "بوفه",
    "welcome": "خوش آمدید",
    "login": "وارد شدن",
    "register": "ثبت نام",
    "delete_data": "پاک کردن اطلاعات",
    "set_webcam": "تنظیم دوربین",
    "statistics": "آمار",
    "settings": "تنظیمات",
    "close_application": "بستن برنامه",
    "logout": "خروج از حساب",
    "exit": "خروج",
    "schools": "مدرسه ها",
    "classes": "کلاس ها",
    "products": "محصولات",
    "operation": "نوع تراکنش",
    "date": "تاریخ",
    "users": "کاربران",
    "add_class": "افزودن کلاس",
    "add_school": "افزودن مدرسه",
    "product_duplicated_error": lambda func, name,
    code: "{} محصول تکراری است.".format({"c": "کد",
                                         "n": "نام", "b": "کد و نام"}[
                                             func(name, int(code))[1]]),
    "i_got_it": "فهمیدم",
    "price": "قیمت",
    "code": "کد",
    "name": "نام",
    "product_code": "کد محصول",
    "product_name": "نام محصول",
    "product_price": "قیمت محصول",
    "add_product": "افزودن محصول",
    "role": "نقش",
    "normal": "عادی",
    "admin": "ادمین",
    "change_role": "تغییر نقش",
    "change_name": "تغییر نام",
    "change_face": "تغییر چهره",
    "only_manager": "تنها کاربر مدیر اجازه دسترسی به این بخش را دارد.",
    "delete_data_title": ":اگر از پاک کردن تمام اطلاعات اطمینان دارید جمله زیر را در بخش مشخص شده بنویسید",
    "delete_data_text": "از پاک کردن تمام اطلاعات از جمله عکس ها و الگوریتم و دیگر اطلاعات اطمینان دارم.",
    "username": "نام کاربری",
    "send_code": "ارسال کد",
    "check_code": "بررسی کد",
    "password": "رمز عبور",
    "confirm_password": "تکرار رمز عبور",
    "change_password": "تغییر رمز عبور",
    "network_error": "خطا در اتصال به اینترنت.",
    "name_error": "نام وارد شده اشتباه می باشد.",
    "code_error": "کد وارد شده اشتباه می باشد.",
    "application_name": "نام برنامه",
    "smart_buffet": "بوفه هوشمند",
    "creators": "نام طراحان",
    "creators_names": "پارسا صفایی و محمدحسام افضلی",
    "version_number": "شماره نسخه",
    "enter": "ورود",
    "forgot_password": "فراموشی رمز عبور",
    "name_or_password_error": "نام کاربری یا رمز عبور اشتباه است.",
    "processing": "در حال پردازش",
    "face_not_detected": "چهره شما شناسایی نشد.",
    "reprocessing": "پردازش مجدد",
    "webcam_error": "دوربین متصل نمی باشد.",
    "email": "ایمیل",
    "change_email": "تغییر ایمیل",
    "error": "خطا",
    "network_or_email_error": "این موارد را بررسی کنید: اتصال اینترنت. صحیح بودن ایمیل.",
    "email_duplicated_error": "ایمیل تکراری می باشد.",
    "name_duplicated_error": "نام کاربری وارد شده تکراری می باشد.",
    "name_and_password_error": "لطفا نام کاربری و رمز عبور را صحیح وارد نمایید.",
    "network_error": "اینترنت متصل نمی باشد، دوباره امتحان کنید.",
    "charge": "شارژ",
    "school": "مدرسه",
    "class": "کلاس",
    "taking_picture": "در حال گرفتن تصویر",
    "n_or_c_or_s_or_c_error": "نام، شارژ، مدرسه یا کلاس تکراری یا اشتباه است.",
    "try_again": "امتحان مجدد",
    "webcam_is_connected": "دوربین متصل است.",
    "webcam_error2": "خطا در اتصال به دوربین",
    "manage_database": "مدیریت پایگاه داده",
    "change_theme": "تغییر ظاهر",
    "edit_account": "ویرایش حساب",
    "change_language": "تغییر زبان",
    "change_username": "تغییر نام کاربری",
    "change_password": "تغییر رمز عبور",
    "new_username": "نام کاربری جدید",
    "reopen_application_alert": "برای اعمال تغییر برنامه را دوباره باز کنید.",
    "cancel": "لغو",
    "admin_and_manager": "تنها کاربران ادمین و مدیر اجازه این کار را دارند.",
    "most_popular_products": "محبوب ترین کالاها",
    "transaction_history": "تاریخچه تراکنش ها",
    "rbcc": "کاهش غلظت رنگ پس زمینه",
    "dark_mode": "حالت تاریک",
    "filter": "فیلتر",
    "delete": "پاک کردن",
    "select_date_from": "انتخاب تاریخ از",
    "select_date_to": "انتخاب تاریخ تا",
    "price_log": "قیمت",
    "buy": "خرید",
    "charge": "شارژ",
    "from": "از",
    "to": "تا",
    "done": "اعمال",
    "buy_or_charge": {"buy": "خرید", "charge": "شارژ"},
    "edit": "ویرایش",
    "history": "تاریخچه",
    "home": "خانه",
    "enter_product": "وارد کردن محصول",
    "add_to_buy": "افزودن به خرید",
    "add_to_charge": "افزودن به شارژ",
    "add": "افزودن",
    "charge_or_import_manually": "شارژ / وارد کردن دستی",
    "change": "تغییر",
    "are_you_sure": "آیا مطمئن هستید؟",
    "yes": "بله",
    "number": "تعداد",
    "name_wrong_error": "نام تکراری یا اشتباه است.",
    "new_name": "نام جدید",
    "done2": "انجام",
    'buffet_log_as_chart': 'تاریخچه فروشگاه بر روی نمودار',
    "auto": "خودکار"
}
LANGUAGES_DIALOGS_ENG = {
    "title": "Buffet",
    "welcome": "Welcome",
    "login": "Login",
    "register": "Register",
    "delete_data": "Delete data",
    "set_webcam": "Set webcam",
    "statistics": "Statistics",
    "settings": "Settings",
    "close_application": "Close application",
    "logout": "Logout",
    "exit": "Exit",
    "schools": "Schools",
    "classes": "Classes",
    "products": "Products",
    "operation": "Operation",
    "date": "Date",
    "users": "Users",
    "add_class": "Add class",
    "add_school": "Add school",
    "product_duplicated_error": lambda func, name,
    code: "The product {} duplicated.".format({"c": "code is",
                                         "n": "name is", "b": "code and name are"}[
                                             func(name, int(code))[1]]),
    "i_got_it": "I got it.",
    "price": "Price",
    "code": "Code",
    "name": "Name",
    "product_code": "Product code",
    "product_name": "Product name",
    "product_price": "Product price",
    "add_product": "Add product",
    "role": "Role",
    "normal": "Normal",
    "admin": "Admin",
    "change_role": "Change role",
    "change_name": "Change name",
    "change_face": "Change face",
    "only_manager": "Only the manager user is allowed to access this section.",
    "delete_data_title": "If you are sure to delete all information, write the following sentence in the specified section:",
    "delete_data_text": "I am sure to delete all data including photos and algorithm and other data.",
    "username": "Username",
    "send_code": "Send code",
    "check_code": "Check code",
    "password": "Password",
    "confirm_password": "Confirm password",
    "change_password": "Change password",
    "network_error": "Internet connection failed.",
    "name_error": "The entered name is incorrect.",
    "code_error": "The entered code is wrong.",
    "application_name": "Application name",
    "smart_buffet": "Smart buffet",
    "creators": "Creators",
    "creators_names": "Parsa Safaie and Mohammad Hesam Afzali",
    "version_number": "Version number",
    "enter": "Enter",
    "forgot_password": "Forgot your password",
    "name_or_password_error": "Incorrect username or password.",
    "processing": "Processing",
    "face_not_detected": "Your face was not recognized.",
    "reprocessing": "Reprocessing",
    "webcam_error": "The camera is not connected.",
    "email": "Email",
    "change_email": "Change email",
    "error": "Error",
    "network_or_email_error": "Check these: Internet connection. Email is correct.",
    "email_duplicated_error": "Email is duplicate.",
    "name_duplicated_error": "Name is duplicate.",
    "name_and_password_error": "Please enter the correct username and password.",
    "network_error": "Internet connection failed. please try again.",
    "charge": "Charge",
    "school": "School",
    "class": "Class",
    "taking_picture": "Taking picture",
    "n_or_c_or_s_or_c_error": "The name, charge, school or class is duplicated or wrong.",
    "try_again": "Try again",
    "webcam_is_connected": "Webcam is connected.",
    "webcam_error2": "Error connecting to webcam.",
    "manage_database": "Manage database",
    "change_theme": "Change theme",
    "edit_account": "Edit account",
    "change_language": "Change language",
    "change_username": "Change username",
    "change_password": "Change password",
    "new_username": "New username",
    "reopen_application_alert": "Reopen the app to apply the change.",
    "cancel": "Cancel",
    "admin_and_manager": "Only admin and manager users are allowed to do this.",
    "most_popular_products": "Most popular products",
    "transaction_history": "Transaction history",
    "rbcc": "Reduce background color concentration",
    "dark_mode": "Dark mode",
    "filter": "Filter",
    "delete": "Delete",
    "select_date_from": "Select date from",
    "select_date_to": "Select date to",
    "price_log": "price",
    "buy": "Buy",
    "charge": "Charge",
    "from": "From",
    "to": "To",
    "done": "Done",
    "buy_or_charge": {"buy": "Buy", "charge": "Charge"},
    "edit": "Edit",
    "history": "History",
    "home": "Home",
    "enter_product": "Enter product",
    "add_to_buy": "Add to buy",
    "add_to_charge": "Add to charge",
    "add": "Add",
    "charge_or_import_manually": "Charge / import manually",
    "change": "Change",
    "are_you_sure": "Are you sure?",
    "yes": "Yes",
    "number": "Count",
    "name_wrong_error": "The name is duplicate or incorrect.",
    "new_name": "New name",
    "done2": "Done",
    'buffet_log_as_chart': 'Buffet history as chart',
    "auto": "Auto"
}
