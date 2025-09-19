"use client";
import { useEffect, useState } from "react";
import { Newspaper, Rocket, Lock, ArrowRight, Sparkles } from "lucide-react";

export default function Features() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [hoveredCard, setHoveredCard] = useState(null);

  const features = [
    {
      icon: <Newspaper className="w-10 h-10 text-blue-600" />,
      title: "Curated News",
      desc: "AI-powered summaries so you spend less time reading, more time learning.",
      color: "blue",
      stats: "10k+ articles",
      detail: "Smart algorithms filter through thousands of sources daily"
    },
    {
      icon: <Rocket className="w-10 h-10 text-blue-600" />,
      title: "Multiple Niches",
      desc: "From AI to Space, follow only what matters to you.",
      color: "indigo",
      stats: "50+ categories",
      detail: "Customizable feeds tailored to your interests"
    },
    {
      icon: <Lock className="w-10 h-10 text-blue-600" />,
      title: "Trusted Sources",
      desc: "We scrape verified websites so you always get reliable updates.",
      color: "purple",
      stats: "99.9% accuracy",
      detail: "Only from verified, authoritative news sources"
    },
  ];

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 100,
        y: (e.clientY / window.innerHeight) * 100,
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <section 
      id="features" 
      className="min-h-screen flex flex-col justify-center items-center px-6 py-20 relative overflow-hidden"
    >
      {/* Animated Background Elements */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Floating geometric shapes */}
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className={`absolute w-2 h-2 bg-blue-200/30 rounded-full animate-pulse`}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 2}s`,
            }}
          />
        ))}
        
        {/* Dynamic gradient orbs */}
        <div 
          className="absolute w-96 h-96 bg-blue-100/10 rounded-full blur-3xl"
          style={{
            left: `${20 + mousePosition.x * 0.02}%`,
            top: `${10 + mousePosition.y * 0.02}%`,
            transition: 'all 0.3s ease-out',
          }}
        />
        <div 
          className="absolute w-72 h-72 bg-gray-100/10 rounded-full blur-3xl"
          style={{
            right: `${15 + mousePosition.x * 0.015}%`,
            bottom: `${20 + mousePosition.y * 0.015}%`,
            transition: 'all 0.4s ease-out',
          }}
        />
      </div>

      {/* Section Header */}
      <div className="text-center mb-16 relative z-10">
        <div className="inline-flex items-center gap-2 bg-gray-100 px-4 py-2 rounded-full text-gray-700 font-medium text-sm mb-4">
          <Sparkles className="w-4 h-4" />
          Our Features
        </div>
        
        <h2 className="text-5xl md:text-6xl font-bold mb-6 text-gray-900">
          Why Choose Us?
        </h2>
        
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Discover what makes our platform the perfect choice for staying informed in today's fast-paced world
        </p>
        
        {/* Decorative line */}
        <div className="w-24 h-1 bg-blue-600 mx-auto mt-8 rounded-full"></div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 max-w-7xl relative z-10">
        {features.map((feature, i) => (
          <div
            key={i}
            className="group relative"
            onMouseEnter={() => setHoveredCard(i)}
            onMouseLeave={() => setHoveredCard(null)}
          >
            {/* Card Background with Hover Effects */}
            <div className="absolute inset-0 bg-white rounded-2xl transform group-hover:scale-105 transition-all duration-300 shadow hover:shadow-lg"></div>
            
            {/* Animated Border */}
            <div className="absolute inset-0 bg-blue-600 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-0.5">
              <div className="w-full h-full bg-white rounded-2xl"></div>
            </div>

            {/* Card Content */}
            <div className="relative bg-white p-8 rounded-2xl border border-gray-100 group-hover:border-transparent transition-all duration-300">
              {/* Icon Container */}
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-gray-50 rounded-xl flex items-center justify-center group-hover:bg-blue-50 transition-all duration-300 group-hover:scale-110">
                  {feature.icon}
                </div>
                
                {/* Floating badge */}
                <div className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs px-2 py-1 rounded-full font-semibold opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
                  {feature.stats}
                </div>
              </div>

              {/* Title */}
              <h3 className="text-2xl font-bold mb-3 text-gray-800 group-hover:text-blue-600 transition-colors duration-300">
                {feature.title}
              </h3>

              {/* Description */}
              <p className="text-gray-600 mb-4 leading-relaxed transition-colors duration-300">
                {feature.desc}
              </p>

              {/* Additional Detail (shown on hover) */}
              <div className={`overflow-hidden transition-all duration-300 ${
                hoveredCard === i ? 'max-h-20 opacity-100' : 'max-h-0 opacity-0'
              }`}>
                <p className="text-sm text-blue-600 font-medium flex items-center gap-2 pt-2 border-t border-gray-100">
                  <ArrowRight className="w-4 h-4" />
                  {feature.detail}
                </p>
              </div>

              {/* Interactive Elements */}
              <div className="absolute inset-0 pointer-events-none">
                {/* Hover glow effect */}
                <div className="absolute inset-0 bg-blue-600/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                
                {/* Sparkle effects on hover */}
                {hoveredCard === i && (
                  <>
                    <div className="absolute top-4 right-4 w-1 h-1 bg-blue-400 rounded-full animate-ping"></div>
                    <div className="absolute top-6 right-8 w-0.5 h-0.5 bg-indigo-400 rounded-full animate-ping" style={{ animationDelay: '0.5s' }}></div>
                    <div className="absolute bottom-8 left-6 w-1 h-1 bg-purple-400 rounded-full animate-ping" style={{ animationDelay: '1s' }}></div>
                  </>
                )}
              </div>

              {/* Card number indicator */}
              <div className="absolute top-4 left-4 w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-sm font-bold text-gray-400 group-hover:bg-blue-100 group-hover:text-blue-600 transition-all duration-300">
                {i + 1}
              </div>
            </div>

            {/* Card shadow that follows mouse */}
            <div 
              className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 pointer-events-none"
              style={{
                background: `radial-gradient(circle at ${mousePosition.x}% ${mousePosition.y}%, rgba(59, 130, 246, 0.15) 0%, transparent 70%)`,
              }}
            ></div>
          </div>
        ))}
      </div>

      {/* Bottom Call-to-Action */}
      <div className="mt-16 text-center relative z-10">
        <button 
          onClick={() => {
            const element = document.getElementById('headlines');
            if (element) {
              element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }}
          className="group relative px-8 py-4 bg-blue-600 text-white font-semibold rounded-full hover:bg-blue-700 transition-all duration-300 hover:scale-105 shadow hover:shadow-lg"
        >
          <span className="relative z-10 flex items-center gap-2">
            Get Started Today
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
          </span>
          <div className="absolute inset-0 bg-white/20 rounded-full scale-0 group-hover:scale-100 transition-transform duration-300"></div>
        </button>
      </div>

      {/* Animated connecting lines (subtle) */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 1 }}>
        <defs>
          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="rgb(59, 130, 246)" stopOpacity="0" />
            <stop offset="50%" stopColor="rgb(59, 130, 246)" stopOpacity="0.1" />
            <stop offset="100%" stopColor="rgb(59, 130, 246)" stopOpacity="0" />
          </linearGradient>
        </defs>
        
        {/* Connecting lines between cards on larger screens */}
        <g className="hidden md:block">
          <line 
            x1="25%" y1="50%" x2="50%" y2="50%" 
            stroke="url(#lineGradient)" 
            strokeWidth="1"
            className="animate-pulse"
          />
          <line 
            x1="50%" y1="50%" x2="75%" y2="50%" 
            stroke="url(#lineGradient)" 
            strokeWidth="1"
            className="animate-pulse"
            style={{ animationDelay: '1s' }}
          />
        </g>
      </svg>
    </section>
  );
}