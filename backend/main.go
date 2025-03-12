package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
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
	TextAnnotation struct {
		FullText string `json:"fullText"`
	} `json:"textAnnotation"`
	Error struct {
		Code    int    `json:"code"`
		Message string `json:"message"`
	} `json:"error"`
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
	req.Header.Add("Authorization", "Bearer YOUR_IAM_TOKEN")
	req.Header.Add("x-folder-id", "YOUR_FOLDER_ID")
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

	var ocrResponse OCRResponse
	err = json.Unmarshal(respBody, &ocrResponse)
	if err != nil {
		return nil, fmt.Errorf("ошибка разбора ответа: %v", err)
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

	if ocrResponse.Error.Code != 0 {
		json.NewEncoder(w).Encode(APIResponse{Error: ocrResponse.Error.Message})
		return
	}

	json.NewEncoder(w).Encode(APIResponse{Text: ocrResponse.TextAnnotation.FullText})
}

func main() {
	http.HandleFunc("/ocr", handleOCR)
	fmt.Println("Сервер запущен на порту 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
