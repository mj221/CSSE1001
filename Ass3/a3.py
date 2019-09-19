import tkinter as tk
import math
from tkinter.simpledialog import askstring
from tkinter import messagebox
from tkinter import *
from model import TowerGame
from tower import (SimpleTower, MissileTower, AbstractTower,
                   PulseTower, TurretTower) 
from enemy import (SimpleEnemy, SteelEnemy, InvincibleEnemy)
from utilities import Stepper
from view import GameView
from level import AbstractLevel
from advanced_view import TowerView, SimpleView
from high_score_manager import HighScoreManager


from core import Unit, Point2D, UnitManager
from enemy import AbstractEnemy
from range_ import AbstractRange, CircularRange, PlusRange, DonutRange
from utilities import Countdown, euclidean_distance, rotate_point, rotate_toward, angle_between, polar_to_rectangular, \
    rectangles_intersect, get_delta_through_centre

BACKGROUND_COLOUR = "#4a2f48"

__author__ = "Minjae Lee"
__copyright__ = ""


# Could be moved to a separate file, perhaps levels/simple.py, and imported
class MyLevel(AbstractLevel):
    """A simple game level containing examples of how to generate a wave"""
    waves = 20

    def get_wave(self, wave):
        """Returns enemies in the 'wave_n'th wave

        Parameters:
            wave_n (int): The nth wave

        Return:
            list[tuple[int, AbstractEnemy]]: A list of (step, enemy) pairs in the
                                             wave, sorted by step in ascending order 
        """
        enemies = []

        if wave == 1:
            # A hardcoded singleton list of (step, enemy) pairs

            enemies = [(10, SimpleEnemy()), (50, SimpleEnemy())]
            
        elif wave == 2:
            # A hardcoded list of multiple (step, enemy) pairs

            enemies = [(10, SimpleEnemy()), (15, CustomEnemy()), (30, CustomEnemy())]
        elif 3 <= wave < 10:
            # List of (step, enemy) pairs spread across an interval of time (steps)

            steps = int(40 * (wave ** .5))  # The number of steps to spread the enemies across
            count = wave * 2  # The number of enemies to spread across the (time) steps

            for step in self.generate_intervals(steps, count):
                enemies.append((step, SimpleEnemy()))

        elif wave == 10:
            # Generate sub waves
            sub_waves = [
                # (steps, number of enemies, enemy constructor, args, kwargs)
                (50, 10, SimpleEnemy, (), {}),  # 10 enemies over 50 steps
                (100, None, None, None, None),  # then nothing for 100 steps
                (50, 10, SteelEnemy, (), {})  # then another 10 enemies over 50 steps
            ]
            
            enemies = self.generate_sub_waves(sub_waves)
            enemies = [(10, BossEnemy())]
        else:  # 11 <= wave <= 20
            # Now it's going to get hectic

            sub_waves = [
                (
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    SimpleEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),
                # ...
            ]
            enemies = self.generate_sub_waves(sub_waves)
            enemies = [(10, CustomEnemy()), (15, SteelEnemy()), (30, BossEnemy())]
        
        return enemies


