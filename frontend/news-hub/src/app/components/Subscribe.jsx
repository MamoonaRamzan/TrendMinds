"use client";
import { useState } from "react";
import { Mail, Bell, Check, X, Sparkles, ArrowRight, Users, Shield } from "lucide-react";

export default function Subscribe() {
  const API_BASE = "http://127.0.0.1:8000";
  const [email, setEmail] = useState("");
  const [niche, setNiche] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [focusedField, setFocusedField] = useState(null);

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

  const handleSubscribe = async (e) => {
    if (e) e.preventDefault();
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

  const getSelectedNiche = () => niches.find(n => n.value === niche);

  return (
    <section id="subscribe" className="min-h-screen flex flex-col justify-center items-center bg-white px-6 py-20 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-20 left-20 w-40 h-40 bg-blue-50/30 rounded-full blur-2xl animate-pulse"></div>
        <div className="absolute bottom-32 right-16 w-56 h-56 bg-gray-50/40 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
        
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-blue-200/40 rounded-full animate-ping"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 2}s`,
            }}
          />
        ))}
      </div>

      <div className="max-w-2xl mx-auto relative z-10 w-full">
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-blue-50 px-4 py-2 rounded-full text-blue-700 font-medium text-sm mb-6">
            <Bell className="w-4 h-4" />
            Join Our Community
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Subscribe to Newsletter
          </h2>
          
          <p className="text-lg text-gray-600 mb-6 leading-relaxed">
            Stay ahead of the curve with TrendMinds — receive concise, AI-curated insights from the niches that matter most to you. 
          </p>

          {/* Stats */}
          <div className="flex items-center justify-center gap-6 text-sm text-gray-500 mb-8">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              <span>Personalized topics </span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4" />
              <span>Privacy protected</span>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              <span>Weekly updates</span>
            </div>
          </div>
        </div>

        {/* Subscription Form */}
        <div className="space-y-6">
          {/* Email Input */}
          <div className="relative group">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <div className={`absolute inset-0 rounded-lg transition-all duration-300 ${
                focusedField === 'email' ? 'bg-blue-50 border-2 border-blue-500' : 'bg-gray-50 border border-gray-200'
              }`}></div>
              
              <div className="relative flex items-center">
                <Mail className={`absolute left-4 w-5 h-5 transition-colors duration-300 ${
                  focusedField === 'email' ? 'text-blue-600' : 'text-gray-400'
                }`} />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onFocus={() => setFocusedField('email')}
                  onBlur={() => setFocusedField(null)}
                  placeholder="your.email@example.com"
                  className="w-full pl-12 pr-4 py-4 bg-transparent text-gray-900 placeholder-gray-500 focus:outline-none font-medium"
                />
                {email && (
                  <Check className="absolute right-4 w-5 h-5 text-green-500 animate-scale-in" />
                )}
              </div>
            </div>
          </div>

          {/* Niche Selection */}
          <div className="relative group">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Choose Your Interest
            </label>
            <div className="relative">
              <div className={`absolute inset-0 rounded-lg transition-all duration-300 ${
                focusedField === 'niche' ? 'bg-blue-50 border-2 border-blue-500' : 'bg-gray-50 border border-gray-200'
              }`}></div>
              
              <div className="relative">
                <select
                  required
                  value={niche}
                  onChange={(e) => setNiche(e.target.value)}
                  onFocus={() => setFocusedField('niche')}
                  onBlur={() => setFocusedField(null)}
                  className="w-full px-4 py-4 bg-transparent text-gray-900 focus:outline-none font-medium appearance-none cursor-pointer"
                >
                  <option value="">Select your interest...</option>
                  {niches.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.icon} {option.label}
                    </option>
                  ))}
                </select>
                <ArrowRight className={`absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 rotate-90 transition-colors duration-300 ${
                  focusedField === 'niche' ? 'text-blue-600' : 'text-gray-400'
                }`} />
              </div>
            </div>
            
            {/* Selected niche preview */}
            {getSelectedNiche() && (
              <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-100 animate-fade-in">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{getSelectedNiche().icon}</span>
                  <div>
                    <p className="font-medium text-gray-900">{getSelectedNiche().label}</p>
                    <p className="text-sm text-gray-600">{getSelectedNiche().desc}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Subscribe Button */}
          <button
            onClick={handleSubscribe}
            disabled={loading || !email || !niche}
            className="group relative w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-300 hover:scale-105 hover:shadow-lg overflow-hidden"
          >
            <span className="relative z-10 flex items-center justify-center gap-2">
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Subscribing...
                </>
              ) : (
                <>
                  Subscribe Now
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
                </>
              )}
            </span>
            
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-white/20 to-blue-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
          </button>

          {/* Features list */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8 pt-6 border-t border-gray-100">
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                <Check className="w-3 h-3 text-green-600" />
              </div>
              <span>AI-curated content</span>
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                <Check className="w-3 h-3 text-green-600" />
              </div>
              <span>Weekly digest format</span>
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                <Check className="w-3 h-3 text-green-600" />
              </div>
              <span>Unsubscribe anytime</span>
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                <Check className="w-3 h-3 text-green-600" />
              </div>
              <span>No spam guarantee</span>
            </div>
          </div>
        </div>

        {/* Status Messages */}
        {status && (
          <div className={`mt-8 p-4 rounded-lg border animate-fade-in ${
            status.type === "success"
              ? "bg-green-50 border-green-200 text-green-800"
              : "bg-red-50 border-red-200 text-red-800"
          }`}>
            <div className="flex items-center gap-3">
              {status.type === "success" ? (
                <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                  <Check className="w-4 h-4 text-white" />
                </div>
              ) : (
                <div className="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
                  <X className="w-4 h-4 text-white" />
                </div>
              )}
              <span className="font-medium">{status.text}</span>
            </div>
          </div>
        )}

        {/* Privacy Notice */}
        <p className="text-center text-xs text-gray-500 mt-8 leading-relaxed">
          By subscribing, you agree to receive weekly newsletters. We respect your privacy and will never share your email. 
          You can unsubscribe at any time by clicking the link in any email.
        </p>
      </div>

      {/* Custom CSS for animations */}
      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes scale-in {
          from { opacity: 0; transform: scale(0); }
          to { opacity: 1; transform: scale(1); }
        }
        
        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
        
        .animate-scale-in {
          animation: scale-in 0.2s ease-out;
        }
      `}</style>
    </section>
  );
}