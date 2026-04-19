import { LivabilityPredictor } from "@/components/livability/LivabilityPredictor";
import { generateMetadata } from "@/utils";

export const metadata = generateMetadata({
  title: "Seawater livability | Aqualog",
  description:
    "Submit seawater sample fields and get livability class, confidence, and per-class probabilities from the prediction API.",
});

export default function LivabilityPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <main className="flex-1 pt-20 pb-8">
        <LivabilityPredictor />      
      </main>
    </div>
    
  );

  
}
