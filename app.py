class WaterBuddyApp:
    def __init__(self):
        self.current_view = 'blueprint'  # or 'demo'
        self.age_group = ''
        self.daily_goal = 2000
        self.total_intake = 0
        self.mobile_menu_open = False

    def reset_app(self):
        self.age_group = ''
        self.total_intake = 0

    def switch_view(self, view):
        if view in ['blueprint', 'demo']:
            self.current_view = view

    def set_age_group(self, age_group):
        self.age_group = age_group

    def set_daily_goal(self, goal):
        self.daily_goal = goal

    def add_intake(self, amount):
        self.total_intake += amount

    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    def render(self):
        if self.current_view == 'blueprint':
            self.render_blueprint()
        else:
            self.render_demo()

    def render_blueprint(self):
        print("Rendering Blueprint View")
        # More detailed rendering and tab selection logic would go here

    def render_demo(self):
        if not self.age_group:
            self.render_welcome_screen()
        else:
            self.render_home_screen()

    def render_welcome_screen(self):
        print("Welcome Screen - Please select age group")

    def render_home_screen(self):
        print(f"Home Screen - Age group: {self.age_group}, Daily Goal: {self.daily_goal}, Total Intake: {self.total_intake}")

# Example usage:
app = WaterBuddyApp()
app.render()  # renders initial view
app.set_age_group('25-35')
app.add_intake(500)
app.render()
