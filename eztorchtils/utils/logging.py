from datetime import datetime

import numpy as np
import torch
from rich.console import Console
from rich.tree import Tree

console = Console()


def print_creator(color):
    def print_creator_inner(*args, **kwargs):
        console.print(*args, **kwargs, style=color)

    return print_creator_inner


red = print_creator("red")
green = print_creator("green")
bold = print_creator("bold")
blue = print_creator("blue")
purple = print_creator("purple")
orange = print_creator("orange")


def inspect(obj):
    console = Console(record=True)

    class TreeWrapper:
        def __init__(self) -> None:
            self.tree = None

        def add(self, label):
            if self.tree is None:
                self.tree = Tree(label)  # type: ignore
                return self.tree
            else:
                return self.tree.add(label)  # type: ignore

    def add_children(obj: object, root: Tree) -> None:
        if isinstance(obj, dict):
            dict_node = root.add(f"dict")
            for key in obj.keys():
                add_children(obj[key], dict_node.add(f"[bold]{key}[/bold]"))
        elif isinstance(obj, list) or isinstance(obj, np.ndarray):
            list_node = root.add(f"{type(obj)}[{len(obj)}]")
            if len(obj) > 0:
                add_children(obj[0], list_node)
            if len(obj) > 1:
                list_node.add("...")
        elif isinstance(obj, torch.Tensor):
            root.add(f"tensor[[blue]{tuple(obj.shape)}[/blue]; {obj.dtype}]")
        else:
            root.add(str(type(obj)))

    treewrapper = TreeWrapper()
    add_children(obj, treewrapper)  # type: ignore
    console.print(treewrapper.tree)


def datestr(full=True):
    now = datetime.now()
    if full:
        return f'{now.strftime("%Y-%m-%d")}-{now.strftime("%H-%M-%S")}'
    else:
        return f'{now.strftime("%Y-%m-%d")}-{now.strftime("%H-%M")}'
