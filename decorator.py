#! /bin/env python
#
# github decorator
# \m/ 2013, skazhy

import os
import fileinput

from datetime import date, timedelta
from subprocess import Popen


REPO = "decorator"
repodir = os.path.join(os.path.dirname(__file__), REPO)


class HumbleList(list):
    def __getitem__(self, i):
        try:
            return super(HumbleList, self).__getitem__(i)
        except IndexError:
            return None


def transform_matrix(matrix):
    rows = max(len(r) for r in matrix)
    return [[matrix[c][r] for c in range(7)] for r in range(rows)]


def exe(*cmds, **kwargs):
    cwd = kwargs.get("cwd", repodir)
    for cmd in cmds:
        pid = Popen(["/bin/sh", "-c", cmd], cwd=cwd).pid
        while(os.waitpid(pid, 0)[1] != 0):
            continue
    return


def create_repo():
    exe("git init --quiet %s" % REPO, cwd=None)


def commit(day):
    timestamp = day.strftime("%Y.%m.%d 16:00:00 +0200")
    filename = "coolfile"
    exe("echo '%s' > %s" % (timestamp, filename),
        "git add %s" % filename,
        "git commit -m '%s' --date='%s' " % (timestamp, timestamp))


def closest_sunday(day):
    # GitHub weeks start on Sundays. *americans*
    return day - timedelta(days=day.weekday() + 1 % 7)


def decorate(matrix):
    create_repo()
    d = closest_sunday(date.today() - timedelta(weeks=len(matrix)-1))

    for row in matrix:
        for col in row:
            if col and col != " ":
                commit(d)
            d += timedelta(days=1)


if __name__ == "__main__":
    stdin_matrix = [HumbleList(line[:-1]) for line in fileinput.input()]

    for _ in range(len(stdin_matrix), 7):
        stdin_matrix.append(HumbleList([None]))

    decorate(transform_matrix(stdin_matrix))
