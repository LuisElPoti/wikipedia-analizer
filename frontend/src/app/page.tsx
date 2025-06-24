"use client"

import { useState, useEffect } from "react"
import { Search, BookmarkPlus, BookmarkCheck, LogOut, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { LoginForm } from "../components/login-form"
import { ArticleDetailModal } from "../components/article-detail-modal"
import { searchArticles, getArticleDetail, saveArticle, getSavedArticles, getSavedArticleById, updateArticle, deleteArticle} from "@/lib/api"


interface WikipediaArticle {
  id?: number
  pageid: number
  title: string
  summary?: string
  url?: string
  extract: string
  thumbnail?: {
    source: string
  }
  note?: string
}


export default function WikipediaSearch() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState("")
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState<WikipediaArticle[]>([])
  const [savedArticles, setSavedArticles] = useState<WikipediaArticle[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [articlesPerPage] = useState(5) // articulos guardados por pagina
  const [selectedArticle, setSelectedArticle] = useState<WikipediaArticle | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [searchCurrentPage, setSearchCurrentPage] = useState(1)
  const [searchResultsPerPage] = useState(10) // articulos busqueda por paginas
  const [editingNote, setEditingNote] = useState<number | null>(null)
   const [noteText, setNoteText] = useState("")

  useEffect(() => {
    // Verificar si hay una sesión guardada
    const savedUser = localStorage.getItem("wikipediaUser")
    if (savedUser) {
      setIsLoggedIn(true)
      setCurrentUser(savedUser)
      loadSavedArticles()
    }
  }, [])

  const loadSavedArticles = async () => {
    try {
      const articles = await getSavedArticles()
      setSavedArticles(articles)
    } catch (error) {
      console.error("Error cargando artículos guardados:", error)
      setSavedArticles([])
    }
  }

  const handleLogin = (username: string) => {
    setIsLoggedIn(true)
    setCurrentUser(username)
    localStorage.setItem("wikipediaUser", username)
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setCurrentUser("")
    localStorage.removeItem("wikipediaUser")
  }

  const searchWikipedia = async () => {
    if (!searchQuery.trim()) return

    setIsLoading(true)
    setSearchResults([])
    setSearchCurrentPage(1)

    try {
      const results = await searchArticles(searchQuery)
      if (!results || results.length === 0) {
        setSearchResults([])
        return
      }
      
      console.log("Resultados de búsqueda:", results)
      const articles = Object.values(results).map((item: any) => ({
        pageid: item.pageid,
        title: item.title,
        extract: item.extract,
        thumbnail: item.thumbnail ? { source: item.thumbnail.source } : undefined,
      }))

      setSearchResults(articles)
      setSearchCurrentPage(1)
    } catch (error) {
      console.error("Error buscando artículos:", error)
      setSearchResults([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateArticle = async (id: number, note: string) => {
    try {
      const updatedArticle = await updateArticle(id, note)
      setSavedArticles((prev) =>
        prev.map((article) => (article.id === id ? { ...article, note: updatedArticle.note } : article)),
      )
    } catch (error) {
      console.error("Error actualizando artículo:", error)
    }
  }
  
  // Iniciar edición de nota
  const startEditingNote = (id: number, currentNote?: string) => {
    setEditingNote(id)
    setNoteText(currentNote || "")
  }

  const saveNote = (id: number) => {
    handleUpdateArticle(id, noteText)
    setEditingNote(null)
    setNoteText("")
  }

  const cancelEditingNote = () => {
    setEditingNote(null)
    setNoteText("")
  }

  const handleSaveArticle = async (article: WikipediaArticle) => {
    const isAlreadySaved = savedArticles.some((saved) => saved.title === article.title)
    if (isAlreadySaved) return

    console.log("Guardando artículo:", savedArticles)
    try {
      const detail = await getArticleDetail(article.title)
      
      console.log("Detalles del artículo:", detail)

      const saved = await saveArticle(detail)
      setSavedArticles((prev) => [...prev, saved])
    } catch (error) {
      console.error("Error guardando el artículo:", error)
    }
  }

  const removeSavedArticle = async (id: number) => {
    try {
      await deleteArticle(id)
      setSavedArticles((prev) => prev.filter((article) => article.id !== id))
    } catch (error) {
      console.error("Error eliminando artículo:", error)
    }
  }


  const isArticleSaved = (title: string) => {
    return savedArticles.some((article) => article.title === title)
  }

  const openArticleModal = (article: WikipediaArticle) => {
    setSelectedArticle(article)
    setIsModalOpen(true)
  }

  const closeArticleModal = () => {
    setIsModalOpen(false)
    setSelectedArticle(null)
  }

  // Lógica de paginación
  const indexOfLastArticle = currentPage * articlesPerPage
  const indexOfFirstArticle = indexOfLastArticle - articlesPerPage
  const currentArticles = savedArticles.slice(indexOfFirstArticle, indexOfLastArticle)
  const totalPages = Math.ceil(savedArticles.length / articlesPerPage)

  const goToPage = (page: number) => {
    setCurrentPage(page)
  }

  const goToPreviousPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1))
  }

  const goToNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages))
  }

  // Reset página cuando se elimina un artículo y la página actual queda vacía
  useEffect(() => {
    if (currentPage > totalPages && totalPages > 0) {
      setCurrentPage(totalPages)
    }
  }, [savedArticles.length, currentPage, totalPages])

  // Lógica de paginación para resultados de búsqueda
  const searchIndexOfLastResult = searchCurrentPage * searchResultsPerPage
  const searchIndexOfFirstResult = searchIndexOfLastResult - searchResultsPerPage
  const currentSearchResults = searchResults.slice(searchIndexOfFirstResult, searchIndexOfLastResult)
  const searchTotalPages = Math.ceil(searchResults.length / searchResultsPerPage)

  const goToSearchPage = (page: number) => {
    setSearchCurrentPage(page)
  }

  const goToSearchPreviousPage = () => {
    setSearchCurrentPage((prev) => Math.max(prev - 1, 1))
  }

  const goToSearchNextPage = () => {
    setSearchCurrentPage((prev) => Math.min(prev + 1, searchTotalPages))
  }

  if (!isLoggedIn) {
    return <LoginForm onLogin={handleLogin} />
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8 bg-white p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <Search className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Wikipedia Search</h1>
              <p className="text-sm text-gray-600">Busca y guarda artículos de Wikipedia</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Avatar className="w-8 h-8">
                <AvatarFallback>
                  <User className="w-4 h-4" />
                </AvatarFallback>
              </Avatar>
              <span className="text-sm font-medium">{currentUser}</span>
            </div>
            <Button variant="outline" size="sm" onClick={handleLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              Salir
            </Button>
          </div>
        </div>

        <Tabs defaultValue="search" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="search">Buscar Artículos</TabsTrigger>
            <TabsTrigger value="saved">
              Artículos Guardados
              {savedArticles.length > 0 && (
                <Badge variant="secondary" className="ml-2">
                  {savedArticles.length}
                </Badge>
              )}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="search" className="space-y-6">
            {/* Search Bar */}
            <Card>
              <CardHeader>
                <CardTitle>Buscar en Wikipedia</CardTitle>
                <CardDescription>Ingresa el término que deseas buscar en Wikipedia</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-2">
                  <Input
                    placeholder="Ej: Albert Einstein, Madrid, Inteligencia Artificial..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && searchWikipedia()}
                    className="flex-1"
                  />
                  <Button onClick={searchWikipedia} disabled={isLoading}>
                    <Search className="w-4 h-4 mr-2" />
                    {isLoading ? "Buscando..." : "Buscar"}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Search Results */}
            <div className="space-y-4">
              {currentSearchResults.map((article) => (
                <Card key={article.pageid} className="hover:shadow-md transition-shadow cursor-pointer">
                  <CardContent className="p-6" onClick={() => openArticleModal(article)}>
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors">
                            {article.title}
                          </h3>
                          <Button
                            variant="ghost"
                            onClick={() => handleSaveArticle(article)}
                            disabled={isArticleSaved(article.title)}
                          >
                            {isArticleSaved(article.title) ? (
                              <>
                                <BookmarkCheck className="mr-2 h-4 w-4" /> Guardado
                              </>
                            ) : (
                              <>
                                <BookmarkPlus className="mr-2 h-4 w-4" /> Guardar
                              </>
                            )}
                          </Button>
                        </div>
                        <p className="text-gray-700 leading-relaxed line-clamp-3">{article.extract}</p>
                        <div className="flex items-center gap-4 mt-2">
                          <Button variant="link" className="p-0 h-auto text-blue-600">
                            Ver detalles →
                          </Button>
                          <Button
                            variant="link"
                            className="p-0 h-auto text-gray-500"
                            onClick={(e) => {
                              e.stopPropagation()
                              window.open(
                                  `${article.url || `https://es.wikipedia.org/wiki/${encodeURIComponent(article.title)}`}`,
                                  "_blank",
                              )
                            }}
                          >
                            Artículo original
                          </Button>
                        </div>
                      </div>
                      {article.thumbnail && (
                        <img
                          src={article.thumbnail.source || "/placeholder.svg"}
                          alt={article.title}
                          className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
                        />
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}

              {/* Paginación de resultados de búsqueda */}
              {searchResults.length > searchResultsPerPage && (
                <Card>
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-gray-600">
                        Mostrando {searchIndexOfFirstResult + 1}-
                        {Math.min(searchIndexOfLastResult, searchResults.length)} de {searchResults.length} resultados
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={goToSearchPreviousPage}
                          disabled={searchCurrentPage === 1}
                        >
                          Anterior
                        </Button>

                        <div className="flex items-center gap-1">
                          {Array.from({ length: Math.min(searchTotalPages, 5) }, (_, i) => {
                            const page = i + 1
                            return (
                              <Button
                                key={page}
                                variant={searchCurrentPage === page ? "default" : "outline"}
                                size="sm"
                                onClick={() => goToSearchPage(page)}
                                className="w-8 h-8 p-0"
                              >
                                {page}
                              </Button>
                            )
                          })}
                          {searchTotalPages > 5 && <span className="text-gray-400">...</span>}
                        </div>

                        <Button
                          variant="outline"
                          size="sm"
                          onClick={goToSearchNextPage}
                          disabled={searchCurrentPage === searchTotalPages}
                        >
                          Siguiente
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {searchResults.length === 0 && searchQuery && !isLoading && (
                <Card>
                  <CardContent className="p-6 text-center">
                    <p className="text-gray-500">No se encontraron resultados para "{searchQuery}"</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          <TabsContent value="saved" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Artículos Guardados</CardTitle>
                <CardDescription>Tus artículos favoritos de Wikipedia ({savedArticles.length})</CardDescription>
              </CardHeader>
            </Card>

            {savedArticles.length === 0 ? (
              <Card>
                <CardContent className="p-6 text-center">
                  <BookmarkPlus className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500 mb-2">No tienes artículos guardados</p>
                  <p className="text-sm text-gray-400">
                    Busca artículos y guárdalos haciendo clic en el ícono de marcador
                  </p>
                </CardContent>
              </Card>
            ) : (
              <>
                <div className="space-y-4">
                  {currentArticles.map((article) => (
                    <Card key={article.title} className="hover:shadow-md transition-shadow">
                      <CardContent className="p-6" onClick={() => openArticleModal(article)}>
                        <div className="flex justify-between items-start gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <h3 className="text-xl font-semibold text-gray-900">{article.title}</h3>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => removeSavedArticle(article.id!)}
                                className="text-blue-600"
                              >
                                <BookmarkCheck className="w-4 h-4" />
                              </Button>
                            </div>
                            <p className="text-gray-700 leading-relaxed">{article.summary}</p>

                            {/* Sección de notas */}
                            <div className="border-t pt-3 mt-3">
                              <div className="flex items-center justify-between mb-2">
                                <h4 className="text-sm font-medium text-gray-600">Mi Nota:</h4>
                                {editingNote !== article.id && (
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={(e) => {
                                      e.stopPropagation() 
                                      startEditingNote(article.id!, article.note)
                                      
                                    }}
                                    className="text-xs"
                                  >
                                    {article.note ? "Editar" : "Agregar nota"}
                                  </Button>
                                )}
                              </div>

                              {editingNote === article.id ? (
                                <div className="space-y-2">
                                  <textarea
                                    value={noteText}
                                    onChange={(e) => setNoteText(e.target.value)}
                                    placeholder="Escribe tu nota personal sobre este artículo..."
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm resize-none"
                                    onClick={(e) => e.stopPropagation()}
                                    rows={3}
                                    autoFocus
                                  />
                                  <div className="flex gap-2">
                                    <Button size="sm" onClick={(e) => {
                                      e.stopPropagation()
                                      saveNote(article.id!)
                                    }}>
                                      Guardar
                                    </Button>
                                    <Button size="sm" variant="outline" onClick={(e) => {
                                      e.stopPropagation()
                                      cancelEditingNote()
                                      
                                    }}>
                                      Cancelar
                                    </Button>
                                  </div>
                                </div>
                              ) : (
                                <div className="min-h-[2rem]">
                                  {article.note ? (
                                    <p className="text-sm text-gray-600 bg-yellow-50 p-2 rounded border-l-4 border-yellow-400">
                                      {article.note}
                                    </p>
                                  ) : (
                                    <p className="text-xs text-gray-400 italic">Sin notas</p>
                                  )}
                                </div>
                              )}
                            </div>

                            <Button
                              variant="link"
                              className="p-0 h-auto mt-2"
                              onClick={() =>
                                window.open(
                                  `${article.url || `https://es.wikipedia.org/wiki/${encodeURIComponent(article.title)}`}`,
                                  "_blank",
                                )
                              }
                            >
                              Leer artículo completo →
                            </Button>
                            
                          </div>
                          {article.thumbnail && (
                            <img
                              src={article.thumbnail.source || "/placeholder.svg"}
                              alt={article.title}
                              className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
                            />
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>

                {/* Controles de paginación */}
                {totalPages > 1 && (
                  <Card>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-600">
                          Mostrando {indexOfFirstArticle + 1}-{Math.min(indexOfLastArticle, savedArticles.length)} de{" "}
                          {savedArticles.length} artículos
                        </div>
                        <div className="flex items-center gap-2">
                          <Button variant="outline" size="sm" onClick={goToPreviousPage} disabled={currentPage === 1}>
                            Anterior
                          </Button>

                          <div className="flex items-center gap-1">
                            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                              <Button
                                key={page}
                                variant={currentPage === page ? "default" : "outline"}
                                size="sm"
                                onClick={() => goToPage(page)}
                                className="w-8 h-8 p-0"
                              >
                                {page}
                              </Button>
                            ))}
                          </div>

                          <Button
                            variant="outline"
                            size="sm"
                            onClick={goToNextPage}
                            disabled={currentPage === totalPages}
                          >
                            Siguiente
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </>
            )}
          </TabsContent>
        </Tabs>
      </div>
      {/* Modal de detalles del artículo */}
      <ArticleDetailModal
        article={selectedArticle}
        isOpen={isModalOpen}
        onClose={closeArticleModal}
        onSave={handleSaveArticle}
        isSaved={selectedArticle ? isArticleSaved(selectedArticle.title) : false}
      />
    </div>
  )
}
