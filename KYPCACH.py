import sys
import time
import random
from colors import *
from Class import *
from hint import *
 
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Деревня - Экономическая стратегия")

mouse_x, mouse_y = pygame.mouse.get_pos()

BOTTOM_BAR_HEIGHT = 90  
REMAINING_HEIGHT = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
LEFT_PANEL_WIDTH = REMAINING_HEIGHT // 3  
RIGHT_PANEL_WIDTH = SCREEN_WIDTH - LEFT_PANEL_WIDTH

GRID_CELL_SIZE = 40  

gold = 400                 
gold_limit = 500            
potions = 400               
potions_limit = 500         
population = 10             
free_population = 10        
village_level = 0           
hint_level = [0]
defenders_village = 0       
defenders_village_limit = 0 
last_income_time = time.time()  
game_over = False
game_won = False

selected_building = None   
buildings = []              
unique_buildings = {}       
mines = {}                  
potions_maker = {}          
military_camp = {}          
defenders = []

BUILDING_SIZES = {
    "Ратуша": (3, 2),          
    "Золотохранилище": (2, 2),      
    "Шахта": (2, 2),                
    "Зельехранилище": (2, 2),     
    "Зельеварка": (2, 2),          
    "Стрелковая башня": (2, 2),
    "Военный лагерь": (3, 3),
    "Стена" : (1, 1)
}

BUILDING_COSTS = {
    "Ратуша": {"gold": 200, "potions": 0},  
    "Золотохранилище": {"gold": 50, "potions": 0},
    "Шахта": {"gold": 50, "potions": 0},
    "Зельехранилище": {"gold": 50, "potions": 0},
    "Зельеварка": {"gold": 50, "potions": 0},
    "Стрелковая башня": {"gold": 50, "potions": 0},
    "Военный лагерь": {"gold": 100, "potions": 0},
    "Стена" : {"gold": 5, "potions": 0}
}

BUILDING_LIMITS = {
    0: {"Ратуша": 1, "Золотохранилище": 0, "Шахта": 0, "Зельехранилище": 0,
        "Зельеварка": 0, "Стрелковая башня": 0, "Военный лагерь": 0, "Стена": 0},
    1: {"Ратуша": 1, "Золотохранилище": 2, "Шахта": 2, "Зельехранилище": 2,
        "Зельеварка": 2, "Стрелковая башня": 4, "Военный лагерь": 2, "Стена": 15},
    2: {"Ратуша": 1, "Золотохранилище": 3, "Шахта": 3, "Зельехранилище": 3,
        "Зельеварка": 3, "Стрелковая башня": 5, "Военный лагерь": 3, "Стена": 30},
    3: {"Ратуша": 1, "Золотохранилище": 4, "Шахта": 4, "Зельехранилище": 4,
        "Зельеварка": 4, "Стрелковая башня": 6, "Военный лагерь": 4, "Стена": 45},
    4: {"Ратуша": 1, "Золотохранилище": 5, "Шахта": 5, "Зельехранилище": 5,
        "Зельеварка": 5, "Стрелковая башня": 7, "Военный лагерь": 5, "Стена": 60},
    5: {"Ратуша": 1, "Золотохранилище": 6, "Шахта": 6, "Зельехранилище": 6,
        "Зельеварка": 6, "Стрелковая башня": 8, "Военный лагерь": 6, "Стена": 75}
}

BUILDING_LEVEL_LIMITS = {
    1: {"Ратуша": 1, "Золотохранилище": 1, "Шахта": 1, "Зельехранилище": 1,
        "Зельеварка": 1, "Стрелковая башня": 1, "Военный лагерь": 1, "Стена": 1},
    2: {"Ратуша": 2, "Золотохранилище": 2, "Шахта": 2, "Зельехранилище": 2,
        "Зельеварка": 2, "Стрелковая башня": 2, "Военный лагерь": 2, "Стена": 2},
    3: {"Ратуша": 3, "Золотохранилище": 3, "Шахта": 3, "Зельехранилище": 3,
        "Зельеварка": 3, "Стрелковая башня": 3, "Военный лагерь": 3, "Стена": 3},
    4: {"Ратуша": 4, "Золотохранилище": 4, "Шахта": 4, "Зельехранилище": 4,
        "Зельеварка": 4, "Стрелковая башня": 4, "Военный лагерь": 4, "Стена": 4},
    5: {"Ратуша": 5, "Золотохранилище": 5, "Шахта": 5, "Зельехранилище": 5,
        "Зельеварка": 5, "Стрелковая башня": 5, "Военный лагерь": 5, "Стена": 5},
}

BUILDING_HEALTH = {
    "Ратуша": 250,
    "Золотохранилище": 50,  
    "Шахта": 50,
    "Зельехранилище": 50,
    "Зельеварка": 50,
    "Стрелковая башня": 100,
    "Военный лагерь": 100,
    "Стена" : 20
}

UPGRADE_COSTS = {
    "Золотохранилище": {"gold": 100, "potions": 50},
    "Шахта": {"gold": 80, "potions": 40},
    "Зельехранилище": {"gold": 100, "potions": 50},
    "Зельеварка": {"gold": 80, "potions": 40},
    "Стрелковая башня": {"gold": 120, "potions": 60},
    "Военный лагерь": {"gold": 150, "potions": 75},
    "Стена": {"gold": 20, "potions": 10}
}

UPGRADE_MULTIPLIERS = {
    "Золотохранилище": {"capacity": 1.5, "health": 1.2},
    "Шахта": {"income": 1.5, "health": 1.2},
    "Зельехранилище": {"capacity": 1.5, "health": 1.2},
    "Зельеварка": {"income": 1.5, "health": 1.2},
    "Стрелковая башня": {"damage": 1.5, "range": 1.2, "health": 1.3},
    "Военный лагерь": {"capacity": 1.5, "health": 1.2},
    "Стена": {"health": 1.5},
    "Ратуша": {"health": 1.3}
}

ENEMY_LEVEL = {
    1: 16,
    2: 20,
    3: 28,
    4: 32,
    5: 44
}

selected_building_id = None  
menu_visible = [False, None]
levelup_menu_visible = [False, None]
building_menu_rect = pygame.Rect(0, 0, 300, 150)
assign_input_active = False
assign_input_text = ""
recall_input_active = False
recall_input_text = ""
legend_active = False
hint_active = True
hint_updated = False 
shown_hints = set() 
current_menu_buttons = {}
levelup_menu_rect = None
upgrade_button_rect = None
cancel_button_rect = None

left_panel_rect = pygame.Rect(0, 0, LEFT_PANEL_WIDTH, REMAINING_HEIGHT)
right_panel_rect = pygame.Rect(LEFT_PANEL_WIDTH, 0, RIGHT_PANEL_WIDTH, REMAINING_HEIGHT)
bottom_bar_rect = pygame.Rect(0, REMAINING_HEIGHT, SCREEN_WIDTH, BOTTOM_BAR_HEIGHT)

