package main

import (
	"github.com/ryanwidmaier/adventofcode/golang/util/io"
)

func main() {
	textLines := io.ReadLinesArg1()
	parsedLines := parse(textLines)
	parsedLines := io.ParseLineGroups(textLines, " ")
	//part1(parsedLines, coord3.Coord{X: 3, Y: 1})
	//part2(parsedLines)
}

func part1(lines []string) {
	for _, line := range lines {

	}
}
