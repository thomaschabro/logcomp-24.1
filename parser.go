package parser

import (
	"compiler/tokenizer"
	"errors"
	"fmt"
	"strconv"
)

func Parse(input string) (int, error) {
	tok := tokenizer.CreateTokenizer(input)
	reg, err := parseTerm(tok)
	if err != nil {
		return 0, err
	}

	for {
		switch tok.Next.Type {
		case tokenizer.EOF:
			return reg, nil
		case tokenizer.PLUS:
			tok.NextToken()
			if tok.Next.Type != tokenizer.NUMBER {
				return reg, createError("a number", tok.Next)
			}
			num, err := parseTerm(tok)
			if err != nil {
				return reg, err
			}
			reg += num
		case tokenizer.MINUS:
			tok.NextToken()
			if tok.Next.Type != tokenizer.NUMBER {
				return reg, createError("a number", tok.Next)
			}
			num, err := parseTerm(tok)
			if err != nil {
				return reg, err
			}
			reg -= num
		default:
			return reg, createError("an operator", tok.Next)
		}
	}

}

func parseTerm(tok *tokenizer.Tokenizer) (int, error) {
	if tok.Next.Type != tokenizer.NUMBER {
		return 0, createError("a number", tok.Next)
	}
	reg, _ := strconv.Atoi(tok.Next.Literal)
	for {
		tok.NextToken()
		switch tok.Next.Type {
		case tokenizer.DIVIDE:
			tok.NextToken()
			if tok.Next.Type != tokenizer.NUMBER {
				return 0, createError("a number", tok.Next)
			}
			num, _ := strconv.Atoi(tok.Next.Literal)
			reg /= num
		case tokenizer.MULTIPLY:
			tok.NextToken()
			if tok.Next.Type != tokenizer.NUMBER {
				return 0, createError("a number", tok.Next)
			}
			num, _ := strconv.Atoi(tok.Next.Literal)
			reg *= num
		default:
			return reg, nil
		}
	}
}

func createError(expected string, token tokenizer.Token) error {
	msg := fmt.Sprintf(
		"Error: expected '%s' but got '%s'", expected, token.Literal,
	)
	return errors.New(msg)
}
