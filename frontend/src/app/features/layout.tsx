import { generateMetadata } from "@/utils";

export const metadata = generateMetadata({
  title: "Select Feature | Aqualog",
  description:
    "Choose between water livability assessment or algae bloom detection to analyze coastal water data.",
});

export default function FeaturesLayout({ children, }: { children: React.ReactNode; }) {
  return <>{children}</>;
}
