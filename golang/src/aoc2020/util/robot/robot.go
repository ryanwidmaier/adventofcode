package robot

import (
	"aoc2020/util/coord"
)

const NORTH = 0
const EAST = 1
const SOUTH = 2
const WEST = 3

type Direction int

func (d *Direction) TurnLeft() {
	*d = ((*d) - 1) % 4
}

func (d *Direction) TurnRight() {
	*d = ((*d) + 1) % 4
}

func (d Direction) String() string {
	switch d {
	case NORTH:
		return "N"
	case EAST:
		return "E"
	case SOUTH:
		return "S"
	case WEST:
		return "E"
	}
	return "?"
}

type Robot struct {
	Position coord.Coord
	Facing   Direction
}

func (r *Robot) Forward(amount int) {
	var adjust coord.Coord
	switch r.Facing {
	case NORTH:
		adjust = coord.Coord{X: 0, Y: -amount}
	case EAST:
		adjust = coord.Coord{X: amount, Y: 0}
	case SOUTH:
		adjust = coord.Coord{X: 0, Y: amount}
	case WEST:
		adjust = coord.Coord{X: -amount, Y: 0}
	}

	r.Position = coord.Add(r.Position, adjust)
}

func (r *Robot) Backward(amount int) {
	r.Forward(-amount)
}

func (r *Robot) Move(offset coord.Coord) {
	r.Position = coord.Add(r.Position, offset)
}

func (r *Robot) TurnLeft() {
	r.Facing.TurnLeft()
}

func (r *Robot) TurnRight() {
	r.Facing.TurnRight()
}
