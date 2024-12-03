package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/ryanwidmaier/adventofcode/golang/util/io"
	"github.com/ryanwidmaier/adventofcode/golang/util/math"
)

type Pair struct {
	left, right int
}

func main() {
	textLines := io.ReadLineTokens(os.Args[1])
	parsedLines := parse(textLines)
	part1(parsedLines)
	part2(parsedLines)
}

func parse(lines [][]string) []Pair {
	var result []Pair

	for _, line := range lines {
		if len(line) != 2 {
			log.Printf("skipping line %s", strings.Join(line, " "))
			continue
		}

		i, err := strconv.Atoi(line[0])
		if err != nil {
			panic(err)
		}

		i2, err := strconv.Atoi(line[1])
		if err != nil {
			panic(err)
		}

		result = append(result, Pair{i, i2})
	}

	return result
}

func part1(lines []Pair) {
	var sum int
	ordered := sortLists(lines)

	for _, p := range ordered {
		sum += math.Abs(p.left - p.right)
	}

	fmt.Printf("Part 1: %v\n", sum)
}

func part2(lines []Pair) {
	right := make(map[int]int)

	for _, p := range lines {
		right[p.right]++
	}

	var sum int
	for _, p := range lines {
		sum += p.left * right[p.left]
	}

	fmt.Printf("Part 2: %v\n", sum)
}

func sortLists(lines []Pair) []Pair {
	var left []int
	var right []int

	for _, p := range lines {
		left = append(left, p.left)
		right = append(right, p.right)
	}

	sort.Slice(left, func(i, j int) bool {
		return left[i] < left[j]
	})
	sort.Slice(right, func(i, j int) bool {
		return right[i] < right[j]
	})

	var result []Pair
	for i, _ := range left {
		result = append(result, Pair{left[i], right[i]})
	}
	return result
}
