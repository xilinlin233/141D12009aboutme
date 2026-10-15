import turtle
import time
import os 

# ==========================================
# 1. 圖片檔案設定
# ==========================================
IMG_IDLE = "chicken_idle.gif"       
IMG_SLEEP = "chicken_sleep.gif"     

IMG_ACTION = {
    "drink": "chicken_drink.gif",   
    "eat": "chicken_eat.gif",       
    "snack": "chicken_snack.gif",   
    "shower": "chicken_shower.gif", 
    "3c": "chicken_3c.gif",         
    "sport": "chicken_sport.gif",   
    "read": "chicken_read.gif"      
}

# ==========================================
# 2. 按鈕顏色設定 (一般顏色 : 按下顏色)
# ==========================================
BUTTON_COLORS = {
    "drink":  ("cyan", "darkcyan"),
    "eat":    ("yellow", "gold"),
    "snack":  ("pink", "hotpink"),
    "shower": ("lightblue", "steelblue"),
    "sleep":  ("lightgray", "gray"),
    "3c":     ("violet", "darkviolet"),
    "sport":  ("orange", "darkorange"),
    "read":   ("lightgreen", "forestgreen"),
    "start":  ("lightgreen", "forestgreen"), # 開始按鈕
    "retry":  ("lightgreen", "forestgreen")  # 再玩一次按鈕
}

# ==========================================
# 3. 遊戲數值與設定
# ==========================================

wn = turtle.Screen()
wn.title("健康電子雞") 
wn.bgcolor("white") 
wn.setup(width=800, height=600)
wn.tracer(0)

def register_images_safe():
    images_to_load = [IMG_IDLE, IMG_SLEEP] + list(IMG_ACTION.values())
    for img in images_to_load:
        if os.path.exists(img):
            wn.addshape(img)
            print(f"成功載入: {img}")
        else:
            print(f"找不到: {img} (將使用預設方塊)")

register_images_safe()

START_MINUTES = 7 * 60 
current_minutes = START_MINUTES

counters = {
    "drink": 0, "eat": 0, "snack": 0, "3c": 0, 
    "shower": 0, "read": 0, "sport": 0, "water_cc": 0
}

game_state = "start"

# ==========================================
# 4. 建立繪圖物件
# ==========================================

pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()

btn_pen = turtle.Turtle()
btn_pen.speed(0)
btn_pen.hideturtle()

player = turtle.Turtle()
player.speed(0)
player.shape("square") 
player.color("gold")   
player.penup()
player.hideturtle()    

# ==========================================
# 5. 繪圖輔助函數
# ==========================================

def update_player_image(img_name):
    if img_name in wn.getshapes():
        player.shape(img_name)
        player.color("white") 
    else:
        player.shape("square")
        player.color("gold")

def draw_rect(t, x, y, w, h, color, fill=True):
    t.penup()
    t.goto(x, y)
    t.color(color)
    if fill:
        t.begin_fill()
    else:
        t.pensize(3) 
    for _ in range(2):
        t.forward(w)
        t.right(90)
        t.forward(h)
        t.right(90)
    if fill:
        t.end_fill()
    else:
        t.pensize(1)

def draw_button(x, y, text, color, width=140, height=50):
    """繪製按鈕的基本函數"""
    draw_rect(btn_pen, x, y, width, height, color, fill=True)
    btn_pen.penup()
    btn_pen.goto(x + width/2, y - height + 15)
    btn_pen.color("black")
    btn_pen.write(text, align="center", font=("Arial", 12, "bold"))

def animate_click(x, y, text, action_key):
    """
    [新增] 按鈕點擊動畫函數
    x, y: 按鈕位置
    text: 按鈕文字
    action_key: 對應 BUTTON_COLORS 的鍵值
    """
    normal_color, press_color = BUTTON_COLORS[action_key]
    
    # 1. 畫出「按下顏色」
    draw_button(x, y, text, press_color)
    wn.update() # 強制更新畫面
    time.sleep(0.1) # 暫停 0.1 秒
    
    # 2. 畫回「一般顏色」
    draw_button(x, y, text, normal_color)
    wn.update()

