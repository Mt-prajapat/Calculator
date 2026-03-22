import sys
import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout,
    QVBoxLayout, QTextEdit, QLabel, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class ScientificCalculator(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Professional Graphing Calculator")
        self.setFixedSize(500,520)

        self.expression=""
        self.history=[]
        self.showing_history=False
        self.dark_theme=True

        self.create_ui()

    def create_ui(self):

        layout=QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(8,8,8,8)

        title=QLabel("Professional Graphing Calculator")
        title.setFont(QFont("Segoe UI",14))
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        # DISPLAY PANEL
        self.display=QTextEdit("")
        self.display.setFont(QFont("Segoe UI",22))
        self.display.setFixedHeight(80)

        # allow typing
        self.display.setReadOnly(False)

        # remove 0 when clicked
        self.display.mousePressEvent=self.clear_default

        layout.addWidget(self.display)

        # HISTORY + THEME BUTTONS
        top_buttons=QHBoxLayout()

        self.history_btn=QPushButton("History")
        self.history_btn.setFixedHeight(40)
        self.history_btn.clicked.connect(self.toggle_history)

        self.theme_btn=QPushButton("Switch Theme")
        self.theme_btn.setFixedHeight(40)
        self.theme_btn.clicked.connect(self.toggle_theme)

        top_buttons.addWidget(self.history_btn)
        top_buttons.addWidget(self.theme_btn)

        layout.addLayout(top_buttons)

        grid=QGridLayout()
        grid.setSpacing(8)

        buttons=[
        ('sin',0,0),('cos',0,1),('tan',0,2),('log',0,3),('ln',0,4),

        ('7',1,0),('8',1,1),('9',1,2),('÷',1,3),('C',1,4),

        ('4',2,0),('5',2,1),('6',2,2),('×',2,3),('⌫',2,4),

        ('1',3,0),('2',3,1),('3',3,2),('-',3,3),('%',3,4),

        ('0',4,0),('.',4,1),('+/-',4,2),('+',4,3),('=',4,4),

        ('GRAPH',5,0),('GRAPH3D',5,2),('SOLVE',5,4)
        ]

        for text,row,col in buttons:

            btn=QPushButton(text)
            btn.setFont(QFont("Segoe UI",11))
            btn.setFixedHeight(42)

            btn.clicked.connect(lambda checked,t=text:self.click(t))

            grid.addWidget(btn,row,col)

        layout.addLayout(grid)

        self.setLayout(layout)

        self.apply_theme()

    # remove default 0
    def clear_default(self,event):

        if self.display.toPlainText()=="":
            self.display.clear()

        QTextEdit.mousePressEvent(self.display,event)

    # toggle history
    def toggle_history(self):

        if not self.history:
            return

        if self.showing_history:
            self.display.setText(self.expression if self.expression else "0")
            self.showing_history=False
        else:
            history_text="\n".join(self.history[-8:])
            self.display.setText(history_text)
            self.showing_history=True

    # theme switch
    def toggle_theme(self):

        self.dark_theme=not self.dark_theme
        self.apply_theme()

    def apply_theme(self):

        if self.dark_theme:

            self.setStyleSheet("""
            QWidget{background:#121212;color:white;}

            QTextEdit{
                background:#1e1e1e;
                color:#7FFFD4;
                border:none;
                padding:12px;
                border-radius:15px;
            }

            QPushButton{
                background:#2c2c2c;
                border:none;
                border-radius:14px;
            }

            QPushButton:hover{
                background:#3a3a3a;
            }

            QPushButton:pressed{
                background:#00aa44;
            }
            """)

        else:

            self.setStyleSheet("""
            QWidget{background:#f0f0f0;color:black;}

            QTextEdit{
                background:white;
                color:black;
                border:1px solid gray;
                padding:12px;
                border-radius:15px;
            }

            QPushButton{
                background:#e0e0e0;
                border-radius:14px;
            }

            QPushButton:hover{
                background:#d0d0d0;
            }

            QPushButton:pressed{
                background:#00aa44;
            }
            """)

    def click(self,key):

        self.expression=self.display.toPlainText()

        if key=="=":
            self.calculate()

        elif key=="C":

            self.expression=""
            self.history.clear()
            self.showing_history=False
            self.display.setText("")
            return

        elif key=="⌫":

            self.expression=self.expression[:-1]

        elif key=="sin":
            self.expression="math.sin("+self.expression+")"

        elif key=="cos":
            self.expression="math.cos("+self.expression+")"

        elif key=="tan":
            self.expression="math.tan("+self.expression+")"

        elif key=="log":
            self.expression="math.log10("+self.expression+")"

        elif key=="ln":
            self.expression="math.log("+self.expression+")"

        elif key=="GRAPH":
            self.plot_graph()
            return

        elif key=="GRAPH3D":
            self.plot_3d()
            return

        elif key=="SOLVE":
            self.solve_equation()
            return

        else:

            if key=="×":
                key="*"
            if key=="÷":
                key="/"

            self.expression+=key

        self.display.setText(self.expression if self.expression else "")

    def calculate(self):

        try:

            self.expression=self.display.toPlainText()
            result=str(eval(self.expression))

            entry=self.expression+" = "+result
            self.history.append(entry)

            self.display.setText(result)
            self.expression=result

        except:

            self.display.setText("Error")
            self.expression=""

    def plot_graph(self):

        try:

            expr=self.display.toPlainText()

            x=np.linspace(-10,10,400)
            y=eval(expr)

            plt.figure("2D Graph")
            plt.plot(x,y)
            plt.grid()
            plt.title(expr)
            plt.show()

        except:
            print("Graph Error")

    def plot_3d(self):

        try:

            from mpl_toolkits.mplot3d import Axes3D

            fig=plt.figure()
            ax=fig.add_subplot(111,projection='3d')

            x=np.linspace(-5,5,50)
            y=np.linspace(-5,5,50)

            x,y=np.meshgrid(x,y)
            z=np.sin(np.sqrt(x**2+y**2))

            ax.plot_surface(x,y,z,cmap='viridis')
            plt.show()

        except:
            print("3D Error")

    def solve_equation(self):

        try:

            expr=self.display.toPlainText()

            x=sp.symbols('x')
            expr=sp.sympify(expr)

            solution=sp.solve(expr,x)

            self.history.append("Solve "+str(expr)+" → "+str(solution))

        except:
            self.history.append("Solve Error")


if __name__=="__main__":

    app=QApplication(sys.argv)

    calc=ScientificCalculator()
    calc.show()

    sys.exit(app.exec())