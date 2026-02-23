



import tkinter as tk
from tkinter import messagebox


class SalesGUI:

    def __init__(self, logic):
        self.logic = logic
        self.root = tk.Tk()
        self.root.title("売上分析アプリ")
        self.root.geometry("600x600")

        self._create_widgets()

    def _create_widgets(self):


        tk.Label(self.root, text="並び順").pack()

        self.sort_order = tk.StringVar()
        self.sort_order.set("降順")

        tk.Radiobutton(self.root, text="降順", variable=self.sort_order, value="降順").pack()
        tk.Radiobutton(self.root, text="昇順", variable=self.sort_order, value="昇順").pack()


        # 列選択
        tk.Label(self.root, text="集計項目").pack()

        self.columns = ["商品", "日付", "支払方法", "担当者", "店舗"]
        self.selected_column = tk.StringVar()
        self.selected_column.set("商品")

        tk.OptionMenu(self.root, self.selected_column, *self.columns).pack()

        # 期間入力
        tk.Label(self.root, text="開始日 (YYYY-MM-DD)").pack()
        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack()

        tk.Label(self.root, text="終了日 (YYYY-MM-DD)").pack()
        self.end_entry = tk.Entry(self.root)
        self.end_entry.pack()

        # ボタン
        tk.Button(self.root, text="集計", command=self.show_result).pack(pady=5)
        tk.Button(self.root, text="グラフ表示", command=self.show_graph).pack(pady=5)
        tk.Button(self.root, text="CSV出力", command=self.export_csv).pack(pady=5)


        # 出力エリア
        self.output = tk.Text(self.root, height=15)
        self.output.pack(pady=10)

    def _get_filtered_data(self):

        start = self.start_entry.get()
        end = self.end_entry.get()

        if start and end:
            data = self.logic.filter_by_period(start, end)

            if data is None:
                messagebox.showerror("日付エラー", "YYYY-MM-DD形式で入力してください")
                return None

            return data

        return self.logic.data

    def show_result(self):

        data = self._get_filtered_data()
        if data is None:
            return

        column = self.selected_column.get()
        result = self.logic.total_by_column(column, data)

        self.output.delete("1.0", tk.END)

        reverse_flag = True if self.sort_order.get() == "降順" else False

        for k, v in sorted(result.items(), key=lambda x: x[1], reverse=reverse_flag):
            self.output.insert(tk.END, f"{k} : {v:,} 円\n")



        # for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True):
        #     self.output.insert(tk.END, f"{k} : {v:,} 円\n")

    def export_csv(self):

        data = self._get_filtered_data()
        if data is None:
            return

        column = self.selected_column.get()
        result = self.logic.total_by_column(column, data)

        if not result:
            messagebox.showinfo("データなし", "出力するデータがありません")
            return

        import csv

        with open("export_result.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([column, "売上"])

            for k, v in result.items():
                writer.writerow([k, v])

        messagebox.showinfo("完了", "export_result.csv を出力しました")



    def show_graph(self):

        data = self._get_filtered_data()
        if data is None:
            return

        column = self.selected_column.get()
        result = self.logic.total_by_column(column, data)

        if not result:
            messagebox.showinfo("データなし", "集計結果がありません")
            return

        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        import matplotlib

        matplotlib.rcParams["font.family"] = "Meiryo"

        labels = list(result.keys())
        values = list(result.values())

        plt.close("all")
        plt.figure()

        plt.bar(labels, values)

        plt.title(f"{column}別 売上")
        plt.xticks(rotation=45)

        plt.gca().yaxis.set_major_formatter(
            ticker.StrMethodFormatter('{x:,.0f}')
        )

        plt.tight_layout()
        plt.show()

    def run(self):
        self.root.mainloop()
