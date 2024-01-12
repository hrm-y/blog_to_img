import os
import pathlib
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from settings import member_num
from screenshot import main


def app():
    member_name = member_name_combobox.get()
    selected_save_path = save_path_input.get()
    if selected_save_path == "":
        selected_save_path = os.path.dirname(sys.argv[0])

        """
        ### --noconsoleでapp化し保存先が空欄の場合 ###
        【os.path.dirname(sys.argv[0])】が【/Users/xxx/yyy/zzz/app.app/Contents/MacOS】を取得する
        app.appと同ディレクトリ（/Users/xxx/yyy/zzz）に画像を保存するために【parents[2]】で
        selected_save_path = /Users/xxx/yyy/zzz
        としている。
        """
        if ".app" in selected_save_path:
            selected_save_path = pathlib.Path(selected_save_path).parents[2]

    main(member_name, selected_save_path)
    messagebox.showinfo("完了", "すべてのブログを保存しました")


# フォルダ指定の関数
def dirdialog_clicked():
    init_dir = os.path.abspath(os.path.dirname(__file__))
    dir_path = filedialog.askdirectory(initialdir=init_dir)
    save_path.set(dir_path)


# ------------------------------------------------------------
# GUI設計
# ------------------------------------------------------------
# 画面全体
main_win = tk.Tk()
main_win.title("Blog to Image")
main_win.geometry("600x150")

# フレーム
frame = ttk.Frame(main_win)
frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

# ------------------------------------------------------------
# メンバー名ラベル
member_name_label = ttk.Label(frame, text="メンバー名")

# メンバー名選択コンボボックス
member_name = list(member_num)
variable = tk.StringVar()
member_name_combobox = ttk.Combobox(
    frame, values=member_name, textvariable=variable, state="readonly"
)
member_name_combobox.set(member_name[0])

# ------------------------------------------------------------
# 保存先ラベル
save_path_label = ttk.Label(frame, text="保存先")

# 保存先入力欄
save_path = tk.StringVar()
save_path_input = ttk.Entry(frame, textvariable=save_path, width=30, state="readonly")

# 「フォルダ参照」ボタン
browse_folder_button = ttk.Button(frame, text="参照", command=dirdialog_clicked)

# ------------------------------------------------------------
# 実行ボタン
app_btn = ttk.Button(frame, text="保存開始", width=12, command=app)

# ------------------------------------------------------------
# ウィジェットの配置
member_name_label.grid(column=0, row=0, pady=10)
member_name_combobox.grid(column=1, row=0, sticky=tk.EW, padx=5)
save_path_label.grid(column=0, row=1, pady=10)
save_path_input.grid(column=1, row=1, sticky=tk.EW, padx=5)
browse_folder_button.grid(column=2, row=1, sticky=tk.EW, padx=5)
app_btn.grid(column=1, row=3, padx=10, pady=10)

# 伸縮設定
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

main_win.mainloop()
