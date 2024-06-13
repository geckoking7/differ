#---------------------------------------------------------------------------
# differ.py - A basic dungeon crawler called differ
# Author: Luis Fratti
# Date created: 4/6/24
# Last modified: 13/6/24
#---------------------------------------------------------------------------

import pygame
import math
import random
pygame.init()

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    K_a,
    K_w,
    K_s,
    K_d,
    K_e,
    K_1,
    K_2,
    KEYDOWN,
    QUIT,
)

screen = pygame.display.set_mode([1200, 600])
running = True

# data for room generation
room0 = "1b18c1d 1e4a1j13a1e 1e4a1j13a1e 1f4a10j4a1f 20a 20a 20a 20a 1g4a10j4a1g 1e4a1j13a1e 1e4a1j13a1e 1h18c1i"; # shielded room
room1 = "1b18c1d 1e18a1e 1e18a1e 1f18a1f 4a4j4a4j4a 4a4j4a4j4a 4a4j4a4j4a 4a4j4a4j4a 1g18a1g 1e18a1e 1e18a1e 1h18c1i" # 2 square room
room2 = "1b18c1d 1e18a1e 1e18a1e 1f18a1f 7a6j7a 6a8j6a 6a8j6a 7a6j7a 1g18a1g 1e18a1e 1e18a1e 1h18c1i" # circle room
room3 = "1b18c1d 1e17a1j1e 1e16a1j1a1e 1f15a1j2a1f 7a1j7a1j4a 6a1j7a1j5a 5a1j7a1j6a 4a1j7a1j7a 1g2a1j15a1g 1e1a1j16a1e 1e1j17a1e 1h18c1i" # "staircase" room
room4 = "1b18c1d 1e5a1j12a1e 1e5a1j12a1e 1f5a1j12a1f 6a1j6a1j6a 6a1j6a1j6a 6a1j6a1j6a 6a1j6a1j6a 1g12a1j5a1g 1e12a1j5a1e 1e12a1j5a1e 1h18c1i"; # 3part room
room5 = "1b18c1d 1e18a1e 1e18a1e 1h7c1k2a1m7c1i 20a 20a 20a 20a 1b7c1k2a1m7c1d 1e18a1e 1e18a1e 1h18c1i" #"treasure" room     //make it so 2 enemies gaurd 2 loot things
room6 = "1b18c1d 1e1j17a1e 1e18a1e 1f5a8j4a1j1f 5a1j11a1j2a 4a1j11a1j3a 3a1j11a1j4a 2a1j11a1j5a 1g1j4a8j5a1g 1e18a1e 1e17a1j1e 1h18c1i"; # "long" room
room7 = "1b11c1n6c1d 1e11a1e6a1e 1e11a1e6a1e 1h3c1d7a1e6a1f 4a1e2a1g4a1e2a1g4a 4a1e2a1e4a1e2a1e4a 4a1e2a1e4a1e2a1e4a 4a1f2a1e4a1f2a1e4a 1g6a1e7a1h3c1d 1e6a1e11a1e 1e6a1e11a1e 1h6c1o11c1i"; #"maze" room
room8 = "1b18c1d 1e3a1j14a1e 1e3a1j14a1e 1f14a1j3a1f 15a1j4a 4a12j4a 4a12j4a 15a1j4a 1g14a1j3a1g 1e3a1j14a1e 1e3a1j14a1e 1h18c1i"; # T room
room9 = "1b18c1d 1e18a1e 1e18a1e 1f2a2j2a2j2a2j2a2j2a1f 3a2j2a2j2a2j2a2j3a 20a 20a 3a2j2a2j2a2j2a2j3a 1g2a2j2a2j2a2j2a2j2a1g 1e18a1e 1e18a1e 1h18c1i"; # pillar room
room10 = "1b18c1d 1e18a1e 1e18a1e 1e18a1f 1e19a 1e19a 1e19a 1e19a 1e18a1g 1e18a1e 1e18a1e 1h18c1i" # spawn room
# side rooms
room11 = "1b18c1d 1e7j4a7j1e 1e6j6a6j1e 1e5j8a5j1e 1e4j10a4j1e 1e4j10a4j1e 1e4j10a4j1e 1e4j10a4j1e 1e5j8a5j1e 1e6j6a6j1e 1e7j4a7j1e 1h18c1i"; # inverse circle room
room12 = "1b18c1d 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1e7j4a7j1e 1h18c1i"; #"path" room
room13 = "1b18c1d 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1e18a1e 1h18c1i" # empty room
room14 = "1b18c1d 1e18a1e 1e18a1e 1e18a1e 1e2a16j1e 1e18a1e  1e18a1e 1e16j2a1e 1e18a1e 1e18a1e 1e18a1e 1h18c1i"; # 2nd "long" room

# Room code syntax:
#   Tiles are in order from left-right then up-down, number infront of character is amount of tiles that will have the tile type defined by the character after the number
#
#   a = floor (walkable over)
#   b = top left corner
#   c = top and bottom sides (horizontal line)
#   d = top right corner
#   e = left and right sides (vertical line)
#   f = downwards side end
#   g = upwards side end
#   h = bottom left corner
#   i = bottom right corner
#   j = sqaure
#   k = rightwards side end
#   m = leftwards side end (skipped l (L) as it can easily be confused with 1 (one))
#   n = t-joint downwards
#   o = t-joint upwards

