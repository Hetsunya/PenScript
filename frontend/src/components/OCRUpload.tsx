import { useState } from "react";
import axios from "axios";
import "./OCRUpload.css";

const OCRUpload = () => {
  const [image, setImage] = useState<File | null>(null);
  const [text, setText] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setImage(file);
      setText(""); 
      setError(""); 
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!image) return;

    setLoading(true);
    setError(""); 

    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64Image = reader.result?.toString().split(",")[1]; 
      if (!base64Image) {
        setError("Не удалось прочитать изображение");
        setLoading(false);
        return;
      }

      console.log("Отправляем изображение на сервер:", base64Image); // Отладочный вывод

      try {
        const response = await axios.post("http://localhost:8080/ocr", { image: base64Image }, {
          headers: {
            "Content-Type": "application/json",
          },
        });
        console.log("Ответ сервера:", response); // Ответ сервера
        setText(response.data.text);
      } catch (err: any) {
        console.error("Ошибка при отправке запроса:", err);
        if (err.response) {
          setError(`Ошибка: ${err.response.status} - ${err.response.data.error || 'Неизвестная ошибка на сервере'}`);
        } else if (err.request) {
          setError("Ошибка при отправке запроса. Проверьте подключение к серверу.");
        } else {
          setError("Неизвестная ошибка: " + err.message);
        }
      } finally {
        setLoading(false);
      }
    };
    reader.readAsDataURL(image);
  };

  return (
    <div className="ocr-upload-container">
      <h1>Загрузка изображения для OCR</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>
          {loading ? "Загрузка..." : "Отправить"}
        </button>
      </form>
      {text && (
        <div>
          <h2>Распознанный текст:</h2>
          <pre>{text}</pre>
        </div>
      )}
      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default OCRUpload;
