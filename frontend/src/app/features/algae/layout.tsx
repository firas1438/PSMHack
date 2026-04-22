import { generateMetadata } from "@/utils";

export const metadata = generateMetadata({
  title: "Algae segmentation | Aqualog",
  description:
    "Upload a satellite image and detect algae using our segmentation model.",
});

export default function AlgaeLayout({ children, }: { children: React.ReactNode; }) {
  return <>{children}</>;
}
