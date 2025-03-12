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
	Text  string `json:"text"`
	Error string `json:"error,omitempty"`
}

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "OK")
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
	req.Header.Add("Authorization", "Bearer t1.9euelZrHjJqLmsyNnYvLjsmPkc-Uie3rnpWalJ3GmszNz8ySzpOdys3HjZrl9PdxNDpB-e9Xchz73fT3MWM3QfnvV3Ic-83n9euelZqLm5KKl46TmIqezcnNy5SLjO_8xeuelZqLm5KKl46TmIqezcnNy5SLjA.FiXxkrVdyLjSFP41JEh9W0FCD8aAsoRi2-JhvSoHezRGzFxDiMnLpwDzGt3n99oPh2MhONQtw15okDcIPDyOBA")
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

// handleOCR - обработчик API для получения текста из изображения
func handleOCR(w http.ResponseWriter, r *http.Request) {
	var req APIRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}

	ocrResponse, err := sendOCRRequest(req.Image)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Проверяем, есть ли ошибка в ответе от Yandex OCR
	if ocrResponse.Result.TextAnnotation.FullText == "" {
		// Если текст пустой, возвращаем ошибку
		json.NewEncoder(w).Encode(APIResponse{Error: "Не удалось распознать текст"})
		return
	}

	// Возвращаем распознанный текст
	json.NewEncoder(w).Encode(APIResponse{Text: ocrResponse.Result.TextAnnotation.FullText})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/ocr", handleOCR)

	// Настройка CORS
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"http://localhost:5173"}, // Укажите адрес фронтенда
		AllowedMethods:   []string{"GET", "POST"},
		AllowedHeaders:   []string{"Content-Type"},
		AllowCredentials: true,
	})

	// Оборачиваем сервер в CORS-обработчик
	handlerWithCors := c.Handler(mux)

	log.Println("Сервер работает на порту 8080")
	log.Fatal(http.ListenAndServe(":8080", handlerWithCors))
}
