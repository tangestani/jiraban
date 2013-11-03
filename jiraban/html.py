#
# Copyright (c) 2013, Marc Tardif <marc@interunion.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__metaclass__ = type

__all__ = [
    "generate_html",
    "priority_style",
    "sprite_url",
    "status_style",
    ]

import os

from base64 import b64encode
from datetime import datetime

from jinja2 import (
    Environment,
    PackageLoader,
    )

from jiraban.board import (
    IN_PROGRESS,
    PRIORITY_ORDER,
    READY_FOR_QA,
    READY_FOR_SPRINT,
    STATUS_ORDER,
    )
from jiraban.colors import html_colors


def priority_style(priority):
    """Filter a priority into a CSS class."""
    return "priority-%s" % priority.lower()


def status_style(status):
    """Filter a status into a CSS class."""
    if status in (IN_PROGRESS, READY_FOR_QA, READY_FOR_SPRINT):
        return "status-inprogress"

    return "status-%s" % status.lower()


def sprite_url(sprite, media="media"):
    """Filter a sprite name into a base64 encoded data url."""
    filename = "%s.png" % sprite.replace("-", "_")
    path = os.path.join(media, filename)
    with open(path) as f:
        data = b64encode(f.read())
        return "data:image/png;base64,%s" % data


def generate_html(board, media="media"):
    """Generate an HTML kanban board to represent L{Item}s."""
    environment = Environment(loader=PackageLoader("jiraban", "templates"))

    # Filter identity names to unique colors.
    names = [i.name for i in board.identities]
    colors = html_colors(len(names))
    names_to_colors = dict(zip(names, colors))
    environment.filters["identity_color"] = lambda i: names_to_colors[i]

    # Filter images to sprites.
    sprites = sorted(set(
        [priority_style(p) for p in PRIORITY_ORDER] +
        [status_style(s) for s in STATUS_ORDER]))
    environment.filters["sprite_url"] = lambda s: sprite_url(s, media)

    # Filter priority and status names to CSS classes.
    environment.filters["priority_style"] = priority_style
    environment.filters["status_style"] = status_style

    template = environment.get_template("board.html")
    return template.render(
        board=board,
        sprites=sprites,
        now=datetime.utcnow().strftime("%a %e %b at %H:%M UTC"))
