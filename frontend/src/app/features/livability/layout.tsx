import { generateMetadata } from "@/utils";

export const metadata = generateMetadata({
  title: "Seawater livability | Aqualog",
  description:
    "Submit seawater sample fields and get livability class, confidence, and per-class probabilities.",
});

export default function LivabilityLayout({ children, }: { children: React.ReactNode; }) {
  return <>{children}</>;
}
