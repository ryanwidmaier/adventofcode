package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	lines := readLines(os.Args[1])
	values := parse(lines)
	fmt.Println(values)
	fmt.Println("Part1: ", part1(values))
	fmt.Println("Part2: ", part2(values))
}

func readLines(filename string) []string {
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)
	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return lines
}

func parse(lines []string) []int {
	var result []int
	for _, v := range lines {
		intVal, _ := strconv.Atoi(v)
		result = append(result, intVal)
	}
	return result
}

func part1(values []int) int {
	for i1, v1 := range values {
		for i2, v2 := range values {
			if i1 == i2 {
				continue
			}

			if v1+v2 != 2020 {
				continue
			}

			return v1 * v2
		}
	}

	return 0
}

func part2(values []int) int {
	for i1, v1 := range values {
		for i2, v2 := range values {
			if i1 == i2 {
				continue
			}
			for i3, v3 := range values {
				sum := v1 + v2 + v3
				if i3 == i2 || i3 == i1 {
					continue
				}

				if sum != 2020 {
					continue
				}

				return v1 * v2 * v3
			}
		}
	}

	return 0
}
