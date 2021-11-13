import struct
import pygame
import pygame.freetype
from pygame.locals import *

import moderngl

import atrium

# Basically load everything lol

pygame.init()

path = 'assets/'

desktop_bg = pygame.image.load(path + 'desktop_bg.png')
cursor = pygame.image.load(path + 'cursor.png')

# Files loaded in atrium


welcomefile = atrium.File(0, 0, "WELCOME.txt", 6, "not displayed")
#class Folder:
    #def __init__():

FPS = 60

clock = pygame.time.Clock()
VIRTUAL_RES=(1280, 720)
REAL_RES=(1056, 594)

screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
pygame.display.set_mode(REAL_RES, DOUBLEBUF|OPENGL)

ctx = moderngl.create_context()

texture_coordinates = [0, 1,  1, 1,
                       0, 0,  1, 0]

world_coordinates = [-1, -1,  1, -1,
                     -1,  1,  1,  1]

render_indices = [0, 1, 2,
                  1, 2, 3]

prog = ctx.program(
    vertex_shader='''
#version 300 es
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}
''',

    fragment_shader='''
#version 300 es
precision mediump float;
uniform sampler2D Texture;

out vec4 color;
in vec2 v_text;
void main() {
  vec2 center = vec2(0.5, 0.5);
  vec2 off_center = v_text - center;

  off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(3.25)); // curvy monitor effect (might make this toggleable separately ??)

  vec2 v_text2 = center+off_center;

  if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
      v_text2.y > 1.0 || v_text2.y < 0.0){
    color=vec4(0.0, 0.0, 0.0, 1.0);
  } else {
    color = vec4(texture(Texture, v_text2).rgb, 1.0);
    float fv = fract(v_text2.y * float(textureSize(Texture,0).y));
    fv=min(1.0, 0.8+0.3*min(fv, 1.0-fv));
    color.rgb*=fv;
  }
}
''')

prog_nc = ctx.program(
    vertex_shader='''
#version 300 es
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}
''',

    fragment_shader='''
#version 300 es
precision mediump float;
uniform sampler2D Texture;
in vec2 v_text;

out vec3 f_color;
void main() {
  f_color = texture(Texture,v_text).rgb;
}
''')

screen_texture = ctx.texture(
    VIRTUAL_RES, 3,
    pygame.image.tostring(screen, "RGB", 1))

screen_texture.repeat_x = False
screen_texture.repeat_y = False

vbo = ctx.buffer(struct.pack('8f', *world_coordinates))
uvmap = ctx.buffer(struct.pack('8f', *texture_coordinates))
ibo= ctx.buffer(struct.pack('6I', *render_indices))

vbo_nc = ctx.buffer(struct.pack('8f', *world_coordinates))
uvmap_nc = ctx.buffer(struct.pack('8f', *texture_coordinates))
ibo_nc = ctx.buffer(struct.pack('6I', *render_indices))

vao_content = [
    (vbo, '2f', 'vert'),
    (uvmap, '2f', 'in_text')
]
vao_content_nc = [
    (vbo_nc, '2f', 'vert'),
    (uvmap_nc, '2f', 'in_text')
]

vao = ctx.vertex_array(prog, vao_content, ibo)
vao_nc = ctx.vertex_array(prog_nc, vao_content_nc, ibo_nc) # i have to double the code so i can make the shaders work separately :/
crt = True
def render():
    texture_data = screen.get_view('1')
    screen_texture.write(texture_data)
    ctx.clear(14/255,40/255,66/255)
    screen_texture.use()
    if crt == 1:
        vao.render()
    else:
        vao_nc.render()
    pygame.display.flip()

# loop de poop

closed = False
nx_loop = False
pygame.mouse.set_visible(False)
wfWindow = atrium.npWindow("WELCOME.txt", "hi", 460, 297)
wfWindow.onClose() # make the window hidden

while True:
    while not closed: # in one loop now
        # quick maths
        original_x = pygame.mouse.get_pos()[0]
        original_y = pygame.mouse.get_pos()[1]
        fixed_x = pygame.mouse.get_pos()[0] * 1.5
        fixed_y = pygame.mouse.get_pos()[1] * 1.5
        for event in pygame.event.get():
            if event.type == QUIT: 
                closed = True
            # file onclick
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if welcomefile.checkClicked([fixed_x, fixed_y]):
                        welcomefile.clicked()
                        if welcomefile.currclicks == 0:
                            wfWindow.onReopen()
                    elif wfWindow.isDragging(fixed_x, fixed_y):
                        if not wfWindow.isMyAssGettingDragged:
                            wfWindow.whenMouseDrag(fixed_x, fixed_y)
                    
            
            if pygame.mouse.get_pressed()[0]:
                if wfWindow.isDragging(fixed_x, fixed_y):
                    wfWindow.whileMouseDragging(fixed_x, fixed_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if wfWindow.isDragging(fixed_x, fixed_y):
                    wfWindow.whenStopDrag()
            elif event.type == pygame.KEYDOWN:
                crt *= -1
        # rendering
        screen.blit(desktop_bg, (0,0))
        welcomefile.blit(screen)
        wfWindow.blit(screen)
        screen.blit(cursor, (fixed_x, fixed_y))
        render()
        clock.tick(FPS)
    if closed:
        pygame.quit()
        quit()
        
