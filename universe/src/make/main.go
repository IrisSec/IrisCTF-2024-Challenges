package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
)

// flag: g/NIfdcRgtJrd2l5gOHxI5zx9JAm0fbUm+0gIajLT6aE7D56anjPyArERG8REakv6vY2yCto
// 0x83,0xf3,0x48,0x7d,0xd7,0x11,0x82,0xd2,0x6b,0x77,0x69,0x79,0x80,0xe1,0xf1,0x23,0x9c,0xf1,0xf4,0x90,0x26,0xd1,0xf6,0xd4,0x9b,0xed,0x20,0x21,0xa8,0xcb,0x4f,0xa6,0x84,0xec,0x3e,0x7a,0x6a,0x78,0xcf,0xc8,0xa,0xc4,0x44,0x6f,0x11,0x11,0xa9,0x2f,0xea,0xf6,0x36,0xc8,0x2b,0x68,
// key: UGQiuplJUcK3YGPonxoWYMVnShkrkbS88U/RY7ohMBk=
// 0x50,0x64,0x22,0xba,0x99,0x49,0x51,0xc2,0xb7,0x60,0x63,0xe8,0x9f,0x1a,0x16,0x60,0xc5,0x67,0x4a,0x19,0x2b,0x91,0xb4,0xbc,0xf1,0x4f,0xd1,0x63,0xba,0x21,0x30,0x19,

var flag = []byte("irisctf{uN!v3rSaL5_B1n4Ries_arE_wEirD}")

var key = []byte{
	0x6a, 0x6d, 0xfe, 0xd4, 0xaa, 0x4d, 0x89, 0xe2,
	0xbf, 0x62, 0x1d, 0x2d, 0x68, 0x27, 0xfc, 0x71,
}

func print(b []byte) {
	for _, a := range b {
		fmt.Printf("0x%x,", a)
	}
	fmt.Printf("\n")
}

func main() {
	f, err := Encrypt(key, flag)
	if err != nil {
		fmt.Println("failed to encrypt")
		return
	}

	fmt.Printf("flag: %s\n", base64.StdEncoding.EncodeToString(f))
	print(f)

	k, err := Encrypt(f[len(f)-16:], key)
	if err != nil {
		fmt.Printf("failed to encrypt key: %s", err)
		return
	}

	fmt.Printf("key: %s\n", base64.StdEncoding.EncodeToString(k))
	print(k)
}

func Encrypt(key []byte, pt []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	ct := make([]byte, aes.BlockSize+len(pt))
	iv := ct[:aes.BlockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		return nil, err
	}

	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ct[aes.BlockSize:], pt)

	return ct, nil
}
