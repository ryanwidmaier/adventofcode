package coord

type Coord struct {
	X, Y, Z int
}

func Add(lhs Coord, rhs Coord) Coord {
	return Coord{
		X: lhs.X + rhs.X,
		Y: lhs.Y + rhs.Y,
		Z: lhs.Z + rhs.Z,
	}
}

func Sub(lhs Coord, rhs Coord) Coord {
	return Coord{
		X: lhs.X - rhs.X,
		Y: lhs.Y - rhs.Y,
		Z: lhs.Z - rhs.Z,
	}
}
