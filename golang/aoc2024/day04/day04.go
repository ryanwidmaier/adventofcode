package main

import (
	c "github.com/ryanwidmaier/adventofcode/golang/util/coord2"
	g "github.com/ryanwidmaier/adventofcode/golang/util/grid2"
	"github.com/ryanwidmaier/adventofcode/golang/util/io"
)

func main() {
	lines := io.ReadLines("day04/sample.txt")
	grid := g.FromLines(lines)
	part1(grid)
}

func part1(grid g.Grid2) {

}

func get4(grid g.Grid2, start c.Coord2, dx int, dy int) string {
	for dx_ := range 4 {
		for dy_ := range 4 {

		}
	}

}
