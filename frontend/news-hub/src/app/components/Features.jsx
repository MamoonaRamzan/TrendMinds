import { Newspaper, Rocket, Lock } from "lucide-react";

export default function Features() {
  const features = [
    {
      icon: <Newspaper className="w-10 h-10 text-blue-600" />,
      title: "Curated News",
      desc: "AI-powered summaries so you spend less time reading, more time learning.",
    },
    {
      icon: <Rocket className="w-10 h-10 text-blue-600" />,
      title: "Multiple Niches",
      desc: "From AI to Space, follow only what matters to you.",
    },
    {
      icon: <Lock className="w-10 h-10 text-blue-600" />,
      title: "Trusted Sources",
      desc: "We scrape verified websites so you always get reliable updates.",
    },
  ];

  return (
    <section id="features" className="h-screen flex flex-col justify-center items-center px-6">
      <h2 className="text-3xl font-bold mb-10">Why Choose Us?</h2>
      <div className="grid md:grid-cols-3 gap-8 max-w-5xl">
        {features.map((f, i) => (
          <div
            key={i}
            className="bg-white p-8 rounded-xl shadow hover:shadow-lg transition"
          >
            {f.icon}
            <h3 className="text-xl font-bold mt-4 mb-2">{f.title}</h3>
            <p className="text-gray-600">{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
