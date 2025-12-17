
import pygame
import math
import numpy as np

class Building:
    def __init__(self, x, y, width, height, health=100, color=(0, 255, 0), name = "Ратуша"):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.max_health = health
        self.color = color
        self.destroyed = False
        self.name = name
        self.purpose = None
        self.damage = 50
        self.attack_cooldown = 0
        self.attack_delay = 60  
        self.timer_building = 0
        self.max_time_building = 50 
        self.construction_readiness = False 
        self.added_an_effect = False 
        self.level = 1


    def attacking_building_scan_for_target(self, enemies, right_panel_rect, GRID_CELL_SIZE):
        if not enemies:
            return None
        
        closest_enemy = None
        min_distance = float('inf')

        building_pixel_x = right_panel_rect.left + self.rect.x * GRID_CELL_SIZE + (self.rect.width * GRID_CELL_SIZE) // 2
        building_pixel_y = right_panel_rect.top + self.rect.y * GRID_CELL_SIZE + (self.rect.height * GRID_CELL_SIZE) // 2
                        
        for enemy in enemies:
            if not enemy.destroyed:
                distance = math.sqrt((enemy.x - building_pixel_x)**2 + (enemy.y - building_pixel_y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        return closest_enemy
        
    def attack_building(self, right_panel_rect, GRID_CELL_SIZE):
        if self.purpose and not self.purpose.destroyed and self.attack_cooldown <= 0:
            building_pixel_rect = pygame.Rect(
                right_panel_rect.left + self.rect.x * GRID_CELL_SIZE - self.rect.width * GRID_CELL_SIZE * 2,
                right_panel_rect.top + self.rect.y * GRID_CELL_SIZE - self.rect.height * GRID_CELL_SIZE * 2,
                self.rect.width * GRID_CELL_SIZE * 5,
                self.rect.height * GRID_CELL_SIZE * 5
            )

            enemy_rect = pygame.Rect(self.purpose.x - self.purpose.radius, self.purpose.y - self.purpose.radius, 
                                     self.purpose.radius * 2, self.purpose.radius * 2
            )

            if enemy_rect.colliderect(building_pixel_rect):
                self.purpose.take_damage(self.damage)
                self.attack_cooldown = self.attack_delay
                
                return True
        return False
    
    def update_attacking_building(self, enemies, right_panel_rect, GRID_CELL_SIZE):
        if self.construction_readiness and self.name == "Стрелковая башня":
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            
            if not self.purpose or self.purpose.destroyed:
                self.purpose = self.attacking_building_scan_for_target(enemies, right_panel_rect, GRID_CELL_SIZE)
                
            if self.purpose and not self.purpose.destroyed:
                self.attack_building(right_panel_rect, GRID_CELL_SIZE)

    def take_damage(self, damage):
        if self.construction_readiness:
            if not self.destroyed:
                self.health -= damage
                if self.health <= 0:
                    self.destroyed = True
                    self.health = 0
                return True
            return False
 
class Enemy:
    def __init__(self, x, y, health=100, damage=10, speed=2, radius=10):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.radius = radius
        self.purpose = None  
        self.color = (255, 0, 0)
        self.attack_cooldown = 0
        self.attack_delay = 60  
        self.destroyed = False
    
    def scan_for_target(self, buildings, defenders, right_panel_rect, GRID_CELL_SIZE):
        if not buildings and defenders:
            return None
        
        build_and_defend = []
        build_and_defend = [*buildings, *defenders]

        closest_building = None
        min_distance = float('inf')
        
        for element in build_and_defend:
            if not element.destroyed:
                if type(element) == Building:
                    building_pixel_x = right_panel_rect.left + element.rect.x * GRID_CELL_SIZE + (element.rect.width * GRID_CELL_SIZE) // 2
                    building_pixel_y = right_panel_rect.top + element.rect.y * GRID_CELL_SIZE + (element.rect.height * GRID_CELL_SIZE) // 2
                     
                    distance = math.sqrt((self.x - building_pixel_x)**2 + (self.y - building_pixel_y)**2)
                      
                    if distance < min_distance:
                        min_distance = distance
                        closest_building = element
                elif type(element) == Defender:
                    distance = math.sqrt((self.x - element.x)**2 + (self.y - element.y)**2)

                    if distance < min_distance:
                        min_distance = distance
                        closest_building = element
        return closest_building    
    
    def move_towards_target(self, right_panel_rect, GRID_CELL_SIZE):
        if self.purpose and not self.purpose.destroyed:
            if GRID_CELL_SIZE / 40 < 1:
                self.x = (self.x - 236) * (1 - (GRID_CELL_SIZE / 40) + 236)
            if type(self.purpose) == Building:
                target_x = right_panel_rect.left + self.purpose.rect.x * GRID_CELL_SIZE + (self.purpose.rect.width * GRID_CELL_SIZE) // 2
                target_y = right_panel_rect.top + self.purpose.rect.y * GRID_CELL_SIZE + (self.purpose.rect.height * GRID_CELL_SIZE) // 2
                
                dx = target_x - self.x
                dy = target_y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance > 0:
                    dx /= distance
                    dy /= distance
                    
                    self.x += dx * self.speed
                    self.y += dy * self.speed
            elif type(self.purpose) == Defender:
                dx = self.purpose.x - self.x
                dy = self.purpose.y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance > self.purpose.radius*2:
                    dx /= distance
                    dy /= distance
                    
                    self.x += dx * self.speed
                    self.y += dy * self.speed
        
    def attack(self, right_panel_rect, GRID_CELL_SIZE):
        if self.purpose and not self.purpose.destroyed and self.attack_cooldown <= 0:
            enemy_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                    self.radius * 2, self.radius * 2
            )

            if type(self.purpose) == Building:
                building_pixel_rect = pygame.Rect(
                    right_panel_rect.left + self.purpose.rect.x * GRID_CELL_SIZE,
                    right_panel_rect.top + self.purpose.rect.y * GRID_CELL_SIZE,
                    self.purpose.rect.width * GRID_CELL_SIZE,
                    self.purpose.rect.height * GRID_CELL_SIZE
                )
                
                if enemy_rect.colliderect(building_pixel_rect):
                    damage_dealt = self.purpose.take_damage(self.damage)
                    self.attack_cooldown = self.attack_delay
                    
                    return True
            elif type(self.purpose) == Defender:
                defender_rect = pygame.Rect(self.purpose.x - self.purpose.radius, self.purpose.y - self.purpose.radius, 
                                        self.purpose.radius * 2, self.purpose.radius * 2
                )

                if enemy_rect.colliderect(defender_rect):
                    damage_dealt = self.purpose.take_damage(self.damage)
                    self.attack_cooldown = self.attack_delay
                    
                    return True

        return False
    
    def update(self, buildings, defenders, right_panel_rect, GRID_CELL_SIZE):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if not self.purpose or self.purpose.destroyed:
            self.purpose = self.scan_for_target(buildings, defenders, right_panel_rect, GRID_CELL_SIZE)
        
        if self.purpose and not self.purpose.destroyed:
            self.move_towards_target(right_panel_rect, GRID_CELL_SIZE)
            self.attack(right_panel_rect, GRID_CELL_SIZE)
    
    def draw(self, screen, GRID_CELL_SIZE):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius * (GRID_CELL_SIZE / 40))
        health_text = f"HP: {self.health}"
        font = pygame.font.Font(None, 20)
        text_surface = font.render(health_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x - 15, self.y - 25))

    def take_damage(self, damage):
        if not self.destroyed:
            self.health -= damage
            if self.health <= 0:
                self.destroyed = True
                self.health = 0
            return True
        return False
    
