#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_sql.py
# Copyright 2008-2010 Stefano Costa <steko@iosa.it>
#
# This file is part of Total Open Station.
#
# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.


def to_sql(point, tablename):
    '''Generate SQL line corresponding to the input point.

    At this moment the column names are fixed, but they could change in the
    future. The default names are reasonable.'''

    params = {
        'wkt': to_wkt(point),
        'tablename': tablename,
        'pid': point[0],
        'text': point[4]}
    sql_string = "INSERT INTO %(tablename)s" % params
    sql_string += "(point_id, point_geom, point_text) VALUES"
    sql_string += "(%(pid)s,GeomFromText('%(wkt)s'),'%(text)s');\n" % params
    return sql_string


def to_wkt(point):
    pid, x, y, z, text = point
    wkt_representation = 'POINT(%s %s)' % (x, y)
    return wkt_representation


class OutputFormat:

    """
    Exports points data in SQL format suitable for use with PostGIS & friends.

    http://postgis.refractions.net/documentation/manual-1.3/ch04.html#id2986280
    has an example of loading an SQL file into a PostgreSQL database.

    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data, tablename='topsdata'):
        self.data = data
        self.tablename = tablename

    def process(self):
        lines = [to_sql(e, self.tablename) for e in self.data]
        lines.insert(0, 'BEGIN;\n')
        lines.append('COMMIT;\n')
        output = "".join(lines)
        return output

if __name__ == "__main__":
    TotalOpenSQL(
        [(1, 2, 3, 4, 'qwerty'),
         ("2.3", 42, 45, 12, 'asdfg')],
        'prova')