visibleSprites = pygame.sprite.Group() # sprite group for rendering
floorTiles = pygame.sprite.Group() # tiles that entities can move over, if tile is not in this group then it cannot be moved over
bulletSprites = pygame.sprite.Group() # sprite group for bullets that need to move every tick
for i in range(1,15):
    exec("room" + str(i) + "Sprites = pygame.sprite.Group()") # sprite group for entities (like items and enemies) that will appear once a player enters a certain room

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/player.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL) # Sets black as transparent
        self.rect = self.surf.get_rect()
        self.rect.left = 475
        self.rect.top = 275

    def update(self, keysPressed):
        global roomPlayerIn
        global zoneData
        global playerWon
        if keysPressed[K_a]:
            if checkMoveValid(self, math.pi, playerSpeed) and self.rect.left >= playerSpeed:
                self.rect.move_ip(-playerSpeed, 0)
            else:
                if self.rect.left > playerSpeed:
                    self.rect.left = math.floor(self.rect.left / 50) * 50 # snaps player to touch non-floor tile on left side
                else: # player moves to the room to the left
                    self.rect.left = 925
                    i = 1
                    while i <= 3:
                        if ord(zoneData[roomPlayerIn - i]) < 64:
                            roomPlayerIn = roomPlayerIn - i
                            generateRoom(zoneData[roomPlayerIn])
                            i = 4
                        i = i + 1
        if keysPressed[K_w]:
            if checkMoveValid(self, math.pi / 2, playerSpeed) and self.rect.top >= playerSpeed:
                self.rect.move_ip(0, -playerSpeed)
            else:
                if self.rect.top > playerSpeed:
                    self.rect.top = math.floor(self.rect.top / 50) * 50 # snaps player to touch non-floor tile on top side
                else:
                    self.rect.top = 525
                    if ord(zoneData[roomPlayerIn]) < 64:
                        roomPlayerIn = roomPlayerIn + 1
                        generateRoom(zoneData[roomPlayerIn])
                    else:
                        i = 1
                        while i <= 2:
                            if ord(zoneData[roomPlayerIn - i]) < 64:
                                roomPlayerIn = roomPlayerIn - i
                                generateRoom(zoneData[roomPlayerIn])
                                i = 3
                            i = i + 1
        if keysPressed[K_s]:
            if checkMoveValid(self, (3 * math.pi) / 2, playerSpeed) and self.rect.top <= 550 - playerSpeed:
                self.rect.move_ip(0, playerSpeed)
            else:
                if self.rect.top < 550 - playerSpeed:
                    self.rect.top = math.ceil(self.rect.top / 50) * 50 # snaps player to touch non-floor tile on bottom side
                else:
                    self.rect.top = 25
                    if ord(zoneData[roomPlayerIn]) < 64:
                        i = 1
                        while i <= 2:
                            if ord(zoneData[roomPlayerIn + i]) > 96:
                                roomPlayerIn = roomPlayerIn + i
                                generateRoom(zoneData[roomPlayerIn])
                                i = 3
                            i = i + 1
                    else:
                        roomPlayerIn = roomPlayerIn - 1
                        generateRoom(zoneData[roomPlayerIn])
        if keysPressed[K_d]:
            if checkMoveValid(self, 0, playerSpeed) and self.rect.left <= 950 - playerSpeed:
                self.rect.move_ip(playerSpeed, 0)
            else:
                if self.rect.left < 950 - playerSpeed:
                    self.rect.left = math.ceil(self.rect.left / 50) * 50 # snaps player to touch non-floor tile on right side
                else: # player moves to the room to the right
                    if roomPlayerIn != lastRoom:
                        self.rect.left = 25
                        i = 1
                        while i <= 3:
                            if ord(zoneData[roomPlayerIn + i]) < 64:
                                roomPlayerIn = roomPlayerIn + i
                                generateRoom(zoneData[roomPlayerIn])
                                i = 4
                            i = i + 1
                    else: 
                        if currentZone < 5:
                            self.rect.left = 475
                            generateZone()
                        else:
                            playerWon = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, left, top):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/enemy.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.value = 4 # health of enemy
        self.value2 = 0 # cooldown of enemy weapon
        
    def update(self):
        if self.value <= 0:
            randomNumber = random.randint(1,32) # enemy drops a random item upon death
            if randomNumber <= 16:
                createItem(2, 20, self.rect.left, self.rect.top, roomPlayerIn)
            elif randomNumber <= 24:
                createItem(2, 50, self.rect.left, self.rect.top, roomPlayerIn)
            elif randomNumber <= 28:
                createItem(1, 0, self.rect.left, self.rect.top, roomPlayerIn)
            elif randomNumber <= 30:
                createItem(4, 0, self.rect.left, self.rect.top, roomPlayerIn)
            elif randomNumber <= 31:
                createItem(3, 0, self.rect.left, self.rect.top, roomPlayerIn)
            self.kill()
        else:
            if self.value2 <= 0 and seePlayerTest(self.rect.left, self.rect.top): # note enemy uses a weapon with same stats as SMG
                if self.rect.left - player.rect.left == 0: # checks if denominator = 0
                    if self.rect.top - player.rect.top > 0: # checks if bullet should move up or down
                        angle = 90
                    else:
                        angle = -90
                elif player.rect.left > self.rect.left: # checks if bullet should move left or right
                    angle = math.atan((self.rect.top - player.rect.top) / (self.rect.left - player.rect.left)) * 180 / math.pi + 180 + random.randint(-getWeaponData(20 + currentZone, "spread"), getWeaponData(20 + currentZone, "spread")) # get angle for the bullet and convert it into degrees + spread
                else:
                    angle = math.atan((self.rect.top - player.rect.top) / (self.rect.left - player.rect.left)) * 180 / math.pi + random.randint(-getWeaponData(20 + currentZone, "spread"), getWeaponData(20 + currentZone, "spread"))
                bullet = EnemyBullet(180 + angle)
                bullet.rect.left = self.rect.left + 25
                bullet.rect.top = self.rect.top + 25
                self.value2 = getWeaponData(20 + currentZone, "firerate")
            elif self.value2 > 0:
                self.value2 = self.value2 - 1

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, angle):
        super(PlayerBullet, self).__init__()
        self.surf = pygame.Surface((10, 5))
        self.surf = pygame.image.load("resources/bulletPlayer.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.surf = pygame.transform.rotate(self.surf, - angle)
        visibleSprites.add(self)
        bulletSprites.add(self)
        self.value = angle
    
    def update(self):
        if checkMoveValid(self, self.value * math.pi / 180, 15): # checks if bullet hits a wall
            self.rect.left = self.rect.left + 15 * math.cos(self.value * math.pi / 180) # convert back into radians
            self.rect.top = self.rect.top + 15 * math.sin(self.value * math.pi / 180)
            if roomPlayerIn != 0:
                exec("currentRoomEntites = room" + str(roomPlayerIn) + "Sprites")
                entitiesHit = pygame.sprite.spritecollide(bullet, currentRoomEntites, False) # sprite collision list --> https://www.pygame.org/docs/ref/sprite.html
                for entity in entitiesHit: # check if bullet hits enemy
                    if isinstance (entity, Enemy):
                        self.kill()
                        entity.value = entity.value - 1
        else:
            self.kill()

class PlayerArrow(pygame.sprite.Sprite): # arrows are faster and larger than regular bullets and oneshot enemies
    def __init__(self, angle):
        super(PlayerArrow, self).__init__()
        self.surf = pygame.Surface((20, 5))
        self.surf = pygame.image.load("resources/arrowPlayer.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.surf = pygame.transform.rotate(self.surf, - angle)
        visibleSprites.add(self)
        bulletSprites.add(self)
        self.value = angle
        
    def update(self):
        if checkMoveValid(self, self.value * math.pi / 180, 30): # checks if bullet hits a wall
            self.rect.left = self.rect.left + 30 * math.cos(self.value * math.pi / 180) # convert back into radians
            self.rect.top = self.rect.top + 30 * math.sin(self.value * math.pi / 180)
            if roomPlayerIn != 0:
                exec("currentRoomEntites = room" + str(roomPlayerIn) + "Sprites")
                entitiesHit = pygame.sprite.spritecollide(bullet, currentRoomEntites, False) # sprite collision list --> https://www.pygame.org/docs/ref/sprite.html
                for entity in entitiesHit: # check if arrow hits enemy
                    if isinstance (entity, Enemy):
                        self.kill()
                        entity.value = 0
        else:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, angle):
        super(EnemyBullet, self).__init__()
        self.surf = pygame.Surface((10, 5))
        self.surf = pygame.image.load("resources/bulletEnemy.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.surf = pygame.transform.rotate(self.surf, - angle)
        visibleSprites.add(self)
        bulletSprites.add(self)
        self.value = angle
    
    def update(self):
        if checkMoveValid(self, self.value * math.pi / 180, 15): # checks if bullet hits a wall
            self.rect.left = self.rect.left + 15 * math.cos(self.value * math.pi / 180) # convert back into radians
            self.rect.top = self.rect.top + 15 * math.sin(self.value * math.pi / 180)
            if pygame.sprite.spritecollideany(self, playerSprite):
                self.kill()
                playerDamage(1)
        else:
            self.kill()

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon):
        super(Weapon, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/weapon" + str(weapon) + ".png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.value = weapon

class Ammo(pygame.sprite.Sprite):
    def __init__(self, amount):
        super(Ammo, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/ammoPack.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.value = amount

class SpeedPack(pygame.sprite.Sprite):
    def __init__(self):
        super(SpeedPack, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/speedPack.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        
class HealthPack(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthPack, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/healthPack.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

tileTop = 0
tileLeft = 0
class Tile(pygame.sprite.Sprite):
    def __init__(self):
        super(Tile, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf = pygame.image.load("resources/tile_a.png").convert()
        self.rect = self.surf.get_rect()
        self.rect.left = tileLeft
        self.rect.top = tileTop
        floorTiles.add(self)
        visibleSprites.add(self)
    
    def update(self, tileType): # change tile type
        self.surf = pygame.image.load("resources/tile_" + tileType +".png").convert()
        if tileType == 'a':
            floorTiles.add(self)
        else:
            floorTiles.remove(self)

class SlotInUse(pygame.sprite.Sprite):
    def __init__(self):
        super(SlotInUse, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((127, 127, 255))
        self.rect = self.surf.get_rect()
        self.rect.left = 1050
        self.rect.top = 150
        visibleSprites.add(self)
    
    def update(self, keysPressed):
        global currentActiveSlot
        if keysPressed[K_1]: # weapon in first slot is active
            self.rect.top = 150
            currentActiveSlot = 1
        elif keysPressed[K_2]: # weapon in second slot is active
            self.rect.top = 275
            currentActiveSlot = 2

class ItemSlot(pygame.sprite.Sprite):
    def __init__(self, number):
        super(ItemSlot, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load("resources/weaponSlotEmpty.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = 1075
        self.rect.top = 25 + number * 125
        visibleSprites.add(self)
    
    def update(self, weapon): # change item slot image to show equipped weapon
        self.surf = pygame.image.load("resources/weapon" + str(weapon) +"S.png").convert() # weapon in item slot resource files contain a capital S at the end
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

class SidePanel(pygame.sprite.Sprite): #move health bar down 
    def __init__(self):
        super(SidePanel, self).__init__()
        self.surf = pygame.Surface((200, 600))
        self.surf = pygame.image.load("resources/sidePanel.png").convert()
        self.rect = self.surf.get_rect()
        self.rect.left = 1000
        visibleSprites.add(self)

def generateZone():
    global zoneData
    global roomPlayerIn
    global lastRoom
    global currentZone
    for i in range(1,15): # deletes all items in previous zone
        roomEntities = globals()["room" + str(i) + "Sprites"]
        for entity in roomEntities:
            entity.kill()
        if not roomEntities: # ensures the array is empty, otherwise will clear. Check for array empty --> https://stackoverflow.com/questions/53513/how-do-i-check-if-a-list-is-empty
            i = i - 1
    generateRoom("#") # hashtag (#) symbol represents spawn room
    zoneData = "#"
    roomPlayerIn = 0
    currentZone = currentZone + 1
    for i in range(5):
        zoneData = zoneData + str(random.randint(0,9)) # adds random normal room to zone
        createRoomEntites(zoneData[len(zoneData) - 1], len(zoneData) - 1)
        if i == 4:
            lastRoom = len(zoneData) - 1
        if random.randint(0,3) == 3: # 25% chance for a side room generating above aswell as another 25% for one below. Capatil letter represents room above and lowercase represents one below
            zoneData = zoneData + chr(65 + random.randint(0,3))
            createRoomEntites(zoneData[len(zoneData) - 1], len(zoneData) - 1)
        if random.randint(0,3) == 3:
            zoneData = zoneData + chr(97 + random.randint(0,3))
            createRoomEntites(zoneData[len(zoneData) - 1], len(zoneData) - 1)
    # print(zoneData) can be used for bugfixing zone generation

def generateRoom(roomNumber):
    global roomPlayerIn
    doorwayType = 0 # generates a hole in the wall to allow the player to enter a room above/below. 0 = none, 1 = hole at top, 2 = hole at bottom, 3 = hole at both
    for i in range(1): # deletes all bullets in previous room
        for entity in bulletSprites:
            entity.kill()
        if not bulletSprites:
            i = i - 1
    if ord(roomNumber) > 60:
        if ord(roomNumber) > 96:
            roomNumber = ord(roomNumber) - 86
            doorwayType = 1
        else:
            roomNumber = ord(roomNumber) - 54
            doorwayType = 2
    else:
        if roomNumber == "#":
            roomNumber = 10
        else:
            roomNumber = int(roomNumber)
            if len(zoneData) >= roomPlayerIn + 2 and ord(zoneData[roomPlayerIn + 1]) > 60: # check if side room above exists for current room
                doorwayType = 1
                if len(zoneData) >= roomPlayerIn + 3 and ord(zoneData[roomPlayerIn + 2]) > 96: # check if side room below exists for current room
                    doorwayType = 3
            if len(zoneData) >= roomPlayerIn + 2 and ord(zoneData[roomPlayerIn + 1]) > 96: # check if side room below exists for current room
                doorwayType = 2
    roomText = globals()["room" + str(roomNumber)]
    currentTile = 1
    rangeOfTiles = ""
    tileType = ""
    for i in range(len(roomText)):
        if ord(roomText[i]) > 47 and ord(roomText[i]) < 58: #returns false if roomText[i] is not a number
            rangeOfTiles = rangeOfTiles + roomText[i]
        elif roomText[i] != ' ':
            tileType = roomText[i]
            rangeOfTiles = int(rangeOfTiles)
            for j in range(currentTile, currentTile + rangeOfTiles):
                exec("tile" + str(j) + ".update('" + tileType + "')")
            currentTile = currentTile + rangeOfTiles
            rangeOfTiles = ""
    if doorwayType == 1 or doorwayType == 3: # creates a doorway on top side
        tile8.update('k')
        if roomNumber == 7:
            tile13.update('b')
        else:
            tile13.update('m')
        for i in range(4):
            exec("tile" + str(i + 9) + ".update('a')")
    if doorwayType > 1: # creates a doorway on bottom side
        tile233.update('m')
        if roomNumber == 7:
            tile228.update('i')
        else:
            tile228.update('k')
        for i in range(4):
            exec("tile" + str(i + 229) + ".update('a')")

def createRoomEntites(roomType, roomNumber): # generates enemies and items for the room. Rach room has 4 possible sets of entities
    randomNumber = random.randint(1,4)
    if roomType == "0": # shielded Room
        if randomNumber == 1:
            createEnemy(1, 325, 75, roomNumber)
            createEnemy(1, 325, 475, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 325, 75, roomNumber)
        elif randomNumber == 3:
            createItem(2, 20, 325, 475, roomNumber)
            createItem(2, 20, 325, 75, roomNumber)
            createEnemy(1, 400, 75, roomNumber)
            createEnemy(1, 400, 475, roomNumber)
        else:
            createEnemy(1, 325, 475, roomNumber)
    elif roomType == "1": # 2 square Room
        if randomNumber == 1:
            createItem(1, 0, 475, 275, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 425, 275, roomNumber)
            createEnemy(1, 525, 275, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 475, 275, roomNumber)
        else:
            createEnemy(1, 400, 250, roomNumber)
            createEnemy(1, 450, 250, roomNumber)
            createEnemy(1, 500, 250, roomNumber)
            createEnemy(1, 550, 250, roomNumber)
            createEnemy(1, 400, 300, roomNumber)
            createEnemy(1, 450, 300, roomNumber)
            createEnemy(1, 500, 300, roomNumber)
            createEnemy(1, 550, 300, roomNumber)
    elif roomType == "2": # circle Room
        if randomNumber == 2: # if randomNumber == 1 then room will be empty
            createEnemy(1, 775, 200, roomNumber)
            createEnemy(1, 775, 350, roomNumber)
            createItem(2, 20, 775, 275, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 775, 200, roomNumber)
            createEnemy(1, 775, 350, roomNumber)
        else:
            createEnemy(1, 775, 275, roomNumber)
    elif roomType == "3": # staircase Room
        if randomNumber == 1:
            createEnemy(1, 275, 425, roomNumber)
            createEnemy(1, 825, 275, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 475, 275, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 250, 450, roomNumber)
            createEnemy(1, 350, 450, roomNumber)
            createEnemy(1, 350, 350, roomNumber)
        else:
            createItem(2, 20, 475, 275, roomNumber)
    elif roomType == "4": # 3 part room
        if randomNumber == 1:
            createEnemy(1, 475, 275, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 800, 100, roomNumber)
            createEnemy(1, 475, 275, roomNumber)
            createEnemy(1, 800, 450, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 475, 100, roomNumber)
            createEnemy(1, 800, 100, roomNumber)
        else:
            createItem(2, 20, 150, 100, roomNumber)
            createEnemy(1, 800, 450, roomNumber)
    elif roomType == "5": # "treasure" room
        if randomNumber == 1:
            createEnemy(1, 75, 75, roomNumber)
            createEnemy(1, 75, 475, roomNumber)
            createItem(2, 20, 875, 75, roomNumber)
            createItem(2, 20, 875, 475, roomNumber)
        elif randomNumber == 2:
            createItem(1, 0, 75, 475, roomNumber)
            createItem(4, 0, 75, 75, roomNumber)
            createEnemy(1, 175, 75, roomNumber)
            createEnemy(1, 175, 475, roomNumber)
            createEnemy(1, 875, 75, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 75, 75, roomNumber)
            createEnemy(1, 75, 475, roomNumber)
            createEnemy(1, 875, 75, roomNumber)
            createEnemy(1, 875, 475, roomNumber)
        else:
            createEnemy(1, 475, 75, roomNumber)
            createEnemy(1, 475, 475, roomNumber)
    elif roomType == "6": # "long" room
        if randomNumber == 1:
            createEnemy(1, 475, 75, roomNumber)
            createEnemy(1, 475, 275, roomNumber)
            createEnemy(1, 475, 475, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 475, 275, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 275, 275, roomNumber)
            createEnemy(1, 675, 275, roomNumber)
        else:
            createItem(2, 20, 475, 275, roomNumber)
    elif roomType == "7": # "maze" room
        if randomNumber == 1:
            createEnemy(1, 475, 275, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 75, 75, roomNumber)
            createEnemy(1, 875, 475, roomNumber)
        elif randomNumber == 3:
            createItem(2, 20, 75, 75, roomNumber)
            createItem(2, 20, 875, 475, roomNumber)
        else:
            createEnemy(1, 75, 75, roomNumber)
            createEnemy(1, 875, 475, roomNumber)
            createEnemy(1, 475, 75, roomNumber)
            createEnemy(1, 475, 275, roomNumber)
            createEnemy(1, 475, 475, roomNumber)
    elif roomType == "8": # T room
        if randomNumber == 1:
            createEnemy(1, 275, 75, roomNumber)
            createEnemy(1, 275, 475, roomNumber)
        elif randomNumber == 2:
            createItem(3, 0, 825, 275, roomNumber)
        elif randomNumber == 3:
            createEnemy(1, 825, 275, roomNumber)
        else:
            createEnemy(1, 825, 225, roomNumber)
            createEnemy(1, 825, 325, roomNumber)
    elif roomType == "9": # pillar room
        if randomNumber == 1:
            createEnemy(1, 475, 75, roomNumber)
            createEnemy(1, 475, 475, roomNumber)
        elif randomNumber == 2:
            createEnemy(1, 475, 175, roomNumber)
            createEnemy(1, 475, 375, roomNumber)
        elif randomNumber == 3:
            createItem(2, 20, 475, 275, roomNumber)
        else:
            createEnemy(1, 275, 175, roomNumber)
            createEnemy(1, 475, 175, roomNumber)
            createEnemy(1, 675, 175, roomNumber)
            createEnemy(1, 275, 375, roomNumber)
            createEnemy(1, 475, 375, roomNumber)
            createEnemy(1, 675, 375, roomNumber)
    elif roomType == "A" or roomType == "a": # inverse circle room (both top and bottom)
        if randomNumber == 1:
            createItem(2, 50, 475, 275, roomNumber)
        elif randomNumber == 2:
            createItem(2, 100, 475, 275, roomNumber)
        elif randomNumber == 3:
            createItem(1, 0, 475, 275, roomNumber)
        else:
            createItem(3, 0, 475, 275, roomNumber)
    elif roomType == "B": # line room top
        if randomNumber == 1:
            createItem(4, 0, 475, 75, roomNumber)
        elif randomNumber == 2:
            createItem(1, 0, 475, 75, roomNumber)
        elif randomNumber == 3:
            createItem(2, 50, 475, 75, roomNumber)
        else:
            createItem(3, 0, 475, 75, roomNumber)
    elif roomType == "C": # empty room top
        if randomNumber == 1:
            createEnemy(1, 475, 175, roomNumber)
        elif randomNumber == 2:
            createItem(2, 100, 475, 175, roomNumber)
        elif randomNumber == 3:
            createItem(3, 0, 425, 175, roomNumber)
            createItem(3, 0, 525, 175, roomNumber)
        else:
            createEnemy(1, 350, 150, roomNumber)
            createEnemy(1, 400, 150, roomNumber)
            createEnemy(1, 450, 150, roomNumber)
            createEnemy(1, 500, 150, roomNumber)
            createEnemy(1, 550, 150, roomNumber)
            createEnemy(1, 600, 150, roomNumber)
            createEnemy(1, 350, 200, roomNumber)
            createEnemy(1, 400, 200, roomNumber)
            createEnemy(1, 450, 200, roomNumber)
            createEnemy(1, 500, 200, roomNumber)
            createEnemy(1, 550, 200, roomNumber)
            createEnemy(1, 600, 200, roomNumber)
    elif roomType == "D": # 2nd "long" room
        if randomNumber == 1:
            createItem(1, 0, 850, 100, roomNumber)
        elif randomNumber == 2:
            createItem(2, 100, 850, 100, roomNumber)
        elif randomNumber == 3:
            createItem(4, 0, 850, 100, roomNumber)
        else:
            createItem(2, 1, 850, 100, roomNumber)
    elif roomType == "b": # line room bottom
        if randomNumber == 1:
            createItem(4, 0, 475, 475, roomNumber)
        elif randomNumber == 2:
            createItem(1, 0, 475, 475, roomNumber)
        elif randomNumber == 3:
            createItem(2, 50, 475, 475, roomNumber)
        else:
            createItem(3, 0, 475, 475, roomNumber)
    elif roomType == "c": # empty room bottom
        if randomNumber == 1:
            createEnemy(1, 475, 375, roomNumber)
        elif randomNumber == 2:
            createItem(2, 100, 475, 375, roomNumber)
        elif randomNumber == 3:
            createItem(3, 0, 425, 375, roomNumber)
            createItem(3, 0, 525, 375, roomNumber)
        else:
            createEnemy(1, 350, 400, roomNumber)
            createEnemy(1, 400, 400, roomNumber)
            createEnemy(1, 450, 400, roomNumber)
            createEnemy(1, 500, 400, roomNumber)
            createEnemy(1, 550, 400, roomNumber)
            createEnemy(1, 600, 400, roomNumber)
            createEnemy(1, 350, 350, roomNumber)
            createEnemy(1, 400, 350, roomNumber)
            createEnemy(1, 450, 350, roomNumber)
            createEnemy(1, 500, 350, roomNumber)
            createEnemy(1, 550, 350, roomNumber)
            createEnemy(1, 600, 350, roomNumber)
    elif roomType == "d": # 2nd "long" room bottom
        if randomNumber == 1:
            createItem(1, 0, 100, 450, roomNumber)
        elif randomNumber == 2:
            createItem(2, 100, 100, 450, roomNumber)
        elif randomNumber == 3:
            createItem(4, 0, 100, 450, roomNumber)
        else:
            createItem(2, 1, 100, 450, roomNumber)

def createItem(itemType, itemValue, left, top, roomNumber):
    if itemType == 1: # creates weapon drop
        if itemValue == 0: # if itemValue = 0 then the item drop will be a random weapon
            itemValue = random.randint(1, 4) * 10 + random.randint(1, currentZone)
        weapon = Weapon(itemValue)
        weapon.rect.left = left
        weapon.rect.top = top
        exec("room" + str(roomNumber) + "Sprites.add(weapon)")
    elif itemType == 2: # creates ammo pack
        ammoPack = Ammo(itemValue)
        ammoPack.rect.left = left
        ammoPack.rect.top = top
        exec("room" + str(roomNumber) + "Sprites.add(ammoPack)")
    elif itemType == 3:
        speedPack = SpeedPack()
        speedPack.rect.left = left
        speedPack.rect.top = top
        exec("room" + str(roomNumber) + "Sprites.add(speedPack)")
    else:
        healthPack = HealthPack()
        healthPack.rect.left = left
        healthPack.rect.top = top
        exec("room" + str(roomNumber) + "Sprites.add(healthPack)")

def createEnemy(enemyType, left, top, roomNumber): # currently only one enemy type
    if enemyType == 1:
        newEnemy = Enemy(left, top)
        exec("room" + str(roomNumber) + "Sprites.add(newEnemy)")

def checkMoveValid(entity, direction, speed): # checks if entity is planned to move to a non-floor tile or out of the map, works on entities smaller or equal to 50x50
    projectedTile1 = math.floor((entity.rect.left + math.cos(direction) * speed) / 50) + 20 * math.floor((entity.rect.top - math.sin(direction) * speed) / 50) + 1 # top left tile for projected movement
    projectedTile2 = math.floor((entity.rect.left + entity.rect.width - 1 + math.cos(direction) * speed) / 50) + 20 * math.floor((entity.rect.top - math.sin(direction) * speed) / 50) + 1 # top right tile
    projectedTile3 = math.floor((entity.rect.left + entity.rect.width - 1 + math.cos(direction) * speed) / 50) + 20 * math.floor((entity.rect.top + entity.rect.height - 1 - math.sin(direction) * speed) / 50) + 1 # bottom right tile
    projectedTile4 = math.floor((entity.rect.left + math.cos(direction) * speed) / 50) + 20 * math.floor((entity.rect.top + entity.rect.height - 1 - math.sin(direction) * speed) / 50) + 1 # bottom left tile
    if entity.rect.left + math.cos(direction) * speed > 0 and entity.rect.left + math.cos(direction) * speed < 950 and entity.rect.top - math.sin(direction) * speed > 0 and entity.rect.top - math.sin(direction) * speed < 550:
        if globals()["tile" + str(projectedTile1)] in floorTiles and globals()["tile" + str(projectedTile2)] in floorTiles and globals()["tile" + str(projectedTile3)] in floorTiles and globals()["tile" + str(projectedTile4)] in floorTiles:
            return True
        else:
            return False
    else:
        return False

def equipWeapon(weapon, left, top): # weapon name comes from 2 digits with the first digit determining the weapon family (1 = pistol, 2 = SMG, 3 = shotgun, 4 = crossbow) and 2nd digit determining tier
    global itemInSlot1
    global itemInSlot2
    global currentActiveSlot
    if itemInSlot1 == 0:
        itemSlot1.update(11)
        itemInSlot1 = 11
    elif itemInSlot2 == 0:
        
        itemSlot2.update(weapon)
        itemInSlot2 = weapon
    elif currentActiveSlot == 1:
        createItem(1, itemInSlot1, left, top, roomPlayerIn)
        itemInSlot1 = weapon
        itemSlot1.update(weapon)
    else:
        createItem(1, itemInSlot2, left, top, roomPlayerIn)
        itemInSlot2 = weapon
        itemSlot2.update(weapon)
        
def displayStats(): # For fonts that update --> https://stackoverflow.com/questions/10077644/how-to-display-text-with-font-and-color-using-pygame 3rd highest rated answer
    font = pygame.font.Font(None,24)
    ammoText = font.render("Ammo: "+ str(ammo), 1,(127,95,63))
    if roomPlayerIn <= 1:
        roomText = font.render("Room: " + str(currentZone) + "." + str(roomPlayerIn), 1,(127,127,63))
    else:
        count = 1
        for i in range(2, roomPlayerIn + 1): # counts how many side rooms away from the start the player is
            if ord(zoneData[i]) < 60:
                count = count + 1
        if ord(zoneData[roomPlayerIn]) < 60: # checks what type of room player in
            roomText = font.render("Room: " + str(currentZone) + "." + str(count), 1,(127,127,63))
        elif ord(zoneData[roomPlayerIn]) < 96:
            roomText = font.render("Room: " + str(currentZone) + "." + str(count) + "a", 1,(127,127,63))
        else:
            roomText = font.render("Room: " + str(currentZone) + "." + str(count) + "b", 1,(127,127,63))
            
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(1025, 50, playerHealth * 15, 25)) # draw healthBar
    screen.blit(ammoText, (1070, 467))
    screen.blit(roomText, (1070, 540))

def playerDamage(damage): # used to damage/heal the player
    global playerHealth
    playerHealth = playerHealth - damage
    if playerHealth < 0:
        playerHealth = 0
    elif playerHealth > 10:
        playerHealth = 10

def getWeaponData(weapon, info):
    if info == "firerate":
        if weapon < 20: # pistols
            return 22 - 2 * (weapon - 10) # firerate is in ticks per bullet
        elif weapon < 30: # SMGs
            return 11 - 1 * (weapon - 20)
        elif weapon < 40: # shotguns
            return 55 - 5 * (weapon - 30)
        else: # crossbows
            return 75 - 5 * (weapon - 40)
    elif info == "spread":
        if weapon < 20: # pistols
            return 7 - 1 * (weapon - 10) # spread is in degrees
        elif weapon < 30: # SMGs
            return 13 - 1 * (weapon - 20)
        elif weapon < 40: # shotguns
            return 21 - 1 * (weapon - 30)
        else: # crossbows
            return 0
    elif info == "ammo":
        if weapon < 30: # pistol and smg
            return 1
        elif weapon < 40: # shotgun
            return 8
        else: # crossbow
            return 12

def seePlayerTest(left, top):
    returnValue = True
    distanceBetween = ((left - player.rect.left) ** 2 + (top - player.rect.top) ** 2) ** 0.5 # pythag
    if left - player.rect.left == 0: # checks if denominator = 0
        if top - player.rect.top > 0: # checks if entity is above or below
            angle = 90
        else:
            angle = -90
    elif player.rect.left > left: # checks if entity is left or right of player
        angle = math.atan((top - player.rect.top) / (left - player.rect.left))
    else:
        angle = math.atan((top - player.rect.top) / (left - player.rect.left)) + math.pi
    for i in range(1, math.floor(distanceBetween / 50)): # checks tiles inbetween entity and player are floor tiles
        leftProjection = left + 50 * i * math.cos(angle) + 25
        topProjection = top + 50 * i * math.sin(angle) + 25
        tile = math.floor(leftProjection / 50) + 20 * math.floor(topProjection / 50) + 1
        if tile > 240 or tile < 1 or globals()["tile" + str(tile)] not in floorTiles:
            returnValue = False
    return returnValue
    
for i in range(1, 241):
    exec("tile" + str(i) + " = Tile()") # creates the varible name '"tile" + i' to be linked directly to the tile
    tileLeft = tileLeft + 50
    if tileLeft >= 1000:
        tileLeft = 0
        tileTop = tileTop + 50

screenBackground = pygame.image.load("resources/homeBackground.png")

gameStart = False
earlyEscape = 0
helpScreenDisplayed = False

while gameStart == False:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                earlyEscape = 1
                gameStart = True
        elif event.type == QUIT:
            earlyEscape = 1
            gameStart = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cursorLeft = pos[0]
            cursorTop = pos[1]
            if cursorLeft > 200 and cursorLeft < 500 and cursorTop > 300 and cursorTop < 400 and helpScreenDisplayed == False:
                gameStart = True
            elif cursorLeft > 700 and cursorLeft < 1000 and cursorTop > 300 and cursorTop < 400 and helpScreenDisplayed == False:
                screenBackground = pygame.image.load("resources/helpBackground.png")
            elif cursorLeft > 750 and cursorLeft < 1050 and cursorTop > 450 and cursorTop < 550 and helpScreenDisplayed == False:
                gameStart = True
    screen.blit(screenBackground, (0, 0))
    pygame.display.flip()

if earlyEscape == 1:
    pygame.quit()

player = Player()
playerSprite = pygame.sprite.Group()
playerSprite.add(player)

sidePanel = SidePanel()
itemSlot1 = ItemSlot(1)
itemSlot2 = ItemSlot(2)
slotInUse = SlotInUse()
itemInSlot1 = 0
itemInSlot2 = 0
itemSlot1Cooldown = 0 # cooldown is in ticks (1/50 of a second)
itemSlot2Cooldown = 0
currentActiveSlot = 1
playerHealth = 10
equipWeapon(11, 0, 0)
playerSpeed = 5
roomPlayerIn = 0
currentZone = 0
lastRoom = 0
ammo = 100
zoneData = ""
playerWon = 0
eKeyCheck = 1 # checks if the the player already pressed the e key to equip an item, and prevents them from equipping the item they just dropped on the next tick
isMouseButtonClicked = 0 # checks if mouse button is currently pressed
generateZone()

clock = pygame.time.Clock()
while running and playerWon == 0 and playerHealth > 0:
    if itemSlot1Cooldown > 0: # reduces cooldown of weapon slots
        itemSlot1Cooldown = itemSlot1Cooldown - 1
    if itemSlot2Cooldown > 0:
        itemSlot2Cooldown = itemSlot2Cooldown - 1
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            isMouseButtonClicked = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            isMouseButtonClicked = 0
    
    if isMouseButtonClicked == 1:
        pos = pygame.mouse.get_pos()
        cursorLeft = pos[0]
        cursorTop = pos[1]
        if currentActiveSlot == 1 and itemSlot1Cooldown == 0 and ammo >= getWeaponData(itemInSlot1, "ammo"): # player shoots weapon 1
            itemSlot1Cooldown = getWeaponData(itemInSlot1, "firerate")
            ammo = ammo - getWeaponData(itemInSlot1, "ammo")
            if itemInSlot1 < 40:
                bullets = 1
                if itemInSlot1 > 30: # shotguns shoot multiple bullets
                    bullets = itemInSlot1 - 25
                for i in range(bullets):
                    if cursorLeft - player.rect.left - 25 == 0: # checks if denominator = 0
                        if cursorTop - player.rect.top - 25 > 0: # checks if bullet should move up or down
                            angle = 90
                        else:
                            angle = -90
                    elif player.rect.left + 25 > cursorLeft: # checks if bullet should move left or right
                        angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi + 180 + random.randint(-getWeaponData(itemInSlot1, "spread"), getWeaponData(itemInSlot1, "spread")) # get angle for the bullet and convert it into degrees + spread
                    else:
                        angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi + random.randint(-getWeaponData(itemInSlot1, "spread"), getWeaponData(itemInSlot1, "spread"))
                    bullet = PlayerBullet(angle)
                    bullet.rect.left = player.rect.left + 25
                    bullet.rect.top = player.rect.top + 25
            else:
                if cursorLeft - player.rect.left - 25 == 0: # checks if denominator = 0
                    if cursorTop - player.rect.top - 25 > 0: # checks if bullet should move up or down
                        angle = 90
                    else:
                        angle = -90
                elif player.rect.left + 25 > cursorLeft: # checks if bullet should move left or right
                    angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi + 180 # crossbows have no spread
                else:
                    angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi
                arrow = PlayerArrow(angle)
                arrow.rect.left = player.rect.left + 25
                arrow.rect.top = player.rect.top + 25
        elif currentActiveSlot == 2 and itemSlot2Cooldown == 0 and ammo >= getWeaponData(itemInSlot2, "ammo") and itemInSlot2 > 0: # player shoots weapon 2
            itemSlot2Cooldown = getWeaponData(itemInSlot2, "firerate")
            ammo = ammo - getWeaponData(itemInSlot2, "ammo")
            if itemInSlot2 < 40:
                bullets = 1
                if itemInSlot2 > 30: # shotguns shoot multiple bullets
                    bullets = itemInSlot2 - 25
                for i in range(bullets):
                    if cursorLeft - player.rect.left - 25 == 0: # checks if denominator = 0
                        if cursorTop - player.rect.top - 25 > 0: # checks if bullet should move up or down
                            angle = 90
                        else:
                            angle = -90
                    elif player.rect.left + 25 > cursorLeft: # checks if bullet should move left or right
                        angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi + 180 + random.randint(-getWeaponData(itemInSlot2, "spread"), getWeaponData(itemInSlot2, "spread")) # get angle for the bullet and convert it into degrees + spread
                    else:
                        angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi + random.randint(-getWeaponData(itemInSlot1, "spread"), getWeaponData(itemInSlot2, "spread"))
                    bullet = PlayerBullet(angle)
                    bullet.rect.left = player.rect.left + 25
                    bullet.rect.top = player.rect.top + 25
            else:
                if cursorLeft - player.rect.left - 25 == 0: # checks if denominator = 0
                    if cursorTop - player.rect.top - 25 > 0: # checks if bullet should move up or down
                        angle = 90
                    else:
                        angle = -90
                elif player.rect.left + 25 > cursorLeft: # checks if bullet should move left or right
                    angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi + 180 # crossbows have no spread
                else:
                    angle = math.atan((cursorTop - player.rect.top - 25) / (cursorLeft - player.rect.left - 25)) * 180 / math.pi
                arrow = PlayerArrow(angle)
                arrow.rect.left = player.rect.left + 25
                arrow.rect.top = player.rect.top + 25
    
    for bullet in bulletSprites:
        bullet.update()
    player.update(pygame.key.get_pressed())
    slotInUse.update(pygame.key.get_pressed())
    for entity in visibleSprites:
        screen.blit(entity.surf, entity.rect)
    if pygame.key.get_pressed()[K_e] == False:
        eKeyCheck = 1
    if roomPlayerIn != 0:
        exec("currentRoomEntites = room" + str(roomPlayerIn) + "Sprites")
        for entity in currentRoomEntites:
            screen.blit(entity.surf, entity.rect)
            if isinstance (entity, Weapon):
                if pygame.sprite.spritecollideany(entity, playerSprite) and pygame.key.get_pressed()[K_e] and eKeyCheck == 1:
                    equipWeapon(entity.value, entity.rect.left, entity.rect.top)
                    entity.kill()
                    eKeyCheck = 0
            elif isinstance (entity, Ammo):
                if pygame.sprite.spritecollideany(entity, playerSprite):
                    ammo = ammo + entity.value
                    entity.kill()
            elif isinstance (entity, SpeedPack):
                if pygame.sprite.spritecollideany(entity, playerSprite):
                    playerSpeed = playerSpeed + 1
                    entity.kill()
            elif isinstance (entity, HealthPack):
                if pygame.sprite.spritecollideany(entity, playerSprite) and playerHealth < 10: # cannot be wasted when player has max health
                    playerDamage(-5) # heals the player by ten
                    entity.kill()
            else:
                entity.update()
    displayStats() # renders ammo text, room number text and healthbar above sideBar
    screen.blit(player.surf, player.rect) # render player above all other entities
    pygame.display.flip()
    clock.tick(50)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    if playerWon == 1:
        screenBackground = pygame.image.load("resources/winBackground.png")
    else:
        screenBackground = pygame.image.load("resources/loseBackground.png")
    screen.blit(screenBackground, (0, 0))
    pygame.display.flip()
pygame.quit()
