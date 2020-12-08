package main

import (
"aoc2020/util/coord"
"aoc2020/util/io"
"aoc2020/util/robot"
"fmt"
)

func main() {
	textLines := io.ReadLinesArg1()
	parsedLines := parse(textLines)
	parsedLines := io.ParseLineGroups(textLines, " ")
	//part1(parsedLines, coord.Coord{X: 3, Y: 1})
	//part2(parsedLines)
}

func part1(lines []string) {
	for _, line := range lines {
		
	}
}
