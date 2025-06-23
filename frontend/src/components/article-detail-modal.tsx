"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { BookmarkPlus, BookmarkCheck, ExternalLink, Clock, FileText, TrendingUp, Loader2 } from "lucide-react"
// import { processArticleSummary, generateArticleAnalysis } from "../actions"
import { getArticleDetail} from "@/lib/api"

interface WikipediaArticle {
  pageid: number
  title: string
  extract: string
  thumbnail?: {
    source: string
  }
}

interface ArticleDetailModalProps {
  article: WikipediaArticle | null
  isOpen: boolean
  onClose: () => void
  onSave: (article: WikipediaArticle) => void
  isSaved: boolean
}

interface ProcessedData {
  processedSummary: string
  wordCount: number
  readingTime: number
}

interface AnalysisData {
  topics: string[]
  url: string
  mostFrequentWords: string[] 
  sentiment: string
  complexity: string
  wordCount: number
  sentences: number
  avgWordsPerSentence: number
  estimatedReadingTime: number
  keyInsights: string[]
}

export function ArticleDetailModal({ article, isOpen, onClose, onSave, isSaved }: ArticleDetailModalProps) {
  const [processedData, setProcessedData] = useState<ProcessedData | null>(null)
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  useEffect(() => {
    if (article && isOpen) {
      loadArticleData()
    }
  }, [article, isOpen])

  const loadArticleData = async () => {
    if (!article) return

    setIsProcessing(true)
    setIsAnalyzing(true)
    setProcessedData(null)
    setAnalysisData(null)

    try {
      const detail = await getArticleDetail(article.title);
      console.log("Detalles del artículo:", detail)
      setProcessedData({
        processedSummary: detail.summary,
        wordCount: detail.analisis.word_count,
        readingTime: detail.analisis.estimated_reading_time,
      });

      setAnalysisData({
        url: detail.url,
        topics: detail.analisis.topics,
        mostFrequentWords: detail.analisis.frequent_words,
        sentiment: detail.analisis.sentiment,
        complexity: detail.analisis.complexity,
        wordCount: detail.analisis.word_count,
        sentences: detail.analisis.sentences,
        avgWordsPerSentence: detail.analisis.avg_words_per_sentence,
        estimatedReadingTime: detail.analisis.estimated_reading_time,
        keyInsights: detail.analisis.key_insights,
      });

    } catch (error) {
      console.error("Error cargando detalles del artículo:", error)
    } finally {
      setIsProcessing(false)
      setIsAnalyzing(false)
    }
  }

  if (!article) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold pr-8">{article.title}</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Imagen y acciones principales */}
          <div className="flex gap-4">
            {article.thumbnail && (
              <img
                src={article.thumbnail.source || "/placeholder.svg"}
                alt={article.title}
                className="w-32 h-32 object-cover rounded-lg flex-shrink-0"
              />
            )}
            <div className="flex-1 space-y-3">
              <div className="flex gap-2">
                <Button onClick={() => onSave(article)} variant={isSaved ? "default" : "outline"} className="flex-1">
                  {isSaved ? (
                    <>
                      <BookmarkCheck className="w-4 h-4 mr-2" />
                      Guardado
                    </>
                  ) : (
                    <>
                      <BookmarkPlus className="w-4 h-4 mr-2" />
                      Guardar Artículo
                    </>
                  )}
                </Button>

                
                <Button
                  variant="outline"
                  onClick={() =>
                    window.open(`https://es.wikipedia.org/wiki/${encodeURIComponent(article.title)}`, "_blank")
                  }
                >
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Ver Original
                </Button>
              </div>
            </div>
          </div>

          <Separator />

          {/* Resumen procesado */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Resumen Procesado
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isProcessing ? (
                <div className="flex items-center gap-2 text-gray-500">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Procesando resumen...
                </div>
              ) : processedData ? (
                <div className="space-y-3">
                  <p className="text-gray-700 leading-relaxed">{processedData.processedSummary}</p>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span className="flex items-center gap-1">
                      <FileText className="w-3 h-3" />
                      {processedData.wordCount} palabras
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {processedData.readingTime} min de lectura
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Error al procesar el resumen</p>
              )}
            </CardContent>
          </Card>

          {/* Análisis generado */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Análisis del Artículo
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isAnalyzing ? (
                <div className="flex items-center gap-2 text-gray-500">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Generando análisis...
                </div>
              ) : analysisData ? (
                <div className="space-y-4">

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {/* Temas principales */}
                    <div>
                      <h4 className="font-medium mb-2">Temas Principales:</h4>
                      <div className="flex gap-2 flex-wrap">
                        {analysisData.topics.map((topic, index) => (
                          <Badge key={index} variant="secondary">
                            {topic}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Palabras más repetidas */}
                    {analysisData.mostFrequentWords && analysisData.mostFrequentWords.length > 0 && (
                      <div>
                        <h4 className="font-medium mb-2">Palabras Más Repetidas:</h4>
                        <div className="flex gap-2 flex-wrap">
                          {analysisData.mostFrequentWords.map((word, index) => (
                            <Badge key={index} variant="outline"> {/* Usar "outline" para diferenciar o "secondary" si quieres igual */}
                              {word}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Sentimiento */}
                    {analysisData.sentiment && (
                      <div>
                        <h4 className="font-medium mb-2">Análisis de Sentimiento:</h4>
                        <div className="flex items-center flex gap-1 p-2  bg-gray-50 rounded-lg justify-center">
                          {analysisData.sentiment === "positivo" && (
                            <span className="text-green-100 text-xl animate-bounce-once">✅</span> // Emoji feliz animado
                          )}
                          {analysisData.sentiment === "negativo" && (
                            <span className="text-red-100 text-xl animate-shake">❌</span> // Emoji enojado animado
                          )}
                          {analysisData.sentiment === "neutro" && (
                            <span className="text-gray-100 text-xl animate-pulse">⚪</span> // Emoji neutral pulsando
                          )}
                          <span className="text-xl font-semibold capitalize">
                            {analysisData.sentiment}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Métricas */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">{analysisData.complexity}</div>
                      <div className="text-xs text-gray-500">Complejidad</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">{analysisData.sentences}</div>
                      <div className="text-xs text-gray-500">Oraciones</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">{analysisData.avgWordsPerSentence}</div>
                      <div className="text-xs text-gray-500">Palabras/Oración</div>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">{analysisData.estimatedReadingTime}</div>
                      <div className="text-xs text-gray-500">Min. Lectura</div>
                    </div>
                  </div>

                  {/* Insights clave */}
                  <div>
                    <h4 className="font-medium mb-2">Insights Clave:</h4>
                    <ul className="space-y-1">
                      {analysisData.keyInsights.map((insight, index) => (
                        <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                          <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                          {insight}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Error al generar el análisis</p>
              )}
            </CardContent>
          </Card>

          
        </div>
      </DialogContent>
    </Dialog>
  )
}
