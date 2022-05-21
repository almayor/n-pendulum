#!/usr/bin/env python
# coding: utf-8

import argparse
import dill
import imageio
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

from scipy.integrate import odeint
from tqdm import tqdm

from matplotlib.collections import LineCollection
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import Circle
from matplotlib import animation

from argparser import get_parser


class DoublePendulum:
    
    def __init__(self, m1, m2, l1, l2, state0, g=9.8, fun_dir="data/double_pend"):
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.state0 = state0
        self.g = g

        #loading precomputed ODE with SymPy
        self._load_sympy_funs(fun_dir)
        
    
    def _load_sympy_funs(self, fun_dir):
        double_pend_funs = ["dz1_f", "dz2_f", "dth1_f", "dth2_f", "E_f"]
        package_directory = os.path.dirname(os.path.abspath(__file__))

        for fun_name in double_pend_funs:
            filename = os.path.join(package_directory, fun_dir, f'double_pend_{fun_name}')
            with open(filename, 'rb') as f:
                fun = dill.load(f)
                setattr(self, fun_name, fun)

    
    def run(self, t_max=30, dt=0.01):
        self.t_max = t_max
        self.dt = dt
        self.t = np.arange(0, self.t_max+self.dt, self.dt)
        
        ans = odeint(
            self.integrate,
            y0=self.state0, t=self.t,
            args=(self.g,self.m1,self.m2,self.l1,self.l2)
        )
        self.th1 = ans.T[0]
        self.th2 = ans.T[2]
        
        self.x1 = self.l1*np.sin(self.th1)
        self.y1 = -self.l1*np.cos(self.th1)
        self.x2 = self.x1 + self.l2*np.sin(self.th2)
        self.y2 = self.y1 - self.l2*np.cos(self.th2) 
        
        self._check_energy_drift(ans)
                

    def _check_energy_drift(self, ans, E_drift=0.05):
        E0 = self.E_f(self.g, self.m1, self.m2, self.l1, self.l2, *self.state0)
        for i in range(len(ans)):
            E1 = self.E_f(self.g, self.m1, self.m2, self.l1, self.l2, *ans[i])
            if np.abs(E0 - E1) > E_drift:
                sys.exit(f"Something's wrong! Maximum energy drift exceeded {E_drift}")
        
        
    def plot(self, filepath=None, fps=30, max_trail=100, ns=20): 
        r0 = 0.03
        r1 = 0.01 + np.clip(self.m1, 1, 10) * 0.05
        r2 = 0.01 + np.clip(self.m2, 1, 10) * 0.05
            
        fig = plt.figure(facecolor="w", figsize=(6.25 / 2, 6.25 / 2), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.set_axis_off()
        ax.set_xlim(-self.l1-self.l2-max(r1, r2), self.l1+self.l2+max(r1, r2))
        ax.set_ylim(-self.l1-self.l2-max(r1, r2), self.l1+self.l2+max(r1, r2))
        ax.set_aspect('equal', adjustable='box')
        
        self.rods, = ax.plot([], [], lw=1, c='k')
        self.trail = [ax.plot([], [], lw=1, c='r', alpha=0, solid_capstyle='butt')[0]
                      for _ in range(ns)]
        
        self.c0 = Circle((0, 0), r0/2, fc='k', zorder=10)
        self.c1 = Circle((0, 0), r1, fc='b', ec='b', zorder=10)
        self.c2 = Circle((0, 0), r2, fc='r', ec='r', zorder=10) 
        
        ax.add_patch(self.c0)
        ax.add_patch(self.c1)
        ax.add_patch(self.c2)
        
        fig.tight_layout()
        frames = tqdm(range(0, self.t.size, 1), leave=False)
        self.ani = animation.FuncAnimation(
            fig, self._animate, frames=frames,
            fargs=(max_trail,ns), interval=self.dt*1000*2
        )
        
        if filepath:
            self.ani.save(filepath, writer='pillow',fps=0.5*1/self.dt, dpi=150)                        
            
    
    def _animate(self, i, max_trail, ns):
        self.c1.center = (self.x1[i], self.y1[i])
        self.c2.center = (self.x2[i], self.y2[i])
        self.rods.set_data(
            [0, self.x1[i], self.x2[i]],
            [0, self.y1[i], self.y2[i]]
        )
        
        s = max_trail // ns
        for j in range(ns):
            imin = max(i - (ns-j)*s, 0)
            imax = imin + s + 1
                    
            alpha = (j/ns)**3
            self.trail[j].set_data(self.x2[imin:imax], self.y2[imin:imax])
            self.trail[j].set_alpha(alpha)
        
        
    def integrate(self, state, t, g, m1, m2, l1, l2):
        th1, z1, th2, z2 = state
        return [
            self.dth1_f(z1),
            self.dz1_f(t, g, m1, m2, l1, l2, th1, th2, z1, z2),
            self.dth2_f(z2),
            self.dz2_f(t, g, m1, m2, l1, l2, th1, th2, z1, z2),
        ]


class TriplePendulum:
    
    def __init__(self, m1, m2, m3, l1, l2, l3, state0, g=9.8, fun_dir="data/triple_pend"):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        
        self.state0 = state0
        self.g = g 

        #loading precomputed ODE with SymPy
        self._load_sympy_funs(fun_dir)

    
    def _load_sympy_funs(self, fun_dir):
        triple_pend_funs = ["dz1_f", "dz2_f", "dz3_f", "dth1_f", "dth2_f", "dth3_f", "E_f"]
        package_directory = os.path.dirname(os.path.abspath(__file__))

        for fun_name in triple_pend_funs:
            filename = os.path.join(package_directory, fun_dir, f'triple_pend_{fun_name}')
            with open(filename, 'rb') as f:
                fun = dill.load(f)
                setattr(self, fun_name, fun)
    
    
    def run(self, t_max=30, dt=0.01):
        self.t_max = t_max
        self.dt = dt
        self.t = np.arange(0, self.t_max+self.dt, self.dt)
        
        ans = odeint(
            self.integrate,
            y0=self.state0, t=self.t,
            args=(self.g,self.m1,self.m2,self.m3,self.l1,self.l2,self.l3)
        )
        self.th1 = ans.T[0]
        self.th2 = ans.T[2]
        self.th3 = ans.T[4]
        
        self.x1 = self.l1*np.sin(self.th1)
        self.y1 = -self.l1*np.cos(self.th1)
        self.x2 = self.x1 + self.l2*np.sin(self.th2)
        self.y2 = self.y1 - self.l2*np.cos(self.th2)
        self.x3 = self.x2 + self.l3*np.sin(self.th3)
        self.y3 = self.y2 - self.l3*np.cos(self.th3)
        
        self._check_energy_drift(ans)
                

    def _check_energy_drift(self, ans, E_drift=0.05):
        E0 = self.E_f(self.g, self.m1, self.m2, self.m3, self.l1, self.l2, self.l3, *self.state0)
        for i in range(len(ans)):
            E1 = self.E_f(self.g, self.m1, self.m2, self.m3, self.l1, self.l2, self.l3, *ans[i])
            if np.abs(E0 - E1) > E_drift:
                sys.exit(f"Something's wrong! Maximum energy drift exceeded {E_drift}")
        
        
    def plot(self, filepath=None, fps=30, max_trail=100, ns=20): 
        r0 = 0.03
        r1 = 0.01 + np.clip(self.m1, 1, 10) * 0.05
        r2 = 0.01 + np.clip(self.m2, 1, 10) * 0.05
        r3 = 0.01 + np.clip(self.m3, 1, 10) * 0.05
            
        fig = plt.figure(facecolor="w", figsize=(6.25 / 2, 6.25 / 2), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.set_axis_off()
        lim = self.l1+self.l2+self.l3+max(r1, r2, r3)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect('equal', adjustable='box')
        
        self.rods, = ax.plot([], [], lw=1, c='k')
#         self.trail1 = [ax.plot([], [], lw=1, c='b', alpha=0, solid_capstyle='butt')[0]
#                        for _ in range(ns)]
        self.trail2 = [ax.plot([], [], lw=1, c='r', alpha=0, solid_capstyle='butt')[0]
                       for _ in range(ns)]
        self.trail3 = [ax.plot([], [], lw=1, c='g', alpha=0, solid_capstyle='butt')[0]
                       for _ in range(ns)]
        
        self.c0 = Circle((0, 0), r0/2, fc='k', zorder=10)
        self.c1 = Circle((0, 0), r1, fc='b', ec='b', zorder=10)
        self.c2 = Circle((0, 0), r2, fc='r', ec='r', zorder=10)
        self.c3 = Circle((0, 0), r3, fc='g', ec='g', zorder=10) 
        
        ax.add_patch(self.c0)
        ax.add_patch(self.c1)
        ax.add_patch(self.c2)
        ax.add_patch(self.c3)
        
        fig.tight_layout()
        frames = tqdm(range(0, self.t.size, 1), leave=False)
        
        self.ani = animation.FuncAnimation(
            fig, self._animate, frames=frames,
            fargs=(max_trail,ns), interval=self.dt*1000*2
        )
        
        if filepath:
            self.ani.save(filepath,writer='pillow',fps=0.5*1/self.dt, dpi=150)                        
            
    
    def _animate(self, i, max_trail, ns):
        self.c1.center = (self.x1[i], self.y1[i])
        self.c2.center = (self.x2[i], self.y2[i])
        self.c3.center = (self.x3[i], self.y3[i])
        
        self.rods.set_data(
            [0, self.x1[i], self.x2[i], self.x3[i]],
            [0, self.y1[i], self.y2[i], self.y3[i]]
        )
        
        s = max_trail // ns
        for j in range(ns):
            imin = max(i - (ns-j)*s, 0)
            imax = imin + s + 1   
            
            alpha = (j/ns)**3
#             self.trail1[j].set_data(self.x1[imin:imax], self.y1[imin:imax])
#             self.trail1[j].set_alpha(alpha)
            self.trail2[j].set_data(self.x2[imin:imax], self.y2[imin:imax])
            self.trail2[j].set_alpha(alpha)
            self.trail3[j].set_data(self.x3[imin:imax], self.y3[imin:imax])
            self.trail3[j].set_alpha(alpha)
        
        
    def integrate(self, state, t, g, m1, m2, m3, l1, l2, l3):
        th1, z1, th2, z2, th3, z3 = state
        return [
            self.dth1_f(z1),
            self.dz1_f(t, g, m1, m2, m3, l1, l2, l3, th1, th2, th3, z1, z2, z3),
            self.dth2_f(z2),
            self.dz2_f(t, g, m1, m2, m3, l1, l2, l3, th1, th2, th3, z1, z2, z3),
            self.dth3_f(z3),
            self.dz3_f(t, g, m1, m2, m3, l1, l2, l3, th1, th2, th3, z1, z2, z3),
        ]



if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.n == "2":
        pend = DoublePendulum(
            g=args.g,
            m1=args.m1, m2=args.m2,
            l1=args.l1, l2=args.l2,
            state0=(
                args.theta1, args.dtheta1,
                args.theta2, args.dtheta2)
        )
        pend.run(t_max=args.t_max)
        pend.plot(filepath=args.output_file)
        plt.show()

    elif args.n == "3":
        pend = TriplePendulum(
            g=args.g,
            m1=args.m1, m2=args.m2, m3=args.m3,
            l1=args.l1, l2=args.l2, l3=args.l3,
            state0=(
                args.theta1, args.dtheta1,
                args.theta2, args.dtheta2,
                args.theta3, args.dtheta3)
        )
        pend.run(t_max=args.t_max)
        pend.plot(filepath=args.output_file)

    plt.show()
