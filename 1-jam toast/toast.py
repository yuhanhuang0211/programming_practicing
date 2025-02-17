import tkinter as tk
from PIL import Image, ImageTk
import random

# 建立主視窗
window = tk.Tk()
window.geometry("1000x500")         # 視窗寬 1000、高 500
window.title("toast")               # 標題「toast」
window.configure(bg="white")        # 背景顏色為白色

# 初始化圖片參數
current_image = None                # 用來儲存目前顯示的圖片
toast_on_floor_image = None         # 用來儲存掉到地板後顯示的圖片
img_width, img_height = 175, 130    # 設定圖片的顯示大小（寬 175、高 130）

# 載入圖片
try:
    # 第一張圖片
    img = Image.open("jam on toast_.png").convert("RGBA")   # 開啟圖片並轉換為 RGBA 格式
    resized_img = img.resize((img_width, img_height))       # 調整圖片大小
    current_image = ImageTk.PhotoImage(resized_img)         # 將圖片轉換為 tkinter 可用格式
    
    # 第二張圖片
    img2 = Image.open("toast on floor_.png").convert("RGBA")  # 開啟第二張圖片並轉換為 RGBA 格式
    resized_img2 = img2.resize((img_width, img_height))  # 調整第二張圖片的大小
    toast_on_floor_image = ImageTk.PhotoImage(resized_img2)  # 將第二張圖片轉換為 tkinter 格式
except Exception as e:
    print("圖片載入錯誤：", e)  # 如果圖片載入失敗，顯示錯誤訊息

# 使用 Canvas
canvas = tk.Canvas(window, width=1000, height=500, bg="white", highlightthickness=0)  # 建立畫布，大小為 1000x500，背景為白色，去除邊框
canvas.pack()  # 顯示畫布

# 隨機初始位置
x = random.randint(0, 1000 - img_width)  # 隨機生成圖片的 X 座標
y = random.randint(0, 500 - img_height)  # 隨機生成圖片的 Y 座標

# 在 Canvas 上繪製圖片
image_id = canvas.create_image(x, y, anchor="nw", image=current_image)  # 在畫布上放置圖片，位置為隨機生成的 (x, y)

# 記錄拖曳狀態
is_dragging = False  # 是否正在拖曳圖片
is_fallen = False  # 圖片是否已經掉到地板
current_display_image = current_image  # 記錄目前顯示的圖片

# 滑鼠事件
def start_drag(event):
    global is_dragging, is_fallen, current_display_image
    is_dragging = True  # 開始拖曳圖片
    
    # 如果圖片已經掉到地板，則恢復為原來的圖片
    if is_fallen:
        current_display_image = current_image
        canvas.itemconfig(image_id, image=current_display_image)  # 更新畫布上的圖片
        is_fallen = False  # 標記圖片未掉落

def drag_image(event):
    if is_dragging:  # 如果圖片正在被拖曳
        canvas.coords(image_id, event.x, event.y)  # 更新圖片位置為滑鼠當前位置

def stop_drag(event):
    global is_dragging, is_fallen
    is_dragging = False  # 停止拖曳
    
    # 如果圖片未曾掉落，則觸發掉落動作
    if not is_fallen:
        drop_to_bottom()  # 開始圖片的掉落

# 慢速下落
def drop_to_bottom():
    global is_fallen, current_display_image
    x, y = canvas.coords(image_id)  # 取得圖片當前的位置
    target_y = 500 - img_height - 50  # 計算圖片應該下落的目標位置，距離底部 50 像素
    
    def fall():
        nonlocal y  # 設定 y 為外部變數
        if y < target_y:  # 當圖片還沒到達目標位置
            y += 5  # 每次下落 5 像素
            canvas.coords(image_id, x, y)  # 更新圖片的座標
            canvas.after(5, fall)  # 每 5 毫秒執行一次 fall 函數，達到下落效果
        else:
            # 當圖片到達底部時，顯示掉落後的圖片
            current_display_image = toast_on_floor_image
            canvas.itemconfig(image_id, image=current_display_image)  # 更新畫布上的圖片為掉到地板的圖片
            is_fallen = True  # 標記圖片已經掉落
    
    fall()  # 開始掉落過程

# 綁定滑鼠事件
canvas.tag_bind(image_id, "<Button-1>", start_drag)  # 綁定滑鼠按下事件，開始拖曳
canvas.tag_bind(image_id, "<B1-Motion>", drag_image)  # 綁定滑鼠移動事件，拖曳圖片
canvas.tag_bind(image_id, "<ButtonRelease-1>", stop_drag)  # 綁定滑鼠釋放事件，停止拖曳並觸發掉落

# 開始主迴圈
window.mainloop()  # 啟動 tkinter 主迴圈，讓視窗顯示並等待用戶操作
