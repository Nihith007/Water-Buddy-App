
import tkinter as tk
from tkinter import ttk, messagebox
from math import floor
import random
import time
import threading

# --------------------------
# Configuration (tweakable)
# --------------------------
WINDOW_WIDTH = 420   # width similar to mobile screenshot
WINDOW_HEIGHT = 900  # height similar to screenshot
FONT = ("Inter", 11)
HEADER_FONT = ("Inter", 22, "bold")
BIG_FONT = ("Inter", 42, "bold")
TILE_FONT = ("Inter", 14)
TANK_WIDTH = 220
TANK_HEIGHT = 260

# Base goal by age mapping (ml)
def base_goal_by_age(age:int) -> int:
    if age <= 5:
        return 1000
    if age <= 12:
        return 1400
    if age <= 18:
        return 1700
    if age <= 55:
        return 2000
    if age <= 70:
        return 1800
    return 1600

BMI_ADJUSTMENTS = {
    "Underweight": -200,
    "Normal": 0,
    "Overweight": 200,
    "Obese": 300,
    "Unknown": 0
}

HEALTH_CONDITION_ADJUSTMENTS = {
    "Normal / Healthy": 0,
    "Athlete / High Activity": 300,
    "Summer / Hot Climate": 300,
    "Pregnancy / Nursing": 500,
    "Diabetic": 100,
    "Heart / Kidney issues": -250
}

DAILY_TIPS = [
    "Staying hydrated keeps your skin healthy and glowing!",
    "Drink a glass of water before each meal.",
    "Carry a reusable bottle — you'll drink more when it’s nearby.",
    "Infuse water with lemon or cucumber for a flavor boost.",
    "Set an alarm every 90 minutes to take a sip.",
    "Swap one sugary drink a day with water for better health.",
]

HEALTH_OPTIONS = list(HEALTH_CONDITION_ADJUSTMENTS.keys())

# --------------------------
# Helper functions
# --------------------------
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0:
        return 0.0
    h_m = height_cm / 100.0
    bmi = weight_kg / (h_m * h_m)
    return round(bmi, 1)

def bmi_category(bmi: float) -> str:
    if bmi == 0:
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"

