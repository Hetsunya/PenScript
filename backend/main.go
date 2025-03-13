package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/rs/cors"
)

// OCRRequest - структура запроса к Yandex OCR
type OCRRequest struct {
	MimeType      string   `json:"mimeType"`
	LanguageCodes []string `json:"languageCodes"`
	Model         string   `json:"model"`
	Content       string   `json:"content"`
}

// OCRResponse - структура ответа от Yandex OCR
type OCRResponse struct {
	Result struct {
		TextAnnotation struct {
			FullText string `json:"fullText"`
		} `json:"textAnnotation"`
	} `json:"result"`
	Error interface{} `json:"error"`
}

// APIRequest - структура входного запроса в наш API
type APIRequest struct {
	Image string `json:"image"`
}

// APIResponse - структура ответа нашего API
type APIResponse struct {
	Text           string `json:"text,omitempty"`
	PredictedClass string `json:"predicted_class,omitempty"`
	Error          string `json:"error,omitempty"`
}

// sendOCRRequest отправляет изображение в Yandex OCR
func sendOCRRequest(encodedImage string) (*OCRResponse, error) {
	data := OCRRequest{
		MimeType:      "image/jpeg",
		LanguageCodes: []string{"*"},
		Model:         "page",
		Content:       encodedImage,
	}

	requestBody, err := json.Marshal(data)
	if err != nil {
		return nil, fmt.Errorf("ошибка маршаллинга запроса: %v", err)
	}

	url := "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(requestBody))
	if err != nil {
		return nil, fmt.Errorf("ошибка создания запроса: %v", err)
	}

	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authorization", "Bearer t1.9euelZrOnYuRkJidnp7OjpzOk8iekO3rnpWalJ3GmszNz8ySzpOdys3HjZrl9Pd9dzVB-e9hK2303fT3PSYzQfnvYStt9M3n9euelZqKnIqdnZiYmZeUx5qUxsvMx-_8xeuelZqKnIqdnZiYmZeUx5qUxsvMxw.FSCOVqmAuP9V65U1-7W23QUSfn6utHPiw_auUzxLgb3YeI1ymSgoRLlO_7-1WLvBnnsdYV4dxO-u-kyf4xBuAQ")
	req.Header.Add("x-folder-id", "b1g1g3i36s0esvqv39re")
	req.Header.Add("x-data-logging-enabled", "true")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("ошибка отправки запроса: %v", err)
	}
	defer resp.Body.Close()

	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("ошибка чтения ответа: %v", err)
	}

	fmt.Println("Ответ от Yandex OCR:", string(respBody)) // Для отладки

	var ocrResponse OCRResponse
	err = json.Unmarshal(respBody, &ocrResponse)
	if err != nil {
		return nil, fmt.Errorf("ошибка разбора ответа: %v", err)
	}

	// Если есть ошибка в ответе, обрабатываем её
	if ocrResponse.Error != nil {
		// Если ошибка — это строка, то выводим её как строку
		switch err := ocrResponse.Error.(type) {
		case string:
			return nil, fmt.Errorf("ошибка OCR: %v", err)
		default:
			return nil, fmt.Errorf("неизвестная ошибка OCR: %v", ocrResponse.Error)
		}
	}

	return &ocrResponse, nil
}

// sendToPython отправляет изображение в Python-скрипт для предсказания
// func sendToPython(encodedImage string) (string, error) {
// 	data := map[string]string{"image": encodedImage}
// 	requestBody, err := json.Marshal(data)
// 	if err != nil {
// 		return "", fmt.Errorf("ошибка маршаллинга запроса: %v", err)
// 	}
//
// 	url := "http://localhost:5000/predict"
// 	req, err := http.NewRequest("POST", url, bytes.NewBuffer(requestBody))
// 	if err != nil {
// 		return "", fmt.Errorf("ошибка создания запроса: %v", err)
// 	}
//
// 	req.Header.Add("Content-Type", "application/json")
//
// 	client := &http.Client{}
// 	resp, err := client.Do(req)
// 	if err != nil {
// 		return "", fmt.Errorf("ошибка отправки запроса: %v", err)
// 	}
// 	defer resp.Body.Close()
//
// 	respBody, err := ioutil.ReadAll(resp.Body)
// 	if err != nil {
// 		return "", fmt.Errorf("ошибка чтения ответа: %v", err)
// 	}
//
// 	var response map[string]string
// 	err = json.Unmarshal(respBody, &response)
// 	if err != nil {
// 		return "", fmt.Errorf("ошибка разбора ответа: %v", err)
// 	}
//
// 	return response["predicted_class"], nil
// }

// handleOCR - обработчик API для получения текста из изображения
func handleOCR(w http.ResponseWriter, r *http.Request) {
	var req APIRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}

	// Отправляем изображение в Yandex OCR
	ocrResponse, err := sendOCRRequest(req.Image)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Отправляем изображение в Python-скрипт для предсказания
	/*predictedClass, err := sendToPython(req.Image)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	Возвращаем распознанный текст и предсказанный класс
	*/
	json.NewEncoder(w).Encode(APIResponse{Text: ocrResponse.Result.TextAnnotation.FullText})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/ocr", handleOCR)

	// Настройка CORS
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://localhost:*"}, // Укажите адрес фронтенда
		AllowedMethods:   []string{"GET", "POST"},
		AllowedHeaders:   []string{"*"},
		AllowCredentials: true,
	})

	// Оборачиваем сервер в CORS-обработчик
	handlerWithCors := c.Handler(mux)

	log.Println("Сервер работает на порту 8080")
	log.Fatal(http.ListenAndServe(":8080", handlerWithCors))
}
