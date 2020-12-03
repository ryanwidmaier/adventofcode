package regex

import (
	"regexp"
)

func FindAllStringSubmatch(re *regexp.Regexp, target string) map[string]string {
	//re := regexp.MustCompile("(?P<first_char>.)(?P<middle_part>.*)(?P<last_char>.)")
	result := re.FindAllStringSubmatch(target, -1)[0]
	groupMap := map[string]string{}
	for i, n := range result {
		groupMap[re.SubexpNames()[i]] = n
	}
	return groupMap
}
