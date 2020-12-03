package io

import (
	"bufio"
	"log"
	"os"
	"regexp"
)

/** Read file from first cli arg and return lines */
func ReadLinesArg1() []string {
	return ReadLines(os.Args[1])
}

/** Return all the lines from a file */
func ReadLines(filename string) []string {
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

func ReadLinesRegexp(filename string, pattern string) [][]string {
	var result [][]string
	re := regexp.MustCompile(pattern)
	lines := ReadLines(filename)

	for _, v := range lines {
		result = append(result, re.FindStringSubmatch(v))
	}
	return result
}
