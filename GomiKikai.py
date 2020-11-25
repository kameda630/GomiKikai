#import cv2
#print(cv2.__version__)
#import sys

#cv2.namedWindow("window_l", cv2.WINDOW_KEEPRATIO)

import tkinter
from tkinter import messagebox
#import scipy.sparse.linalg as spla
from sympy import symbols
from sympy.solvers import solve
import random
from numpy import arange
from numpy import abs


points = []
pcounter = 0
t = 0.001

#点を著すクラス
class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

#ウィンドウ座標をキャンバス座標に変換
def cp(p):
    return Point(p.x + 5, p.y + 5)

#拡大点を縮小点に変換
def p_small(p):
    return Point(p.x / 100, p.y / 100)

#縮小点を拡大点に変換
def p_big(p):
    return Point(p.x * 100, p.y * 100)

#マウス左ボタンクリック時の処理
def left_clicked(event):
    global pcounter
    if(pcounter < 10):
        dot(cp(event))
        points.append(p_small(Point(event.x, event.y)))
        pcounter = pcounter + 1

#点を描画する
def dot(p):
    canvas.create_oval(p.x - 2, p.y - 2, p.x + 2, p.y + 2, fill = 'black')

#二次関数を描画
def draw_niji(a):
    canvas.create_rectangle(5, 5, 500, 500, fill = 'white')
    for x in arange(0.02, 5, 0.02):
        sp = cp(p_big(Point(x - 0.02, a[0]*(x - 0.02)**2 + a[1]*(x - 0.02) + a[2])))
        ep = cp(p_big(Point(x, a[0]*x**2 + a[1]*x + a[2])))
        sx = sp.x
        sy = sp.y
        ex = ep.x
        ey = ep.y
        canvas.create_line(sx, sy , ex, ey)
    distance([0.7,0,1], Point(0,5))
        

#点と2次関数との距離を求める
def distance2(a, poi):
    x = symbols('x')
    psi = solve(2*(a[0]**2)*(x**3) + 3*a[0]*a[1]*(x**2) + (2*a[0]*a[2]+a[1]**2-2*a[0]*poi.y+1)*x + (a[1]*a[2]-poi.x-a[1]*poi.y))
    ps = []
    for p in psi:
        p_r, p_i = p.as_real_imag()
        if(p_i < 0.000001):
            ps.append(p_r)
    qs = []
    for p in ps:
        qs.append(a[0]*p**2 + a[1]*p + a[2])
    dists = []
    for i in range(0, len(ps) - 1):
        dists.append(((ps[i] - poi.x)**2 + (qs[i] - poi.y)**2)**0.5)
    dist = min(dists)
    return dist

def distance(a, poi):
    return abs(a[0]*(poi.x)**2 + a[1]*poi.x + a[2] - poi.y)

#機械学習処理
def gomi_kikai():
    global points
    global t
    a = [random.random(), random.random(), random.random()]
    now_gosa = 0
    next_gosa = 0
    next_a = a
    for point in points:
        now_gosa = now_gosa + distance(a, point)**2

    while next_gosa < now_gosa:
        if(next_gosa != 0):
            now_gosa = next_gosa
        a = next_a

        da0 = [a[0] + t, a[1], a[2]]
        gosa0 = 0
        for point in points:
            gosa0 = gosa0 + distance(da0, point)**2
        dgda0 = gosa0 - now_gosa

        da1 = [a[0], a[1] + t, a[2]]
        gosa1 = 0
        for point in points:
            gosa1 = gosa1 + distance(da1, point)**2
        dgda1 = gosa1 - now_gosa

        da2 = [a[0], a[1], a[2] + t]
        gosa2 = 0
        for point in points:
            gosa2 = gosa2 + distance(da2, point)**2
        dgda2 = gosa2 - now_gosa

        grad = [dgda0, dgda1, dgda2]
        gradsize = (dgda0**2 + dgda1**2 + dgda2**2)**0.5
        grad = [dgda0 / gradsize * t, dgda1 / gradsize * t, dgda2 / gradsize * t]

        next_a = [a[0] - grad[0], a[1] - grad[1], a[2] - grad[2]]

        next_gosa = 0
        for point in points:
            next_gosa = next_gosa + distance(next_a, point)**2
        print(str(now_gosa) + '   ' + str(next_gosa))
        #print(next_a)

    draw_niji(a)
    for point in points:
        dot(p_big(point))

#クリア
def clear():
    global points
    global pcounter
    points = []
    pcounter = 0
    canvas.create_rectangle(5, 5, 500, 500, fill = 'white')




#========メイン処理========

#ウィンドウ生成
main_wnd = tkinter.Tk()
main_wnd.geometry("630x530")

#キャンバス生成
canvas = tkinter.Canvas(main_wnd, width = 500, height = 500)
canvas.create_rectangle(5, 5, 500, 500, fill = 'white')
canvas.place(x = 1, y = 1)

#計算ボタン生成
b_culc = tkinter.Button(text = '計算', command = gomi_kikai)
b_culc.pack()
b_culc.place(x = 530, y = 100)

#クリアボタン生成
b_clear = tkinter.Button(text = 'クリア', command = clear)
b_clear.pack()
b_clear.place(x = 530, y = 150)

#イベント設定
canvas.bind('<Button-1>', left_clicked)

#待機
main_wnd.mainloop()
