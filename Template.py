# CTK: Cherokee Toolkit
#
# Authors:
#      Alvaro Lopez Ortega <alvaro@alobbs.com>
#
# Copyright (C) 2009 Alvaro Lopez Ortega
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public 
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import os
import stat
import inspect

from Widget import Widget


class Template (Widget):
    cache = {}

    def __init__ (self, filename):
        Widget.__init__ (self)
        self.filename = filename

    def _content_update (self):
        content = open(self.filename, 'r').read()
        mtime   = os.stat (self.filename)[stat.ST_MTIME]
        Template.cache[self.filename] = {'mtime':   mtime,
                                         'content': content}

    def _content_get (self):
        try:
            cached = Template.cache[self.filename]
            s = os.stat (self.filename)
            mtime = s[stat.ST_MTIME]
            if mtime <= cached['mtime']:
                # Hit
                return cached['content']
        except:
            pass

        # Miss
        self._content_update()
        return Template.cache[self.filename]['content']


    def Render (self):
        vars = globals()
        vars.update (inspect.currentframe(1).f_locals)

        content = self._content_get()
        while True:
            prev = content[:]
            content = content % (vars)

            if content == prev:
                break

        return content
