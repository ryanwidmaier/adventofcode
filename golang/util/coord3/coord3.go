package coord3

type Coord3 struct {
	X, Y, Z int
}

func Add(lhs Coord3, rhs Coord3) Coord3 {
	return Coord3{
		X: lhs.X + rhs.X,
		Y: lhs.Y + rhs.Y,
		Z: lhs.Z + rhs.Z,
	}
}

func Sub(lhs Coord3, rhs Coord3) Coord3 {
	return Coord3{
		X: lhs.X - rhs.X,
		Y: lhs.Y - rhs.Y,
		Z: lhs.Z - rhs.Z,
	}
}
