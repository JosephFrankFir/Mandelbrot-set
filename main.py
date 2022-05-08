from PIL import Image
from mandelbrot import MandelbrotSet
from viewport import Viewport
import matplotlib.cm
import time
import sys 
import os
import threading 
import argparse

ap = argparse.ArgumentParser(description='Mandelbrot settings.')
ap.add_argument("-o", "--output", required=False, help="Save image")
ap.add_argument("-s", "--show", action="store_true",required=False, help="Show image")
args = ap.parse_args()

if len(sys.argv) > 1:
 ap.print_help()
 exit()

done = False
# Function for implementing the loading animation
def load_animation():
  
    # String to be displayed when the application is loading
    load_str = "this may take a while"
    ls_len = len(load_str)
  
  
    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of
    # the duration of animation
    counttime = 0        
      
    # pointer for travelling the loading string
    i = 0                     
  
    while (done != True):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.075) 
                              
        # converting the string to list
        # as string is immutable
        load_str_list = list(load_str) 
          
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
          
        # y->for storing altered ASCII code
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered
        # switch uppercase to lowercase and vice-versa 
        if x != 32 and x != 46:             
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
          
        # for storing the resultant string
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
              
        # displaying the resultant string
        sys.stdout.write("\r"+f"{res} " + animation[anicount])
        sys.stdout.flush()
  
        # Assigning loading string
        # to the resultant string
        load_str = res
  
          
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
      
    # for windows OS
    if os.name =="nt":
        os.system("cls")
          
    # for linux / Mac OS
    else:
        os.system("clear")
t = threading.Thread(target=load_animation)
t.start()


def paint(mandelbrot_set, viewport, palette, smooth):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth)
        index = int(min(stability * len(palette), len(palette) - 1))
        pixel.color = palette[index % len(palette)]

def denormalize(palette):
    return [
        tuple(int(channel * 255) for channel in color)
        for color in palette
    ]


colormap = matplotlib.cm.get_cmap("inferno").colors
palette = denormalize(colormap)


mandelbrot_set = MandelbrotSet(max_iterations=1366, escape_radius=1000)
image = Image.new(mode="RGB", size=(1366 , 768))
viewport = Viewport(image, center=-0.7435 + 0.1314j, width=0.002)
t2 = threading.Thread(target=paint(mandelbrot_set, viewport, palette, smooth=True))
t2.start()

if args.show == True:
 t3 = threading.Thread(image.show())
 t3.start()
else:
 print("Error")

if args.output:
 image.save(f"{args.output}.jpg")
elif args.show == None:
 print("Error") 


done = True
sys.stdout.write("Done!")
