## metaL core /Nim/

import os

## graph

type Object = object
    val: string
    nest: seq[Object]

import strutils

proc pad(self: Object, depth: int): string =
    "\n" & repeat("\t", depth)

proc head(self: Object, prefix: string): string =
    prefix & "<object:" & self.val & ">"

proc dump(self: Object, depth: int = 0, prefix: string = ""): string =
    let head = self.pad(depth) & self.head(prefix)
    return head

proc `$`(self: Object): string = self.dump("X")

let hello = Object(val: "Hello")
echo $hello

## init

doAssert paramCount() > 0, "no source files"

for i in commandLineParams():
    let srcfile = i
    echo srcfile
