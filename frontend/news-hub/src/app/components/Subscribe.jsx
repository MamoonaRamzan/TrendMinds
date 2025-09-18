"use client";
import { useState } from "react";

export default function Subscribe() {
  const API_BASE = "http://127.0.0.1:8000";
  const [email, setEmail] = useState("");
  const [niche, setNiche] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubscribe = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch(`${API_BASE}/subscribe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, niche }),
      });
      const result = await res.json();
      if (res.ok) {
        setStatus({ type: "success", text: result.message });
        setEmail("");
        setNiche("");
      } else {
        setStatus({ type: "error", text: result.error });
      }
    } catch {
      setStatus({ type: "error", text: "❌ Failed. Try again." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="subscribe" className="h-screen flex flex-col justify-center items-center bg-gray-100 px-6">
      <h2 className="text-3xl font-bold mb-6">Subscribe to Newsletter</h2>
      <form onSubmit={handleSubscribe} className="space-y-4 w-full max-w-md">
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your.email@example.com"
          className="w-full p-3 border rounded-lg"
        />
        <select
          required
          value={niche}
          onChange={(e) => setNiche(e.target.value)}
          className="w-full p-3 border rounded-lg"
        >
          <option value="">Select your interest...</option>
          <option value="AI">🤖 Artificial Intelligence</option>
          <option value="Crypto">₿ Cryptocurrency</option>
          <option value="Climate">🌍 Climate & Sustainability</option>
          <option value="Tech">💻 Technology</option>
          <option value="Business">📈 Business</option>
          <option value="BioTech">🧬 Health & Biotech</option>
          <option value="Space">🚀 Space & Aerospace</option>
          <option value="EdTech">🎓 Education Technology</option>
          <option value="Science&Research">🔬 Science & Research</option>
          <option value="Cybersecurity">🔐 Cybersecurity</option>
        </select>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700"
        >
          {loading ? "⏳ Subscribing..." : "Subscribe Now"}
        </button>
      </form>

      {status && (
        <div
          className={`mt-4 p-3 rounded-lg ${
            status.type === "success"
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {status.text}
        </div>
      )}
    </section>
  );
}
