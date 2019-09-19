"""Contains view logic for tower ranges

Ideally, there would be a view class for each range, inheriting from a super class (i.e. AbstractRangeView) with a more
complicated file structure. However, for simplicity's sake, this has been avoided in favour of a single view class with
methods for each kind of range.

If you wish to add additional range shapes, simply inherit from this class
"""

#                                                  ,  ,
#                                                / \/ \
#                                               (/ //_ \_
#      .-._                                      \||  .  \
#       \  '-._                            _,:__.-"/---\_ \
#  ______/___  '.    .--------------------'~-'--.)__( , )\ \
# `'--.___  _\  /    |             Here        ,'    \)|\ `\|
#      /_.-' _\ \ _:,_          Be Dragons           " ||   (
#    .'__ _.' \'-/,`-~`                                |/
#        '. ___.> /=,|  Abandon hope all ye who enter  |
#         / .-'/_ )  '---------------------------------'
#         )'  ( /(/
#              \\ "
#               '=='

import tkinter as tk

import range_

__author__ = "Benjamin Martin"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__version__ = "1.0.0"


class RangeView:
    """Manages view logic for Range classes"""
    # Sorting ensures child classes are given higher precedence than their parent classes
    draw_methods = sorted([
        (range_.CircularRange, '_draw_circular'),
        (range_.DonutRange, '_draw_donut'),
        (range_.PlusRange, '_draw_plus')
    ], key=lambda i: len(i[0].mro()), reverse=True)

    @classmethod
    def draw(cls, canvas, range_: range_.AbstractRange, position, cell_size, *args, **kwargs):
        for key, method in cls.draw_methods:
            if isinstance(range_, key) or range_ == key:
                return getattr(cls, method)(canvas, range_, position, cell_size, *args, **kwargs)

        raise KeyError(f"Unable to find draw method for {range_}")

    @classmethod
    def _draw_circular(cls, canvas: tk.Canvas, range_: range_.CircularRange, position, cell_size, *args, **kwargs):
        x, y = position
        dr = range_.radius * cell_size
        return [canvas.create_oval(x - dr, y - dr, x + dr, y + dr, tag='range')]

    @classmethod
    def _draw_donut(cls, canvas: tk.Canvas, range_: range_.DonutRange, position, cell_size, *args, **kwargs):
        tags = []
        x, y = position
        for radius in (range_.inner_radius, range_.outer_radius):
            dr = radius * cell_size
            tag = canvas.create_oval(x - dr, y - dr, x + dr, y + dr, tag='range')
            tags.append(tag)
        return tags

    @classmethod
    def _draw_plus(cls, canvas: tk.Canvas, range_: range_.PlusRange, position, cell_size, *args, **kwargs):
        x, y = position
        o = range_.outer_radius * cell_size
        i = range_.inner_radius * cell_size

        # Could derive a formula, but cbf
        coords = [
            (-o, i), (-i, i), (-i, o),
            (i, o), (i, i), (o, i),
            (o, -i), (i, -i), (i, -o),
            (-i, -o), (-i, -i), (-o, -i)
        ]

        coords.append(coords[0])

        coords = [(x + dx, y + dy) for dx, dy in coords]

        return [canvas.create_polygon(coords, tag='range', fill='')]
