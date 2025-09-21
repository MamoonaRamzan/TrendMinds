"use client";
import { useState, useEffect } from "react";
import { TrendingUp, Clock, ExternalLink, Sparkles, RefreshCw, AlertCircle } from "lucide-react";

export default function Headlines() {
  const API_BASE = "http://127.0.0.1:8000";
  const [headlines, setHeadlines] = useState([]);
  const [headlinesNiche, setHeadlinesNiche] = useState("Tech");
  const [loading, setLoading] = useState(false);
  const [hoveredCard, setHoveredCard] = useState(null);

  const niches = [
  { value: "ai_data_science", label: "AI & Data Science", icon: "🤖", color: "purple" },
  { value: "market_business_innovation", label: "Business & Innovation", icon: "💼", color: "blue" },
  { value: "biotech_healthcare", label: "Biotech & Healthcare", icon: "🧬", color: "red" },
  { value: "climate_sustainability", label: "Climate & Sustainability", icon: "🌍", color: "green" },
  { value: "space_frontier_tech", label: "Space & Frontier Tech", icon: "🚀", color: "indigo" },
  { value: "cybersecurity_risk", label: "Cybersecurity", icon: "🔒", color: "slate" },
  { value: "science_research", label: "Science & Research", icon: "🔬", color: "teal" },
  { value: "fintech_digital_economy", label: "Fintech & Digital Economy", icon: "₿", color: "yellow" },
  { value: "policy_regulation", label: "Policy & Regulation", icon: "⚖️", color: "orange" },
  { value: "venture_capital_startups", label: "VC & Startups", icon: "💡", color: "pink" },
  { value: "supply_chain_industry4", label: "Supply Chain & Industry 4.0", icon: "🏭", color: "gray" },
  { value: "energy_cleantech", label: "Energy & Cleantech", icon: "⚡", color: "green" },
  { value: "healthcare_digital_health", label: "Digital Health", icon: "🏥", color: "red" },
];

  const fetchHeadlines = async (niche = headlinesNiche) => {
    setLoading(true);
    setHeadlines([{ type: "loading", text: "Fetching latest headlines..." }]);
    try {
      const res = await fetch(`${API_BASE}/headlines/${niche}`);
      const data = await res.json();
      if (data.error) {
        setHeadlines([{ type: "error", text: `❌ ${data.error}` }]);
      } else if (data.stories?.length > 0) {
        setHeadlines(data.stories);
      } else {
        setHeadlines([{ type: "no-news", text: "There is no news for this week" }]);
      }
    } catch {
      setHeadlines([{ type: "error", text: "❌ Backend not reachable." }]);
    } finally {
      setLoading(false);
    }
  };

  // Load Tech news by default
  useEffect(() => {
    fetchHeadlines("market_business_innovation");
  }, []);

  const handleNicheChange = (newNiche) => {
    setHeadlinesNiche(newNiche);
    fetchHeadlines(newNiche);
  };

  const getCurrentNiche = () => niches.find(n => n.value === headlinesNiche) || niches[0];

  return (
    <section id="headlines" className="min-h-screen bg-gradient-to-br from-gray-50 to-white py-20 px-6 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-20 left-10 w-64 h-64 bg-blue-100/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-48 h-48 bg-purple-100/15 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-blue-100 px-4 py-2 rounded-full text-blue-700 font-medium text-sm mb-4">
            <TrendingUp className="w-4 h-4" />
            Breaking News
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Latest Insights
          </h2>
          
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Stay ahead with AI-curated briefs across research, business, and technology. Discover the trends shaping tomorrow.
          </p>
        </div>

        {/* Niche Selection */}
        <div className="mb-8">
          <div className="flex flex-wrap justify-center gap-3 mb-6">
            {niches.map((niche) => (
              <button
                key={niche.value}
                onClick={() => handleNicheChange(niche.value)}
                className={`group relative px-6 py-3 rounded-full font-medium transition-all duration-300 hover:scale-105 ${
                  headlinesNiche === niche.value
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-white text-gray-700 hover:bg-gray-50 shadow-sm border border-gray-200 hover:border-blue-300'
                }`}
              >
                <span className="flex items-center gap-2">
                  <span>{niche.icon}</span>
                  <span className="hidden sm:inline">{niche.label}</span>
                  <span className="sm:hidden">{niche.value}</span>
                </span>
                
                {headlinesNiche === niche.value && (
                  <div className="absolute inset-0 bg-blue-500 rounded-full animate-ping opacity-20"></div>
                )}
              </button>
            ))}
          </div>

          {/* Current Selection Display */}
          <div className="text-center">
            <div className="inline-flex items-center gap-3 bg-white px-6 py-3 rounded-lg shadow-sm border">
              <span className="text-2xl">{getCurrentNiche().icon}</span>
              <div>
                <p className="text-sm text-gray-500">Currently viewing</p>
                <p className="font-semibold text-gray-900">{getCurrentNiche().label}</p>
              </div>
              <button
                onClick={() => fetchHeadlines()}
                disabled={loading}
                className="ml-4 p-2 text-blue-600 hover:bg-blue-50 rounded-full transition-colors duration-200"
                title="Refresh headlines"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>
        </div>

        {/* Headlines Content */}
        <div className="max-w-4xl mx-auto">
          {headlines.length > 0 && headlines[0].type === "loading" && (
            <div className="text-center py-12">
              <div className="inline-flex items-center gap-3 bg-blue-50 px-6 py-4 rounded-lg">
                <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <span className="text-blue-700 font-medium">Fetching latest headlines...</span>
              </div>
            </div>
          )}

          {headlines.length > 0 && headlines[0].type === "error" && (
            <div className="text-center py-12">
              <div className="inline-flex items-center gap-3 bg-red-50 px-6 py-4 rounded-lg border border-red-200">
                <AlertCircle className="w-5 h-5 text-red-500" />
                <span className="text-red-700 font-medium">{headlines[0].text}</span>
              </div>
            </div>
          )}

          {headlines.length > 0 && headlines[0].type === "no-news" && (
            <div className="text-center py-16">
              <div className="max-w-md mx-auto">
                <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-4xl">📰</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">No News This Week</h3>
                <p className="text-gray-600 mb-6">
                  There are no news articles available for {getCurrentNiche().label} this week. 
                  Check back later or try a different niche.
                </p>
                <button
                  onClick={() => fetchHeadlines()}
                  className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  <RefreshCw className="w-4 h-4" />
                  Try Again
                </button>
              </div>
            </div>
          )}

          {headlines.length > 0 && !headlines[0].type && (
            <div className="space-y-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <Clock className="w-5 h-5 text-gray-500" />
                  <span className="text-gray-600 font-medium">
                    {headlines.length} articles found
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  Last updated: {new Date().toLocaleTimeString()}
                </div>
              </div>

              <div className="grid gap-6">
                {headlines.map((article, i) => (
                  <article
                    key={i}
                    className="group relative bg-white rounded-xl border border-gray-200 hover:border-blue-300 transition-all duration-300 hover:shadow-lg overflow-hidden"
                    onMouseEnter={() => setHoveredCard(i)}
                    onMouseLeave={() => setHoveredCard(null)}
                  >
                    {/* Hover glow effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-50/50 to-purple-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    
                    <div className="relative p-6">
                      {/* Article number badge */}
                      <div className="absolute top-4 right-4 w-8 h-8 bg-gray-100 group-hover:bg-blue-100 rounded-full flex items-center justify-center text-sm font-bold text-gray-400 group-hover:text-blue-600 transition-all duration-300">
                        {i + 1}
                      </div>

                      {/* Title */}
                      <h3 className="text-xl font-bold text-gray-900 mb-3 pr-12 group-hover:text-blue-700 transition-colors duration-300">
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:underline flex items-start gap-2"
                        >
                          {article.title}
                          <ExternalLink className="w-4 h-4 mt-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex-shrink-0" />
                        </a>
                      </h3>

                      {/* Summary */}
                      <div className="mb-4">
                        <div className="flex items-center gap-2 mb-2">
                          <Sparkles className="w-4 h-4 text-blue-600" />
                          <span className="text-sm font-semibold text-gray-700">AI Summary</span>
                        </div>
                        <p className="text-gray-600 leading-relaxed pl-6">
                          {article.summary}
                        </p>
                      </div>

                      {/* Why it matters */}
                      {article.why && (
                        <div className="mb-4">
                          <div className="flex items-center gap-2 mb-2">
                            <TrendingUp className="w-4 h-4 text-green-600" />
                            <span className="text-sm font-semibold text-gray-700">Why it matters</span>
                          </div>
                          <p className="text-gray-600 leading-relaxed pl-6">
                            {article.why}
                          </p>
                        </div>
                      )}

                      {/* Interactive elements */}
                      {hoveredCard === i && (
                        <div className="absolute inset-0 pointer-events-none">
                          <div className="absolute top-6 left-6 w-1 h-1 bg-blue-400 rounded-full animate-ping"></div>
                          <div className="absolute bottom-6 right-8 w-0.5 h-0.5 bg-purple-400 rounded-full animate-ping" style={{ animationDelay: '0.5s' }}></div>
                        </div>
                      )}

                      {/* Read more indicator */}
                      <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <Clock className="w-4 h-4" />
                          <span>2 min read</span>
                        </div>
                        
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm group/link"
                        >
                          Read full article
                          <ExternalLink className="w-4 h-4 group-hover/link:translate-x-1 transition-transform duration-200" />
                        </a>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}