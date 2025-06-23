import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// Buscar artículos en Wikipedia
export const searchArticles = async (query: string) => {
  const response = await axios.get(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);
  return response.data;
};

// Obtener análisis de un artículo
export const getArticleDetail = async (title: string) => {
  const response = await axios.get(`${BASE_URL}/articles/${encodeURIComponent(title)}`);
  return response.data;
};

// Guardar un artículo analizado
export const saveArticle = async (articleData: any) => {
  const response = await axios.post(`${BASE_URL}/saved_articles/`, articleData);
  return response.data;
};

// Listar artículos guardados
export const getSavedArticles = async () => {
  const response = await axios.get(`${BASE_URL}/saved_articles/`);
  return response.data;
};

// Actualizar un artículo guardado
export const updateArticle = async (id: number, articleData: any) => {
  const response = await axios.put(`${BASE_URL}/saved_articles/${id}`, articleData);
  return response.data;
};

// Eliminar un artículo guardado
export const deleteArticle = async (id: number) => {
  await axios.delete(`${BASE_URL}/saved_articles/${id}`);
};

