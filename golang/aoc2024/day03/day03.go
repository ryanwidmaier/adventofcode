package main

import (
	"fmt"
	"github.com/ryanwidmaier/adventofcode/golang/util/io"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	solve("sample.txt")
	fmt.Println()
	solve("sample2.txt")
	fmt.Println()
	solve("input.txt")
}

func solve(filename string) {
	lines := io.ReadLines(filename)
	line := strings.Join(lines, "\n")
	part1(line)
	part2(line)
}

func part1(line string) {
	var answer int
	re := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)`)
	found := re.FindAllStringSubmatch(line, -1)
	for _, mult := range found {

		left, _ := strconv.Atoi(mult[1])
		right, _ := strconv.Atoi(mult[2])
		answer += left * right

		//fmt.Printf("%v -> %v\n", mult, left*right)
	}

	fmt.Printf("Part 1: %v\n", answer)
}

func part2(line string) {
	var answer int
	flag := true
	re := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)`)
	found := re.FindAllStringSubmatch(line, -1)

	for _, mult := range found {
		if mult[0] == "do()" {
			flag = true
		} else if mult[0] == "don't()" {
			flag = false
		} else if flag {
			left, _ := strconv.Atoi(mult[1])
			right, _ := strconv.Atoi(mult[2])
			answer += left * right
		}

		//fmt.Printf("%v -> %v\n", mult, left*right)
	}

	fmt.Printf("Part 2: %v\n", answer)
}