building_buttons = {}
text_surface = []

font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 24)

def check_game_over(buildings):
    for building in buildings:
        if building.name == "Ратуша" and building.destroyed:
            return True
    return False

def check_game_won(village_level):
    max_level = 5
    return village_level > max_level

def reset_game():
    global gold, gold_limit, potions, potions_limit, population, free_population
    global village_level, hint_level, defenders_village, defenders_village_limit
    global selected_building, buildings, unique_buildings, mines, potions_maker, military_camp, defenders
    global selected_building_id, menu_visible, levelup_menu_visible
    global assign_input_active, assign_input_text, recall_input_active, recall_input_text
    global legend_active, hint_active, game_over, game_won
    global enemies, wave_active, hint_updated, shown_hints
    
    gold = 400
    gold_limit = 500
    potions = 400
    potions_limit = 500
    population = 10
    free_population = 10
    village_level = 0
    hint_level = [0]
    defenders_village = 0
    defenders_village_limit = 0
    
    selected_building = None
    buildings = []
    unique_buildings = {}
    mines = {}
    potions_maker = {}
    military_camp = {}
    defenders = []
    enemies = []
    wave_active = False  

    selected_building_id = None
    menu_visible = [False, None]
    levelup_menu_visible = [False, None]
    assign_input_active = False
    assign_input_text = ""
    recall_input_active = False
    recall_input_text = ""
    legend_active = False
    hint_active = True
    game_over = False
    game_won = False
    hint_updated = False  
    shown_hints.clear()
    
    update_building_buttons()


