from entity import TexturedEntity
from buff import Buff
import pyray as rl 
import registry

class Player(TexturedEntity):

    texture: rl.Texture
    buffs: list[Buff]

    def __init__(self):
        super().__init__(speed=rl.Vector2(10,10))
        self.lerp_x = self.position.x
        self.lerp_y = self.position.y
        self.buffs = []


    def move(self):
        move_x = int(rl.is_key_down(rl.KeyboardKey.KEY_D)) - int(rl.is_key_down(rl.KeyboardKey.KEY_A))
        move_y = int(rl.is_key_down(rl.KeyboardKey.KEY_S)) - int(rl.is_key_down(rl.KeyboardKey.KEY_W))

        if move_x != 0 and move_y != 0:
            self.lerp_x += (move_x)/2. * self.speed.x
            self.lerp_y += (move_y)/2. * self.speed.y
        else:
            self.lerp_x += move_x * self.speed.x
            self.lerp_y += move_y * self.speed.y
    
        self.position.x = rl.lerp(self.position.x, self.lerp_x, 0.15)
        self.position.y = rl.lerp(self.position.y, self.lerp_y, 0.15)

# Public player instance
player_instance = Player()
registry.register_texture(Player)