class TowerGameApp(Stepper):
    """Top-level GUI application for a simple tower defence game"""

    # All private attributes for ease of reading
    _current_tower = None
    _paused = False
    _won = None

    _level = None
    _wave = None
    _score = None
    _coins = None
    _lives = None

    _master = None
    _game = None
    _view = None

    _highscore = None
    
    _name = str

    
    def __init__(self, master: tk.Tk, delay: int = 20):
        """Construct a tower defence game in a root window

        Parameters:
            master (tk.Tk): Window to place the game into
        """
        self._master = master
        super().__init__(master, delay=delay)

        self._highscore = highscore = HighScoreManager()
        highscore.load(filename='high_scores.json')
        
        self._game = game = TowerGame()
        master.title("Tower of Defence by Minjae Lee")
        self.setup_menu(master)

        # create a game view and draw grid borders
        self._view = view = GameView(master, size=game.grid.cells,
                                     cell_size=game.grid.cell_size,
                                     bg='antique white')
        view.pack(side=tk.LEFT, expand=True)

        # Task 1.3 (Status Bar): instantiate status bar

        self._status_bar = StatusBar(master)
        self._status_bar.pack(fill = tk.X)

        # Task 1.5 (Play Controls): instantiate widgets here
        
        self.play_control = tk.Frame(master, bg = 'white')
        self.play_control.pack(side = tk.BOTTOM, fill = tk.Y)

        self.click_next_wave = tk.Button(self.play_control, text = "Next Wave", command = self.next_wave)
        self.click_next_wave.pack(side = tk.LEFT)
        
        self.click_play = tk.Button(self.play_control, text = "Play", command =self._toggle_paused)
        self.click_play.pack(side = tk.LEFT)
        
        # bind game events
        game.on("enemy_death", self._handle_death)
        game.on("enemy_escape", self._handle_escape)
        game.on("cleared", self._handle_wave_clear)

        # Task 1.2 (Tower Placement): bind mouse events to canvas here
        self._view.bind('<Button-1>', self._left_click)
        self._view.bind('<Motion>', self._move)
        self._view.bind('<Leave>', self._mouse_leave)

        self._view.bind('<Button-3>', self._right_click)

        # Level
        self._level = MyLevel()

        self.select_tower(SimpleTower)
        view.draw_borders(game.grid.get_border_coordinates())

        # Get ready for the game
        self._setup_game()

        towers = [ ]
        for positions, tower in towers:
            for position in positions:
                self._game.place(position, tower_type=tower)

