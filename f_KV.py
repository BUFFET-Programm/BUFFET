import f_components
import f_home
import f_setting
import f_theming
import f_login
import f_user_account
import f_information
import f_register
import f_database_setting
import f_set_webcam
import f_statistics
import f_delete_data
import f_login_admins
import f_register_admins
import f_forgot_password
import f_total_log

WM_KV = """
<WindowManager>:
    Home:
        name: "home"
    RegisterGetFace:
        name: "register_get_face"
    ChangeUserFaceProcess:
        name: "change_user_face_process"
    Login:
        name: "login"
    SetWebcam:
        name: "set_webcam"
    NotLogined:
        name: "not_logined"
    RegisterGetName:
        name: "register_get_name"
    UserAccount:
        name: "user_account"
    Setting:
        name: "setting"
    ChangeUserName:
        name: "change_user_name"
    ChangeUserFaceAsk:
        name: "change_user_face_ask"
    AskDeleteData:
        name: "ask_delete_data"
    ApplicationSettings:
        name: "settings"
    DatabaseSetting:
        name: "database_setting"
    Information:
        name: "information"
    Log:
        name: "log"
    Filter:
        name: "filter"
    ChangeTheme:
        name: "change_theme"
    Statistics:
        name: "statistics"
    LoginAdmins:
        name: "login_admins"
    RegisterAdminsEmail:
        name: "register_admins_email"
    RegisterAdminsCode:
        name: "register_admins_code"
    RegisterAdminsLastStep:
        name: "register_admins_last_step"
    AccountSetting:
        name: "account_setting"
    ForgotPassword:
        name: "forgot_password"
    ForgotPasswordCode:
        name: "forgot_password_code"
    ForgotPasswordChangePassword:
        name: "forgot_password_change_password"
    ChangeAdminsName:
        name: "change_admins_name"
    ChangeAdminsPassword:
        name: "change_admins_password"
    TotalLog:
        name: "total_log"
    TotalLogFilter:
        name: "total_log_filter"
"""

KV = f"""
{f_components.KV}
{f_home.KV}
{f_setting.KV}
{f_theming.KV}
{f_login.KV}
{f_user_account.KV}
{f_information.KV}
{f_register.KV}
{f_database_setting.KV}
{f_set_webcam.KV}
{f_statistics.KV}
{f_delete_data.KV}
{f_login_admins.KV}
{f_register_admins.KV}
{f_forgot_password.KV}
{f_total_log.KV}
{WM_KV}
"""
