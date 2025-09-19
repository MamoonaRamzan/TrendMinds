import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Headlines from "./components/Headlines";
import Subscribe from "./components/Subscribe";
import Features from "./components/Features";
import Footer from "./components/Footer";

export default function Home() {
  return (
    <main className="bg-gray-50 text-gray-800">
      <Navbar />
      <Hero />
      <Features />
      <Headlines />
      <Subscribe />
      <Footer />
    </main>
  );
}