##        # Task 2.3 (ShopTowerView): instantiate gui here
        self.towers = [
            SimpleTower,
            MissileTower,
            EnergyTower,
            PulseTower,
            TurretTower,
            CoinTower
        ]

        shop = tk.Frame(master)
        shop.pack(fill=tk.X)
        
        # Create views for each tower & store to update if availability changes
        self._tower_views = []
        for tower_class in self.towers:
            tower = tower_class(self._game.grid.cell_size // 2)

            self._shop_view = view= ShopTowerView(shop, tower, bg=BACKGROUND_COLOUR, highlight="#4b3b4a",
                                 click_command=lambda class_=tower_class: self.select_tower(class_))
            view.pack(fill=tk.X)
            self._tower_views.append((tower, view))  # Can use to check if tower is affordable when refreshing view
        
    def is_available(self, tower):
        """Check if the selected tower is affordable 

        Parameters:
            tower (AbstractTower): The tower type selected
        """
        if tower(self._game.grid.cell_size).get_value() <= self._coins:
            # True if the tower value is smaller than the current coin value
            self._available = True
        else:
            self._available = False
        
    def setup_menu(self, master):
        """Setup file menu 

        Parameters:
            master (tk.Tk): Place into the current window form
        """
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self._new_game)
        filemenu.add_command(label="High Scores", command=self._get_highscore)
        filemenu.add_command(label="Exit", command=self._exit)

    def _toggle_paused(self, paused=None):
        """Toggles or sets the paused state

        Parameters:
            paused (bool): Toggles/pauses/unpauses if None/True/False, respectively
        """
        if paused is None:
            paused = not self._paused

        # Task 1.5 (Play Controls): Reconfigure the pause button here
        self.click_play.config(state="normal", text = "Play")
        
        if paused:
            self.click_play.config(text="Play")
            self.pause()
        else:
            self.click_play.config(text="Pause")
            self.start()

        self._paused = paused

    def _setup_game(self):
        """Sets up the game"""
        self._wave = 0
        self._score = 0
        self._coins = 140
        self._lives = 20

        self._won = False       
        # Task 1.3 (Status Bar): Update status here
        # Calls _set method for respective values
        self._set_wave(self._wave)  
        self._set_score(self._score)
        self._set_gold(self._coins)
        self._set_lives(self._lives)
        # Task 1.5 (Play Controls): Re-enable the play controls here (if they were ever disabled)
        self.click_play.config(state="normal")
        self.click_next_wave.config(state="normal")
        self._game.reset()

        self._toggle_paused(paused=True)

    def _new_game(self):
        """Restart game."""
        
        self._view.delete("tower", "enemy", "obstacle") # delete towers, enemies and all obstacle objects from view    
        self._game.enemies=[]
        self._setup_game()
        
    def _get_highscore(self):
        """Get high scores in a new window."""
        self._player_list = player_list = self._highscore.get_entries(game='basic')
        
        self.high_scores=tk.Toplevel(root)
        self.high_scores.title('High Score List')

        self.high_score_title = tk.Label(self.high_scores, text= 'Top 10 Players\n')
        self.high_score_title.pack()

        for i, player_list in enumerate(player_list):   # List top scoring players from 1 to 10 format
            self.high_score_list = tk.Label(self.high_scores, text = "[{}] ,{}\n".format(i+1,player_list)).pack()
                  
    def _exit(self) :
        """Close the application."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    def refresh_view(self):
        """Refreshes the game view"""
        if self._step_number % 2 == 0:
            self._view.draw_enemies(self._game.enemies)

            self._coins += (EarntCoins._earnings * EarntCoins._counter) #Used for updating Advanced Tower: 'Coin Supply'. Coin earning rate will increase when more towers are placed.
            self._set_gold(self._coins)
                # Advanced Tower: 1 Coin Tower = 3 coins earnt occasionally =, 2 Coin tower = 4 coins earnt, etc
                # There is only a little subtantial increase in coin earning rate when 2 or more coin towers are placed.
          
        self._view.draw_towers(self._game.towers)
        self._view.draw_obstacles(self._game.obstacles)
        
    def refresh_view_shop(self):
        """Refreshes the shop tower availability"""
        if self._step_number % 2 ==0:
            for tower in self.towers:
                self.is_available(tower)
                self._shop_view.set_available(self._available)
                
        
    def _step(self):
        """
        Perform a step every interval

        Triggers a game step and updates the view

        Returns:
            (bool) True if the game is still running
        """
        self._game.step()
        self.refresh_view()
        if self._step_number % 2 ==0:   # Let boss spawn a minion (simple enemy) using steps
            if call_enemy._spawn_count == 50:
                
                minion = SimpleEnemy()
                boss = BossEnemy()
                minion.position = self._game.grid.cell_to_pixel_centre(self._game.grid.pixel_to_cell((call_enemy._position)))
                minion.set_cell_size(self._game.grid.cell_size)
                self._game.enemies.append(minion)
                
##        self.refresh_view_shop()      Refer to ShopTowerView(tk.Frame), as to why I commented this method out.
        return not self._won
    
    def _move(self, event):
        """
        Handles the mouse moving over the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        if self._current_tower.get_value() > self._coins:
            return

        # move the shadow tower to mouse position
        position = event.x, event.y
        self._current_tower.position = position

        legal, grid_path = self._game.attempt_placement(position)

        # find the best path and covert positions to pixel positions
        path = [self._game.grid.cell_to_pixel_centre(position)
                for position in grid_path.get_shortest()]

        # Task 1.2 (Tower placement): Draw the tower preview here
        self._view.draw_preview(self._current_tower, legal)
        self._view.draw_path(path)

    def _mouse_leave(self, event):
        """
        Delete the previews when the mouse leaves the window

        Parameter:
            event (tk.Event): Tkinter mouse event  
        """
        if (event.x > self._view.cell_size or event.x < 0 or
            event.y > self._view.cell_size or event.y < 0):
            self._view.delete("path", "range", "shadow")
            
    def _left_click(self, event):
        """
        Place tower when a grid is left clicked

        Parameter:
            event (tk.Event): Tkinter mouse event  
        """

        if self._lives != 0 and self._won == False:
            if self._coins >= int(self._current_tower.__class__.base_cost):
                self._coins -= int(self._current_tower.__class__.base_cost)
                self._set_gold(self._coins)
                self._view.delete("shadow")
                # retrieve position to place tower
                position = event.x, event.y
                cell_position = self._game.grid.pixel_to_cell(position)

                if self._game.place(cell_position, tower_type=self._current_tower.__class__):
                    # Task 1.2 (Tower Placement): Attempt to place the tower being previewed
                    pass
                elif not self._game.place(cell_position, tower_type=SimpleTower(self._game.grid.cell_size).__class__):
                    # If a tower cannot be placed in that position, then a tower exists so call method upgrade_tower.
                    self.upgrade_tower(event)
        self.refresh_view()

    def upgrade_tower(self, event):
        """
        Provide an option to upgrade tower when a tower is left clicked.
        There are things to note: The upgrade option is only available for Simple Towers
                                  I had changed the design element of the upgrade bar so that a small window pops up instead of in a new frame 
                                  
        Parameter:
            event (tk.Event): Tkinter mouse event  
        """
        # Get tower position
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)
        # Get the name of the tower
        removed_tower = self._game.remove(cell_position)
        self._game.place(cell_position, tower_type=removed_tower.__class__)
        self._coins += int(self._current_tower.__class__.base_cost)
        self._set_gold(self._coins)
    
        if removed_tower.name == "Coin Supply":
            # Fixed a bug when Coin Supply Tower's earning rate is skyrocketed when it is selected
            if self._paused:
                EarntCoins._counter -= 1
                return None
            else:
                EarntCoins._counter -= 1
                self._coins -= EarntCoins._counter
                self._set_gold(self._coins)
                self.refresh_view()
                
        elif removed_tower.name == "Simple Tower":
            def confirm_upgrade():
                if self.upgrade_1.get() == 1 and self.upgrade_2.get() ==0:
                    if SimpleTower2(self._game.grid.cell_size).get_value()>self._coins:
                        # An upgrade can be made only if there are enough coins
                        messagebox.showinfo("Tower Upgrade", "Not enough coins to upgrade")
                        self.upgrades.destroy()
                    else:
                        self._coins -= SimpleTower2(self._game.grid.cell_size).get_value()
                        self._game.remove(cell_position)
                        self._game.place(cell_position, tower_type=SimpleTower2(self._game.grid.cell_size).__class__)
                        self.refresh_view()
                elif self.upgrade_1.get() == 0 and self.upgrade_2.get() ==1:
                    if SimpleTower3(self._game.grid.cell_size).get_value()>self._coins:
                        messagebox.showinfo("Tower Upgrade", "Not enough coins to upgrade")
                        self.upgrades.destroy()
                    else: 
                        self._coins -= SimpleTower3(self._game.grid.cell_size).get_value()
                        self._game.remove(cell_position)
                        self._game.place(cell_position, tower_type=SimpleTower3(self._game.grid.cell_size).__class__)
                        self.refresh_view()
                elif self.upgrade_1.get() == 1 and self.upgrade_2.get() ==1:
                    if SimpleTower4(self._game.grid.cell_size).get_value()>self._coins:
                        messagebox.showinfo("Tower Upgrade", "Not enough coins to upgrade")
                        self.upgrades.destroy()
                    else:
                        self._coins -= SimpleTower4(self._game.grid.cell_size).get_value()
                        self._game.remove(cell_position)
                        self._game.place(cell_position, tower_type=SimpleTower4(self._game.grid.cell_size).__class__)
                        self.refresh_view()
                self._set_gold(self._coins)
                
            # Open a new window with checkboxes that lists possible upgrade options
            self.upgrades=tk.Toplevel(root)
            self.upgrades.geometry('+{}+{}'.format(event.x, event.y))
            self.upgrades.wm_attributes('-alpha',0.7)
            self.upgrades.title('Upgrade Selected Tower')
            
            self.upgrade_1 = IntVar()
            self.upgrade_tower_1=tk.Checkbutton(self.upgrades, text = "Upgrade Range (Cost:40)", variable = self.upgrade_1).pack()
            self.upgrade_2 = IntVar()
            self.upgrade_tower_2=tk.Checkbutton(self.upgrades, text = "Upgrade Damage (Cost:40)", variable = self.upgrade_2).pack()
            self.upgrade_confirm = tk.Button(self.upgrades, text = "Ok",
                                             command = lambda: [f() for f in [confirm_upgrade, self.upgrades.destroy]]).pack()


    def _right_click(self, event):
        """Event handler for clicking the tower (Selling towers)"""
        # retrieve position to place tower

        if self._lives != 0 and self._won == False:            
            position = event.x, event.y
            cell_position = self._game.grid.pixel_to_cell(position)
            removed_tower = self._game.remove(cell_position)
            self._coins += int(removed_tower.get_value()* 0.8)  # 0.8 of the original tower price
            self._set_gold(self._coins)
            # Advanced Tower: Coin Supply - Remove 1 count from the counter which is used to determine the rate at which coin is earnt.
            if removed_tower.name == "Coin Supply": 
                EarntCoins._counter -= 1
            self.refresh_view()
            
    def next_wave(self):
        """Sends the next wave of enemies against the player"""
        if self._wave == self._level.get_max_wave():
            return

        if self._lives != 0:
            self._wave += 1
        else:
            return None

        # Task 1.3 (Status Bar): Update the current wave display here
        self._set_wave(self._wave)

        # Task 1.5 (Play Controls): Disable the add wave button here (if this is the last wave)
        if self._wave == 20:
            self.click_next_wave.config(state="disabled")
        
        # Generate wave and enqueue
        wave = self._level.get_wave(self._wave)
        for step, enemy in wave:
            enemy.set_cell_size(self._game.grid.cell_size)

        self._game.queue_wave(wave)

    def select_tower(self, tower):
        """
        Set 'tower' as the current tower

        Parameters:
            tower (AbstractTower): The new tower type
        """
        self._current_tower = tower(self._game.grid.cell_size)

    def _handle_death(self, enemies):
        """
        Handles enemies dying

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which died in a step
        """
        bonus = len(enemies) ** .5
        for enemy in enemies:
            self._coins += enemy.points
            self._score += int(enemy.points * bonus)

        # Task 1.3 (Status Bar): Update coins & score displays here
        self._set_score(self._score)
        self._set_gold(self._coins)

    def _handle_escape(self, enemies):
        """
        Handles enemies escaping (not being killed before moving through the grid

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which escaped in a step
        """
        self._lives -= len(enemies)
        for enemy in enemies:
            enemy.health = 0
        if self._lives < 0:
            self._lives = 0
        
        # Task 1.3 (Status Bar): Update lives display here
        self._set_lives(self._lives)  

        # Handle game over
        if self._lives == 0:
            self._set_lives(self._lives)
            self._handle_game_over(won=False)

    def _handle_wave_clear(self):
        """Handles an entire wave being cleared (all enemies killed)"""
        if self._wave == self._level.get_max_wave():
            self._handle_game_over(won=True)

        # Task 1.5 (Play Controls): remove this line
        self.next_wave()

    def _handle_game_over(self, won=False):
        """Handles game over
        
        Parameter:
            won (bool): If True, signals the game was won (otherwise lost)
        """
        self._won = won
        self.stop()
        self.click_next_wave.config(state='disabled')
        self.click_play.config(state='disabled')
        # Task 1.4 (Dialogs): show game over dialog here
        if self._won:
            messagebox.showinfo("Game Over!", "You Won")
        else:
            messagebox.showinfo("Game Over!", "You Lost")

        self._highscore = highscore = HighScoreManager()    # Call highscore manager
        if highscore.does_score_qualify(self._score):
            self._name = askstring('High Score Achieved!', 'Please tell us your name!')
            while self._name == None or self._name == '':
                # Asking for a valid name(if none or empty string)
                self._name = askstring('High Score Achieved!', 'Please Enter a valid name!')
            highscore.add_entry(self._name, self._score)
            highscore.save(filename = 'high_scores.json')
        else:
            return None
        
            
    def _set_wave(self, wave_num):
        """Update wave label in status bar

        Parameters:
            wave_num (int): Current wave
        """
        self._status_bar._wave_label.config(text="Wave: {}/20".format(wave_num))
    def _set_score(self, score_num):
        """Update score label in status bar

        Parameters:
            score_num (int): Current score
        """
        self._status_bar._score_label.config(text="{}".format(score_num))
    def _set_gold(self, gold_num):
        """Update the coin label in status bar

        Parameters:
            gold_num (int): Current number of coins
        """
        self._status_bar._gold_label.config(text="{} coins".format(gold_num))
    def _set_lives(self, lives_num):
        """Update lives label in status bar

        Parameters:
            lives_num (int): Lives remaining
        """
        self._status_bar._lives_label.config(text="{} lives".format(lives_num))

    
