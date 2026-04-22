import { FeatureSelect } from "@/components/select/FeatureSelect";
import { generateMetadata } from "@/utils";

export const metadata = generateMetadata({
  title: "Select Feature | Aqualog",
  description:
    "Choose between water livability assessment or algae bloom detection to analyze coastal water data.",
});

export default function SelectPage() {
  return (
    <div className="flex min-h-screen flex-col px-3 lg:px-0">
      <main className="flex-1 py-20">
        <FeatureSelect />
      </main>
    </div>
  );
}
