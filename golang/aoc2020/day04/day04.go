package main

import (
	"fmt"
	"github.com/ryanwidmaier/adventofcode/golang/util/io"
	"regexp"
	"strconv"
	"strings"
)

type Identification struct {
	raw map[string]string
	byr int
	iyr int
	eyr int
	hgt string
	hcl string
	ecl string
	pid string
	cid int
}

func (id *Identification) IsValidPart1() bool {
	keys := []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
	for _, k := range keys {
		_, prs := id.raw[k]
		if !prs {
			return false
		}
	}
	return true
}

func (id *Identification) IsValidPart2() bool {
	return id.IsValidPart1() &&
		id.byr != 0 &&
		id.iyr != 0 &&
		id.eyr != 0 &&
		id.hgt != "" &&
		id.hcl != "" &&
		id.ecl != "" &&
		id.pid != ""
	//id.cid != 0
}

func main() {
	textLines := io.ReadLinesArg1()
	parsedLines := parse(textLines)
	part1(parsedLines)
	part2(parsedLines)
}

func parse(lines []string) []Identification {
	result := make([]Identification, 0)
	build := ""

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			result = append(result, parseLine(build))
			build = ""
		} else {
			if len(build) > 0 {
				build += " "
			}
			build += line
		}
	}
	if len(build) > 0 {
		result = append(result, parseLine(build))
	}

	return result
}

func parseLine(line string) Identification {
	tokens := strings.Fields(line)
	id := Identification{
		raw: make(map[string]string),
	}

	for _, token := range tokens {
		split := strings.Split(token, ":")
		field, value := split[0], split[1]

		id.raw[field] = value
	}

	id.byr = parseIntRange(id.raw["byr"], 1920, 2002)
	id.iyr = parseIntRange(id.raw["iyr"], 2010, 2020)
	id.eyr = parseIntRange(id.raw["eyr"], 2020, 2030)
	id.hgt = parseHeight(id.raw["hgt"])
	id.hcl = parseHColor(id.raw["hcl"])
	id.ecl = parseEColor(id.raw["ecl"])
	id.pid = parsePID(id.raw["pid"])
	id.cid, _ = strconv.Atoi(id.raw["cid"])

	return id
}

func parseIntRange(val string, min int, max int) int {
	i, _ := strconv.Atoi(val)
	if i >= min && i <= max {
		return i
	}
	return 0
}

func parseHeight(val string) string {
	r, _ := regexp.Compile("^(\\d+)(cm|in)$")
	match := r.FindStringSubmatch(val)
	if len(match) == 3 {
		if match[2] == "cm" {
			if parseIntRange(match[1], 150, 193) != 0 {
				return val
			}
		} else if match[2] == "in" {
			if parseIntRange(match[1], 59, 76) != 0 {
				return val
			}
		}
	}

	return ""
}

func parseHColor(val string) string {
	m, _ := regexp.MatchString("^#[0-9a-f]{6}$", val)
	if m {
		return val
	}
	return ""
}

func parseEColor(val string) string {
	set := map[string]struct{}{
		"amb": {},
		"blu": {},
		"brn": {},
		"gry": {},
		"grn": {},
		"hzl": {},
		"oth": {},
	}
	_, prs := set[val]
	if prs {
		return val
	}
	return ""
}

func parsePID(val string) string {
	m, _ := regexp.MatchString("^[0-9]{9}$", val)
	if m {
		return val
	}
	return ""
}

func part1(idens []Identification) {
	var valid, invalid int
	for _, id := range idens {
		if id.IsValidPart1() {
			valid++
		} else {
			invalid++
		}
	}

	fmt.Println("Part1")
	fmt.Println("  Valid: ", valid)
	fmt.Println("  Invalid: ", invalid)
}

func part2(idens []Identification) {
	var valid, invalid int
	for _, id := range idens {
		if id.IsValidPart2() {
			valid++
		} else {
			invalid++
		}
	}

	fmt.Println("Part2")
	fmt.Println("  Valid: ", valid)
	fmt.Println("  Invalid: ", invalid)
}
