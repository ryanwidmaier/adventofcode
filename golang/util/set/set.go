package set

type StringSet = map[string]struct{}

func (lhs StringSet) Add(val string) {
	lhs[val] = struct{}{}
}

func (lhs StringSet) Intersection(rhs StringSet) StringSet {
	shorter, longer := shorterLonger(lhs, rhs)
	var intersect StringSet
	intersect = make(StringSet)

	for v1, _ := range shorter {
		_, prs := longer[v1]
		if prs {
			intersect.Add(v1)
		}
	}
	return intersect
}

func shorterLonger(lhs StringSet, rhs StringSet) (StringSet, StringSet) {
	if len(lhs) < len(rhs) {
		return lhs, rhs
	}
	return rhs, lhs
}
