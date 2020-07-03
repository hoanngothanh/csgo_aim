# Fastest CSGO Deep Learning cheat! New Features!

  - Extremely fast detection on GPU as well as good inference time on cpu 
  - Even more accurate models.
  - Currently supported maps: Dust(but you can also try other maps)
### How to use

Choose either detectionTkInterGui.py(still in beta) or detectionOpenCvGui.py(you will be able to see a screen with boxex around predicted models )

Download yolov3-tiny.weights and yolov3-tiny.cfg(you can also use yolov3-tiny-prn_last.weights and yolov3-tiny-prn.cfg for greater speed but lower accuracy) from the following [link](https://drive.google.com/drive/folders/10QvwT857wyShDlkZ9JWOJ1FGrL963OCU?usp=sharing)

Edit friendlyTeam.txt file to add the classes that you want to detect (0 ,1 for Terrorist, Terrorist Head and 2,3 for Counter Terrorist and CT head)

Change capture params in .ini file according to your screen

### New Release is out !!!!
If you dont want to compile the file or you dont have python you can just go to the [release](https://github.com/kir486680/csgo_aim/releases) page and run .exe file in the archive 
### Features Planned For Next Release
  - Use YOLOv5 model for more convinient and faster GPU inference(In progress)
  - Using a config file instead of txt(done)
  - Add a yolov3-tiny-prn model(done)
  - Use Multithreading to read the screen(In progress)
  - Make a convinient recording utility to get more data(In progress)

### Want To Help?

I would highly appreciate anybodys help with my project! If you are interested in working in a team you can contact me!(kir486680@protonmail.com)
