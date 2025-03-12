package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type APIRequest struct {
	Image string `json:"image"`
}

func main() {
	// Читаем файл и кодируем его в base64
	imagePath := "test.jpg"
	imageData, err := ioutil.ReadFile(imagePath)
	if err != nil {
		fmt.Println("Ошибка чтения файла:", err)
		return
	}
	base64Image := base64.StdEncoding.EncodeToString(imageData)

	// Формируем JSON-запрос
	requestBody, err := json.Marshal(APIRequest{Image: base64Image})
	if err != nil {
		fmt.Println("Ошибка маршалинга JSON:", err)
		return
	}

	// Отправляем POST-запрос на ваш сервер
	url := "http://localhost:8080/ocr"
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Println("Ошибка при отправке запроса:", err)
		return
	}
	defer resp.Body.Close()

	// Читаем и выводим ответ сервера
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Ошибка чтения ответа:", err)
		return
	}

	fmt.Println("Ответ сервера:", string(body))
}
