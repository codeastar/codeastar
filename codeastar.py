import turtle, math, random, os, yaml, sys, time
from datetime import datetime
from PIL import Image

dt_string = datetime.now().strftime("%d%m%Y_%H%M%S")     #get current datetime string

config_file = sys.argv[1] if len(sys.argv) >= 2 else "config.yml"      #get the configuration file from command line or use the default one
with open(os.path.dirname(os.path.abspath(__file__))+os.path.sep+config_file, 'r') as yaml_file:
  star_config = yaml.safe_load(yaml_file)
yaml_file.close()

codeastar = turtle.Turtle()    #initialize our turtle instance

length = star_config["screen"]["size"]
change_range_percent = star_config["screen"]["percentage change"]
margin = star_config["screen"]["margin"]
opposite_range_min = star_config["star"]["opposite"]["ratio to adjacent"]["min"]
opposite_range_max = star_config["star"]["opposite"]["ratio to adjacent"]["max"]
point_min = star_config["star"]["point"]["min"]
point_max = star_config["star"]["point"]["max"]
starting_angle_min = star_config["star"]["starting angle"]["min"]
starting_angle_max = star_config["star"]["starting angle"]["max"]
distance_from_center_min = star_config["star"]["distance from center"]["min"]
distance_from_center_max = star_config["star"]["distance from center"]["max"]
star_path = star_config["path"]

star_path = (star_path+os.path.sep) if os.path.sep != star_path[-1] else star_path
os.makedirs(os.path.dirname(star_path), exist_ok=True)

r_change_range_percent = (100+random.randrange(-change_range_percent, change_range_percent))/100
screen_length=round(length*r_change_range_percent)

turtle.title("Code A Star")
screen = turtle.Screen()
screen.setup(width=screen_length, height=screen_length)

distance_from_center = random.uniform(distance_from_center_min, distance_from_center_max)
#distance_from_center=0.86
adjacent = round((screen_length/(3.5 if (distance_from_center>0.45) else 2.4))*(1-margin/100))
opposite = round(adjacent * random.uniform(opposite_range_min, opposite_range_max))
print(f"Screen: {screen_length} Percentage: {r_change_range_percent} Opposite:{opposite} Adjacent:{adjacent}")
point = random.randrange(point_min, point_max)
#point=8
starting_angle = random.randrange(starting_angle_min, starting_angle_max)
#starting_angle=18


hypotenuse  = math.hypot(adjacent,opposite)
angle = math.degrees(math.atan(opposite/adjacent))  
next_angle = 90 - angle
point_angle = 360/point
print(f"Starting angle: {starting_angle} Point angle: {point_angle} Angle: {angle} DFC: {distance_from_center}")

codeastar.speed(0)
if ((starting_angle>45) or (distance_from_center > 0.45) or (starting_angle<-45) ):   #position handler
  codeastar.up()
  if (starting_angle>45):
    codeastar.forward(starting_angle/2)
  if (distance_from_center> 0.45):
    codeastar.backward(distance_from_center*14.5)
    if (distance_from_center> 0.8):
      codeastar.backward(distance_from_center*10+point*-7)
      codeastar.left(90)
      codeastar.forward(distance_from_center*16+point*5)
      codeastar.setheading(0)      #back to initial heading position
  if (starting_angle<-45):  
    codeastar.forward(starting_angle/2)
  codeastar.down()

#time.sleep(10)

codeastar.right(starting_angle)
for i in range(point):
  codeastar.color((random.random(),random.random(),random.random()),(random.random(),random.random(),random.random()))
  codeastar.begin_fill()
  codeastar.right(point_angle if (i>0) else 0)

  codeastar.forward(adjacent)
  codeastar.right(180-angle)
  codeastar.forward(hypotenuse)
  codeastar.right(180-next_angle)
  codeastar.forward(opposite)
  codeastar.end_fill()

  codeastar.up()
  codeastar.backward(opposite*distance_from_center)
  codeastar.right(90)
  codeastar.forward(opposite*distance_from_center)
  codeastar.down()

codeastar.hideturtle()
#'''
screen.getcanvas().postscript(file=f"{star_path}{dt_string}.eps")
img = Image.open(f"{star_path}{dt_string}.eps") 
img.save(f"{star_path}{dt_string}.png") 
img.close()
os.remove(f"{star_path}{dt_string}.eps")
#'''
#turtle.mainloop()  