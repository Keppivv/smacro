## Usage

> each line corresponds to one command, each line can only have one command.
> 
> each command consist of 5 key variables, [Type, XPosition, YPositon, Duration, Key]
>
> commands such as Left Click does not use the last Key variable, and Key Presses don't use X or Y position.

### Types
> **Middle Mouse Click acceptable command type names : "mclick", "middleclick", "scrollclick", "scrollwheelclick", "wheelclick"**
> 
> **Right Mouse Click acceptable command type names : "rightclick", "rclick"**
> 
> **Left Mouse Click acceptable command type names : "leftclick", "click", "lclick", "normalclick"**
> 
> **Key Press acceptable command type names : "press", "presskey"**
> 
> **Sleep acceptable command type names : "sleep", "duration", "delay"**

Left Mouse Click : "leftclick x=200 y=200 delay=200"
> Moves cursor to x 200 y 200 in 200 milliseconds and performs a left click

Right Mouse Click : "rclick delay=50"
> Right Click at current cursor position at 50 millisecond delay

Key Press : "press key=r delay=5"
> Presses "R" key for 5 milliseconds