class StatusBar(tk.Frame):
    def __init__(self, master):
        """Construct a status bar in a root window

        Parameters:
            master (tk.Tk): Window to place the status bar into
        """

        self._master = master
        super().__init__(master, bg = 'white')

        # create a game view and draw grid borders

        self._wave_label = tk.Label(self, text='Wave: ', bg = 'white')
        self._wave_label.pack()
        
        self._score_label = tk.Label(self, text='Score', bg = 'white')
        self._score_label.pack(pady = 10)

        self.gold_image = tk.PhotoImage(file="coins.gif")
        self.lives_image = tk.PhotoImage(file="heart.gif")
        self._gold_label = tk.Label(self, text='Gold', image=self.gold_image, compound ="left", bg = 'white')
        self._gold_label.pack(side = tk.LEFT, anchor = tk.N, expand = True)
        
        self._lives_label = tk.Label(self, text='Lives Remaining', bg = 'white', image = self.lives_image,
                                     compound = "left")
        self._lives_label.pack(side = tk.LEFT,anchor = tk.N, expand = True)

class ShopTowerView(tk.Frame):

    def __init__(self, master, tower, click_command, *args, **kwargs):
        """Construct a shop bar for tower in a root window

        Parameters:
            master (tk.Tk): Frame to place the shop into
        """
        self._master = master
        super().__init__(master, bg = 'purple')
        tower.position = (tower.cell_size // 1, tower.cell_size // 1)  # Position in centre
        tower.rotation = 3 * math.pi / 2  # Point up
        self._canvas = w = tk.Canvas(self, bg = 'purple', bd=3, height = 55)
        w.pack(fill=tk.X)
        TowerView.draw(w, tower)
        self.item = w.create_text(180,30,fill = 'white',font = "Times 15 italic bold",
                                 text=tower.name +"\n{}".format(tower.get_value()))
        
        def click(event):
            """call back function for when a tower is clicked from the canvas
            """
            return click_command()
            

        w.bind("<Button-1>", click)
        
    def set_available(self, available):
        # The updating of the availability of the towers DO WORK to a certain extent, however, due to
        # unprecedented reasons, it severely interferes with how the step method works for 'Advanced Tower: Coin Supply'. So I had
        # commented out the function that is responsible for calling set_available in the _step(self) method.
        """ Check if the tower is available

        Parmeters:
            available (bool): True if the tower is available
        """
        if available == True:
            self._canvas.itemconfig(self.item, fill = 'white')
##            ("It is available")
            
        elif available == False:
            self._canvas.itemconfig(self.item, fill = 'red')
##            ("It is not available")

        
class EnergyTower(SimpleTower):
    """A tower that deals energy damage"""
    name = "Energy Tower"

    range = CircularRange(1.5)
    cool_down_steps = 0
    base_cost = 70
    level_cost = 50

    colour = 'yellow'

    rotation_threshold = (1 / 6) * math.pi

    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=7, level: int = 1):
        super().__init__(cell_size, grid_size, rotation, base_damage, level)

    def step(self, data):
        """Rotates toward 'target' and attacks if possible"""
        self.cool_down.step()

        target = self.get_unit_in_range(data.enemies)

        if target is None:
            return

        angle = angle_between(self.position, target.position)
        partial_angle = rotate_toward(self.rotation, angle, self.rotation_threshold)
        self.rotation = partial_angle

        if partial_angle == angle:
            target.damage(self.get_damage(), 'energy')

