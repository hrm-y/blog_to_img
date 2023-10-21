import os
import pathlib
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from screenshot import main
from screenshot import member_num


def app():
    member_name = combo.get()
    selected_save_dir = entry1.get()
    if selected_save_dir == "":
        selected_save_dir = os.path.dirname(sys.argv[0])

        """
        ### --noconsoleでapp化し保存先が空欄の場合 ###
        【os.path.dirname(sys.argv[0])】が【/Users/xxx/yyy/zzz/app.app/Contents/MacOS】を取得する
        app.appと同ディレクトリ（/Users/xxx/yyy/zzz）に画像を保存するために【parents[2]】で
        selected_save_dir = /Users/xxx/yyy/zzz
        としている。
        """
        if ".app" in selected_save_dir:
            selected_save_dir = pathlib.Path(selected_save_dir).parents[2]

    main(member_name, selected_save_dir)
    messagebox.showinfo("完了", "すべてのブログを保存しました")


# フォルダ指定の関数
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    entry1.set(iDirPath)


# ------------------------------------------------------------
# GUI設計
# ------------------------------------------------------------

# 画面全体
main_win = tk.Tk()
main_win.title("Blog to Image")
main_win.geometry("600x150")

# フレーム
frame1 = ttk.Frame(main_win)
frame1.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

# メンバー名ラベル
member_name_label = ttk.Label(frame1, text="メンバー名")

# メンバー名選択コンボボックス
member_name = list(member_num)
variable = tk.StringVar()
combo = ttk.Combobox(
    frame1, values=member_name, textvariable=variable, state="readonly"
)
combo.set(member_name[0])

# ------------------------------------------------------------

# 保存先ラベル
out_path_label = ttk.Label(frame1, text="保存先")

# 保存先入力欄
entry1 = tk.StringVar()
IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=30, state="readonly")

# 「フォルダ参照」ボタン
IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)

# ------------------------------------------------------------

# 実行ボタン
app_btn = ttk.Button(frame1, text="保存開始", width=12, command=app)

# ------------------------------------------------------------

# ウィジェットの配置
member_name_label.grid(column=0, row=0, pady=10)
combo.grid(column=1, row=0, sticky=tk.EW, padx=5)
out_path_label.grid(column=0, row=1, pady=10)
IDirEntry.grid(column=1, row=1, sticky=tk.EW, padx=5)
IDirButton.grid(column=2, row=1, sticky=tk.EW, padx=5)
app_btn.grid(column=1, row=3, padx=10, pady=10)

# 伸縮設定
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)

main_win.mainloop()
