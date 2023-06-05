#this file stores neatly all the CSS needed-
#for the GUI of the application

lineEditCSS = """
background-color: rgb(35,35,35);
border: 1px rgb(35,35,35);
color: white;
border-radius:5px;
"""

pushButtonCSS = """
QPushButton{
            background-color: rgb(35,35,35);
            border: 1px rgb(60,60,60);
            color: white;
            font-size:12;
            highlight: white;
            border-radius:10px
        }
        QPushButton:hover {
            background-color: rgb(80,80,80);
        }
        QPushButton:pressed {
            background-color: rgb(40,40,40);
        }
"""


callButtonCSS = """
QPushButton{
	background-color: rgb(48, 214, 76);
	border: 1px rgb(60,60,60);
	color: lime;
	font-size:12;
	highlight: white;
	border-radius:10px
}
QPushButton:hover {
	background-color: rgb(80,80,80);
}
QPushButton:pressed {
	background-color: rgb(40,40,40);
}
"""


frameCSS = """
background-color: rgb(35,35,35);
border: 1px rgb(60,60,60);
color: white;
font-size:12;
highlight: white;
border-radius:10px;
"""

utilityButtonCSS = """
QPushButton{
    background-color: rgb(104, 104, 104);
    border: 1px rgb(60,60,60);
    color: lime;
    font-size:12;
    highlight: white;
    border-radius:10px
}
QPushButton:hover {
    background-color: rgb(80,80,80);
}
QPushButton:pressed {
    background-color: rgb(40,40,40);
}

"""


hangUpCallCSS = """
QPushButton{
    background-color: rgb(214, 47, 47);
    border: 1px rgb(60,60,60);
    color: lime;
    font-size:12;
    highlight: white;
    border-radius:10px
}
QPushButton:hover {
    background-color: rgb(80,80,80);
}
QPushButton:pressed {
    background-color: rgb(40,40,40);
}
"""