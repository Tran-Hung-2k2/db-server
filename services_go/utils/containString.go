package utils

import "strings"

func Contains(child string, parent []string) bool {
	for _, r := range parent {
		if strings.EqualFold(child, r) {
			return true
		}
	}
	return false
}
