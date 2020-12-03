package main

import (
	"aoc2020/util/io"
	"fmt"
	"regexp"
	"strconv"
)

func main() {
	textLines := io.ReadLinesArg1()
	lineLines := parse(textLines)
	part1(lineLines)
	part2(lineLines)
}

type Line struct {
	min, max int
	letter   rune
	password string
}

func parse(lines []string) []Line {
	var result []Line
	re := regexp.MustCompile("(\\d+)-(\\d+) (\\w): (\\w+)")
	for _, v := range lines {
		match := re.FindStringSubmatch(v)

		min, _ := strconv.Atoi(match[1])
		max, _ := strconv.Atoi(match[2])

		parsed := Line{
			min:      min,
			max:      max,
			letter:   []rune(match[3])[0],
			password: match[4],
		}
		result = append(result, parsed)
	}
	return result
}

func part1(lines []Line) {
	var valid, invalid int

	for _, v := range lines {
		count := 0
		for _, r := range v.password {
			if r == v.letter {
				count++
			}
		}

		if v.min <= count && count <= v.max {
			valid++
		} else {
			invalid++
		}
	}

	fmt.Println()
	fmt.Println("Part 1")
	fmt.Println("Valid: ", valid)
	fmt.Println("Invalid: ", invalid)
}

func part2(lines []Line) {
	var valid, invalid int

	for _, v := range lines {
		runes := []rune(v.password)

		if (runes[v.min-1] == v.letter) != (runes[v.max-1] == v.letter) {
			valid++
		} else {
			invalid++
		}
	}

	fmt.Println()
	fmt.Println("Part 2")
	fmt.Println("Valid: ", valid)
	fmt.Println("Invalid: ", invalid)
}
