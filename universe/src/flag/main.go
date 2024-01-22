package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"errors"
	"fmt"
	"os"
)

var flag = []byte{
	0x83, 0xf3, 0x48, 0x7d, 0xd7, 0x11, 0x82, 0xd2,
	0x6b, 0x77, 0x69, 0x79, 0x80, 0xe1, 0xf1, 0x23,
	0x9c, 0xf1, 0xf4, 0x90, 0x26, 0xd1, 0xf6, 0xd4,
	0x9b, 0xed, 0x20, 0x21, 0xa8, 0xcb, 0x4f, 0xa6,
	0x84, 0xec, 0x3e, 0x7a, 0x6a, 0x78, 0xcf, 0xc8,
	0x0a, 0xc4, 0x44, 0x6f, 0x11, 0x11, 0xa9, 0x2f,
	0xea, 0xf6, 0x36, 0xc8, 0x2b, 0x68,
}

func main() {
	fmt.Printf("%s\n", base64.StdEncoding.EncodeToString(flag))
	fmt.Printf("Key: ")

	var k string
	if _, err := fmt.Scanln(&k); err != nil {
		fmt.Println("Failed to read input.")
		os.Exit(1)
	}

	key, err := base64.StdEncoding.DecodeString(k)
	if err != nil {
		fmt.Println("Failed to decode base64.")
		os.Exit(1)
	}

	out, err := Decrypt(key, flag)
	if err != nil {
		fmt.Println("Failed to decrypt.")
		os.Exit(1)
	}

	fmt.Printf("Flag: %s\n", out)
}

func Decrypt(key []byte, ct []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	if len(ct) < aes.BlockSize {
		return nil, errors.New("block size too small")
	}

	iv := ct[:aes.BlockSize]
	ct = ct[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	stream.XORKeyStream(ct, ct)

	return ct, err
}