class CoinTower(SimpleTower):
    """Tower that supplies coin for use. 1 tower gains 3 coins each interval (it makes use of the in game steps).
       2 towers = 4, 3 towers = 5 coins, etc.
    """
    name = "Coin Supply"

    colour = 'gold'

    cool_down_steps = 45
    base_cost = 40
    level_cost = 60

    range = DonutRange(0,0) # Give a range of 0 to prevent targeting of enemies

    rotation_threshold = (1 / 3) * math.pi

    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=150, level: int = 1):
        super().__init__(cell_size, grid_size=grid_size, rotation=rotation, base_damage=base_damage, level=level)
        self._earning_rate = 1  # However due to the step interval in-game, the player earns 3 coins for first tower
        EarntCoins._counter += 1    # Counter allows the player to stack up coin earning rates when two or more coin supply is placed
    def step(self, units):
        self.cool_down.step()
        if not self.cool_down.is_done():
            # Stop the tower from earning coins during the cooldown process.
            EarntCoins._earnings = 0
            return None
        else:
            EarntCoins._earnings = self._earning_rate
            self.cool_down.start()

class EarntCoins(object):   # A simple temp class used to share values with the Coin Supply Tower and the main function(globally)
    # All private attributes for ease of reading
    _earnings = 0
    _counter = 0
    
