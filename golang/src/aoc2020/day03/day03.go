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
	part1(parsedLines, coord.Coord{X: 3, Y: 1})
	part2(parsedLines)
}

func parse(lines []string) [][]bool {
	result := make([][]bool, 0)
	for _, line := range lines {
		row := make([]bool, 0)
		for _, ch := range line {
			row = append(row, ch == '#')
		}
		result = append(result, row)
	}

	return result
}

func part1(lines [][]bool, offset coord.Coord) int {
	sled := robot.Robot{}
	var trees int

	for sled.Position.Y < len(lines) {
		line := lines[sled.Position.Y]
		if line[sled.Position.X%len(line)] {
			trees++
		}
		sled.Move(offset)
	}

	fmt.Println("Trees: ", trees)
	return trees
}

func part2(lines [][]bool) {
	offsets := []coord.Coord{
		{X: 1, Y: 1},
		{X: 3, Y: 1},
		{X: 5, Y: 1},
		{X: 7, Y: 1},
		{X: 1, Y: 2},
	}

	prod := part1(lines, offsets[0])
	for _, offset := range offsets[1:] {
		prod *= part1(lines, offset)
	}

	fmt.Println("Part2: ", prod)
}
