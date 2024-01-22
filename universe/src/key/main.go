package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"errors"
	"fmt"
	"os"
)

var key = []byte{
	0x50, 0x64, 0x22, 0xba, 0x99, 0x49, 0x51, 0xc2,
	0xb7, 0x60, 0x63, 0xe8, 0x9f, 0x1a, 0x16, 0x60,
	0xc5, 0x67, 0x4a, 0x19, 0x2b, 0x91, 0xb4, 0xbc,
	0xf1, 0x4f, 0xd1, 0x63, 0xba, 0x21, 0x30, 0x19,
}

func main() {
	fmt.Printf("Flag: ")

	var f string
	if _, err := fmt.Scanln(&f); err != nil {
		fmt.Println("Failed to read input.")
		os.Exit(1)
	}

	flag, err := base64.StdEncoding.DecodeString(f)
	if err != nil {
		fmt.Println("Failed to decode base64.")
		os.Exit(1)
	}

	out, err := Decrypt(flag[len(flag)-16:], key)
	if err != nil {
		fmt.Println("Failed to decrypt.")
		os.Exit(1)
	}

	fmt.Printf("Key: %s\n", base64.StdEncoding.EncodeToString(out))
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