# --------------------------
# Confetti animation class
# --------------------------
class ConfettiCanvas(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.geometry(f"{master.winfo_screenwidth()}x{master.winfo_screenheight()}+0+0")
        self.lift()
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.particles = []
        self.running = True
        self.colors = ['#ff595e', '#ffca3a', '#8ac926', '#1982c4', '#6a4c93']
        self.spawn(200)
        self.animate()

    def spawn(self, n=100):
        w = self.winfo_screenwidth()
        for _ in range(n):
            self.particles.append({
                'x': random.uniform(0, w),
                'y': random.uniform(-400, -10),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(2, 8),
                'size': random.uniform(6, 14),
                'color': random.choice(self.colors),
                'rot': random.uniform(0, 360)
            })

    def animate(self):
        if not self.running:
            return
        self.canvas.delete("all")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        new_particles = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15  # gravity
            x, y, s = p['x'], p['y'], p['size']
            # draw rotated rectangle approximation as oval for simplicity
            self.canvas.create_oval(x, y, x+s, y+s, fill=p['color'], outline="")
            if y < h + 20:
                new_particles.append(p)
        self.particles = new_particles
        if len(self.particles) < 80:
            self.spawn(80)
        self.after(16, self.animate)

    def stop(self):
        self.running = False
        self.destroy()

# --------------------------
# Main Application
# --------------------------
class WaterBuddyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaterBuddy+")
        # fixed window size to match screenshots
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        # center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.geometry(f"+{x}+{y}")
        self.configure(bg="#ffffff")

        # Shared state
        self.age = tk.IntVar(value=13)
        self.height_cm = tk.DoubleVar(value=165.0)
        self.weight_kg = tk.DoubleVar(value=45.0)
        self.condition = tk.StringVar(value=HEALTH_OPTIONS[0])
        self.bmi = tk.DoubleVar(value=calculate_bmi(self.weight_kg.get(), self.height_cm.get()))
        self.bmi_cat = tk.StringVar(value=bmi_category(self.bmi.get()))
        self.base_goal = tk.IntVar(value=base_goal_by_age(self.age.get()))
        self.goal = tk.IntVar(value=max(300, self.base_goal.get()))
        self.drunk = tk.IntVar(value=0)
        self.daily_tip = tk.StringVar(value=random.choice(DAILY_TIPS))

        # Page frames
        self.container = tk.Frame(self, bg="#f7f9ff")
        self.container.place(relwidth=1, relheight=1)

        self.frames = {}
        for F in (OnboardingPage, ReviewPage, TrackerPage):
            page = F(parent=self.container, controller=self)
            self.frames[F.__name__] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)

        # start on onboarding
        self.show_frame("OnboardingPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def update_bmi_and_goal(self):
        bmi = calculate_bmi(self.weight_kg.get(), self.height_cm.get())
        self.bmi.set(bmi)
        self.bmi_cat.set(bmi_category(bmi))
        base = base_goal_by_age(max(1, self.age.get()))
        self.base_goal.set(base)
        bmi_adj = BMI_ADJUSTMENTS.get(self.bmi_cat.get(), 0)
        health_adj = HEALTH_CONDITION_ADJUSTMENTS.get(self.condition.get(), 0)
        self.goal.set(max(300, base + bmi_adj + health_adj))
        # reset drunk when recalculating (consistent with screenshots where starting new calculation sets 0)
        self.drunk.set(0)
        self.daily_tip.set(random.choice(DAILY_TIPS))

    def add_water(self, amount_ml):
        self.drunk.set(self.drunk.get() + amount_ml)
        self.daily_tip.set(random.choice(DAILY_TIPS))
        # if goal reached or exceeded, trigger confetti
        if self.drunk.get() >= self.goal.get():
            # spawn confetti window
            confetti = ConfettiCanvas(self)
            # stop confetti after 6 seconds
            def stop_confetti_after_delay():
                time.sleep(6)
                try:
                    confetti.stop()
                except:
                    pass
            threading.Thread(target=stop_confetti_after_delay, daemon=True).start()
            # also show a messagebox and possibly balloons-like message (messagebox used)
            messagebox.showinfo("Goal reached!", f"Congratulations — you reached your daily goal of {self.goal.get()} ml!\nTotal drank: {self.drunk.get()} ml")

    def reset_to_onboarding(self):
        # clear and set defaults
        self.age.set(13)
        self.height_cm.set(165.0)
        self.weight_kg.set(45.0)
        self.condition.set(HEALTH_OPTIONS[0])
        self.update_bmi_and_goal()
        # Go to onboarding page
        self.show_frame("OnboardingPage")

# --------------------------
# Page: Onboarding
# --------------------------
class OnboardingPage(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        # header
        header_frame = tk.Frame(self, bg="#ffffff")
        header_frame.pack(pady=18)
        drip = tk.Label(header_frame, text="💧", font=("Segoe UI Emoji", 44), bg="#ffffff")
        drip.pack()
        title = tk.Label(header_frame, text="Welcome to WaterBuddy+", font=HEADER_FONT, bg="#ffffff", fg="#123d8a")
        title.pack()
        subtitle = tk.Label(header_frame, text="Your personalized hydration companion", font=("Inter", 12), bg="#ffffff", fg="#666")
        subtitle.pack()

        # form area with card like backgrounds
        form = tk.Frame(self, bg="#ffffff")
        form.pack(pady=12, padx=14, fill="x")

        # Age card
        age_card = tk.Frame(form, bg="#eef6ff", bd=0, relief="flat", padx=12, pady=16)
        age_card.pack(fill="x", pady=(6, 12))
        tk.Label(age_card, text="Age (years)", bg="#eef6ff", fg="#123d8a", font=TILE_FONT).pack(anchor="w")
        self.age_spin = tk.Spinbox(age_card, from_=1, to=120, textvariable=controller.age, font=FONT, width=8)
        self.age_spin.pack(pady=6, anchor="w")

        # Height card
        h_card = tk.Frame(form, bg="#fbf0ff", padx=12, pady=16)
        h_card.pack(fill="x", pady=(6, 12))
        tk.Label(h_card, text="Height (cm)", bg="#fbf0ff", fg="#6a2fb8", font=TILE_FONT).pack(anchor="w")
        self.height_entry = tk.Entry(h_card, textvariable=controller.height_cm, font=FONT)
        self.height_entry.pack(pady=6, anchor="w")

        # Weight card
        w_card = tk.Frame(form, bg="#f2fff4", padx=12, pady=16)
        w_card.pack(fill="x", pady=(6, 12))
        tk.Label(w_card, text="Weight (kg)", bg="#f2fff4", fg="#1b7a49", font=TILE_FONT).pack(anchor="w")
        self.weight_entry = tk.Entry(w_card, textvariable=controller.weight_kg, font=FONT)
        self.weight_entry.pack(pady=6, anchor="w")

        # Health condition
        hc_card = tk.Frame(form, bg="#fff3ea", padx=12, pady=16)
        hc_card.pack(fill="x", pady=(6, 12))
        tk.Label(hc_card, text="Health Condition", bg="#fff3ea", fg="#6b2f22", font=TILE_FONT).pack(anchor="w")
        self.condition_combo = ttk.Combobox(hc_card, values=HEALTH_OPTIONS, state="readonly", textvariable=controller.condition)
        self.condition_combo.pack(pady=6, anchor="w", fill="x")

        # Calculate button
        calc_btn = tk.Button(self, text="Calculate My Goal →", font=("Inter", 14), bg="#9aa0a6", fg="#fff", relief="flat", padx=8, pady=8,
                             command=self.on_calculate)
        calc_btn.pack(pady=10, ipadx=10)

        # small footer note
        footer = tk.Label(self, text="💡 No login required • All data stays private • Free forever", bg="#ffffff", fg="#3773d6", font=("Inter", 10))
        footer.pack(side="bottom", pady=8)

    def on_calculate(self):
        # Validate inputs, update controller state
        try:
            age = int(self.controller.age.get())
            height = float(self.controller.height_cm.get())
            weight = float(self.controller.weight_kg.get())
        except Exception as e:
            messagebox.showerror("Invalid input", "Please enter valid numeric values for age, height, and weight.")
            return
        self.controller.update_bmi_and_goal()
        self.controller.show_frame("ReviewPage")

# --------------------------
# Page: Review / Goal Calculation
# --------------------------
class ReviewPage(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        # header
        header = tk.Frame(self, bg="#ffffff")
        header.pack(pady=12)
        tk.Label(header, text="💧", font=("Segoe UI Emoji", 44), bg="#ffffff").pack()
        tk.Label(header, text="Welcome to WaterBuddy+", font=HEADER_FONT, bg="#ffffff", fg="#123d8a").pack()
        tk.Label(header, text="Your personalized hydration companion", font=("Inter", 12), bg="#ffffff", fg="#666").pack()

        card = tk.Frame(self, bg="#eef7ff", bd=1, relief="solid", padx=12, pady=12)
        card.pack(pady=12, padx=12, fill="x")

        # Profile tiles (age, bmi, height, weight)
        tiles = tk.Frame(card, bg="#eef7ff")
        tiles.pack(pady=6)
        # grid 2x2
        t1 = ttk.Label(tiles, text=f"Age\n{controller.age.get()} years", justify="center", anchor="center", font=TILE_FONT, background="#ffffff")
        t2 = ttk.Label(tiles, text=f"BMI\n{controller.bmi.get()} \n{controller.bmi_cat.get()}", justify="center", anchor="center", font=TILE_FONT, background="#ffffff")
        t3 = ttk.Label(tiles, text=f"Height\n{controller.height_cm.get()} cm", justify="center", anchor="center", font=TILE_FONT, background="#ffffff")
        t4 = ttk.Label(tiles, text=f"Weight\n{controller.weight_kg.get()} kg", justify="center", anchor="center", font=TILE_FONT, background="#ffffff")
        # Place them
        t1.grid(row=0, column=0, padx=8, pady=8, ipadx=10, ipady=10)
        t2.grid(row=0, column=1, padx=8, pady=8, ipadx=10, ipady=10)
        t3.grid(row=1, column=0, padx=8, pady=8, ipadx=10, ipady=10)
        t4.grid(row=1, column=1, padx=8, pady=8, ipadx=10, ipady=10)
        condition_label = tk.Label(card, text=f"Condition: {controller.condition.get()}", bg="#eef7ff", font=TILE_FONT)
        condition_label.pack(pady=(8,0))

        # Goal calculation area
        goal_card = tk.Frame(self, bg="#f2fff4", bd=1, relief="solid", padx=12, pady=12)
        goal_card.pack(pady=12, padx=12, fill="x")
        tk.Label(goal_card, text="Goal Calculation", bg="#f2fff4", font=("Inter", 16, "bold")).pack(anchor="w")

        # details
        details = tk.Frame(goal_card, bg="#f2fff4")
        details.pack(pady=8, fill="x")
        tk.Label(details, text=f"Base Goal (Age): {controller.base_goal.get()} ml", bg="#f2fff4", anchor="w").pack(fill="x")
        bmi_adj = BMI_ADJUSTMENTS.get(controller.bmi_cat.get(), 0)
        health_adj = HEALTH_CONDITION_ADJUSTMENTS.get(controller.condition.get(), 0)
        tk.Label(details, text=f"BMI Adjustment ({controller.bmi_cat.get()}): {bmi_adj:+} ml", bg="#f2fff4", anchor="w").pack(fill="x")
        tk.Label(details, text=f"Health Condition ({controller.condition.get()}): {health_adj:+} ml", bg="#f2fff4", anchor="w").pack(fill="x")

        tk.Label(goal_card, text=f"Your Daily Goal: {controller.goal.get()} ml", font=("Inter", 18, "bold"), bg="#f2fff4").pack(pady=8)

        # Back / Start buttons
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(pady=6)
        back_btn = tk.Button(btn_frame, text="← Back", bg="#e6e7ea", fg="#000", command=self.back)
        back_btn.grid(row=0, column=0, padx=8)
        start_btn = tk.Button(btn_frame, text="Start Tracking! →", bg="#1f66ff", fg="#fff", command=self.start_tracking)
        start_btn.grid(row=0, column=1, padx=8)

    def back(self):
        self.controller.show_frame("OnboardingPage")

    def start_tracking(self):
        # refresh state values shown in tracker (some labels update on show)
        self.controller.show_frame("TrackerPage")

# --------------------------
# Page: Tracker
# --------------------------
class TrackerPage(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="#f7fbff")
        self.controller = controller
        header = tk.Frame(self, bg="#f7fbff")
        header.pack(pady=10)
        # top stats row
        stats = tk.Frame(self, bg="#f7fbff")
        stats.pack(pady=6, fill="x")
        self.today_label = tk.Label(stats, text=f"Today's Goal\n{controller.goal.get()} ml", bg="#f7fbff", font=TILE_FONT, anchor="w")
        self.progress_label = tk.Label(stats, text=f"Progress\n0%", bg="#f7fbff", font=TILE_FONT)
        self.remaining_label = tk.Label(stats, text=f"Remaining\n{controller.goal.get()} ml", bg="#f7fbff", font=TILE_FONT, anchor="e")
        self.today_label.pack(side="left", padx=(12,0))
        self.progress_label.pack(side="left", expand=True)
        self.remaining_label.pack(side="right", padx=(0,12))

        # big visual and mood
        visual = tk.Frame(self, bg="#f7fbff")
        visual.pack(pady=8)
        self.mood_lbl = tk.Label(visual, text="😐", font=("Segoe UI Emoji", 40), bg="#f7fbff")
        self.mood_lbl.pack()
        self.mood_text = tk.Label(visual, text="Let's Begin!", bg="#f7fbff")
        self.mood_text.pack()

        # tank canvas
        self.tank_canvas = tk.Canvas(self, width=TANK_WIDTH, height=TANK_HEIGHT, bd=0, highlightthickness=0)
        self.tank_canvas.pack(pady=6)
        # draw tank border
        self.tank_canvas.create_rectangle(6,6,TANK_WIDTH-6,TANK_HEIGHT-6, width=6, outline="#2b7be4", joinstyle="round", radius=0)
        self.water_rect = None
        self.update_visual()

        # amount text + progress bar
        self.amount_label = tk.Label(self, text=f"{controller.drunk.get()} ml / {controller.goal.get()} ml", bg="#f7fbff", font=("Inter", 12, "bold"))
        self.amount_label.pack(pady=6)
        self.pbar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=260)
        self.pbar.pack()

        # add buttons
        btns = tk.Frame(self, bg="#f7fbff")
        btns.pack(pady=12)
        btn250 = tk.Button(btns, text="+250 ml\n1 cup", bg="#2d7aff", fg="#fff", width=12, height=2, command=lambda: self.add_quick(250))
        btn500 = tk.Button(btns, text="+500 ml\n2 cups", bg="#2d7aff", fg="#fff", width=12, height=2, command=lambda: self.add_quick(500))
        btn250.grid(row=0, column=0, padx=8)
        btn500.grid(row=0, column=1, padx=8)

        # custom add
        custom = tk.Frame(self, bg="#f7fbff")
        custom.pack(pady=8)
        tk.Label(custom, text="Custom amount (ml)", bg="#f7fbff").grid(row=0, column=0, padx=6)
        self.custom_entry = tk.Entry(custom, width=10)
        self.custom_entry.grid(row=0, column=1, padx=6)
        add_btn = tk.Button(custom, text="Add", bg="#1cc1a0", fg="#fff", command=self.add_custom)
        add_btn.grid(row=0, column=2, padx=6)

        # Tip and Reset row
        tip_reset = tk.Frame(self, bg="#f7fbff")
        tip_reset.pack(pady=8)
        self.tip_label = tk.Label(tip_reset, text=controller.daily_tip.get(), bg="#efe6ff", fg="#5b2fb8", wraplength=360, justify="center", padx=8, pady=8)
        self.tip_label.pack(pady=6, padx=12, fill="x")

        bottom = tk.Frame(self, bg="#f7fbff")
        bottom.pack(side="bottom", pady=12)
        reset_btn = tk.Button(bottom, text="Reset", bg="#e6e7ea", command=self.on_reset)
        reset_btn.grid(row=0, column=0, padx=8)
        back_btn = tk.Button(bottom, text="← Back", bg="#e6e7ea", command=self.go_back)
        back_btn.grid(row=0, column=1, padx=8)

        # schedule visual update loop
        self.after(200, self.periodic_update)

    def update_visual(self):
        goal = self.controller.goal.get()
        drunk = self.controller.drunk.get()
        remaining = max(0, goal - drunk)
        progress_pct = int((drunk / goal) * 100) if goal > 0 else 0
        # update top labels
        self.today_label.config(text=f"Today's Goal\n{goal} ml")
        self.progress_label.config(text=f"Progress\n{progress_pct}%")
        self.remaining_label.config(text=f"Remaining\n{remaining} ml")
        # mood
        if progress_pct == 0:
            self.mood_lbl.config(text="😐")
            self.mood_text.config(text="Let's Begin!")
        elif progress_pct < 50:
            self.mood_lbl.config(text="🙂")
            self.mood_text.config(text="Good start! Keep drinking!")
        elif progress_pct < 100:
            self.mood_lbl.config(text="😀")
            self.mood_text.config(text="Great progress!")
        else:
            self.mood_lbl.config(text="🏆")
            self.mood_text.config(text="Goal Reached! Well done!")

        # update tank: draw water rectangle height proportional
        self.tank_canvas.delete("all")
        # draw rounded-ish border
        self.tank_canvas.create_rectangle(6,6,TANK_WIDTH-6,TANK_HEIGHT-6, width=6, outline="#2b7be4")
        fill_pct = min(1.0, drunk / goal) if goal > 0 else 0
        fill_h = int(TANK_HEIGHT * fill_pct)
        # draw water (from bottom)
        self.tank_canvas.create_rectangle(8, TANK_HEIGHT - 8 - fill_h, TANK_WIDTH - 8, TANK_HEIGHT - 8, fill="#79c8ff", outline="")
        # couple of bubble circles:
        if fill_h > 60:
            self.tank_canvas.create_oval(TANK_WIDTH/2 - 10, TANK_HEIGHT - 14 - fill_h + 20, TANK_WIDTH/2 + 10, TANK_HEIGHT - fill_h + 6, fill="#bfeaff", outline="")
        self.amount_label.config(text=f"{drunk} ml / {goal} ml")
        self.pbar['value'] = min(100, (drunk / goal) * 100 if goal > 0 else 0)
        self.tip_label.config(text=self.controller.daily_tip.get())

    def periodic_update(self):
        self.update_visual()
        # autorun next update
        self.after(300, self.periodic_update)

    def add_quick(self, amount):
        self.controller.add_water(amount)

    def add_custom(self):
        try:
            amt = int(self.custom_entry.get())
            if amt <= 0:
                raise ValueError
        except:
            messagebox.showerror("Invalid amount", "Enter a positive integer amount in ml.")
            return
        self.controller.add_water(amt)
        self.custom_entry.delete(0, tk.END)

    def go_back(self):
        # just go to review
        self.controller.show_frame("ReviewPage")

    def on_reset(self):
        # Confirmation dialog with progress snapshot
        goal = self.controller.goal.get()
        drunk = self.controller.drunk.get()
        pct = int((drunk / goal) * 100) if goal > 0 else 0
        msg = f"This will clear your current progress and reset your daily water intake to 0 ml.\n\nCurrent progress: {drunk} ml / {goal} ml ({pct}%)\n\nThis action cannot be undone.\n\nReset now?"
        if messagebox.askyesno("Start New Day?", msg):
            # reset in controller and return to onboarding
            self.controller.reset_to_onboarding()

# --------------------------
# Run the app
# --------------------------
if __name__ == "__main__":
    app = WaterBuddyApp()
    app.mainloop()