class CustomEnemy(SimpleEnemy):
    """A custom enemy that can only be dealt with by energy damage"""
    max_health = 250
    colour = 'green'
    points = 150

    def damage(self, damage, type_):
        if type_ in ('energy',):
            super().damage(damage, type_)
            
class BossEnemy(SimpleEnemy):
    """Advanced Enemy: Boss is an enemy with an absurd amount of health and occasionally heals itself.
        Boss spawns in SimpleEnemies occasionally as well.
        
    """
    name = "Boss"
    colour = 'grey'
    points = 200
    def __init__(self, grid_size=(.8, .8), grid_speed=1/60, health=5500):
        super().__init__(grid_size, grid_speed, health)
        call_enemy._spawn_count = 0

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)
            
            call_enemy._spawn_count += 1  # Add a count for each step it makes. At count 50, a new minion will be spawned.
            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size
            self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)
            call_enemy._position = self.position    # Current updated position
            movement -= partial_movement
            
            # Heal health
            if self.health < 5500:
                self.health += 10        # Heal health by 15 points
             
            intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas
    
class call_enemy(object):   # Temporary class used to store variables and share between BossEnemy() and steps
    # All private attributes for ease of reading
    _spawn_count =0
    _position = 0
    
class SimpleTower2(SimpleTower):
    """A variation of upgraded simple tower with improved range that rotates towards enemies and shoots projectiles at them"""
    name = 'Simple Tower v2'
    colour = 'dark red' 

    range = CircularRange(5)    # Increased range
    cool_down_steps = 0

    base_cost = 40
    level_cost = 15

    rotation_threshold = (1 / 6) * math.pi

    earn_coins = 0
    
    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=1, level: int = 1):
        super().__init__(cell_size, grid_size, rotation, base_damage, level)
  