def get_time_string():
    total_min = current_minutes
    h = (total_min // 60) % 24
    m = total_min % 60
    day_prefix = "隔日 " if total_min >= 24 * 60 else ""
    return f"{day_prefix}{h:02d}:{m:02d}"

# ==========================================
# 6. 畫面繪製
# ==========================================

def draw_start_screen():
    global game_state
    game_state = "start"
    
    pen.clear()
    btn_pen.clear()
    player.hideturtle() 
    
    pen.goto(0, 200)
    pen.write("健康電子雞", align="center", font=("Arial", 30, "bold"))
    
    rules = (
        "【遊戲規則】\n\n"
        "1. 每天早上 07:00 開始。\n"
        "2. 選擇你的行動，小雞會做出對應動作。\n"
        "3. 按下「睡覺」進入結算畫面。\n\n"
        "【行動消耗時間】\n"
        "● 不耗時：喝水 (+150cc)\n"
        "● 30分鐘：洗澡、吃飯、吃零食、使用3C\n"
        "● 1小時：運動、看書\n"
    )
    pen.goto(0, -50) 
    pen.write(rules, align="center", font=("Arial", 14, "normal"))
    
    # 開始按鈕
    draw_button(-75, -150, "開始遊戲", BUTTON_COLORS["start"][0])

def draw_game_interface():
    global game_state
    game_state = "playing"
    
    pen.clear()
    btn_pen.clear()
    
    player.showturtle()
    player.goto(0, 50)
    update_player_image(IMG_IDLE)
    
    # 第一排
    draw_button(-310, -120, "喝水", BUTTON_COLORS["drink"][0])    
    draw_button(-150, -120, "吃飯", BUTTON_COLORS["eat"][0])  
    draw_button(10,   -120, "吃零食", BUTTON_COLORS["snack"][0])  
    draw_button(170,  -120, "洗澡", BUTTON_COLORS["shower"][0]) 
    
    # 第二排
    draw_button(-310, -200, "睡覺", BUTTON_COLORS["sleep"][0]) 
    draw_button(-150, -200, "使用3C", BUTTON_COLORS["3c"][0]) 
    draw_button(10,   -200, "運動", BUTTON_COLORS["sport"][0])
    draw_button(170,  -200, "看書", BUTTON_COLORS["read"][0]) 

    update_status_text()

def update_status_text():
    pen.clear()
    time_str = get_time_string()
    status_text = (
        f"現在時間: {time_str}  |  今日喝水量: {counters['water_cc']} cc\n"
        f"----------------------------------------"
    )
    pen.goto(0, 180) 
    pen.write(status_text, align="center", font=("Courier", 16, "bold"))

# ==========================================
# 7. 結算畫面
# ==========================================

def get_feedback_message():
    if current_minutes > 1440: return "不要熬夜，早點睡覺！"
    elif current_minutes < 1380: return "7點才起床，現在睡會睡太久哦！"
    elif counters['water_cc'] < 1500: return "記得多喝一點水哦！"
    elif counters['eat'] < 3: return "一日三餐能維持生理時鐘穩定！"
    elif 4 <= counters['eat'] <= 6: return "少量多餐可以穩定血糖，減輕腸胃負擔！"
    elif counters['snack'] > 2: return "零食很好吃，但注意不要吃太多！"
    elif counters['3c'] > 6: return "讓眼睛多多休息，去戶外走走吧！"
    elif counters['sport'] == 0: return "多運動有益身體健康！"
    else: return "今天也是健康的一天!"

def draw_summary_screen():
    global game_state
    game_state = "summary"
    
    pen.clear()
    btn_pen.clear()
    
    update_player_image(IMG_SLEEP)
    player.showturtle()
    player.goto(0, 200) 
    
    pen.goto(0, 100)
    pen.color("blue")
    pen.write("本日生活結算", align="center", font=("Arial", 26, "bold"))
    
    pen.color("black")
    
    stats_list = [
        f"吃飯：{counters['eat']} 次",
        f"喝水：{counters['water_cc']} cc",
        f"吃零食：{counters['snack']} 次",
        f"使用3C：{counters['3c']} 次",
        f"運動：{counters['sport']} 次",
        f"看書：{counters['read']} 次",
        f"洗澡：{counters['shower']} 次",
        f"就寢時間：{get_time_string()}"
    ]
    
    start_y = 50
    for i, text in enumerate(stats_list):
        col_x = -100 if i % 2 == 0 else 100
        row_y = start_y - (i // 2) * 30
        pen.goto(col_x, row_y)
        pen.write(text, align="center", font=("Arial", 14, "normal"))

    feedback = get_feedback_message()
    
    pen.goto(0, -80)
    pen.color("red")
    pen.write("【健康小提醒】", align="center", font=("Arial", 16, "bold"))
    pen.goto(0, -120)
    pen.color("black")
    pen.write(feedback, align="center", font=("Arial", 18, "bold"))
    
    # 再玩一次按鈕
    draw_button(-75, -180, "再玩一次", BUTTON_COLORS["retry"][0])

# ==========================================
# 8. 邏輯控制
# ==========================================

def reset_game():
    global current_minutes, counters
    current_minutes = START_MINUTES
    for key in counters:
        counters[key] = 0
    draw_start_screen()

def add_action(action_type):
    global current_minutes
    
    if action_type in IMG_ACTION:
        update_player_image(IMG_ACTION[action_type])
    
    time_cost = 0
    if action_type == "drink":
        counters['drink'] += 1
        counters['water_cc'] += 150
        time_cost = 0 
    elif action_type in ["eat", "snack", "3c", "shower"]:
        counters[action_type] += 1
        time_cost = 30 
    elif action_type in ["sport", "read"]:
        counters[action_type] += 1
        time_cost = 60 
        
    current_minutes += time_cost
    update_status_text()

# ==========================================
# 9. 事件處理 (已加入動畫呼叫)
# ==========================================

def handle_click(x, y):
    global game_state
    
    # --- 狀態: 開始畫面 ---
    if game_state == "start":
        if -75 < x < 75 and -200 < y < -150:
             # 播放動畫
             animate_click(-75, -150, "開始遊戲", "start")
             
             game_state = "playing"
             draw_game_interface()
        return

    # --- 狀態: 結算畫面 ---
    if game_state == "summary":
        if -75 < x < 75 and -230 < y < -180:
            # 播放動畫
            animate_click(-75, -180, "再玩一次", "retry")
            
            reset_game()
        return

    # --- 狀態: 遊戲中 ---
    if game_state == "playing":
        # 先設定好點擊資訊，預設為 None
        target_btn = None # (x, y, text, key)
        
        # 第一排判斷
        if -170 < y < -120:
            if -310 < x < -170:   target_btn = (-310, -120, "喝水", "drink")
            elif -150 < x < -10:  target_btn = (-150, -120, "吃飯", "eat")
            elif 10 < x < 150:    target_btn = (10, -120, "吃零食", "snack")
            elif 170 < x < 310:   target_btn = (170, -120, "洗澡", "shower")

        # 第二排判斷
        elif -250 < y < -200:
            if -310 < x < -170:   target_btn = (-310, -200, "睡覺", "sleep")
            elif -150 < x < -10:  target_btn = (-150, -200, "使用3C", "3c")
            elif 10 < x < 150:    target_btn = (10, -200, "運動", "sport")
            elif 170 < x < 310:   target_btn = (170, -200, "看書", "read")

        # 如果有點擊到按鈕，執行動畫與動作
        if target_btn:
            btn_x, btn_y, btn_text, btn_key = target_btn
            
            # 1. 播放動畫
            animate_click(btn_x, btn_y, btn_text, btn_key)
            
            # 2. 執行邏輯
            if btn_key == "sleep":
                draw_summary_screen()
            else:
                add_action(btn_key)

# ==========================================
# 10. 啟動程式
# ==========================================

wn.onclick(handle_click)
reset_game()

while True:
    try:
        wn.update()
        time.sleep(0.01)
    except:
        break
