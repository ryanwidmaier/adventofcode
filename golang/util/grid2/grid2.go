package grid2

import c "github.com/ryanwidmaier/adventofcode/golang/util/coord2"

type Grid2 struct {
	data       map[c.Coord2]rune
	minX, maxX int
	minY, maxY int
}

func FromLines(lines []string) Grid2 {
	data := make(map[c.Coord2]rune)
	var maxX int

	for x, row := range lines {
		for y, val := range row {
			data[c.Coord2{X: x, Y: y}] = val
		}
	}

	return Grid2{data: data, minX: 0, maxX: maxX, minY: 0, maxY: len(lines)}
}

func (g *Grid2) Get(x int, y int) rune {
	return g.data[c.Coord2{X: x, Y: y}]
}
