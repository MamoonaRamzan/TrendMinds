"use client";
import { useEffect, useState } from 'react';

export default function Hero() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 100,
        y: (e.clientY / window.innerHeight) * 100,
      });
    };

    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <section 
      id="hero" 
      className="relative h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-600 to-indigo-700 text-white text-center p-8 overflow-hidden"
    >
      {/* Animated Newspaper Background */}
      <div 
        className="absolute inset-0 opacity-10"
        style={{
          transform: `translateY(${scrollY * 0.5}px)`,
        }}
      >
        <div 
          className="absolute inset-0 bg-repeat opacity-30"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='white' fill-opacity='0.1'%3E%3Crect x='10' y='15' width='100' height='3' rx='1'/%3E%3Crect x='10' y='25' width='80' height='2' rx='1'/%3E%3Crect x='10' y='32' width='90' height='2' rx='1'/%3E%3Crect x='10' y='39' width='75' height='2' rx='1'/%3E%3Crect x='10' y='46' width='85' height='2' rx='1'/%3E%3Crect x='10' y='55' width='100' height='3' rx='1'/%3E%3Crect x='10' y='65' width='70' height='2' rx='1'/%3E%3Crect x='10' y='72' width='95' height='2' rx='1'/%3E%3Crect x='10' y='79' width='60' height='2' rx='1'/%3E%3Crect x='10' y='86' width='80' height='2' rx='1'/%3E%3Crect x='10' y='95' width='100' height='3' rx='1'/%3E%3C/g%3E%3C/svg%3E")`,
            transform: `translate(${mousePosition.x * 0.02}px, ${mousePosition.y * 0.02}px)`,
          }}
        />
      </div>

      {/* Floating Paper Elements - Left Side */}
      <div className="absolute left-0 top-0 w-1/4 h-full pointer-events-none overflow-hidden">
        {[...Array(3)].map((_, i) => (
          <div
            key={`left-${i}`}
            className="absolute w-20 h-24 bg-white/15 border border-white/25 rounded-sm shadow-lg"
            style={{
              left: `${10 + i * 5}%`,
              top: `${20 + i * 25}%`,
              transform: `rotate(${-20 + i * 5}deg)`,
              animation: `float${i} 6s ease-in-out infinite`,
              animationDelay: `${i * 1}s`,
            }}
          >
            <div className="p-2 space-y-1">
              <div className="w-full h-1 bg-white/40 rounded"></div>
              <div className="w-3/4 h-0.5 bg-white/30 rounded"></div>
              <div className="w-full h-0.5 bg-white/30 rounded"></div>
              <div className="w-2/3 h-0.5 bg-white/30 rounded"></div>
              <div className="w-4/5 h-0.5 bg-white/25 rounded"></div>
              <div className="w-full h-0.5 bg-white/25 rounded"></div>
            </div>
          </div>
        ))}
      </div>

      {/* Floating Paper Elements - Right Side */}
      <div className="absolute right-0 top-0 w-1/4 h-full pointer-events-none overflow-hidden">
        {[...Array(3)].map((_, i) => (
          <div
            key={`right-${i}`}
            className="absolute w-20 h-24 bg-white/15 border border-white/25 rounded-sm shadow-lg"
            style={{
              right: `${10 + i * 5}%`,
              top: `${15 + i * 30}%`,
              transform: `rotate(${10 + i * 8}deg)`,
              animation: `float${i + 3} 7s ease-in-out infinite`,
              animationDelay: `${i * 1.2}s`,
            }}
          >
            <div className="p-2 space-y-1">
              <div className="w-full h-1 bg-white/40 rounded"></div>
              <div className="w-3/4 h-0.5 bg-white/30 rounded"></div>
              <div className="w-full h-0.5 bg-white/30 rounded"></div>
              <div className="w-2/3 h-0.5 bg-white/30 rounded"></div>
              <div className="w-4/5 h-0.5 bg-white/25 rounded"></div>
              <div className="w-full h-0.5 bg-white/25 rounded"></div>
            </div>
          </div>
        ))}
      </div>

      {/* Animated News Ticker */}
      <div className="absolute top-0 left-0 w-full h-8 bg-black/20 backdrop-blur-sm overflow-hidden">
        <div className="animate-scroll whitespace-nowrap flex items-center h-full text-sm font-medium">
          <span className="mx-8 text-yellow-300">🔴 BREAKING:</span>
          <span className="mx-4">AI Revolution Continues • </span>
          <span className="mx-4">Latest Tech Updates • </span>
          <span className="mx-4">Market Analysis • </span>
          <span className="mx-4">Science Breakthroughs • </span>
          <span className="mx-4">Business Insights • </span>
          <span className="mx-8 text-yellow-300">🔴 BREAKING:</span>
          <span className="mx-4">AI Revolution Continues • </span>
          <span className="mx-4">Latest Tech Updates • </span>
          <span className="mx-4">Market Analysis • </span>
          <span className="mx-4">Science Breakthroughs • </span>
          <span className="mx-4">Business Insights • </span>
        </div>
      </div>

      {/* Interactive Particles */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-white/30 rounded-full animate-ping"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 2}s`,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 space-y-8">
        {/* Animated Title */}
        <div className="relative">
          <h1 className="text-6xl md:text-7xl font-bold mb-6 tracking-tight">
            <span className="inline-block animate-bounce" style={{ animationDelay: '0s' }}>📰</span>
            <span className="ml-4 bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-white animate-pulse">
              AI Newsletter Hub
            </span>
          </h1>
          
          {/* Glowing underline */}
          <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-transparent via-white to-transparent animate-pulse"></div>
        </div>

        {/* Animated Description */}
        <div className="max-w-3xl mx-auto space-y-4">
          <p className="text-xl md:text-2xl leading-relaxed font-light text-blue-100">
            Stay ahead with AI-powered, niche-specific news.
          </p>
          <p className="text-lg md:text-xl leading-relaxed text-blue-200">
            Explore the latest in <span className="text-yellow-300 font-semibold">technology</span>, 
            <span className="text-green-300 font-semibold"> science</span>, 
            <span className="text-purple-300 font-semibold"> business</span>, and more — 
            curated just for you.
          </p>
        </div>

        {/* Animated CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-12">
          <button 
            onClick={() => {
              const element = document.getElementById('headlines');
              if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }}
            className="group relative px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-white font-semibold text-lg hover:bg-white/20 hover:scale-105 transition-all duration-300 overflow-hidden"
            style={{
              boxShadow: '0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.2)',
            }}
          >
            <span className="relative z-10">Get Started</span>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400/0 via-white/10 to-blue-400/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
          </button>
          
          <button 
            onClick={() => {
              const element = document.getElementById('features');
              if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }}
            className="group relative px-8 py-4 bg-transparent border-2 border-white/40 rounded-full text-white font-semibold text-lg hover:bg-white/10 hover:border-white/60 hover:scale-105 transition-all duration-300"
          >
            <span className="relative z-10">Learn More</span>
            <div className="absolute inset-0 rounded-full bg-white/5 scale-0 group-hover:scale-100 transition-transform duration-300"></div>
          </button>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/40 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white/60 rounded-full mt-2 animate-pulse"></div>
        </div>
        <p className="text-sm text-white/60 mt-2">Scroll Down</p>
      </div>
      
      <style jsx>{`
        @keyframes scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-scroll {
          animation: scroll 30s linear infinite;
        }
        
        @keyframes float0 {
          0%, 100% { transform: rotate(-20deg) translateY(0px); }
          50% { transform: rotate(-15deg) translateY(-10px); }
        }
        
        @keyframes float1 {
          0%, 100% { transform: rotate(-15deg) translateY(0px); }
          50% { transform: rotate(-10deg) translateY(-15px); }
        }
        
        @keyframes float2 {
          0%, 100% { transform: rotate(-10deg) translateY(0px); }
          50% { transform: rotate(-5deg) translateY(-8px); }
        }
        
        @keyframes float3 {
          0%, 100% { transform: rotate(10deg) translateY(0px); }
          50% { transform: rotate(15deg) translateY(-12px); }
        }
        
        @keyframes float4 {
          0%, 100% { transform: rotate(18deg) translateY(0px); }
          50% { transform: rotate(23deg) translateY(-18px); }
        }
        
        @keyframes float5 {
          0%, 100% { transform: rotate(26deg) translateY(0px); }
          50% { transform: rotate(31deg) translateY(-10px); }
        }
      `}</style>
    </section>
  );
}