class SimpleTower3(SimpleTower):
    """Another variation of the upgraded simple tower with greater damage capacity that rotates towards enemies and shoots projectiles at them"""
    name = 'Simple Tower v3'
    colour = 'red' 

    range = CircularRange(1.5)
    cool_down_steps = 0

    base_cost = 40
    level_cost = 15

    rotation_threshold = (1 / 6) * math.pi

    earn_coins = 0
    
    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=8, level: int = 1):
        super().__init__(cell_size, grid_size, rotation, base_damage, level)


class SimpleTower4(SimpleTower):
    """A fully upgraded simple tower with both improved range and damage that rotates towards enemies and shoots projectiles at them"""
    name = 'Simple Tower v4'
    colour = 'purple' 

    range = CircularRange(5)
    cool_down_steps = 0

    base_cost = 80
    level_cost = 15

    rotation_threshold = (1 / 6) * math.pi

    earn_coins = 0
    
    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=8, level: int = 1):
        super().__init__(cell_size, grid_size, rotation, base_damage, level)

def main(root):
    
    app = TowerGameApp(root)
    root.protocol("WM_DELETE_WINDOW", app._exit)    # Ask for confirmation when exiting via 'X'
    root.mainloop()
                        
if __name__ == "__main__" :
    root = tk.Tk()
    main(root)



