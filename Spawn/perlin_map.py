import numpy as np
import math
import game
import pyray as rl

class PerlinMap:

    p = np.array([
        # Original perlin noise permutation table (1)
        0x97, 0xa0, 0x89, 0x5b, 0x5a, 0x0f, 0x83, 0x0d,
        0xc9, 0x5f, 0x60, 0x35, 0xc2, 0xe9, 0x07, 0xe1,
        0x8c, 0x24, 0x67, 0x1e, 0x45, 0x8e, 0x08, 0x63,
        0x25, 0xf0, 0x15, 0x0a, 0x17, 0xbe, 0x06, 0x94,
        0xf7, 0x78, 0xea, 0x4b, 0x00, 0x1a, 0xc5, 0x3e,
        0x5e, 0xfc, 0xdb, 0xcb, 0x75, 0x23, 0x0b, 0x20,
        0x39, 0xb1, 0x21, 0x58, 0xed, 0x95, 0x38, 0x57,
        0xae, 0x14, 0x7d, 0x88, 0xab, 0xa8, 0x44, 0xaf,
        0x4a, 0xa5, 0x47, 0x86, 0x8b, 0x30, 0x1b, 0xa6,
        0x4d, 0x92, 0x9e, 0xe7, 0x53, 0x6f, 0xe5, 0x7a,
        0x3c, 0xd3, 0x85, 0xe6, 0xdc, 0x69, 0x5c, 0x29,
        0x37, 0x2e, 0xf5, 0x28, 0xf4, 0x66, 0x8f, 0x36,
        0x41, 0x19, 0x3f, 0xa1, 0x01, 0xd8, 0x50, 0x49,
        0xd1, 0x4c, 0x84, 0xbb, 0xd0, 0x59, 0x12, 0xa9,
        0xc8, 0xc4, 0x87, 0x82, 0x74, 0xbc, 0x9f, 0x56, 
        0xa4, 0x64, 0x6d, 0xc6, 0xad, 0xba, 0x03, 0x40, 
        0x34, 0xd9, 0xe2, 0xfa, 0x7c, 0x7b, 0x05, 0xca, 
        0x26, 0x93, 0x76, 0x7e, 0xff, 0x52, 0x55, 0xd4,
        0xcf, 0xce, 0x3b, 0xe3, 0x2f, 0x10, 0x3a, 0x11, 
        0xb6, 0xbd, 0x1c, 0x2a, 0xdf, 0xb7, 0xaa, 0xd5, 
        0x77, 0xf8, 0x98, 0x02, 0x2c, 0x9a, 0xa3, 0x46, 
        0xdd, 0x99, 0x65, 0x9b, 0xa7, 0x2b, 0xac, 0x09,
        0x81, 0x16, 0x27, 0xfd, 0x13, 0x62, 0x6c, 0x6e, 
        0x4f, 0x71, 0xe0, 0xe8, 0xb2, 0xb9, 0x70, 0x68, 
        0xda, 0xf6, 0x61, 0xe4, 0xfb, 0x22, 0xf2, 0xc1, 
        0xee, 0xd2, 0x90, 0x0c, 0xbf, 0xb3, 0xa2, 0xf1, 
        0x51, 0x33, 0x91, 0xeb, 0xf9, 0x0e, 0xef, 0x6b, 
        0x31, 0xc0, 0xd6, 0x1f, 0xb5, 0xc7, 0x6a, 0x9d, 
        0xb8, 0x54, 0xcc, 0xb0, 0x73, 0x79, 0x32, 0x2d, 
        0x7f, 0x04, 0x96, 0xfe, 0x8a, 0xec, 0xcd, 0x5d, 
        0xde, 0x72, 0x43, 0x1d, 0x18, 0x48, 0xf3, 0x8d, 
        0x80, 0xc3, 0x4e, 0x42, 0xd7, 0x3d, 0x9c, 0xb4,
        # Original perlin noise permutation table (2)
        0x97, 0xa0, 0x89, 0x5b, 0x5a, 0x0f, 0x83, 0x0d,
        0xc9, 0x5f, 0x60, 0x35, 0xc2, 0xe9, 0x07, 0xe1,
        0x8c, 0x24, 0x67, 0x1e, 0x45, 0x8e, 0x08, 0x63,
        0x25, 0xf0, 0x15, 0x0a, 0x17, 0xbe, 0x06, 0x94,
        0xf7, 0x78, 0xea, 0x4b, 0x00, 0x1a, 0xc5, 0x3e,
        0x5e, 0xfc, 0xdb, 0xcb, 0x75, 0x23, 0x0b, 0x20,
        0x39, 0xb1, 0x21, 0x58, 0xed, 0x95, 0x38, 0x57,
        0xae, 0x14, 0x7d, 0x88, 0xab, 0xa8, 0x44, 0xaf,
        0x4a, 0xa5, 0x47, 0x86, 0x8b, 0x30, 0x1b, 0xa6,
        0x4d, 0x92, 0x9e, 0xe7, 0x53, 0x6f, 0xe5, 0x7a,
        0x3c, 0xd3, 0x85, 0xe6, 0xdc, 0x69, 0x5c, 0x29,
        0x37, 0x2e, 0xf5, 0x28, 0xf4, 0x66, 0x8f, 0x36,
        0x41, 0x19, 0x3f, 0xa1, 0x01, 0xd8, 0x50, 0x49,
        0xd1, 0x4c, 0x84, 0xbb, 0xd0, 0x59, 0x12, 0xa9,
        0xc8, 0xc4, 0x87, 0x82, 0x74, 0xbc, 0x9f, 0x56, 
        0xa4, 0x64, 0x6d, 0xc6, 0xad, 0xba, 0x03, 0x40, 
        0x34, 0xd9, 0xe2, 0xfa, 0x7c, 0x7b, 0x05, 0xca, 
        0x26, 0x93, 0x76, 0x7e, 0xff, 0x52, 0x55, 0xd4,
        0xcf, 0xce, 0x3b, 0xe3, 0x2f, 0x10, 0x3a, 0x11, 
        0xb6, 0xbd, 0x1c, 0x2a, 0xdf, 0xb7, 0xaa, 0xd5, 
        0x77, 0xf8, 0x98, 0x02, 0x2c, 0x9a, 0xa3, 0x46, 
        0xdd, 0x99, 0x65, 0x9b, 0xa7, 0x2b, 0xac, 0x09,
        0x81, 0x16, 0x27, 0xfd, 0x13, 0x62, 0x6c, 0x6e, 
        0x4f, 0x71, 0xe0, 0xe8, 0xb2, 0xb9, 0x70, 0x68, 
        0xda, 0xf6, 0x61, 0xe4, 0xfb, 0x22, 0xf2, 0xc1, 
        0xee, 0xd2, 0x90, 0x0c, 0xbf, 0xb3, 0xa2, 0xf1, 
        0x51, 0x33, 0x91, 0xeb, 0xf9, 0x0e, 0xef, 0x6b, 
        0x31, 0xc0, 0xd6, 0x1f, 0xb5, 0xc7, 0x6a, 0x9d, 
        0xb8, 0x54, 0xcc, 0xb0, 0x73, 0x79, 0x32, 0x2d, 
        0x7f, 0x04, 0x96, 0xfe, 0x8a, 0xec, 0xcd, 0x5d, 
        0xde, 0x72, 0x43, 0x1d, 0x18, 0x48, 0xf3, 0x8d, 
        0x80, 0xc3, 0x4e, 0x42, 0xd7, 0x3d, 0x9c, 0xb4,
    ])

    gradients = np.array([
        (1, 1), (-1, 1), (1, -1), (-1, -1),
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ])

    def __init__(self, window_width, window_height, scale, pixels_horizontal=50, perlin_scale=32):
        # Let be a pixel the value (x,y) of the perlin noise function at (x,y).
        # Each "pixel" will be represented as a square on the screen and this 
        # will be its width and height.
        self.pixel_width = int(math.ceil(math.ceil(window_width/pixels_horizontal)/scale))
        
        # How many pixels (vertical x horizontal) will be fit into the window. 
        self.pixels_vertical = int(math.ceil((window_height/scale)/self.pixel_width)) + 2
        self.pixels_horizontal = pixels_horizontal + 2

        np.random.shuffle(self.p)
        self.perlin_scale = perlin_scale
        self.chunk = np.fromfunction(np.vectorize(self.perlin_noise_at), 
            (self.pixels_vertical, self.pixels_horizontal))

        # This is just the offset relative to the game 2D camera.
        self.base_x = int(math.floor(-(window_width/2)/scale)) - self.pixel_width
        self.base_y = int(math.floor(-(window_height/2)/scale)) - self.pixel_width

        # Variables to store the player's movement
        self.previous_player_x = 0
        self.previous_player_y = 0

        # Coordinate (x,y) of the perlin noise function that will be
        # drawn at the top left of the screen.
        self.perlin_x = 0
        self.perlin_y = 0

        # As you can se at pixels_horizontal and pixels_vertical, the map we are going
        # to draw its bigger than the screen. We will move the origin of the map to
        # make a smoother sensation of movement, thus generating less calls to a function
        # perlin.noise_at(x,y) and rotation of rows.
        self.dx = 0
        self.dy = 0

    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(t, a, b):
        return a + t * (b - a)

    def grad(hash, x, y):
        g = PerlinMap.gradients[hash % 8]
        return g[0] * x + g[1] * y

    def perlin_noise_at(self, x, y):
        x /= self.perlin_scale
        y /= self.perlin_scale
        X = math.floor(x) & 255
        Y = math.floor(y) & 255
        x -= math.floor(x)
        y -= math.floor(y)
        u, v = PerlinMap.fade(x), PerlinMap.fade(y)
        A = self.p[X] + Y
        AA, AB = self.p[A], self.p[A + 1]
        B = self.p[X + 1] + Y
        BA, BB = self.p[B], self.p[B + 1]
        return PerlinMap.lerp(v,
            PerlinMap.lerp(u, PerlinMap.grad(self.p[AA], x, y), PerlinMap.grad(self.p[BA], x - 1, y)),
            PerlinMap.lerp(u, PerlinMap.grad(self.p[AB], x, y - 1), PerlinMap.grad(self.p[BB], x - 1, y - 1))
        ) * 0.5 + 0.5


    def update(self):
        # Get the new map drawing offset coordinates
        self.dx -= game.player.position.x - self.previous_player_x
        self.dy -= game.player.position.y - self.previous_player_y
        self.previous_player_x = game.player.position.x
        self.previous_player_y = game.player.position.y

        # As we move the map "image" with map_dx and map_dy following the speed of
        # the player to cause a moving sentation, we need to detect when we need to
        # reposition the map image and calculate new perlin noise rows or columns.

        if self.dy >= self.pixel_width:
            # Generate more terrain up (Move every row down and generate a new
            # perlin noise row at the first row).
            
            for i in range(self.pixels_vertical - 1, 0, -1):
                self.chunk[i] = self.chunk[i - 1]

            self.perlin_y -= 1
            self.dy -= self.pixel_width 

            for j in range(self.pixels_horizontal):
                self.chunk[0][j] = self.perlin_noise_at(self.perlin_x + j, self.perlin_y)
                            
        elif self.dy <= -self.pixel_width:
            # Generate more terrain up (Move every row up and generate a new
            # perlin noise row at the last row).
            for i in range(self.pixels_vertical - 1):
                self.chunk[i] = self.chunk[i + 1]

            self.perlin_y += 1
            self.dy += self.pixel_width

            for j in range(self.pixels_horizontal):
                self.chunk[self.pixels_vertical - 1][j] = self.perlin_noise_at(self.perlin_x + j,
                    self.perlin_y + self.pixels_vertical - 1)
            
        if self.dx <= -self.pixel_width:
            # Generate more terrain at the right (Move every row to the left and 
            # generate a new perlin noise column at the last column).
            for i in range(self.pixels_horizontal - 1):
                self.chunk[:,i] = self.chunk[:,i + 1]

            self.perlin_x += 1
            self.dx += self.pixel_width

            for j in range(self.pixels_vertical):
                self.chunk[j][self.pixels_horizontal - 1] = self.perlin_noise_at(self.perlin_x + 
                    self.pixels_horizontal -1, self.perlin_y + j)

        elif self.dx >= self.pixel_width:
            # Generate more terrain at the right (Move every row to the left and 
            # generate a new perlin noise column at the last column).
            for i in range(self.pixels_horizontal - 1, 0, -1):
                self.chunk[:,i] = self.chunk[:,i - 1]

            self.perlin_x -= 1
            self.dx -= self.pixel_width

            for j in range(self.pixels_vertical):
                self.chunk[j][0] = self.perlin_noise_at(self.perlin_x, self.perlin_y + j)

    
    def draw(self, camera_position):
        for i in range(self.pixels_vertical):
            for j in range(self.pixels_horizontal):
                noise = self.chunk[i][j]

                color = color = rl.Color(0xa8, 0x78, 0x3e, 0xff)
                if(noise <= 0.1):   color = rl.Color(0x4b, 0x35, 0x1b, 0xff)
                elif(noise <= 0.2): color = rl.Color(0x5e, 0x43, 0x22, 0xff)
                elif(noise <= 0.3): color = rl.Color(0x70, 0x50, 0x29, 0xff)
                elif(noise <= 0.4): color = rl.Color(0x82, 0x5d, 0x30, 0xff)
                elif(noise <= 0.5): color = rl.Color(0x95, 0x6b, 0x37, 0xff)

                rl.draw_rectangle(
                    self.base_x + int(camera_position.x) + self.pixel_width * j + int(self.dx),
                    self.base_y + int(camera_position.y) + self.pixel_width * i + int(self.dy),
                    self.pixel_width,
                    self.pixel_width,
                    color)