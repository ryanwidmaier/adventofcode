package main

import (
	"fmt"
	"github.com/ryanwidmaier/adventofcode/golang/util/io"
	"golang.org/x/exp/slices"
	"os"
	"strconv"
)

func main() {
	textLines := io.ReadLineTokens(os.Args[1])
	parsedLines := parse(textLines)
	//part1(parsedLines)
	part2(parsedLines)
}

func parse(lines [][]string) [][]int {
	var result [][]int

	for _, line := range lines {
		var row []int
		for _, val := range line {
			i, _ := strconv.Atoi(val)
			row = append(row, i)
		}

		result = append(result, row)
	}

	return result
}

func part1(lines [][]int) {
	var safeCount int

	for _, row := range lines {
		isSafe := true

		// Make it so values are always increasing
		if row[0] > row[1] {
			slices.Reverse(row)
		}

		// Check each element
		prev := row[0] - 1
		for _, val := range row {
			diff := val - prev
			if diff < 1 || diff > 3 {
				isSafe = false
				break
			}
			prev = val
		}

		if isSafe {
			safeCount++
		}
	}

	fmt.Printf("Part 1: %v", safeCount)
}

func part2(lines [][]int) {
	var safeCount int

	for _, row := range lines {
		var errorCount int

		// Make it so values are always increasing
		if row[0] > row[1] {
			slices.Reverse(row)
		}

		// Check each element
		prev := row[0] - 1
		for _, val := range row {
			diff := val - prev
			if diff < 1 || diff > 3 {
				errorCount++
			}
			prev = val
		}

		if errorCount <= 1 {
			safeCount++
		}
	}

	fmt.Printf("Part 2: %v", safeCount)
}
