import Footer from "@/components/home/footer";
import Navbar from "@/components/home/navbar";

export default function LivabilityLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <main className="flex-1 pt-4">{children}</main>
    </div>
  );
}
