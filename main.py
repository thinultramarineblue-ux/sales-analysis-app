




from logic import SalesLogic
from gui import SalesGUI

if __name__ == "__main__":
    app_logic = SalesLogic("sales_today.csv")
    gui = SalesGUI(app_logic)
    gui.run()

app = SalesLogic("sales_today.csv")

result = app.total_by_column("商品")



print("商品別売上")
for k, v in result.items():
    print(k, v)








# py main.py