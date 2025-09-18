"use client";
import { useState } from "react";

export default function Headlines() {
  const API_BASE = "http://127.0.0.1:8000";
  const [headlines, setHeadlines] = useState([]);
  const [headlinesNiche, setHeadlinesNiche] = useState("AI");
  const [loading, setLoading] = useState(false);

  const fetchHeadlines = async () => {
    setLoading(true);
    setHeadlines([{ type: "loading", text: "Fetching latest headlines..." }]);
    try {
      const res = await fetch(`${API_BASE}/headlines/${headlinesNiche}`);
      const data = await res.json();
      if (data.error) {
        setHeadlines([{ type: "error", text: `❌ ${data.error}` }]);
      } else if (data.stories?.length > 0) {
        setHeadlines(data.stories);
      } else {
        setHeadlines([{ type: "error", text: "No stories found." }]);
      }
    } catch {
      setHeadlines([{ type: "error", text: "❌ Backend not reachable." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="headlines" className="h-screen flex flex-col justify-center px-6">
      <h2 className="text-3xl font-bold text-center mb-8">Latest Headlines</h2>
      <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
        <select
          value={headlinesNiche}
          onChange={(e) => setHeadlinesNiche(e.target.value)}
          className="p-3 border rounded-lg"
        >
          <option value="AI">Artificial Intelligence</option>
          <option value="Crypto">Cryptocurrency</option>
          <option value="Climate">Climate</option>
          <option value="Tech">Technology</option>
          <option value="Business">Business</option>
          <option value="BioTech">Health & Biotech</option>
          <option value="Space">Space</option>
          <option value="EdTech">Education Technology</option>
          <option value="Science&Research">Science & Research</option>
          <option value="Cybersecurity">Cybersecurity</option>
        </select>
        <button
          onClick={fetchHeadlines}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          {loading ? "⏳ Loading..." : "Load Headlines"}
        </button>
      </div>

      <div className="space-y-4 max-h-[50vh] overflow-y-auto">
        {headlines.map((h, i) =>
          h.type === "error" || h.type === "loading" ? (
            <div
              key={i}
              className={`p-3 rounded-lg font-medium ${
                h.type === "error"
                  ? "bg-red-100 text-red-700"
                  : "bg-blue-100 text-blue-700"
              }`}
            >
              {h.text}
            </div>
          ) : (
            <div key={i} className="bg-white p-5 rounded-lg shadow">
              <h3 className="text-lg font-bold mb-2">
                <a
                  href={h.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {h.title}
                </a>
              </h3>
              <p className="text-gray-600">
                <strong>Summary:</strong> {h.summary}
              </p>
              {h.why && (
                <p className="text-gray-600">
                  <strong>Why it matters:</strong> {h.why}
                </p>
              )}
            </div>
          )
        )}
      </div>
    </section>
  );
}
