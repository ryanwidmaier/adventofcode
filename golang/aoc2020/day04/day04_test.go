package main

import (
	"reflect"
	"testing"
)

func TestParse(t *testing.T) {
	lines := []string{
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
		"byr:1937 iyr:2017 cid:147 hgt:183cm",
		"",
		"iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
		"hcl:#cfa07d byr:1929",
		"",
		"hcl:#ae17e1 iyr:2013",
		"eyr:2024",
		"ecl:brn pid:760753108 byr:1931",
		"hgt:179cm",
	}

	actual := parse(lines)
	if len(actual) != 3 {
		t.Error("Length != 3")
	}
}

func TestParseLine(t *testing.T) {
	actual := parseLine("ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm")
	expected := Identification{
		raw: map[string]string{
			"ecl": "gry",
			"pid": "860033327",
			"eyr": "2020",
			"hcl": "#fffffd",
			"byr": "1937",
			"iyr": "2017",
			"cid": "147",
			"hgt": "183cm",
		},
		ecl: "gry",
		pid: "860033327",
		eyr: 2020,
		hcl: "#fffffd",
		byr: 1937,
		iyr: 2017,
		cid: 147,
		hgt: "183cm",
	}

	if !reflect.DeepEqual(actual, expected) {
		t.Errorf("Actual != expected")
	}
}

func TestBYR(t *testing.T) {
	actual := parseLine("byr:1919")
	if actual.byr != 0 {
		t.Error("BYR 1919")
	}
	actual = parseLine("byr:2003")
	if actual.byr != 0 {
		t.Error("BYR 2003")
	}
	actual = parseLine("byr:apples")
	if actual.byr != 0 {
		t.Error("BYR apples")
	}
	actual = parseLine("byr:1920")
	if actual.byr != 1920 {
		t.Error("BYR 1920")
	}
}

func TestIYR(t *testing.T) {
	actual := parseLine("iyr:2009")
	if actual.iyr != 0 {
		t.Error("2009")
	}
	actual = parseLine("iyr:2021")
	if actual.iyr != 0 {
		t.Error("2021")
	}
	actual = parseLine("iyr:apples")
	if actual.iyr != 0 {
		t.Error("apples")
	}
	actual = parseLine("iyr:2010")
	if actual.iyr != 2010 {
		t.Error("2010")
	}
}

func TestEYR(t *testing.T) {
	actual := parseLine("eyr:2019")
	if actual.eyr != 0 {
		t.Error("2009")
	}

	actual = parseLine("eyr:2031")
	if actual.eyr != 0 {
		t.Error("2021")
	}
	actual = parseLine("eyr:apples")
	if actual.eyr != 0 {
		t.Error("apples")
	}
	actual = parseLine("eyr:2020")
	if actual.eyr != 2020 {
		t.Error("2010")
	}
}

func TestHgt(t *testing.T) {
	actual := parseLine("hgt:149cm")
	if actual.hgt != "" {
		t.Error("")
	}

	actual = parseLine("hgt:194cm")
	if actual.hgt != "" {
		t.Error("")
	}

	actual = parseLine("hgt:150cm")
	if actual.hgt == "" {
		t.Error("")
	}

	actual = parseLine("hgt:58in")
	if actual.hgt != "" {
		t.Error("")
	}

	actual = parseLine("hgt:77in")
	if actual.hgt != "" {
		t.Error("")
	}

	actual = parseLine("hgt:59in")
	if actual.hgt == "" {
		t.Error("")
	}

	actual = parseLine("hgt:100ab")
	if actual.hgt != "" {
		t.Error("")
	}

	actual = parseLine("hgt:in")
	if actual.hgt != "" {
		t.Error("")
	}
}

func TestHcl(t *testing.T) {
	actual := parseLine("hcl:abcdef")
	if actual.hcl != "" {
		t.Error("")
	}

	actual = parseLine("hcl:#abcde")
	if actual.hcl != "" {
		t.Error("")
	}

	actual = parseLine("hcl:#012cdef")
	if actual.hcl != "" {
		t.Error("")
	}

	actual = parseLine("hcl:#012cde")
	if actual.hcl == "" {
		t.Error("")
	}
}

func TestEcl(t *testing.T) {
	actual := parseLine("ecl:brn")
	if actual.ecl == "" {
		t.Error("")
	}

	actual = parseLine("ecl:xyz")
	if actual.ecl != "" {
		t.Error("")
	}
}

func TestPID(t *testing.T) {
	actual := parseLine("pid:12345678")
	if actual.pid != "" {
		t.Error("")
	}

	actual = parseLine("pid:012345678")
	if actual.pid == "" {
		t.Error("")
	}
}
