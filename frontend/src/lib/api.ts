import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// Buscar artículos en Wikipedia
export const searchArticles = async (query: string) => {
  const response = await axios.get(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);
  return response.data;
};

// Obtener análisis de un artículo directamente desde Wikipedia
export const getArticleDetail = async (title: string) => {
  const response = await axios.get(`${BASE_URL}/article/${encodeURIComponent(title)}`);
  return response.data;
};

// Guardar un artículo ya analizado
export const saveArticle = async (articleData: any) => {
  const response = await axios.post(`${BASE_URL}/saved_articles/`, articleData);
  console.log("Article saved:", response.data);
  return response.data;
};

// Listar todos los artículos guardados
export const getSavedArticles = async () => {
  const response = await axios.get(`${BASE_URL}/saved_articles/`);
  return response.data;
};

// Obtener un artículo guardado por su ID
export const getSavedArticleById = async (id: number) => {
  const response = await axios.get(`${BASE_URL}/saved_articles/${id}`);
  return response.data;
};

// Actualizar la nota de un artículo guardado
export const updateArticle = async (id: number, note: string) => {
  const response = await axios.put(`${BASE_URL}/saved_articles/${id}`, { note });
  return response.data;
};

// Eliminar un artículo guardado y su análisis
export const deleteArticle = async (id: number) => {
  const response = await axios.delete(`${BASE_URL}/saved_articles/${id}`);
  return response.data;
};