def draw_game_over_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    game_over_font = pygame.font.Font(None, 100)
    game_over_text = game_over_font.render("ПОРАЖЕНИЕ", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 350))
    
    reason_font = pygame.font.Font(None, 50)
    reason_text = reason_font.render("Ратуша была уничтожена!", True, (255, 200, 200))
    screen.blit(reason_text, (SCREEN_WIDTH//2 - reason_text.get_width()//2, SCREEN_HEIGHT//2 - 250))
    
    stats_font = pygame.font.Font(None, 40)
    stats = [
        f"Достигнут уровень: {village_level}",
        f"Построено зданий: {len(buildings)}",
        f"Осталось золота: {gold}",
        f"Осталось зелий: {potions}"
    ]
    
    for i, stat in enumerate(stats):
        stat_text = stats_font.render(stat, True, (200, 200, 255))
        screen.blit(stat_text, (SCREEN_WIDTH//2 - stat_text.get_width()//2, SCREEN_HEIGHT//2 + i*40 - 150))
    
    restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 300, 200, 50)
    pygame.draw.rect(screen, (100, 200, 100), restart_rect, border_radius=8)
    restart_font = pygame.font.Font(None, 40)
    restart_text = restart_font.render("Заново", True, (255, 255, 255))
    screen.blit(restart_text, (restart_rect.x + 50, restart_rect.y + 10))
    
    exit_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 220, 200, 50)
    pygame.draw.rect(screen, (200, 100, 100), exit_rect, border_radius=8)
    exit_text = restart_font.render("Выйти", True, (255, 255, 255))
    screen.blit(exit_text, (exit_rect.x + 55, exit_rect.y + 10))
    
    return restart_rect, exit_rect

def draw_game_won_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    win_font = pygame.font.Font(None, 100)
    win_text = win_font.render("ПОБЕДА!", True, (0, 255, 0))
    screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 350))
    
    message_font = pygame.font.Font(None, 50)
    message_text = message_font.render("Вы построили великую деревню!", True, (200, 255, 200))
    screen.blit(message_text, (SCREEN_WIDTH//2 - message_text.get_width()//2, SCREEN_HEIGHT//2 - 250))
    
    stats_font = pygame.font.Font(None, 40)
    stats = [
        f"Максимальный уровень: {village_level - 1}",
        f"Всего построено зданий: {len(buildings)}",
        f"Золота добыто: {gold}",
        f"Зелий создано: {potions}",
        f"Защитников нанято: {defenders_village}"
    ]
    
    for i, stat in enumerate(stats):
        stat_text = stats_font.render(stat, True, (200, 200, 255))
        screen.blit(stat_text, (SCREEN_WIDTH//2 - stat_text.get_width()//2, SCREEN_HEIGHT//2 + 60 + i*35 - 170))
    
    restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 300, 200, 50)
    pygame.draw.rect(screen, (100, 200, 100), restart_rect, border_radius=8)
    restart_font = pygame.font.Font(None, 40)
    restart_text = restart_font.render("Новая игра", True, (255, 255, 255))
    screen.blit(restart_text, (restart_rect.x + 27, restart_rect.y + 10))
    
    exit_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 220, 200, 50)
    pygame.draw.rect(screen, (200, 100, 100), exit_rect, border_radius=8)
    exit_text = restart_font.render("Выйти", True, (255, 255, 255))
    screen.blit(exit_text, (exit_rect.x + 55, exit_rect.y + 10))
    
    return restart_rect, exit_rect

def upgrade_building(building_id):
    global gold, potions, gold_limit, potions_limit, defenders_village_limit
    
    if building_id < 0 or building_id >= len(buildings):
        return False
    
    building = buildings[building_id]
    
    max_level = BUILDING_LEVEL_LIMITS[village_level][building.name]
    if building.level >= max_level:
        return False
    
    cost = UPGRADE_COSTS[building.name]
    if gold < cost["gold"] or potions < cost["potions"]:
        return False
    
    gold -= cost["gold"]
    potions -= cost["potions"]
    
    building.level += 1
    
    if building.name in UPGRADE_MULTIPLIERS and "health" in UPGRADE_MULTIPLIERS[building.name]:
        health_multiplier = UPGRADE_MULTIPLIERS[building.name]["health"]
        building.max_health = int(building.max_health * health_multiplier)
        building.health = building.max_health
    
    if building.name == "Золотохранилище":
        gold_limit += 50  
    elif building.name == "Шахта" and building_id in mines:
        mines[building_id]["level"] = building.level
    elif building.name == "Зельехранилище":
        potions_limit += 50  
    elif building.name == "Зельеварка" and building_id in potions_maker:
        potions_maker[building_id]["level"] = building.level
    elif building.name == "Военный лагерь":
        defenders_village_limit += 5 
        if building_id in military_camp:
            military_camp[building_id]["level"] = building.level
    
    return True

def update_building_buttons():
    global building_buttons
    building_buttons = {}
    y_offset = 100
    
    for building_name in BUILDING_COSTS:
        current_count = sum(1 for b in buildings if b.name == building_name)
        if building_name in BUILDING_LIMITS.get(village_level, {}): 
            if current_count < BUILDING_LIMITS.get(village_level, {}).get(building_name, 0):
                building_buttons[building_name] = pygame.Rect(20, y_offset, LEFT_PANEL_WIDTH - 40, 60)
                y_offset += 70
                

def draw_grid(surface, rect, cell_size, color):
    start_x = rect.left
    start_y = rect.top
    end_x = rect.right
    end_y = rect.bottom
    
    for x in range(start_x, end_x, cell_size):
        pygame.draw.line(surface, color, (x, start_y), (x, end_y), 1)
    
    for y in range(start_y, end_y, cell_size):
        pygame.draw.line(surface, color, (start_x, y), (end_x, y), 1)

def get_building_color(building_name):
    colors = {
        "Ратуша": TOWN_HALL_COLOR,
        "Золотохранилище": STORAGE_GOLD_COLOR,
        "Шахта": MINE_COLOR,
        "Зельехранилище": STORAGE_POTION_COLOR,
        "Зельеварка": POTION_MAKER_COLOR,
        "Стрелковая башня": SHOOTING_TOWER_COLOR,
        "Военный лагерь": MILITARY_CAMP_COLOR,
        "Стена" : WALL_COLOR
    }
    return colors.get(building_name, (255, 255, 255))

def get_building_preview_color(building_name):
    colors = {
        "Ратуша": TOWN_HALL_PREVIEW_COLOR,
        "Золотохранилище": STORAGE_GOLD_PREVIEW_COLOR,
        "Шахта": MINE_PREVIEW_COLOR,
        "Зельехранилище": STORAGE_POTION_PREVIEW_COLOR,
        "Зельеварка": POTION_MAKER_PREVIEW_COLOR,
        "Стрелковая башня": SHOOTING_TOWER_PREVIEW_COLOR,
        "Военный лагерь": MILITARY_CAMP_PREVIEW_COLOR,
        "Стена": WALL_PREVIEW_COLOR
    }
    return colors.get(building_name, (255, 255, 255, 128))

def draw_buildings():
    global gold, potions, gold_limit, potions_limit, defenders_village_limit, village_level
    global hint_level

    for i, building in enumerate(buildings):
        name, grid_x, grid_y, readiness = building.name, building.rect.x, building.rect.y, building.construction_readiness
        max_width_ready_line, real_width_ready_line = building.max_time_building, building.timer_building
        width, height = BUILDING_SIZES[name]

        pixel_x = right_panel_rect.left + grid_x * GRID_CELL_SIZE
        pixel_y = right_panel_rect.top + grid_y * GRID_CELL_SIZE
        pixel_width = width * GRID_CELL_SIZE
        pixel_height = height * GRID_CELL_SIZE

        width_ready_line = 1 - real_width_ready_line / max_width_ready_line
        if real_width_ready_line < max_width_ready_line:
            building.timer_building += 1
        if not building.added_an_effect:
            if(width_ready_line == 0):
                readiness = True
                building.construction_readiness = True

                if name == "Ратуша":
                    village_level = 1
                    add_hint_level(1)

                if 2 in hint_level and 3 in hint_level:
                    add_hint_level(4)


                if name == "Золотохранилище":
                    gold_limit += 50 * BUILDING_LEVEL_LIMITS[village_level][name]
                elif name == "Шахта":
                    mine_id = len(buildings) - 1
                    mines[mine_id] = {"workers": 0, "last_income": time.time(), "level": 1}
                elif name == "Зельехранилище":
                    potions_limit += 50 * BUILDING_LEVEL_LIMITS[village_level][name]
                elif name == "Зельеварка":
                    potions_maker_id = len(buildings) - 1
                    potions_maker[potions_maker_id] = {"workers": 0, "last_income": time.time(), "level": 1}
                elif name == "Военный лагерь":
                    defenders_village_limit += 5 * BUILDING_LEVEL_LIMITS[village_level][name]
                    military_camp_id = len(buildings) - 1
                    military_camp[military_camp_id] = {"defenders": 0, "level": 1}
                building.added_an_effect = True
            
        if not readiness:
            preview_surface = pygame.Surface((pixel_width, pixel_height), pygame.SRCALPHA)
            preview_color = get_building_preview_color(name)
            preview_surface.fill(preview_color)
            screen.blit(preview_surface, (pixel_x, pixel_y))
        elif building.destroyed:
            color = DESTROYED_BUILDING_COLOR
            pygame.draw.rect(screen, color, (pixel_x, pixel_y, pixel_width, pixel_height))
        else:
            color = get_building_color(name)
            pygame.draw.rect(screen, color, (pixel_x, pixel_y, pixel_width, pixel_height))
        
        if not readiness:
            pygame.draw.rect(screen, BLUE, (pixel_x + 10, pixel_y + pixel_height - 20, (pixel_width - 20) * width_ready_line, 10))
        
        if ((name == "Шахта" or name == "Зельеварка" or name == "Военный лагерь") and selected_building_id == i and not buildings[selected_building_id].destroyed):
            pygame.draw.rect(screen, (255, 255, 0), (pixel_x, pixel_y, pixel_width, pixel_height), 3)
        else:
            pygame.draw.rect(screen, (200, 200, 200), (pixel_x, pixel_y, pixel_width, pixel_height), 2)
        
        if not building.destroyed:
            if name == "Шахта":
                workers_main = mines.get(i, {}).get("workers", 0)
                workers_text = small_font.render(f"Раб: {workers_main}", True, (0, 0, 0))
                screen.blit(workers_text, (pixel_x + 20, pixel_y + 35))
            elif name == "Зельеварка":
                workers_potion_maker = potions_maker.get(i, {}).get("workers", 0)
                workers_text = small_font.render(f"Раб: {workers_potion_maker}", True, (0, 0, 0))
                screen.blit(workers_text, (pixel_x + 20, pixel_y + 35)) 
            elif name == "Военный лагерь":  
                defenders_military_camp = military_camp.get(i, {}).get("defenders", 0)
                defenders_text = small_font.render(f"Защит.: {defenders_military_camp}", True, (0, 0, 0))
                screen.blit(defenders_text, (pixel_x + 20, pixel_y + 35))

def draw_levelup_menu():
    global levelup_menu_rect
    if village_level > 1:
        if levelup_menu_visible[0] and levelup_menu_visible[1] is not None:
            building_id = levelup_menu_visible[1]
            building = buildings[building_id]
            if building.name in UPGRADE_COSTS:
                pixel_x = right_panel_rect.left + building.rect.x * GRID_CELL_SIZE
                pixel_y = right_panel_rect.top + building.rect.y * GRID_CELL_SIZE
                
                levelup_menu_rect = pygame.Rect(pixel_x + 150, pixel_y + 40, 300, 220)
                
                if levelup_menu_rect.right > SCREEN_WIDTH:
                    levelup_menu_rect.right = SCREEN_WIDTH - 10
                if levelup_menu_rect.bottom > REMAINING_HEIGHT:
                    levelup_menu_rect.bottom = REMAINING_HEIGHT - 10
                
                pygame.draw.rect(screen, LEVELUP_MENU_COLOR, levelup_menu_rect, border_radius=8)
                pygame.draw.rect(screen, DIVIDER_COLOR, levelup_menu_rect, 2, border_radius=8)
                
                title_text = font.render(f"Улучшение {building.name}", True, (255, 255, 255))
                screen.blit(title_text, (levelup_menu_rect.x + 10, levelup_menu_rect.y + 10))
                
                current_level = building.level
                max_level = BUILDING_LEVEL_LIMITS[village_level][building.name]
                level_text = small_font.render(f"Текущий уровень: {current_level}/{max_level}", True, (200, 200, 255))
                screen.blit(level_text, (levelup_menu_rect.x + 10, levelup_menu_rect.y + 45))
                
                cost = UPGRADE_COSTS[building.name]
                cost_text = small_font.render(f"Стоимость: {cost['gold']} золота, {cost['potions']} зелий", True, (255, 255, 200))
                screen.blit(cost_text, (levelup_menu_rect.x + 10, levelup_menu_rect.y + 65))
                
                bonuses_text = small_font.render("Бонусы при улучшении:", True, (200, 255, 200))
                screen.blit(bonuses_text, (levelup_menu_rect.x + 10, levelup_menu_rect.y + 85))
                
                if building.name in UPGRADE_MULTIPLIERS:
                    y_offset = 110
                    for bonus, multiplier in UPGRADE_MULTIPLIERS[building.name].items():
                        bonus_percent = int((multiplier - 1) * 100)
                        bonus_text = small_font.render(f"+{bonus_percent}% к {bonus}", True, (200, 200, 200))
                        screen.blit(bonus_text, (levelup_menu_rect.x + 20, levelup_menu_rect.y + y_offset))
                        y_offset += 20
                
                global upgrade_button_rect, cancel_button_rect
                upgrade_button_rect = pygame.Rect(levelup_menu_rect.x + 10, levelup_menu_rect.y + 180, 130, 25)
                cancel_button_rect = pygame.Rect(levelup_menu_rect.x + 150, levelup_menu_rect.y + 180, 130, 25)
                
                can_upgrade = (current_level < max_level and 
                            gold >= cost["gold"] and 
                            potions >= cost["potions"])
                
                upgrade_color = UPGRADE_BUTTON_COLOR if can_upgrade else (100, 100, 100)
                
                pygame.draw.rect(screen, upgrade_color, upgrade_button_rect, border_radius=4)
                upgrade_text = small_font.render("Улучшить", True, (255, 255, 255))
                screen.blit(upgrade_text, (upgrade_button_rect.x + 40, upgrade_button_rect.y + 5))
                
                pygame.draw.rect(screen, BUTTON_COLOR, cancel_button_rect, border_radius=4)
                cancel_text = small_font.render("Отмена", True, (255, 255, 255))
                screen.blit(cancel_text, (cancel_button_rect.x + 40, cancel_button_rect.y + 5))

def draw_building_preview(mouse_pos):
    if selected_building:
        if (right_panel_rect.left <= mouse_pos[0] <= right_panel_rect.right and
            right_panel_rect.top <= mouse_pos[1] <= right_panel_rect.bottom):
            
            grid_x = (mouse_pos[0] - right_panel_rect.left) // GRID_CELL_SIZE
            grid_y = (mouse_pos[1] - right_panel_rect.top) // GRID_CELL_SIZE
            
            width, height = BUILDING_SIZES[selected_building]
            
            if (grid_x + width <= (right_panel_rect.width // GRID_CELL_SIZE) and
                grid_y + height <= (right_panel_rect.height // GRID_CELL_SIZE)):
                
                pixel_x = right_panel_rect.left + grid_x * GRID_CELL_SIZE
                pixel_y = right_panel_rect.top + grid_y * GRID_CELL_SIZE
                pixel_width = width * GRID_CELL_SIZE
                pixel_height = height * GRID_CELL_SIZE
                
                preview_surface = pygame.Surface((pixel_width, pixel_height), pygame.SRCALPHA)
                preview_color = get_building_preview_color(selected_building)
                preview_surface.fill(preview_color)
                screen.blit(preview_surface, (pixel_x, pixel_y))
                
                pygame.draw.rect(screen, (255, 255, 255, 180), (pixel_x, pixel_y, pixel_width, pixel_height), 2)

def draw_building_buttons():
    title_text = font.render("Доступные постройки", True, (255, 255, 255))
    screen.blit(title_text, (8, 50))
    
    for building_name, button_rect in building_buttons.items():
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
        
        pygame.draw.rect(screen, color, button_rect, border_radius=8)
        pygame.draw.rect(screen, DIVIDER_COLOR, button_rect, 2, border_radius=8)
        
        cost = BUILDING_COSTS[building_name]
        button_text = font.render(building_name, True, (255, 255, 255))
        cost_text = small_font.render(f"Золото: {cost['gold']}", True, (200, 200, 200))
        
        screen.blit(button_text, (button_rect.x + 7, button_rect.y + 10))
        screen.blit(cost_text, (button_rect.x + 20, button_rect.y + 35))

def draw_menu(name_building):
    if menu_visible[0] and selected_building_id is not None and not buildings[selected_building_id].destroyed:
        building_info = buildings[selected_building_id]
        grid_x, grid_y = building_info.rect.x, building_info.rect.y
        
        if building_info.construction_readiness:
            pixel_x = right_panel_rect.left + grid_x * GRID_CELL_SIZE
            pixel_y = right_panel_rect.top + grid_y * GRID_CELL_SIZE
            
            building_menu_rect.x = pixel_x + 100
            building_menu_rect.y = pixel_y
            
            if name_building == 'Военный лагерь':
                building_menu_rect.height = 190
            elif name_building in ['Зельеварка', 'Шахта']:
                building_menu_rect.height = 210
            elif name_building in ['Стена', 'Зельехранилище', 'Золотохранилище', 'Стрелковая башня']:
                building_menu_rect.height = 160
            else:
                building_menu_rect.height = 120

            if building_menu_rect.right > SCREEN_WIDTH:
                building_menu_rect.right = SCREEN_WIDTH - 10
            if building_menu_rect.bottom > REMAINING_HEIGHT:
                building_menu_rect.bottom = REMAINING_HEIGHT - 10
            
            pygame.draw.rect(screen, MENU_COLOR, building_menu_rect, border_radius=8)
            pygame.draw.rect(screen, DIVIDER_COLOR, building_menu_rect, 2, border_radius=8)
            
            if name_building == "Шахта":
                workers = mines.get(selected_building_id, {}).get("workers", 0)
                level = mines.get(selected_building_id, {}).get("level", 1)
                income_per_worker = 1 * level
                stats = [
                    f"Уровень: {level}",
                    f"Рабочих: {workers}",
                    f"Доход: {workers * income_per_worker} золота/5сек"
                ]
            elif name_building == "Зельеварка":
                workers = potions_maker.get(selected_building_id, {}).get("workers", 0)
                level = potions_maker.get(selected_building_id, {}).get("level", 1)
                potions_per_worker = 1 * level
                stats = [
                    f"Уровень: {level}",
                    f"Рабочих: {workers}",
                    f"Производит: {workers * potions_per_worker} зелий/5сек"
                ]
            elif name_building == "Военный лагерь":
                defenders_count = military_camp.get(selected_building_id, {}).get("defenders", 0)
                level = military_camp.get(selected_building_id, {}).get("level", 1)
                stats = [
                    f"Уровень: {level}",
                    f"Защитников: {defenders_count}"
                ]
            elif name_building == "Ратуша":
                level = buildings[selected_building_id].level
                stats = [
                    f"Уровень: {level}",
                    f"Здоровье: {buildings[selected_building_id].health}/{buildings[selected_building_id].max_health}"
                ]
            else:
                level = buildings[selected_building_id].level
                stats = [
                    f"Уровень: {level}",
                    f"Здоровье: {buildings[selected_building_id].health}/{buildings[selected_building_id].max_health}"
                ]

            title_text = font.render(f"Меню: {name_building}", True, (255, 255, 255))
            screen.blit(title_text, (building_menu_rect.x + 10, building_menu_rect.y + 10))
            
            y_offset = 40
            for stat in stats:
                stat_text = small_font.render(stat, True, (200, 220, 240))
                screen.blit(stat_text, (building_menu_rect.x + 10, building_menu_rect.y + y_offset))
                y_offset += 20
            
            y_offset += 10
            
            assign_rect = None
            recall_rect = None
            
            if name_building in ["Шахта", "Зельеварка", "Военный лагерь"]:
                assign_rect = pygame.Rect(building_menu_rect.x + 10, building_menu_rect.y + y_offset, 130, 25)
                if name_building in ["Шахта", "Зельеварка"]:
                    recall_rect = pygame.Rect(building_menu_rect.x + 150, building_menu_rect.y + y_offset, 130, 25)
                y_offset += 30
            
            upgrade_rect = None
            close_rect = None
            
            if name_building in ["Золотохранилище", "Шахта", "Зельехранилище", 
                                "Зельеварка", "Стрелковая башня", "Военный лагерь", 
                                "Стена"]:
                upgrade_rect = pygame.Rect(building_menu_rect.x + 10, building_menu_rect.y + y_offset, 130, 25)
                y_offset += 30
            
            close_rect = pygame.Rect(building_menu_rect.x + 10, building_menu_rect.y + y_offset, 270, 25)
            
            if assign_rect:
                assign_color = BUTTON_HOVER_COLOR if assign_input_active else BUTTON_COLOR     
                pygame.draw.rect(screen, assign_color, assign_rect, border_radius=4)
                if name_building in ["Шахта", "Зельеварка"]:
                    assign_text = small_font.render(f"Назначить: {assign_input_text}", True, (255, 255, 255))
                elif name_building == "Военный лагерь":
                    assign_text = small_font.render(f"Нанять: {assign_input_text}", True, (255, 255, 255))
                screen.blit(assign_text, (assign_rect.x + 5, assign_rect.y + 5))
            
            if recall_rect:
                recall_color = BUTTON_HOVER_COLOR if recall_input_active else BUTTON_COLOR
                pygame.draw.rect(screen, recall_color, recall_rect, border_radius=4)
                recall_text = small_font.render(f"Отозвать: {recall_input_text}", True, (255, 255, 255))
                screen.blit(recall_text, (recall_rect.x + 5, recall_rect.y + 5))
            
            if village_level > 1:
                if upgrade_rect:
                    pygame.draw.rect(screen, UPGRADE_BUTTON_COLOR, upgrade_rect, border_radius=4)
                    upgrade_text = small_font.render("Улучшить", True, (255, 255, 255))
                    screen.blit(upgrade_text, (upgrade_rect.x + 40, upgrade_rect.y + 5))
            
            if close_rect:
                pygame.draw.rect(screen, BUTTON_COLOR, close_rect, border_radius=4)
                close_text = small_font.render("Закрыть", True, (255, 255, 255))
                screen.blit(close_text, (close_rect.x + 100, close_rect.y + 5))

def draw_resources():
    gold_text = font.render(f"Золото: {gold}/{gold_limit}", True, GOLD_COLOR)
    potion_text = font.render(f"Зелья: {potions}/{potions_limit}", True, POTION_COLOR)
    population_text = font.render(f"Жители: {free_population}/{population}", True, POPULATION_COLOR)
    level_text = font.render(f"Уровень: {village_level}", True, LEVEL_COLOR)
    
    spacing = SCREEN_WIDTH // 5
    
    screen.blit(gold_text, (spacing * 1 - 120, REMAINING_HEIGHT + 15))
    screen.blit(potion_text, (spacing * 2 - 120, REMAINING_HEIGHT + 15))
    screen.blit(population_text, (spacing * 3 - 120, REMAINING_HEIGHT + 15))
    screen.blit(level_text, (spacing * 4 - 100, REMAINING_HEIGHT + 15))
    
    if selected_building:
        mode_text = font.render(f"Режим строительства: {selected_building}", True, (255, 255, 0))
        screen.blit(mode_text, (50, REMAINING_HEIGHT + 55))
        help_text = small_font.render("Кликните на карте для постройки | ESC для отмены", True, (200, 200, 200))
        screen.blit(help_text, (50, REMAINING_HEIGHT + 85))
    elif menu_visible[0] and not buildings[selected_building_id].destroyed:
        mode_text = font.render("Режим управления шахтой", True, (255, 255, 0))
        screen.blit(mode_text, (50, REMAINING_HEIGHT + 55))
        help_text = small_font.render("Введите количество и нажмите кнопку", True, (200, 200, 200))
        screen.blit(help_text, (50, REMAINING_HEIGHT + 85))

def can_afford_building(building_name):
    cost = BUILDING_COSTS[building_name]
    return gold >= cost["gold"] and potions >= cost["potions"]

def is_building_collision(grid_x, grid_y, width, height):
    for building in buildings:
        name, b_grid_x, b_grid_y = building.name, building.rect.x, building.rect.y
        b_width, b_height = BUILDING_SIZES[name]
        
        if (grid_x < b_grid_x + b_width and 
            grid_x + width > b_grid_x and 
            grid_y < b_grid_y + b_height and 
            grid_y + height > b_grid_y):
            return True
    return False

def add_hint_level(new_level):
    global hint_level, hint_updated, shown_hints
    
    if new_level not in hint_level:
        hint_level.append(new_level)
        
        if new_level not in shown_hints:
            hint_updated = True

def build_building(building_name, grid_x, grid_y):
    global gold, potions, gold_limit, potions_limit, hint_level
    width, height = BUILDING_SIZES[building_name]

    if can_afford_building(building_name) and not is_building_collision(grid_x, grid_y, width, height):
        cost = BUILDING_COSTS[building_name]
        gold -= cost["gold"]
        potions -= cost["potions"]

        if building_name in ['Шахта', 'Зельеварка'] and building_name not in buildings:
            add_hint_level(2)
        elif building_name == 'Военный лагерь' and building_name not in buildings:
            add_hint_level(3)

        buildings.append(Building(grid_x, grid_y, width, height, BUILDING_HEALTH[building_name], get_building_color(building_name), building_name))
        
        update_building_buttons()
        
        return True
    return False

def process_mine_income(name_building):
    global gold, potions, last_income_time
    
    current_time = time.time()
    if current_time - last_income_time >= 5: 
        total_income = 0
        
        if name_building == "Шахта":
            for mine_id, mine_data in mines.items():
                workers = mine_data.get("workers", 0)
                level = mine_data.get("level", 1)
                total_income += workers * level  
            
            if total_income > 0:
                actual_income = min(total_income, gold_limit - gold)
                if actual_income > 0:
                    gold += actual_income
                    
        elif name_building == "Зельеварка":
            for potions_maker_id, potions_maker_data in potions_maker.items():
                workers = potions_maker_data.get("workers", 0)
                level = potions_maker_data.get("level", 1)
                total_income += workers * level  
            
            if total_income > 0:
                actual_income = min(total_income, potions_limit - potions)
                if actual_income > 0:
                    potions += actual_income
        
        last_income_time = current_time

def assign_workers_to_mine(building_id, count, name_building):
    global free_population, potions, defenders_village, defenders_village_limit
    if name_building == "Шахта":
        if building_id in mines and count > 0 and count <= free_population:
            mines[building_id]["workers"] += count
            free_population -= count
            return True
        return False
    elif name_building == "Зельеварка":
        if building_id in potions_maker and count > 0 and count <= free_population:
            potions_maker[building_id]["workers"] += count
            free_population -= count
            return True
        return False
    elif name_building == "Военный лагерь":
        if (building_id in military_camp and count > 0 and 
            defenders_village + count <= defenders_village_limit and
            count * 10 <= potions):
            military_camp[building_id]["defenders"] += count
            defenders_village += count
            potions -= count * 10

            if military_camp:
                defenders_per_camp = defenders_village // len(military_camp)
                remainder = defenders_village % len(military_camp) 
            
            camp_ids = list(military_camp.keys())
            for i, camp_id in enumerate(camp_ids):
                defenders_count = defenders_per_camp + (1 if i < remainder else 0) 
                military_camp[camp_id]["defenders"] = defenders_count

            return True
        
        return False
    

def recall_workers_from_mine(building_id, count, name_building):
    global free_population
    if name_building == "Шахта":
        if building_id in mines:
            current_workers = mines[building_id].get("workers", 0)
            actual_count = min(count, current_workers)
            if actual_count > 0:
                mines[building_id]["workers"] -= actual_count
                free_population += actual_count
                return True
        return False
    elif name_building == "Зельеварка":
        if building_id in potions_maker:
            current_workers = potions_maker[building_id].get("workers", 0)
            actual_count = min(count, current_workers)
            if actual_count > 0:
                potions_maker[building_id]["workers"] -= actual_count
                free_population += actual_count
                return True
        return False
    
def update_level():
    global defenders, defenders_village, village_level
    
    town_hall_exists = False
    for building in buildings:
        if building.name == "Ратуша" and building.health > 0 and not building.destroyed:
            town_hall_exists = True

            if building.level < BUILDING_LEVEL_LIMITS[village_level]["Ратуша"]:
                building.level += 1

                if "health" in UPGRADE_MULTIPLIERS["Ратуша"]:
                    health_multiplier = UPGRADE_MULTIPLIERS["Ратуша"]["health"]
                    building.max_health = int(building.max_health * health_multiplier)
                    building.health = building.max_health
            break
    
    if town_hall_exists:
        for building in buildings:
            building.destroyed = False
            building.health = building.max_health
        
        defenders_village = len(defenders)
        
        if military_camp:
            defenders_per_camp = defenders_village // len(military_camp)
            remainder = defenders_village % len(military_camp)
            
            camp_ids = list(military_camp.keys())
            for i, camp_id in enumerate(camp_ids):
                defenders_count = defenders_per_camp + (1 if i < remainder else 0)
                military_camp[camp_id]["defenders"] = defenders_count

        defenders.clear()
        return True
    return False

def draw_legend():
    if legend_active:
        legend_rect = pygame.Rect(0, 0, LEFT_PANEL_WIDTH, REMAINING_HEIGHT)
        pygame.draw.rect(screen, LEGEND_PANEL_COLOR, legend_rect)
 
        legend_text = font.render("Легенда", True, (255, 255, 255))
        screen.blit(legend_text, (70, 50))

        for building in buildings:
            if building.name not in unique_buildings:
                unique_buildings[building.name] = building.color

        y_offset = 80
        for name, color in unique_buildings.items():
            build_color_text = pygame.Rect(16, y_offset, 20, 20)
            pygame.draw.rect(screen, color, build_color_text)
            pygame.draw.rect(screen, DIVIDER_COLOR, build_color_text, 2)
            
            build_legend_text = font.render(name, True, (255, 255, 255))
            screen.blit(build_legend_text, (47, y_offset))
            
            y_offset += 35

def draw_multiline_text(screen, text, font, color, x, y, line_height):
    global hint_level
    current_y = y
    
    for level in list(set(hint_level)):
        if level in text:
            level_text = text[level]
            lines = level_text.split('\n')
            
            for line in lines:
                line_surface = font.render(line, True, color)
                screen.blit(line_surface, (x, current_y))
                current_y += line_height * 0.8
            
            current_y += line_height // 2

def draw_hint():
    global hint_updated, hint_active, shown_hints

    if hint_active:
        if hint_updated:
            shown_hints.update(hint_level)
            hint_updated = False

        hint_rect = pygame.Rect(100, 30, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60)
        pygame.draw.rect(screen, HINT_PANEL_COLOR, hint_rect, border_radius=8)
        pygame.draw.rect(screen, DIVIDER_COLOR, hint_rect, 2, border_radius=8)
        
        hint_text = font.render("Подсказка", True, (255, 255, 255)) 
        screen.blit(hint_text, (hint_rect.x + 450, hint_rect.y + 40))
        draw_multiline_text(screen, text, font, (255, 255, 255), hint_rect.x + 30, hint_rect.y + 90, 30)

def draw_interface():
    screen.fill(BACKGROUND)
    
    pygame.draw.rect(screen, LEFT_PANEL_COLOR, left_panel_rect)
    pygame.draw.rect(screen, RIGHT_PANEL_COLOR, right_panel_rect)
    pygame.draw.rect(screen, BOTTOM_BAR_COLOR, bottom_bar_rect)
    
    draw_grid(screen, right_panel_rect, GRID_CELL_SIZE, GRID_COLOR)
    
    draw_buildings()

    if village_level == 1:
        update_building_buttons()
    
    draw_building_buttons()
    
    draw_building_preview(pygame.mouse.get_pos())
    
    if menu_visible[0]:
        draw_menu(menu_visible[1])

    draw_levelup_menu()
    
    pygame.draw.line(screen, DIVIDER_COLOR, 
                    (LEFT_PANEL_WIDTH, 0), 
                    (LEFT_PANEL_WIDTH, REMAINING_HEIGHT), 3)
    pygame.draw.line(screen, DIVIDER_COLOR, 
                    (0, REMAINING_HEIGHT), 
                    (SCREEN_WIDTH, REMAINING_HEIGHT), 3)
    
    draw_resources()
    
    if legend_active:
        draw_legend()

    ready_rect = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 150, 60)
    pygame.draw.rect(screen, READY_BUTTON_COLOR, ready_rect, border_radius=4)
    ready_button_text_1 = font.render(f"Cледующий", True, (255, 255, 255))
    ready_button_text_2 = font.render(f"уровень", True, (255, 255, 255))
    screen.blit(ready_button_text_1, (ready_rect.x + 12, ready_rect.y + 5))
    screen.blit(ready_button_text_2, (ready_rect.x + 35, ready_rect.y + 30))

    legend_button_rect = pygame.Rect(SCREEN_WIDTH - 180, 25 , 100, 30)
    pygame.draw.rect(screen, LEGEND_BUTTON_COLOR, legend_button_rect, border_radius=4)
    legend_button_text = font.render("Легенда", True, (255, 255, 255))
    screen.blit(legend_button_text, (legend_button_rect.x + 8, legend_button_rect.y + 7))  

    if hint_active:
        draw_hint() 

    hint_button_rect = pygame.Rect(SCREEN_WIDTH - 60, 25, 30, 30)
    pygame.draw.rect(screen, HINT_BUTTON_COLOR, hint_button_rect, border_radius=4)
    hint_buttun_text = font.render("?", True, (255, 255, 255))
    screen.blit(hint_buttun_text, (hint_button_rect.x + 9, hint_button_rect.y + 7))

    if hint_updated and not hint_active:
        hint_button_rect = pygame.Rect(SCREEN_WIDTH - 60, 25, 30, 30)
        indicator_pos = (hint_button_rect.right - 5, hint_button_rect.top + 5)
        pygame.draw.circle(screen, (255, 0, 0), indicator_pos, 5)

def spawn_enemies(count, buildings, defenders, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
    enemies = []
    
    for i in range(count):
        if i < count/4:
            x = 280  
            y = random.randint(180, screen_height - 120)
        if i >= count/4 and i < count/2:
            x = screen_width - 40
            y = random.randint(130, screen_height - 130)
        if i >= count/2 and i < (count - count/4):
            x = random.randint(280, screen_width - 10)
            y = 130
        if i >= (count - count/4) and i < count:
            x = random.randint(280, screen_width - 10)
            y = screen_height - 120

        health = random.randint(150, 180)
        damage = random.randint(10, 15)
        speed = random.uniform(1.5, 2.5)
        radius = random.randint(8, 12)
        
        enemy = Enemy(x, y - 40, health, damage, speed, radius)
        enemy.purpose = enemy.scan_for_target(buildings, defenders, right_panel_rect, GRID_CELL_SIZE)
        enemies.append(enemy)
    return enemies

def creat_defender(x, y, enemies):
    defender = Defender(x, y, 70, 70, 3, 10)
    defender.purpose = defender.scan_for_target(enemies, right_panel_rect, GRID_CELL_SIZE)
    defenders.append(defender)

    for camp_id in military_camp:
        if military_camp[camp_id]["defenders"] > 0:
            military_camp[camp_id]["defenders"] -= 1
            break

def main():
    clock = pygame.time.Clock()
    running = True
    global selected_building, selected_building_id, menu_visible
    global assign_input_active, assign_input_text, recall_input_active, recall_input_text, defenders_village
    global legend_active, hint_active, village_level, population, free_population
    global levelup_menu_visible, levelup_menu_rect, upgrade_button_rect, cancel_button_rect
    global game_over, game_won, enemies, wave_active

    update_building_buttons()
    enemies = []
    wave_active = False 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game_over or game_won:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    restart_rect = None
                    exit_rect = None
                    
                    if game_over:
                        restart_rect, exit_rect = draw_game_over_screen()

                    elif game_won:
                        restart_rect, exit_rect = draw_game_won_screen()
                    
                    if restart_rect and restart_rect.collidepoint(mouse_pos):
                        reset_game()
                        continue
                    elif exit_rect and exit_rect.collidepoint(mouse_pos):
                        running = False
                        continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_visible[0]:
                        menu_visible[0] = False
                        assign_input_active = False
                        recall_input_active = False
                        assign_input_text = ""
                        recall_input_text = ""
                    else:
                        selected_building = None  

                    if hint_active == True:
                        hint_active = False

                elif menu_visible[0]:
                    if assign_input_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                count = int(assign_input_text)
                                assign_workers_to_mine(selected_building_id, count, menu_visible[1])
                                assign_input_text = ""
                            except ValueError:
                                pass
                        elif event.key == pygame.K_BACKSPACE:
                            assign_input_text = assign_input_text[:-1]
                        elif event.unicode.isdigit():
                            assign_input_text += event.unicode
                    
                    elif recall_input_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                count = int(recall_input_text)
                                recall_workers_from_mine(selected_building_id, count, menu_visible[1])
                                recall_input_text = ""
                            except ValueError:
                                pass
                        elif event.key == pygame.K_BACKSPACE:
                            recall_input_text = recall_input_text[:-1]
                        elif event.unicode.isdigit():
                            recall_input_text += event.unicode
                
                elif not menu_visible[0]:
                    if event.key == pygame.K_g:
                        global gold
                        gold = min(gold + 100, gold_limit)
                    elif event.key == pygame.K_p:
                        global potions
                        potions = min(potions + 100, potions_limit)
                    elif event.key == pygame.K_l:
                        village_level += 1
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.dict['button'] == 1:
                    if wave_active and right_panel_rect.collidepoint(mouse_pos):
                        if defenders_village > 0:
                            creat_defender(mouse_pos[0], mouse_pos[1], enemies)
                            defenders_village -= 1

                    if menu_visible[0]:
                        current_building_name = menu_visible[1]
                        
                        can_be_upgraded = current_building_name in ["Золотохранилище", "Шахта", "Зельехранилище", 
                                                                "Зельеварка", "Стрелковая башня", "Военный лагерь", 
                                                                "Стена"]
                        if menu_visible[1] in ["Шахта", "Зельеварка"]:
                            y_offset = 85 + 25
                        else:
                            y_offset = 85

                        if current_building_name in ["Шахта", "Зельеварка", "Военный лагерь"]:
                            assign_rect = pygame.Rect(building_menu_rect.x + 10, building_menu_rect.y + y_offset, 130, 25)
                            if current_building_name in ["Шахта", "Зельеварка"]:
                                recall_rect = pygame.Rect(building_menu_rect.x + 150, building_menu_rect.y + y_offset, 130, 25)
                            y_offset += 30
                        
                        if can_be_upgraded:
                            upgrade_rect = pygame.Rect(building_menu_rect.x + 10, building_menu_rect.y + y_offset, 130, 25)
                            y_offset += 30
                            
                        close_rect = pygame.Rect(building_menu_rect.x + 10, building_menu_rect.y + y_offset, 270, 25)
                        
                        if current_building_name in ["Шахта", "Зельеварка", "Военный лагерь"]:
                            if assign_rect.collidepoint(mouse_pos):
                                assign_input_active = True
                                recall_input_active = False
                            elif current_building_name in ["Шахта", "Зельеварка"] and recall_rect.collidepoint(mouse_pos):
                                recall_input_active = True
                                assign_input_active = False
                        
                        if can_be_upgraded and upgrade_rect.collidepoint(mouse_pos):
                            levelup_menu_visible = [True, selected_building_id]
                            menu_visible = [False, None]
                            assign_input_active = False
                            recall_input_active = False
                            assign_input_text = ""
                            recall_input_text = ""
                        
                        if close_rect.collidepoint(mouse_pos):
                            menu_visible[0] = False
                            assign_input_active = False
                            recall_input_active = False
                            assign_input_text = ""
                            recall_input_text = ""

                    elif levelup_menu_visible[0]:
                        if 'upgrade_button_rect' in globals() and upgrade_button_rect.collidepoint(mouse_pos):
                            building_id = levelup_menu_visible[1]

                            if upgrade_building(building_id):
                                levelup_menu_visible = [False, None]
                                if 'upgrade_button_rect' in globals():
                                    del upgrade_button_rect
                                if 'cancel_button_rect' in globals():
                                    del cancel_button_rect
                        elif 'cancel_button_rect' in globals() and cancel_button_rect.collidepoint(mouse_pos):
                            levelup_menu_visible = [False, None]

                            if 'upgrade_button_rect' in globals():
                                del upgrade_button_rect
                            if 'cancel_button_rect' in globals():
                                del cancel_button_rect
                        else:
                            levelup_menu_visible = [False, None]

                            if 'upgrade_button_rect' in globals():
                                del upgrade_button_rect
                            if 'cancel_button_rect' in globals():
                                del cancel_button_rect
                    else:
                        ready_rect = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 150, 60)
                        legend_button_rect = pygame.Rect(SCREEN_WIDTH - 180, 25 , 100, 30)
                        hint_button_rect = pygame.Rect(SCREEN_WIDTH - 60, 25, 30, 30)

                        if left_panel_rect.collidepoint(mouse_pos):
                            for building_name, button_rect in building_buttons.items():
                                if button_rect.collidepoint(mouse_pos) and can_afford_building(building_name):
                                    selected_building = building_name
                        elif right_panel_rect.collidepoint(mouse_pos):
                            if selected_building:
                                grid_x = (mouse_pos[0] - right_panel_rect.left) // GRID_CELL_SIZE
                                grid_y = (mouse_pos[1] - right_panel_rect.top) // GRID_CELL_SIZE
                                
                                width, height = BUILDING_SIZES[selected_building]
                                
                                if (grid_x + width <= (right_panel_rect.width // GRID_CELL_SIZE) and
                                    grid_y + height <= (right_panel_rect.height // GRID_CELL_SIZE)):
                                    
                                    if build_building(selected_building, grid_x, grid_y):
                                        selected_building = None  
                            else:
                                grid_x = (mouse_pos[0] - right_panel_rect.left) // GRID_CELL_SIZE
                                grid_y = (mouse_pos[1] - right_panel_rect.top) // GRID_CELL_SIZE
                                
                                for i, building in enumerate(buildings):
                                    name, b_grid_x, b_grid_y = building.name, building.rect.x, building.rect.y
                                    width, height = BUILDING_SIZES[name]
                                    
                                    if (b_grid_x <= grid_x < b_grid_x + width and
                                        b_grid_y <= grid_y < b_grid_y + height):
                                        
                                        selected_building_id = i
                                        menu_visible[0] = True
                                        menu_visible[1] = name
                                        assign_input_active = False
                                        recall_input_active = False
                                        assign_input_text = ""
                                        recall_input_text = ""
                                        break
                        if ready_rect.collidepoint(mouse_pos):
                            if not wave_active:  
                                enemies = spawn_enemies(ENEMY_LEVEL[village_level], buildings, defenders)
                                wave_active = True
                        if legend_button_rect.collidepoint(mouse_pos):
                            legend_active = not legend_active
                        if hint_button_rect.collidepoint(mouse_pos):
                            hint_active = not hint_active
        
        if game_over or game_won:
            screen.fill(BLACK)
            if game_over:
                draw_game_over_screen()
            elif game_won:
                draw_game_won_screen()
            pygame.display.flip()
            clock.tick(60)
            continue

        if wave_active and check_game_over(buildings):
            game_over = True

        if check_game_won(village_level):
            game_won = True

        if wave_active:
            for enemy in enemies[:]: 
                enemy.update(buildings, defenders, right_panel_rect, GRID_CELL_SIZE)
                if enemy.health <= 0:
                    enemies.remove(enemy)

            for building in buildings[:]: 
                building.update_attacking_building(enemies, right_panel_rect, GRID_CELL_SIZE)

            for defender in defenders[:]: 
                defender.update(enemies, right_panel_rect, GRID_CELL_SIZE)
                if defender.health <= 0:
                    defenders.remove(defender)

            if len(enemies) == 0:
                wave_active = False
                village_level += 1
                population += 5
                free_population +=5

                if village_level == 2:
                    add_hint_level(5)

                if update_level():
                    update_building_buttons()
                           
        screen.fill(BLACK)
        process_mine_income(menu_visible[1])
        draw_interface()
            
        for enemy in enemies:
            enemy.draw(screen, GRID_CELL_SIZE)

        for defender in defenders:
            defender.draw(screen)
        
        pygame.display.flip()
        clock.tick(60) 
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()  