class Defender:
    def __init__(self, x, y, health=100, damage=10, speed=2, radius=10):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.radius = radius
        self.purpose = None 
        self.color = (0, 255, 0)
        self.attack_cooldown = 0
        self.attack_delay = 60  
        self.destroyed = False

    def scan_for_target(self, enemies, right_panel_rect, GRID_CELL_SIZE):
        if not enemies:
            return None
        
        closest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            if not enemy.destroyed:
                distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        return closest_enemy
    
    def move_towards_target(self, right_panel_rect, GRID_CELL_SIZE):
        if self.purpose and not self.purpose.destroyed:
            dx = self.purpose.x - self.x
            dy = self.purpose.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.purpose.radius*2:
                dx /= distance
                dy /= distance
                
                self.x += dx * self.speed
                self.y += dy * self.speed
    
    def attack(self, right_panel_rect, GRID_CELL_SIZE):
        if self.purpose and not self.purpose.destroyed and self.attack_cooldown <= 0:
            distance = math.sqrt((self.x - self.purpose.x)**2 + (self.y - self.purpose.y)**2)
            attack_range = self.radius + self.purpose.radius + 5 
            
            if distance <= attack_range:
                damage_dealt = self.purpose.take_damage(self.damage)
                self.attack_cooldown = self.attack_delay
            return True
        return False

    def update(self, buildings, right_panel_rect, GRID_CELL_SIZE):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if not self.purpose or self.purpose.destroyed:
            self.purpose = self.scan_for_target(buildings, right_panel_rect, GRID_CELL_SIZE)
        
        if self.purpose and not self.purpose.destroyed:
            self.move_towards_target(right_panel_rect, GRID_CELL_SIZE)
            self.attack(right_panel_rect, GRID_CELL_SIZE)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        health_text = f"HP: {self.health}"
        font = pygame.font.Font(None, 20)
        text_surface = font.render(health_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x - 15, self.y - 25))

    def take_damage(self, damage):
        if not self.destroyed:
            self.health -= damage
            if self.health <= 0:
                self.destroyed = True
                self.health = 0
            return True

        return False
