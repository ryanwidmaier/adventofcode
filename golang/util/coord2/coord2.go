package coord2

type Coord2 struct {
	X, Y int
}

func Add(lhs Coord2, rhs Coord2) Coord2 {
	return Coord2{
		X: lhs.X + rhs.X,
		Y: lhs.Y + rhs.Y,
	}
}

func Sub(lhs Coord2, rhs Coord2) Coord2 {
	return Coord2{
		X: lhs.X - rhs.X,
		Y: lhs.Y - rhs.Y,
	}
}
