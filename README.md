# n-pendulum

![](examples/warning.png)

**This is an experimental branch! It allows running multiple pendulums on a single plot but it can't save the resulting animation.**

**In order to run multiple pendulums, separate arguments by spaces. For example
`./n-pendulum.py 2 -m1 1 1.5 -m2 2 -l1 0.8 0.9` would create two pendulums: one having `m1=1, m2=2, l1=0.8` and the other one having `m1=1.5, m2=2, l1=0.9`.**

***

This is a simple project studying the behaviour of simple chaotic systems using the Largrangian formulation. In particular, I implement a small plotter of a double and triple pendulum admitting a wide range of initial conditions using Matplotlib and SymPy.

## Usage

See all options:

```sh
> ./n-pendulum.py -h 
```

See options for the double pendulum:  

```sh
> ./n-pendulum.py 2 -h 
``` 

See options for the double pendulum:  

```sh
> ./n-pendulum.py 3 -h 
```

## Examples

#### Double Pendulum

`./n-pendulum.py 2 -theta1 1.346 -theta2 2.356 -o examples/2-pend-ex-1.gif`

![](examples/2-pend-ex-1.gif)

`./n-pendulum.py 2 -theta1 1.346 -theta2 2.356 -m1 2 -l1 2 -o examples/2-pend-ex-2.gif`

![](examples/2-pend-ex-2.gif)

#### Triple Pendulum

`./n-pendulum.py 3 -theta1 2 -theta2 2.356 -m1 2 -l1 2 -l2 2 -l3 2 -o examples/3-pend-ex-1.gif`

![](examples/3-pend-ex-1.gif)

`./n-pendulum.py 3 -theta1 2 -theta2 2 -theta3 2 -m3 2 -o examples/3-pend-ex-2.gif`

![](examples/3-pend-ex-2.gif)

## Future work

* I'd like to add realisations of other n-pendulums to the project, such as springed pendulums.

## Acknowledgements

The following [two](https://scipython.com/blog/the-double-pendulum/) [websites](https://deepnote.com/@jeh15/SymPy-Example-Double-Pendulum-c0d9439f-8e78-4603-8ffd-1c554ef536ad) have been very helpful.
